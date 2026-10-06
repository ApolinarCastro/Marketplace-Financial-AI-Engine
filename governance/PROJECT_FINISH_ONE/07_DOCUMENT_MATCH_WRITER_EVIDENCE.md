# PFO DOCUMENT MATCH WRITER — EVIDENCE

## Task Info

```
TASK_ID: PFO-DOCMATCH-WRITER-001
DATE: 2026-10-06
HEAD_BEFORE: af514885267e33c415569bfdf1516943bc71940d
BRANCH: main
```

Resolves blocker: NO_SAFE_DOCUMENT_MATCH_INGESTION_PATH
(demonstrated in PFO-FA005-GOLDEN-FULLCHAIN-001).
Scope: MATCH PERSISTENCE only. No match decision logic. No DTE. No heuristics.

---

## Schema Source

1. Baseline DB probe (15 columns + DuckDB types, 9,431 existing rows sampled).
2. ReconciliationEngine Level 4 + coverage helpers (join keys, CONCILIATED filter).
3. dte_ledger_matcher.py (match_source/status conventions).

```
DOCUMENT_MATCH_COLUMNS:
match_id VARCHAR, marketplace VARCHAR, ledger_id VARCHAR, order_id VARCHAR,
folio_xml VARCHAR, tipo_dte VARCHAR (nullable), match_rule VARCHAR,
match_source VARCHAR, match_timestamp TIMESTAMP, match_status VARCHAR,
document_date DATE, document_amount DOUBLE, reference_document VARCHAR,
created_by VARCHAR, execution_id VARCHAR
No PRIMARY KEY declared. Natural idempotency key: (marketplace, ledger_id).
Statuses in code: CONCILIATED (L4), MATCHED / MATCHED_CERTIFIED /
  MATCHED_WITH_TOLERANCE / AMOUNT_MISMATCH (certification/matcher).
```

## DDL Change

File: `engine/v4/database.py` (+4 lines, additive only).

```sql
CREATE TABLE IF NOT EXISTS document_match_v1 (match_id VARCHAR, ...);
```

```
FRESH_DB_CREATES_TABLE: TRUE (verified by test, 15/15 columns, 0 rows)
EXISTING_DB_COMPATIBLE: TRUE (IF NOT EXISTS; no migration; no data touched)
DESTRUCTIVE_MIGRATION: FALSE / DROP_TABLE: FALSE / TRUNCATE: FALSE
```

## Writer

```
WRITER_LOCATION: engine/v4/matching/document_match_writer.py
WRITER_CONTRACT:
  input: dict with marketplace, ledger_id, match_status, document_date (required)
         + order_id, folio_xml, tipo_dte, match_rule, match_source,
           match_timestamp, document_amount, reference_document,
           created_by, execution_id (optional)
  output: {"outcome": "INSERTED" | "SKIPPED_EXISTING", "match_id": ...}
  rejects: missing required fields, invalid status, conflicting re-write
  never: amounts math, DTE decisions, folio guessing, ledger/cierre mutation
IDEMPOTENCY_RULE: natural key (marketplace, ledger_id); identical re-write →
  SKIPPED_EXISTING (row count unchanged); conflicting re-write →
  DocumentMatchConflictError. match_id deterministic: "dm-" + sha256(key)[:16].
  Date comparison normalized to calendar date (driver Timestamp safety).
```

Prohibitions honored: no financial math, no DTE matching, no tolerance logic,
no ledger/cierre/DTE mutation, no silent invalid inserts.

## Tests (all isolated tmp_path DBs; production untouched)

File: `tests/test_document_match_writer.py` — 10 tests.

```
FRESH_DB_TEST: PASS (table created, 15/15 columns, 0 rows)
INSERT_TEST: PASS (1 row, readback exact incl. amount 20800.0)
READBACK_TEST: PASS (status/order/amount/match_id verified)
DUPLICATE_TEST: PASS (INSERTED then SKIPPED_EXISTING, count stays 1)
INVALID_RECORD_TEST: PASS x4 (empty marketplace, empty ledger_id,
  bad status, missing document_date; invalid insert leaves 0 rows)
  + conflicting re-write raises DocumentMatchConflictError, count stays 1
DOCUMENT_COVERAGE_TEST: PASS (1 matched / 1 ledger = 100.0 via the exact
  LEFT JOIN contract from ReconciliationEngine._document_coverage)
TEST_RESULTS: 10/10 PASS
```

One writer defect found and fixed during development (Timestamp vs date-string
idempotency comparison); fixed via date normalization, re-verified 10/10.

## Regression

```
GOLDEN_REGRESSION: 11/11 PASS (tests/golden/e2e_v1 integrity, unchanged)
INGESTION_HANDLERS: 46/46 PASS (tests/test_ingestion_handlers.py)
```

## Non-Contamination

```
PRODUCTION_DB_MODIFIED: FALSE (all tests use tmp_path isolated DBs)
REAL_RAW_MODIFIED: FALSE (no RAW files touched)
```

## Blocker Resolution

```
BLOCKER_STATUS: NO_SAFE_DOCUMENT_MATCH_INGESTION_PATH → RESOLVED
  - Fresh DatabaseV4 now creates document_match_v1 (empty, compatible).
  - DocumentMatchWriter persists validated CONCILIATED matches deterministically.
  - Writer output consumable by ReconciliationEngine coverage contract (proven).
FA-005_STATUS: FAIL (unchanged — re-scope/re-execution is a separate task)
FA-006_STATUS: BLOCKED (unchanged)
```

## Next Exact Action

Resume PFO-FA005-GOLDEN-FULLCHAIN-001: build E2E_V2 (treasury row + writer-created
document matches on fresh TEMP_DB), precompute expected reconciliation in engine
vocabulary, execute ReconciliationEngine, compare. No engine changes needed.
