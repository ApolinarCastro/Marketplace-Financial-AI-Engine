# PRODUCTION ROLLOUT READINESS — EVIDENCE

## Task Info

```
TASK_ID: PFO-PRODUCTION-ROLLOUT-READINESS-001
DATE: 2026-10-07
HEAD: 7cd78de747eccf195e2af7f8d75f8c6129e67341
BRANCH: main
```

Audit (not deployment). Certified core frozen — zero engine/golden changes.
All runtime probes used TEMP DBs + golden data; production opened read-only only.

## Persistent State (recovered, not from chat memory)

```
FA-001..FA-007: ALL PASS / FIRST END-TO-END CERTIFIED PASS ACHIEVED
DOCUMENTAL_XML_TRACEABILITY / FINANCIAL_DTE_MATCH / XML_DTE_E2E: PASS
ELECTRONIC_SIGNATURE_CERTIFICATION: NOT_IMPLEMENTED
```

## Startup (§4)

```
START_COMMAND: START_APP.bat → .venv python run_app.py → uvicorn api.api:app
HOST: 127.0.0.1 (HARDCODED) / PORT: 3001 (HARDCODED)
PROJECT_ROOT: repo root DEFAULTED, MF_PROJECT_ROOT override EXPLICIT (loaders)
DATABASE_PATH: C:/.../data/db/meli_financial_v4.db (HARDCODED default)
RAW_PATH: <root>/01_Raw (DEFAULTED, overridable) / LOG_PATH: logs/ / TEMP: system temp
APP_BOOT: PASS / HEALTH_ENDPOINT: PASS (/app 200 88952B; /health READY x8 subsystems)
```

## Config Isolation (§5)

```
PRODUCTION = DatabaseV4.get() defaults (hardcoded DB_PATH + repo-root RAW).
TEST = explicit db_path injection + MF_PROJECT_ROOT redirect + singleton binding.
Separation mechanism PROVEN across all FA tasks (zero contamination, SHA-verified).
BUT: no automatic guard. api.py upload endpoint opens a WRITER on the singleton
production path with hardcoded marketplace="ML"/period="2026-01", marks COMPLETED
without running DETECT/VALIDATE/CLASSIFY ("test loader patching" scaffolding comments
in production code), and no dry-run/confirmation mode exists anywhere.
PRODUCTION_CONFIG_ISOLATION: PARTIAL (mechanism unequivocal; safety by convention only)
```

## Database (§6/§7)

```
FRESH_DB_STARTUP: PASS (6/6 critical tables created empty on fresh init)
PRODUCTION_DB_READ_ONLY_ACCESS: PASS (58,732,544B, 37 tables, ledger 601559,
  clasificado 601559, cierre 203, dte_truth 667, document_match 9431;
  dte_certified_match_v1 absent on production — expected, fresh-DDL table w/o prod writer)
```

## Backup/Restore (§8)

```
BACKUP_PROCEDURE: MISSING (ad-hoc snapshots only; no reproducible backup→verify→restore)
RESTORE_PROCEDURE: MISSING (same)
```

## RAW Safety (§9)

```
RAW_SOURCE_IMMUTABLE: TRUE (loader/ingestion code reads only: pandas/openpyxl/calamine
+ SHA256 registry; zero write/move/rename/delete/archive calls found; real RAW
untouched across every executed run, verified)
```

## Idempotency (§10, TEMP DB + E2E_V2)

```
Run1 COMPLETED 9 new / Run2 SKIPPED_DUPLICATE (SHA256 dedup) 0 new 9 existing
LEDGER: 9 rows (no duplication), total 0.0 (20800 + -20800), 1 execution_id
INGESTION_IDEMPOTENCY: PASS / LEDGER_IDEMPOTENCY: PASS
DOCUMENT_MATCH_IDEMPOTENCY: PASS (INSERTED → SKIPPED_EXISTING)
```

## Crash Safety (§11, code analysis)

```
Atomic transactions: NONE in ingestion path (no BEGIN/COMMIT/ROLLBACK).
Partial state possible (ledger persisted, registry unfinalized).
Forensic recovery: YES via execution_id (STARTED without end_time).
Retry: SAFE for ledger content (DELETE+reinsert per archivo_origen; SHA dedup
skips COMPLETED); registry accumulates FAILED + fresh record (no false CERTIFIED).
CRASH_SAFETY: PARTIAL
```

## Concurrency (§12)

```
DuckDB single-writer enforced by engine; threading.Lock is per-connection only.
No app-level ingestion queue, mutex, or concurrent-write policy found.
CONCURRENT_WRITE_SAFETY: NOT_PROVEN
```

## Auditability (§13)

```
IngestionRecord persists: execution_id, timestamps, user, marketplace, doc type,
SHA256, size, loader, pipeline, counts, errors, warnings, certification/knowledge status.
EXECUTION_AUDITABILITY: PASS
```

## Fail-Closed (§14, TEMP DB, invalid XLSX)

```
Status FAILED + recorded error (PERSIST: NO_DATA), no false COMPLETED.
FAIL_CLOSED: TRUE
```

## Restart After Failure (§15)

```
Fresh TEMP DB + valid golden → COMPLETED, 9 new. Prior failure left no global
corruption (isolated TEMP DBs; singleton reset between phases).
RESTART_AFTER_FAILURE: PASS
```

## Secrets (§17)

```
Tracked .env/.pem/.key/private-key files: 0. Real tokens/keys in api/ + engine/: none
(77 broad-pattern hits all false positives: doc names, test placeholder tokens).
SECRETS_FOUND: NO
```

## E-Sign Boundary (§18, unchanged)

```
ELECTRONIC_SIGNATURE_CERTIFICATION: NOT_IMPLEMENTED (known limitation, never PASS)
```

## Known Findings (§19, re-verified standing)

```
- fresh DB matcher.run() RIPLEY branch needs ripley_settlement_chain: STANDING
  (fresh DDL gap; ML-scoped execution unaffected)
- _trace_transaction KeyError on empty certified set: STANDING (robustness edge)
- e-sign NOT_IMPLEMENTED + degraded-PASS now fail-closed: STANDING as boundary
- pytest basename collision (e2e_v1/e2e_v2 integrity): STANDING (run separately)
- conftest TEMP_V8_BASE race flake: STANDING (retry passes; unrelated to changes)
- NEW: DocumentMatchWriter NaN-vs-None idempotency edge on amount-less rewrites
  (found during audit probing; complete records unaffected, 10/10 certified tests
  pass; recorded for hardening, NOT a blocker — engine untouched per audit rule)
```

## Rollback (§20)

```
CODE_ROLLBACK_POINT: VERIFIED (7cd78de exists locally as commit + remote HEAD)
```

## Readiness Matrix (§21)

```
APP_STARTUP: PASS / DATABASE_STARTUP: PASS / PRODUCTION_DB_READ_ONLY_ACCESS: PASS
CONFIG_ISOLATION: PARTIAL / RAW_IMMUTABILITY: PASS
BACKUP: MISSING / RESTORE: MISSING
INGESTION_IDEMPOTENCY: PASS / LEDGER_IDEMPOTENCY: PASS / DOCUMENT_MATCH_IDEMPOTENCY: PASS
FAIL_CLOSED: PASS / RESTART_AFTER_FAILURE: PASS
CONCURRENT_WRITE_SAFETY: NOT_PROVEN / AUDITABILITY: PASS (EXECUTION_AUDITABILITY)
SECRETS: PASS (SECRETS_FOUND NO) / ROLLBACK: PASS
ELECTRONIC_SIGNATURE: NOT_IMPLEMENTED (boundary, not blocker for controlled rollout)
```

## Rollout Decision (§22/§23)

```
READINESS_DECISION: NOT_READY_FOR_CONTROLLED_ROLLOUT
FIRST_BLOCKER: upload-endpoint production-write hardening (remove test scaffolding,
  run real pipeline stages instead of hardcoded COMPLETED, add explicit
  production confirmation or dry-run mode) + config guard so test/prod separation
  does not rely on caller discipline alone.
ROOT_CAUSE: §23 minimum requires CONFIG_ISOLATION = PASS; assessed PARTIAL
  (mechanism proven, safety by convention; live unguarded writer in upload path).
MINIMAL_NEXT_ACTION: dedicated hardening task scoped to the ingestion upload path
  + config guard; no financial-logic changes needed.
Other material risks (not §23-blocking, recorded): BACKUP/RESTORE MISSING,
  CONCURRENT_WRITE_SAFETY NOT_PROVEN, crash atomicity PARTIAL.
```

## Non-Contamination / Cleanup

```
PRODUCTION_DB_MODIFIED: FALSE / REAL_RAW_MODIFIED: FALSE
TEMP dirs (tmp_pfo_rollout) + scripts (tmp_rollout_run, tmp_health_probe, tmp_prod_health): REMOVED (verified)
ENGINE_FILES_MODIFIED: 0 / GOLDEN_FILES_MODIFIED: 0 / TEST_FILES_MODIFIED: 0
```

## Next Exact Action

Hardening task for the ingestion upload path + config guard (single blocker).
Then re-audit CONFIG_ISOLATION only. No FA re-certification needed (core untouched).
