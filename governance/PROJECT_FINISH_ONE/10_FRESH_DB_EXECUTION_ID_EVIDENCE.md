# PFO FRESH DB EXECUTION_ID — EVIDENCE

## Task Info

```
TASK_ID: PFO-FRESH-DB-EXECUTION-ID-001
DATE: 2026-10-06
HEAD_BEFORE: 2a002000fa1d86371f03df5535fd0ffee72fe5b9
BRANCH: main
```

## Root Cause (demonstrated in E2E_V2 execution)

```
DatabaseV4 init order on fresh DB:
  1. ALTER TABLE marketplace_ledger_v1 ADD COLUMN execution_id TEXT
     → table does not exist yet → silent except-pass (no-op)
  2. CREATE TABLE marketplace_ledger_v1 (... without execution_id ...)
Loader always sets df['execution_id'] (orchestrator passes record.execution_id)
→ insert_df Binder Error on fresh DB only (baseline copies carry the column).
```

## DDL Change

File: `engine/v4/database.py` (+1 column in canonical CREATE, nullable).

```sql
... financial_group TEXT, execution_id TEXT, load_ts TIMESTAMP ...
```

```
DDL_EXECUTION_ID_ADDED: YES (nullable TEXT; legacy rows unaffected)
HOT_MIGRATION_PRESERVED: YES (ALTER at line 116 untouched; still upgrades old DBs)
```

## Tests (tests/test_fresh_db_ingestion_execution_id.py, tmp_path-isolated)

```
FRESH_SCHEMA_TEST: PASS (execution_id VARCHAR, nullable YES)
OLD_DB_MIGRATION_TEST: PASS (legacy table without column → init adds it, data preserved)
FRESH_INGESTION_STATUS: COMPLETED (DETECT/VALIDATE/CLASSIFY/PERSIST all PASS)
RECORDS_NEW: 8 / ERRORS: 0
INGESTION_EXECUTION_ID: <record.execution_id, propagated>
LEDGER_ROWS_WITH_EXECUTION_ID: 8/8
DISTINCT_LEDGER_EXECUTION_IDS: 1
LEDGER_EXECUTION_ID_MATCH: TRUE (ledger value == record value)
LEDGER_ROWS: 8 / LEDGER_TOTAL: 20800.0 (financial content unchanged)
```

One test-harness issue found/fixed during development (pipeline internals
call DatabaseV4.get(); test now binds _instance to temp DB like FA-003 pattern).
Not an engine defect.

## Regression

```
GOLDEN_REGRESSION: 11/11 PASS (E2E_V1 integrity)
RELATED_REGRESSION: 10/10 docmatch writer + 46/46 ingestion handlers (67 total with golden)
```

## Non-Contamination

```
PRODUCTION_DB_MODIFIED: FALSE (every DatabaseV4 instance pointed at tmp_path;
  singleton rebound to temp and reset in finally blocks; production never opened)
REAL_RAW_MODIFIED: FALSE (golden input copied to tmp_path RAW only)
```

## Blocker Status

```
FRESH_DB_LEDGER_MISSING_EXECUTION_ID: RESOLVED
FA-005_STATUS: FAIL (unchanged until E2E_V2 re-execution)
FA-006_STATUS: BLOCKED (unchanged)
E2E_V2_STATUS: READY_FOR_REEXECUTION
```

## Next Exact Action

Re-execute PFO-FA005-E2E-V2-001 full chain on fresh TEMP_DB (golden + executor
already prepared). Then PFO-XML-DTE-E2E-001.
