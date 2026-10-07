# BACKUP / RESTORE RUNBOOK — meli_financial_v4.db

Operational procedure. The tool (`tools/production_db_backup.py`) never
replaces the production DB automatically. Replacement stays manual + supervised.

## Backup (before any controlled write window)

1. Stop the application (`START_APP.bat` backend / uvicorn process).
2. Confirm zero active ingestion (no runaway `run_app.py` / worker processes).
3. Confirm no WAL: no `meli_financial_v4.db.wal` (or `-wal`/`-shm`/`-journal`)
   next to `data/db/meli_financial_v4.db`. If present: STOP, do not copy.
4. Run: `python tools/production_db_backup.py backup`
   → writes `data/backups/meli_financial_v4_<UTC>_<SHA12>.db` + `.manifest.json`.
5. Require `status PASS` and `SOURCE_SHA256 = BACKUP_SHA256` (printed + manifest).
6. Run: `python tools/production_db_backup.py verify <backup_file>`
   → require `status PASS` (open + manifest + schema + row counts match source).
7. Only then open the controlled write window.

## Restore (recovery only)

1. Stop the application.
2. Preserve the failed/current DB first (copy aside with timestamp; NEVER
   overwrite it in place as the first action).
3. Verify chosen backup SHA: `verify <backup_file>` must PASS.
4. Restore to a NEW path first:
   `python tools/production_db_backup.py restore-test <backup_file> --dest <isolated_dir>`
5. Verify the restored copy (open + schema + row counts equal source-at-backup).
6. Compare critical tables (ledger / clasificado / cierre / dte_truth / document_match).
7. Only after explicit operator approval: stop everything, swap the active DB
   file with the verified restore (keep the preserved copy), restart, re-verify
   `/api/v4/health`.

## Retention

- Backup files are immutable; manifests accompany every backup.
- Never overwrite an existing backup (tool refuses).
- No automatic deletion is implemented.
