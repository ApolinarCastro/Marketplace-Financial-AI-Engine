# PFO FA-005 — RECONCILIATION EVIDENCE

## Task Info

```
TASK_ID: PFO-FA005-RECONCILIATION-001
DATE: 2026-10-06
HEAD: a6ecc119f03a2cf9c756e1e85f7072eed2383db8
BRANCH: main
DATASET_ID: E2E_V1
MARKETPLACE: ML
```

## Isolation

```
SOURCE_DB: data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db
SOURCE_DB_SHA256_BEFORE: 733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
SOURCE_DB_SHA256_AFTER:  733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
TEMP_DB: data/db/tmp_pfo_fa005/meli_financial_v4.db (REMOVED after execution)
```

Same f3_03 pattern (TEMP copy + TEMP_RAW + DIR_FACTURACION override),
user="PFO_FA005_E2E_V1", post_persist_stages=False.

## Ingestion Precondition

```
INGESTION_STATUS: COMPLETED
RECORDS_NEW: 8
ERRORS: []
LEDGER_ROWS: 8
LEDGER_TOTAL: 20800.0
```

## Classification (required — engine reads clasificado_v1)

```
CLASSIFICATION_REQUIRED: YES
CLASSIFICATION_COMPONENT: MarketplaceAuditorEngine.run_classification_for_transaction x8
  (scoped to E2E_V1 ids only; baseline rows untouched)
CLASSIFICATION_RESULT: PASS (8 E2E_V1 rows in clasificado_v1, 8 with financial_group)
```

## Closing (required — engine reads cierre_v1)

```
CLOSING_COMPONENT: MarketplaceAuditorEngine.run_financial_closing(ML, 2026-06-01, 2026-06-30)
CLOSING_RESULT: neto=20800.0 (ingresos=80000.0, devoluciones=-50000.0,
  costos_op=-1500.0, costos_com=-7700.0, ajustes=0.0)
NOTE: baseline copy already contained 2 ML-June cierre rows (neto ~30.4M);
  closing replaced only the exact (ML, 2026-06-01, 2026-06-30) row.
  Engine sums ALL June cierre rows (see mismatches below).
```

## Document Match State

```
DOCUMENT_MATCH_ROWS_FOR_E2E: 0 (no DTE/XML in E2E_V1, as designed)
```

## Reconciliation Execution

```
RECONCILIATION_COMMAND: ReconciliationEngine(db=TEMP_DB).validate_marketplace_consistency('ML', '2026-06')
RECONCILIATION_EXECUTED: TRUE
ENGINE_PERIOD: Jun 2026
ENGINE_CERTIFICATION_STATUS: FINANCIAL_INTEGRITY_BROKEN
ENGINE_DELTA: 54944885.22
ENGINE_TAXONOMY_COVERAGE: 100.0
ENGINE_DOCUMENT_COVERAGE: 0.0
ENGINE_TOTAL_RECORDS: 8
```

Engine levels (real output):

| Level | Status | Delta | Source | Target |
|-------|--------|-------|--------|--------|
| INTERNA | ALERTA | 24537650.0 | 20800.0 | 30407235.22 |
| OPERACIONAL | ALERTA | 30386435.22 | 20800.0 | 30407235.22 |
| TESORERÍA | ALERTA | 20800.0 | 0.0 | -20800.0 |
| DOCUMENTAL | ALERTA | 100.0 | 0.0 | 8.0 |

## Comparison vs Golden

```
EXPECTED_LEVELS: 5
ACTUAL_LEVELS: 5
MISSING_LEVELS: 0
UNEXPECTED_LEVELS: 0
FIELD_MISMATCHES: 15
ROW_BY_ROW_EQUAL: FALSE
```

Matched fields: marketplace (5/5), period (5/5), level (5/5), rule (5/5),
taxonomy_coverage 100.0 (5/5), document_coverage 0.0 (5/5),
LEVEL_4 delta 100.0 (1/1).

Mismatched fields (15): full list in 05_FA005_RECONCILIATION_COMPARISON.json.

```
EXPECTED_DOCUMENT_COVERAGE: [0.0 x5]
ACTUAL_DOCUMENT_COVERAGE: [0.0 x5]  (MATCH)
EXPECTED_STATUSES: [PENDIENTE]
ACTUAL_STATUSES: [ALERTA, FINANCIAL_INTEGRITY_BROKEN]  (MISMATCH)
```

## Mismatch Root Causes (read-only analysis, no code modified)

### R1. Baseline cierre pollution (LEVEL_1 + LEVEL_2 deltas)

TEMP_DB is a baseline COPY containing 2 pre-existing ML-June cierre rows
(neto sum ~30.39M). Engine sums ALL June cierre rows (target 30,407,235.22)
against E2E_V1-only clasificado (source 20,800).
Deltas ~24.5M / ~30.4M are baseline data, not E2E_V1 error.

### R2. Treasury mirror gap (LEVEL_3 delta 20800)

E2E_V1 is Facturacion-only: 0 treasury/settlement rows.
Mirror equation operational(20800) + treasury(0) = 20800 ≠ 0 → ALERTA.
Golden expected delta=0. Dataset scope gap, not engine defect.

### R3. Status vocabulary gap (all statuses + LEVEL_5 aggregate)

Engine level vocabulary is PASS/ALERTA; aggregate scale
(CERTIFICADO/PARCIAL/PENDIENTE/ERROR/BROKEN) applies to the aggregate
via _determine_status. With total delta 54.9M > 1000 → BROKEN.
Golden expects PENDIENTE per level. The simplified golden level vocabulary
does not map 1:1 to engine output. No level can emit PENDIENTE.

### R4. Mapping artifacts (LEVEL_4 impact_amount, LEVEL_3 record_count)

Golden LEVEL_4 impact_amount=8.0 counts unmatched records; engine level
delta (100.0, coverage gap) was mapped to impact_amount. Golden LEVEL_3
record_count=0 vs engine total_records=8 applied uniformly. These two
fields reflect mapping decisions documented in the executor, not engine
behavior differences.

## Non-Contamination

```
PRODUCTION_DB_MODIFIED: FALSE
REAL_RAW_MODIFIED: FALSE
```

## Verdict

```
FA-005_RESULT: FAIL (15 field mismatches; engine executed correctly)
FA-006_STATUS: BLOCKED (depends on FA-005 PASS)
FIRST_BLOCKER: FA-005 — golden simplified reconciliation contract does not
  match engine real output: (a) baseline cierre pollution in TEMP_DB copy,
  (b) treasury mirror gap (Facturacion-only dataset), (c) status vocabulary
  gap (ALERTA/BROKEN vs PENDIENTE), (d) 2 mapping artifacts.
  Engine behavior deterministic and correct in all 4 engine levels.
```

## Cleanup

```
TEMP_DIR data/db/tmp_pfo_fa005/: REMOVED
Script tmp_fa005_run.py: REMOVED
SurgicalLoader.DIR_FACTURACION: RESTORED
Raw JSON: governance/PROJECT_FINISH_ONE/05_FA005_RECONCILIATION_COMPARISON.json KEPT
```

## Next Exact Action

Re-scope golden reconciliation expectations to the engine real output
contract (dedicated task): either (a) expand E2E_V1 with treasury/settlement
+ DTE data and use fresh empty TEMP_DB, or (b) redefine expected levels in
engine vocabulary (PASS/ALERTA per level + aggregate status via
_determine_status). Then re-execute FA-005. No engine modification required;
engine behaved correctly.
