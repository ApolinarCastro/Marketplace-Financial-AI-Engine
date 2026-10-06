# PFO FA-005 E2E_V2 — EXECUTION EVIDENCE (FRESH-DB SCHEMA DEFECT)

## Task Info

```
TASK_ID: PFO-FA005-E2E-V2-001
DATE: 2026-10-06
HEAD: 42f15fa2533663f3e5abf03b0a6c8dcc7a4eefc1
BRANCH: main
DATASET_ID: E2E_V2
```

E2E_V2 golden built and integrity-verified (8/8). Full-chain execution
BLOCKED by a fresh-DB schema defect. No engine files modified. E2E_V1 untouched.

---

## E2E_V2 Golden (built, integrity PASS 8/8)

```
tests/golden/e2e_v2/input/ML_Facturacion_E2E_V2.xlsx (6 rows: 5 certified + treasury)
tests/golden/e2e_v2/expected/expected_ledger.csv (9 rows, raw contract)
tests/golden/e2e_v2/expected/expected_reconciliation.csv (engine vocabulary, CERTIFICADO aggregate precomputed)
tests/golden/e2e_v2/expected/expected_summary.json (net 20800, treasury -20800, mirror 0)
tests/golden/e2e_v2/expected/expected_document_matches.csv (9 synthetic CONCILIATED)
tests/golden/e2e_v2/README.md (contracts + certification boundary NOT_TESTED)
tests/golden/e2e_v2/create_input.py
tests/golden/e2e_v2/test_golden_dataset_integrity.py (8/8 PASS)
```

Manual precomputations (BEFORE execution, from real contracts):
- operational 80000-15200-3500-50000+9500 = 20800; treasury -20800; mirror 0
- 9/9 matches → coverage 100; aggregate via _determine_status → CERTIFICADO

## Fresh DB Verification (PASS)

```
Fresh DatabaseV4 init on data/db/tmp_pfo_fa005_v2/ (NO baseline copy):
  document_match_v1 EXISTS (15 cols) — new DDL works
  ML_JUNE_LEDGER_ROWS = 0 / CLASSIFIED = 0 / CLOSING = 0 / DOCMATCH = 0
BASELINE_POLLUTION: NO
```

## Ingestion Result (FAIL — schema defect)

```
INGESTION_STATUS: FAILED
ERROR: Binder Error: Table "marketplace_ledger_v1" does not have a column with name "execution_id"
RECORDS_NEW: 0 / RAW_LEDGER_ROWS: 0 (clean failure, no partial writes)
```

## Defect (demonstrated, engine untouched)

```
DEFECT: FRESH_DB_LEDGER_MISSING_EXECUTION_ID
LOCATION: engine/v4/database.py init order —
  line 116 ALTER TABLE ... ADD COLUMN execution_id (runs BEFORE table exists on fresh DB → silent except-pass)
  line 141 CREATE TABLE marketplace_ledger_v1 (... no execution_id ...)
TRIGGER: SurgicalLoader sets df['execution_id'] when execution_id truthy
  (orchestrator always passes record.execution_id) → insert_df Binder Error.
SCOPE: fresh-DB ingestion only; baseline copies already carry the column.
EFFECT: the task-mandated fresh-DB path (PASO 5) cannot ingest. STOP per protocol.
```

Per task protocol (ENGINE_FILES_MODIFIED must be 0 → STOP + FAIL):
no workaround applied (inline ALTER in test setup would mask a real schema bug
to manufacture PASS). Separate schema-alignment repair task required.

## Chain Status (not reached)

```
CLASSIFICATION: NOT EXECUTED / CLOSING: NOT EXECUTED / DOCUMENT MATCHES: NOT WRITTEN
LEVEL_1/2/3/4: NOT EXECUTED / AGGREGATE: NOT EXECUTED
```

## Non-Contamination

```
PRODUCTION_DB_MODIFIED: FALSE (never opened)
REAL_RAW_MODIFIED: FALSE (E2E_V2 input never copied to 01_Raw/)
```

## Verdict

```
FA-005: FAIL (fresh-DB schema defect blocks mandated path; E2E_V1 FAIL evidence stands)
FA-006_STATUS: BLOCKED
FIRST_BLOCKER: FRESH_DB_LEDGER_MISSING_EXECUTION_ID — init-order schema gap
  (ALTER-before-CREATE); repair = include execution_id in ledger_v1 DDL or
  reorder migration after creation (dedicated task, NOT this one).
```

## Cleanup

```
TEMP_DIR data/db/tmp_pfo_fa005_v2/: REMOVED
Script tmp_fa005_v2_run.py: REMOVED
SurgicalLoader.DIR_FACTURACION: RESTORED (finally-block executed before failure return)
E2E_V2 golden files: KEPT (integrity-verified, insulted by no execution)
```

## XML/DTE Certification Gate (mandatory record)

```
XML_DTE_INGESTED: NO
DTE_TRUTH_POPULATED_FROM_XML: NO
DOCUMENT_MATCH_SOURCE: n/a (no matches written; execution stopped at ingestion)
XML_ELECTRONIC_CERTIFICATION: NOT_TESTED
```

## Next Exact Action

1. Dedicated schema repair task: align fresh-DB ledger_v1 DDL with loader
   contract (execution_id column), regression-test fresh ingestion.
2. Re-execute E2E_V2 full chain (this task's script + golden already prepared).
3. Then PFO-XML-DTE-E2E-001 for electronic certification.
