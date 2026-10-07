# Crash Recovery Runbook

**Scope:** Controlled upload writer lease + ingestion recovery only.

---

## Procedure

### 1. Stop Application / Confirm Writer Stopped

Ensure no active ingestion is running. Check application logs for in-flight uploads.

### 2. Inspect Lease

```bash
python tools/recover_stale_writer_lock.py inspect
```

Review output:
- `LOCK_EXISTS` — is a lease present?
- `PROCESS_STATE` — ALIVE | NOT_FOUND | UNKNOWN
- `AGE_SECONDS` — how old is the lease?

### 3. Check PID

If `PROCESS_STATE = ALIVE`, the writer process is still running.
**Do NOT proceed.** Wait for the process to complete or terminate it manually.

If `PROCESS_STATE = UNKNOWN`, fail closed. Do NOT delete the lock.
Investigate manually.

### 4. Check Ingestion Registry

The inspect command automatically checks for active ingestion records.
If `ACTIVE_INGESTION` is non-empty, recovery is blocked.

### 5. Check WAL

The inspect command automatically checks for WAL files.
If `WAL_EXISTS = TRUE`, recovery is blocked.

### 6. Confirm Recovery Eligibility

Recovery is eligible only if ALL are true:
- `PROCESS_STATE = NOT_FOUND`
- No active ingestion
- No WAL files

### 7. Run Explicit Recovery

```bash
python tools/recover_stale_writer_lock.py recover --confirm
```

This will:
1. Re-run full assessment
2. Verify eligibility
3. Preserve lock metadata to `<lock_path>.recovered.json`
4. Remove only the lock file
5. NOT touch the financial DB

### 8. Re-open DB Read-Only

```python
from engine.v4.database import DatabaseV4
db = DatabaseV4.get(read_only=True)
```

Verify the DB opens successfully.

### 9. Verify Registry / Partial Rows

Check `ingestion_registry` for any abandoned execution records.
Check `marketplace_ledger_v1` for partial rows from the crashed execution.

### 10. Retry Controlled Ingestion

Re-run the upload via the normal endpoint or UI.
The ingestion path's SHA256 dedup ensures idempotency.

### 11. Verify Idempotency / Result

Confirm:
- No duplicate ledger rows
- Result matches expected Golden
- Registry shows correct final status

---

## Emergency: Manual Lock Removal (NOT RECOMMENDED)

If the tool cannot be used, manual removal of `<db>.writer.lock` is possible
but **strongly discouraged**. Only do so if:
1. You have confirmed no writer process is running
2. You have confirmed no active ingestion
3. You have confirmed no WAL files exist
4. You have preserved the lock metadata for evidence

**Never delete a lock file without full assessment.**
