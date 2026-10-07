# PRODUCTION BACKUP / RESTORE — EVIDENCE

## Task Info

```
TASK_ID: PFO-PRODUCTION-BACKUP-RESTORE-001
DATE: 2026-10-07
HEAD_BEFORE: fb714e5507923db0db74f0c2a7abb34726b60947
BRANCH: main
```

## Preconditions (verified before backup)

```
ACTIVE_WRITER_CHECK: NONE (stopped leftover audit backend PID 8360 run_app.py; zero Marketplace processes after)
ACTIVE_INGESTION_CHECK: 0 (no app running)
WAL_STATUS: CLEAN (no .wal/-wal/.db-wal/-shm/.db-shm/-journal artifacts beside production DB)
```

## Backup

```
PRODUCTION_DB_PATH: data/db/meli_financial_v4.db
PRODUCTION_DB_SIZE: 58732544
PRODUCTION_DB_SHA_BEFORE: 4efcaa8aa950aa6731a1f0d16624e3a62f3831b7caaf521e31218deaf8155709
BACKUP_FILE: data/backups/meli_financial_v4_20261007T155646Z_4efcaa8aa950.db (git-ignored, never committed)
BACKUP_MANIFEST: ...db.manifest.json (version 1.0.0, commit fb714e5, engine duckdb, SHA_MATCHED)
BACKUP_SIZE: 58732544 / BACKUP_SHA256: 4efcaa8a... (== source)
SOURCE_BACKUP_SHA_MATCH: TRUE
```

## Verify (backup vs live source, both read-only)

```
BACKUP_DB_OPEN: PASS
ledger 601559 / clasificado 601559 / cierre 203 / dte_truth 667 / document_match 9431
SOURCE counts identical (read live in same execution, not hardcoded).
BACKUP_SCHEMA_MATCH: TRUE / BACKUP_ROW_COUNTS_MATCH: TRUE
```

## Restore Test (isolated path, production never overwritten)

```
RESTORE_TEST_PATH: data/db/tmp_pfo_restore_test/meli_financial_v4_restored.db (removed after)
RESTORE_DB_OPEN: PASS / RESTORE_SIZE: 58732544
RESTORE_SHA256 == BACKUP_SHA256 == SOURCE_SHA256 (triple match)
RESTORE_SCHEMA_MATCH: TRUE / RESTORE_ROW_COUNTS_MATCH: TRUE
APP COMPATIBILITY (DatabaseV4 read_only on restored copy): ledger/classified/
closing/dte/matches all readable with production counts → PASS
```

## Corruption Control

```
Corrupted COPY (byte flip at offset 1024; original untouched):
verify → FAIL via DuckDB checksum error + SHA mismatch + manifest_ok false.
CORRUPTED_BACKUP_REJECTED: TRUE. Corrupt copy deleted.
```

## WAL Safety Guard

```
Covered by unit test (synthetic .wal marker → BLOCKED ACTIVE_DUCKDB_WAL).
Production had no WAL artifacts at backup time.
WAL_SAFETY_GUARD: PASS
```

## Tests (tests/test_production_db_backup.py, synthetic TEMP DBs, 6/6 PASS)

```
byte parity + manifest / verify + restore-test / corrupted rejected /
no-overwrite / WAL guard / restore-never-targets-production
```

## Non-Contamination / Cleanup

```
PRODUCTION_DB_SHA_AFTER: 4efcaa8aa950aa6731a1f0d16624e3a62f3831b7caaf521e31218deaf8155709
PRODUCTION_DB_MODIFIED: FALSE / REAL_RAW_MODIFIED: FALSE
TEMP_ARTIFACTS_LEFT: 0 (restore-test dir, corrupt copy, probe scripts removed)
Real backup + manifest KEPT on disk under git-ignored data/backups/ (operational evidence, never committed).
```

## Runbook / Retention / Security

```
BACKUP_RUNBOOK: governance/PRODUCTION_ROLLOUT/BACKUP_RESTORE_RUNBOOK.md
  (stop → zero ingestion → no WAL → backup → SHA/manifest → verify →
  controlled window; restore = preserve-first → verify → isolated restore →
  compare → explicit approval → swap. Tool never auto-replaces production.)
Retention: immutable files, manifest per backup, never overwrite, no auto-delete.
Security: data/backups/ + data/db/*.db + data/db/tmp_*/ all git-ignored (verified
  via git check-ignore); no backup committed.
```

## Verdict

```
BACKUP_PROCEDURE: PASS / RESTORE_PROCEDURE: PASS
READINESS_DECISION: READY_FOR_CONTROLLED_ROLLOUT (unchanged; backup gap closed)
Open risks retained: CONCURRENT_WRITE_SAFETY NOT_PROVEN, CRASH_SAFETY PARTIAL,
ELECTRONIC_SIGNATURE NOT_IMPLEMENTED. Never FULL_PRODUCTION_READY.
```

## Next Exact Action

PFO-UPLOAD-CENTER-CONTROLLED-UX-001 (only after this PASS; frontend untouched here).
