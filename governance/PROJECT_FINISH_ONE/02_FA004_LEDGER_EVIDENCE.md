# PFO FA-004 — LEDGER EVIDENCE

## Task Info

```
TASK_ID: PFO-FA004-LEDGER-001
DATE: 2026-10-06
HEAD: d7b3f382735f8314a554ad5d0e3bc657bc5539c4
BRANCH: main
DATASET_ID: E2E_V1
MARKETPLACE: ML
```

## Isolation

```
SOURCE_DB: data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db
SOURCE_DB_SHA256_BEFORE: 733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
SOURCE_DB_SHA256_AFTER:  733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
TEMP_DB: data/db/tmp_pfo_fa004/meli_financial_v4.db (REMOVED after execution)
```

Pattern: FA-003 reproduction (TEMP_DIR + TEMP_DB copy + TEMP_RAW +
`SurgicalLoader.DIR_FACTURACION` monkey-patch + `IngestionOrchestrator`
with `post_persist_stages=False`, user="PFO_FA004_E2E_V1").
Monkey-patch restored after execution.

## Ingestion Reproduction

```
INGESTION_STATUS: COMPLETED
RECORDS_NEW: 8
INGESTION_ERRORS: []
```

FA-003 reproduction: PASS (pipeline COMPLETED, 8 new rows, 0 errors).

## Comparison Result

```
EXPECTED_ROWS: 8
ACTUAL_ROWS: 8
EXPECTED_TOTAL: 20800.0
ACTUAL_TOTAL: 20800.0
ROW_BY_ROW_EQUAL: NO
MISSING_ROWS: 8
UNEXPECTED_ROWS: 8
FIELD_MISMATCHES: 0
DUPLICATE_ID_TRANSACCION: 0
NULL_ID_TRANSACCION: 0
```

## Movement Totals

| tipo_movimiento | Expected | Actual | Delta |
|-----------------|----------|--------|-------|
| INGRESO_VENTA | 80000.0 | 80000.0 | 0.0 |
| EGRESO_COMISION | -15200.0 | -15200.0 | 0.0 |
| DEVOLUCION | -50000.0 | -50000.0 | 0.0 |
| AJUSTE | 9500.0 | 9500.0 | 0.0 |
| CARGO | -3500.0 | -3500.0 | 0.0 |
| TOTAL | 20800.0 | 20800.0 | 0.0 |

All financial values match exactly. All movement subtotals match exactly.

## Exact Differences

Every one of the 8 rows differs in exactly ONE field: `id_transaccion`.
All other 8 canonical fields match (id_orden, tipo_movimiento, monto,
detalle, financial_group, marketplace, fecha, archivo_origen).

Pattern (systematic, all 8 rows):

```
EXPECTED:  {PREFIX}__ML_Facturacion_E2E_V1.xlsx_{idx}   (double underscore)
ACTUAL:    {PREFIX}_ML_Facturacion_E2E_V1.xlsx_{idx}    (single underscore)
```

Example:
```
ROW: SALE_E2E-001 (prefix SALE, order E2E-001, idx 1)
FIELD: id_transaccion
EXPECTED: SALE_E2E-001__ML_Facturacion_E2E_V1.xlsx_1
ACTUAL:   SALE_E2E-001_ML_Facturacion_E2E_V1.xlsx_1
DELTA: single-character separator (__ vs _)
```

Full list in `02_FA004_COMPARISON.json` (missing_rows + unexpected_rows arrays).

## Root Cause Analysis (read-only, no code modified)

Engine ID generation (`engine/v4/surgical_loader.py` line 228):

```python
'id_transaccion': f"CHG_{f.name}_{idx}"
```

- f3_03 fixture file: `_f3_03_fixture.xlsx` (leading underscore)
  → `CHG_` + `_f3_03_fixture.xlsx` + `_4` = `CHG__f3_03_fixture.xlsx_4` ✓
- E2E_V1 file: `ML_Facturacion_E2E_V1.xlsx` (no leading underscore)
  → `CHG_` + `ML_Facturacion_E2E_V1.xlsx` + `_4` = `CHG_ML_Facturacion_E2E_V1.xlsx_4` ✓

The engine derived IDs deterministically and correctly from the actual
input filename. The golden `expected_ledger.csv` transcribed the
double-underscore pattern from f3_03 without accounting for the
different filename. This is a golden transcription error, NOT an
engine logic error. No financial value is affected.

Per FA-004 protocol: recorded as FAIL, NOT repaired in this task
(no golden modification, no logic modification).

## Non-Contamination Verification

```
PRODUCTION_DB_MODIFIED: FALSE (SHA256 identical before/after)
REAL_RAW_MODIFIED: FALSE (01_Raw/ML/Facturacion/ML_Facturacion_E2E_V1.xlsx does not exist)
```

## FA-004 Verdict

```
FA-004_RESULT: FAIL
FA-005_STATUS: BLOCKED (depends on FA-004 PASS)
FIRST_BLOCKER: FA-004 — systematic id_transaccion separator mismatch (__ vs _), all financial values exact
```

## Cleanup

```
TEMP_DIR data/db/tmp_pfo_fa004/: REMOVED
Execution script tmp_fa004_run.py: REMOVED
SurgicalLoader.DIR_FACTURACION: RESTORED to original value
Raw JSON output governance/PROJECT_FINISH_ONE/02_FA004_COMPARISON.json: KEPT as evidence
```

## Next Exact Action

Repair golden `expected_ledger.csv` id_transaccion values (single underscore
per engine `f"CHG_{f.name}_{idx}"` derivation) in a dedicated golden-repair
task, then re-execute FA-004. Alternatively, confirm whether IDs should be
excluded from strict parity (they are derived, not financial).
