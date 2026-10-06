# PFO FA-003 — DATASET IMPORT EVIDENCE

## Task Info

```
TASK_ID: PFO-FA003-DATASET-IMPORT-001
DATE: 2026-10-06
HEAD: 67ff4efb32535498d6d844d7a60bde652f797af9
BRANCH: main
DATASET_ID: E2E_V1
MARKETPLACE: ML
```

## Isolation

```
SOURCE_DB: data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db
SOURCE_DB_SHA256_BEFORE: 733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
SOURCE_DB_SHA256_AFTER:  733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
TEMP_DB: data/db/tmp_pfo_fa003/meli_financial_v4.db (REMOVED after execution)
TEMP_RAW: data/db/tmp_pfo_fa003/01_Raw/ML/Facturacion/ (REMOVED after execution)

SOURCE_INPUT: tests/golden/e2e_v1/input/ML_Facturacion_E2E_V1.xlsx
SOURCE_INPUT_SHA256: 024f58dca383655547d1541acd5ed0d2272d523100a176eec0427eb6800bcd7d
TEMP_INPUT_SHA256:   024f58dca383655547d1541acd5ed0d2272d523100a176eec0427eb6800bcd7d
INPUT_COPY_VERIFIED: TRUE
```

Pattern: f3_03 controlled isolation (TEMP_DIR + TEMP_DB copy + TEMP_RAW +
`SurgicalLoader.DIR_FACTURACION` monkey-patch + `IngestionOrchestrator`
with `post_persist_stages=False`). Monkey-patch restored after execution.

## Ingestion Command

```python
registry = IngestionRegistry(db=db)  # db -> TEMP_DB only
orch = IngestionOrchestrator(db=db, registry=registry, post_persist_stages=False)
record = await orch.run(
    file_path="data/db/tmp_pfo_fa003/01_Raw/ML/Facturacion/ML_Facturacion_E2E_V1.xlsx",
    user="PFO_FA003_E2E_V1",
)
```

Stages executed: DETECT → VALIDATE → CLASSIFY → PERSIST (CERTIFY and KNOWLEDGE skipped).

## Ingestion Record

```
execution_id: cb8ee20a-b318-40a9-ba9c-183e5d52f282
pipeline_status: COMPLETED
marketplace: ML
document_type: facturacion
period: (empty — Facturacion has no period in filename)
loader_executed: SurgicalLoader
stages_completed: DETECT, VALIDATE, CLASSIFY, PERSIST
```

## Pipeline Stages

| Stage | Result |
|-------|--------|
| DETECT | PASS |
| VALIDATE | PASS |
| CLASSIFY | PASS (ML / facturacion / SurgicalLoader) |
| PERSIST | PASS |

## Row Counts

```
ROWS_READ: 8
ROWS_NEW: 8
ROWS_EXISTING: 0
ROWS_REJECTED: 0
ERRORS: 0
WARNINGS: 0
```

## Persistence Verification (TEMP_DB read-only)

Queried by `archivo_origen = 'ML_Facturacion_E2E_V1.xlsx'`:

```
LEDGER_ROWS_CREATED: 8 (marketplace_ledger_v1)
VENTAS_ROWS_CREATED: 2 (ventas_marketplace)
LEDGER_TOTAL: 20800.0
FILE_REGISTRY_STATUS: 1 record(s) in ingestion_registry
```

Row-by-row comparison against `expected_ledger.csv` is out of scope for FA-003
(belongs to FA-004). Ledger total 20800.0 incidentally matches expected.

## Non-Contamination Verification

```
PRODUCTION_DB_MODIFIED: FALSE (SHA256 identical before/after)
REAL_RAW_MODIFIED: FALSE (01_Raw/ML/Facturacion/ML_Facturacion_E2E_V1.xlsx does not exist)
```

## FA-003 Verdict

| Check | Result |
|-------|--------|
| GOLDEN_INTEGRITY (11/11 pre-verified) | PASS |
| ISOLATED_DB | PASS |
| ISOLATED_RAW | PASS |
| DETECT | PASS |
| VALIDATE | PASS |
| CLASSIFY | PASS |
| PERSIST | PASS |
| PIPELINE_STATUS = COMPLETED | PASS |
| RECORDS_READ > 0 (8) | PASS |
| RECORDS_NEW > 0 (8) | PASS |
| ERRORS = 0 | PASS |
| PRODUCTION_DB_MODIFIED = FALSE | PASS |
| REAL_RAW_MODIFIED = FALSE | PASS |

```
FA-003_RESULT: PASS
FA-004_STATUS: READY
FIRST_BLOCKER: NONE
```

## Cleanup

```
TEMP_DIR data/db/tmp_pfo_fa003/: REMOVED
Execution script tmp_fa003_run.py: REMOVED
SurgicalLoader.DIR_FACTURACION: RESTORED to original value
Raw JSON output governance/PROJECT_FINISH_ONE/01_FA003_RAW_OUTPUT.json: KEPT as evidence
```

## Next Exact Action

Execute FA-004: compare TEMP_DB ledger rows (by archivo_origen) row-by-row
against tests/golden/e2e_v1/expected/expected_ledger.csv
(8 rows, total 20800.0, per-tipo_movimiento montos).
