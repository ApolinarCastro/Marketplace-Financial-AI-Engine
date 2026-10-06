# PFO FA-004 R1 — LEDGER EVIDENCE (REPAIR RE-EXECUTION)

## Task Info

```
TASK_ID: PFO-FA004-GOLDEN-REPAIR-001
DATE: 2026-10-06
HEAD: d3edd5a5a65cefaf5964b35610684ff2a9c5a2f4
BRANCH: main
DATASET_ID: E2E_V1
RUN: R1
```

## Golden Repair Applied

File: `tests/golden/e2e_v1/expected/expected_ledger.csv`

All 8 `id_transaccion` values corrected (`__` → `_`):

```
CHG__ML..._4 → CHG_ML..._4
CHG__ML..._5 → CHG_ML..._5
COMM_E2E-001__ML..._1 → COMM_E2E-001_ML..._1
COMM_E2E-002__ML..._2 → COMM_E2E-002_ML..._2
REFUND_E2E-001__ML..._3 → REFUND_E2E-001_ML..._3
REVCOMM_E2E-001__ML..._3 → REVCOMM_E2E-001_ML..._3
SALE_E2E-001__ML..._1 → SALE_E2E-001_ML..._1
SALE_E2E-002__ML..._2 → SALE_E2E-002_ML..._2
```

No other field modified. Golden integrity re-validated: 11/11 PASS.

## Isolation (R1)

```
SOURCE_DB: data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db
SOURCE_DB_SHA256_BEFORE: 733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
SOURCE_DB_SHA256_AFTER:  733c759f8ea179d8bcadf4897d8a2998826acab693171636f04ae0653c236e00
TEMP_DB: data/db/tmp_pfo_fa004_r1/meli_financial_v4.db (REMOVED after execution)
```

Same f3_03 pattern, user="PFO_FA004_R1_E2E_V1", post_persist_stages=False.

## Ingestion Reproduction (R1)

```
INGESTION_STATUS: COMPLETED
RECORDS_NEW: 8
INGESTION_ERRORS: []
```

## Comparison Result (R1)

```
EXPECTED_ROWS: 8
ACTUAL_ROWS: 8
EXPECTED_TOTAL: 20800.0
ACTUAL_TOTAL: 20800.0
ROW_BY_ROW_EQUAL: NO
MISSING_ROWS: 0
UNEXPECTED_ROWS: 0
FIELD_MISMATCHES: 9
DUPLICATE_ID_TRANSACCION: 0
NULL_ID_TRANSACCION: 0
MOVEMENT_TOTALS_DELTA: 0.0
```

ID repair verified: missing=0, unexpected=0 (all 8 IDs now match).

## New Differences (R1, distinct from R0)

### A. financial_group — 7 rows

Expected (classified values) vs Actual (NULL in raw ledger_v1):

| Row | Expected | Actual |
|-----|----------|--------|
| CHG_ML..._4 | costos_operacionales | None |
| CHG_ML..._5 | costos_operacionales | None |
| COMM_E2E-001... | costos_comerciales | None |
| COMM_E2E-002... | costos_comerciales | None |
| REFUND_E2E-001... | devoluciones | None |
| REVCOMM_E2E-001... | ajustes | None |
| SALE_E2E-001... | ingresos | None |
| SALE_E2E-002... | ingresos | None |

Root cause: `SurgicalLoader.LEDGER_COLS` does not include `financial_group`;
raw `marketplace_ledger_v1` stores NULL. Classification populates
`marketplace_ledger_clasificado_v1` in a later stage (not executed with
post_persist_stages=False). The golden over-specified this field for
raw-ledger comparison. The proven f3_03 pattern compares only
(id_transaccion, id_orden, tipo_movimiento, monto, detalle) — no
financial_group. No engine logic modified.

### B. detalle encoding — 1 row

```
ROW: REVCOMM_E2E-001_ML_Facturacion_E2E_V1.xlsx_3
FIELD: detalle
EXPECTED: Anulación del cargo por venta (correct UTF-8, U+00F3)
ACTUAL: AnulaciÃ³n del cargo por venta (mojibake: U+00C3 U+00B3)
```

Input XLSX bytes verified valid (`&#243;` XML entity, decodes to U+00F3
via openpyxl/direct read). Calamine read returns correct U+00F3.
Corruption occurs in pipeline write path or DuckDB driver round-trip
on Windows. Financial amount unaffected (+9500.0 matches).
No engine logic modified. Requires dedicated encoding investigation.

## Movement Totals (R1)

All subtotals exact, delta 0.0 (same as R0).

## Non-Contamination (R1)

```
PRODUCTION_DB_MODIFIED: FALSE
REAL_RAW_MODIFIED: FALSE
```

## FA-004 Verdict (R1)

```
FA-004_RESULT: FAIL (new field classes differ from R0; IDs now match)
FA-005_STATUS: BLOCKED
FIRST_BLOCKER: FA-004 R1 — financial_group NULL in raw ledger (golden over-specification) + detalle mojibake (encoding path issue); 0 financial deltas
```

## Cleanup (R1)

```
TEMP_DIR data/db/tmp_pfo_fa004_r1/: REMOVED
Execution script tmp_fa004_r1_run.py: REMOVED
SurgicalLoader.DIR_FACTURACION: RESTORED
Raw JSON: governance/PROJECT_FINISH_ONE/02_FA004_COMPARISON_R1.json KEPT
Prior R0 evidence (02_FA004_LEDGER_EVIDENCE.md + 02_FA004_COMPARISON.json): PRESERVED
```

## Next Exact Action

Dedicated investigation task for the two new difference classes:
1. Decide golden scope for financial_group (exclude from raw-ledger parity
   per f3_03 precedent, or extend FA-004 to run classification stage).
2. Investigate detalle mojibake in pipeline write/DuckDB round-trip path.
Then re-execute FA-004 as R2. Do NOT modify engine logic without
a dedicated repair task with demonstrated cause.
