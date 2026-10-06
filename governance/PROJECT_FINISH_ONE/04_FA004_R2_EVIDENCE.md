# PFO FA-004 R2 — LEDGER PARITY EVIDENCE (POST-REPAIR)

## Task Info

```
TASK_ID: PFO-FA004-REPAIR-R2-001
DATE: 2026-10-06
HEAD_BEFORE: a2de6332d96a338619c61acbafa524bb1a4d0bb4
BRANCH: main
DATASET_ID: E2E_V1
RUN: R2
```

## Repairs Applied (per RCA PFO-FA004-RCA-001)

### Repair A — Golden scope (financial_group)

File: `tests/golden/e2e_v1/expected/expected_ledger.csv`
Change: 8 `financial_group` values → empty (raw `marketplace_ledger_v1`
contract has no financial_group; owned by MarketplaceAuditor classification).
No other field touched.

### Repair B — Source literal (mojibake)

File: `engine/v4/surgical_loader.py`
Change: exactly 2 occurrences `AnulaciÃ³n` (U+00C3 U+00B3) → `Anulación` (U+00F3):
- line 72 (docstring, documentation only)
- line 217 (functional ledger-dict literal)
Verified: 0 corrupt occurrences remain; U+00F3 present in both; git diff = 2 lines only.

## Isolation (R2)

```
SOURCE_DB: data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db
SOURCE_DB_SHA256_BEFORE: 733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
SOURCE_DB_SHA256_AFTER:  733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
TEMP_DB: data/db/tmp_pfo_fa004_r2/meli_financial_v4.db (REMOVED after execution)
```

Same f3_03 pattern, user="PFO_FA004_R2_E2E_V1", post_persist_stages=False.

## Ingestion (R2)

```
INGESTION_STATUS: COMPLETED
RECORDS_NEW: 8
INGESTION_ERRORS: []
```

## Comparison (R2)

```
EXPECTED_ROWS: 8
ACTUAL_ROWS: 8
EXPECTED_TOTAL: 20800.0
ACTUAL_TOTAL: 20800.0
MISSING_ROWS: 0
UNEXPECTED_ROWS: 0
FIELD_MISMATCHES: 0
ROW_BY_ROW_EQUAL: TRUE
MOVEMENT_TOTALS_DELTA: 0.0
DUPLICATE_ID_TRANSACCION: 0
NULL_ID_TRANSACCION: 0
```

## REVCOMM Codepoint Parity (R2)

```
REVCOMM_EXPECTED: Anulación del cargo por venta (U+00F3)
REVCOMM_ACTUAL:   Anulación del cargo por venta (U+00F3)
REVCOMM_CODEPOINT_PARITY: TRUE
```

The mojibake repair is proven end-to-end: correct literal → DataFrame → DuckDB → read-back.

## Non-Contamination (R2)

```
PRODUCTION_DB_MODIFIED: FALSE
REAL_RAW_MODIFIED: FALSE
```

## Verdict (R2)

```
FA-004_RESULT: PASS
FA-005_STATUS: READY
FIRST_BLOCKER: NONE
```

## Cleanup (R2)

```
TEMP_DIR data/db/tmp_pfo_fa004_r2/: REMOVED
Scripts tmp_fa004_r1_run.py, tmp_fa004_r2_run.py, tmp_fix_literal.py: REMOVED
SurgicalLoader.DIR_FACTURACION: RESTORED
Raw JSON: governance/PROJECT_FINISH_ONE/04_FA004_R2_COMPARISON.json KEPT
Prior evidence (02_*, 03_*): PRESERVED
```

## Next Exact Action

FA-005 reconciliation execution against E2E_V1 (expects PENDIENTE /
document_coverage=0 per corrected golden — NOT a failure, the documented
known limitation until DTE evidence exists).
