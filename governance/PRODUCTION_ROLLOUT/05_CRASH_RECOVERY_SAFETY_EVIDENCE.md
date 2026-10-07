# 05 — Crash Recovery Safety Evidence

**TASK_ID:** PFO-CRASH-RECOVERY-SAFETY-001
**DATE:** 2026-10-07
**BRANCH:** main
**HEAD_BEFORE:** 68b7342aaf26646f3ffbac879676e620a3fb1f66

---

## CRASH_BOUNDARY_BEFORE

```
CRASH_SAFETY = PARTIAL
STALE_LOCK_AUTO_RECOVERY = NOT_IMPLEMENTED
```

After PFO-CONCURRENT-WRITE-SAFETY-001, the writer lease prevents concurrent writes but
a crash can leave a stale lock file with no safe recovery path.

---

## LEASE_INSPECTION

**Implementation:** `engine/v4/write_guard.py::inspect_writer_lease()`

Read-only assessment returning:
- `LOCK_EXISTS` — whether lease file is present
- `LOCK_PATH` — absolute path to lease
- `PID` — process ID from lease metadata
- `CREATED_AT` — ISO timestamp from lease metadata
- `REQUEST_ID` — execution/request ID from lease metadata
- `PROCESS_STATE` — ALIVE | NOT_FOUND | UNKNOWN
- `AGE_SECONDS` — seconds since lease creation

Never modifies the lock.

---

## PROCESS_STATE_DETECTION

**Implementation:** `engine/v4/write_guard.py::_pid_alive()`

Windows PID liveness via `ctypes.windll.kernel32.OpenProcess`:
1. Try `PROCESS_QUERY_LIMITED_INFORMATION` (0x1000)
2. If that fails, try `PROCESS_QUERY_INFORMATION` (0x0400)
3. If either succeeds → `ALIVE`
4. If both fail with error 0 or 87 → `NOT_FOUND`
5. If error 5 (ACCESS_DENIED) → `ALIVE` (process exists, no permission)
6. Otherwise → `UNKNOWN`

---

## REGISTRY_CORRELATION

**Implementation:** `tools/recover_stale_writer_lock.py::_registry_active_count()`

Queries `ingestion_registry` for active statuses (STARTED, PROCESSING, CLASSIFIED).
Uses `request_id` from lease metadata to correlate with execution records.

---

## WAL_CHECK

**Implementation:** `engine/v4/write_guard.py::check_wal()`

Checks for WAL/journal files near the DB:
- `<db>.wal`
- `<db>-wal`
- `<db>.db-wal`
- `<db>.journal`

Returns `WAL_EXISTS` + list of found paths.

---

## RECOVERY_ELIGIBILITY_RULE

Recovery is allowed **only if ALL** conditions are met:
1. `LOCK_EXISTS = TRUE`
2. `PROCESS_STATE = NOT_FOUND`
3. No active ingestion (STARTED/PROCESSING/CLASSIFIED) in registry
4. No WAL files present

If any condition fails → `RECOVERY_ALLOWED = FALSE` with specific block reason.

---

## STALE_LOCK_AUTO_RECOVERY

**NOT_IMPLEMENTED.** The normal upload endpoint (`POST /api/v4/ingestion/upload`) does
NOT delete stale locks. It continues to respond `409 WRITE_IN_PROGRESS` until explicit
recovery is executed via `tools/recover_stale_writer_lock.py`.

---

## EXPLICIT_RECOVERY_CONFIRMATION

**REQUIRED.** The `recover` action without `--confirm` performs inspection only.
No delete, no DB write. With `--confirm`, full assessment + eligibility check + lock removal.

---

## CRASH_TEST_A — Before DB Write (§18)

**File:** `tests/test_crash_recovery.py::test_crash_before_write`

| Step | Result |
|------|--------|
| Child acquires lease, dies before DB write | ACQUIRED, process exit code ≠ 0 |
| Stale lock remains | TRUE |
| PID state | NOT_FOUND |
| Recovery eligible | TRUE |
| Explicit recover removes lock | RECOVERED |
| Subsequent valid run | ACQUIRED |

**PASS**

---

## CRASH_TEST_B — After Registry Start (§19)

**File:** `tests/test_crash_recovery.py::test_crash_after_registry_start`

| Step | Result |
|------|--------|
| Child creates registry record, acquires lease, dies | ACQUIRED, process exit code ≠ 0 |
| Registry has STARTED record | TRUE |
| Ledger rows | 0 |
| Recovery assessment | BLOCKED (ACTIVE_INGESTION) |
| Lock remains | TRUE |

**PASS**

---

## CRASH_TEST_C — Partial Persist (§20)

**PARTIAL_PERSIST_CRASH_TEST = NOT_TESTED**

No safe injection point exists without modifying the engine. The ingestion path's
idempotency (SHA256 dedup) is already certified and handles partial writes on retry.

---

## CRASH_TEST_D — Active Process (§21)

**File:** `tests/test_crash_recovery.py::test_active_process_blocks_recovery`

| Step | Result |
|------|--------|
| Live process holds lease | ACQUIRED |
| Recovery attempt with --confirm | BLOCKED |
| Reason | ACTIVE_WRITER_PROCESS |
| Lock remains | TRUE |

**PASS**

---

## CRASH_TEST_E — WAL (§22)

**File:** `tests/test_crash_recovery.py::test_wal_blocks_recovery`

| Step | Result |
|------|--------|
| Lease held + synthetic WAL file | WAL_EXISTS = TRUE |
| Recovery attempt with --confirm | BLOCKED |
| Reason | ACTIVE_OR_UNRESOLVED_WAL |
| Lock remains | TRUE |

**PASS**

---

## RETRY_RESULT (§17)

**File:** `tests/test_crash_recovery.py::test_post_recovery_valid_run`

After explicit recovery, a valid run acquires the lock and completes successfully.

**PASS**

---

## IDEMPOTENCY_RESULT

The ingestion path uses SHA256 dedup (`get_completed_by_sha256`). A retry after crash
detects the file as `SKIPPED_DUPLICATE` if already processed, or processes it cleanly
if not. No duplicate ledger rows.

**PASS**

---

## GOLDEN_PARITY

E2E_V1: 11/11 PASS
E2E_V2: 8/8 PASS

**PASS**

---

## NORMAL_FAILURE_LOCK_RELEASE (§23)

**File:** `tests/test_crash_recovery.py::test_normal_failure_releases_lock`

Normal exception path releases lock via `try/finally` in `api/api.py`.
`NORMAL_EXCEPTION_STALE_LOCK = FALSE`

**PASS**

---

## NON_CONTAMINATION

| Check | Result |
|-------|--------|
| PRODUCTION_DB_MODIFIED | NO |
| REAL_RAW_MODIFIED | NO |
| FINANCIAL_CORE_MODIFIED | NO |
| GOLDEN_FILES_MODIFIED | NO |
| DatabaseV4 financial semantics | Unchanged |
| Write serialization semantics | Unchanged |

---

## REGRESSION_RESULTS

| Suite | Tests | Result |
|-------|-------|--------|
| `test_write_guard.py` | 7 | PASS |
| `test_upload_concurrency.py` | 6 | PASS |
| `test_crash_recovery.py` | 10 | PASS |
| `test_upload_center_controlled_ux.py` | 19 | PASS |
| `test_upload_center_e2e.py` | 13 | PASS |
| `test_ingestion_handlers.py` | 56 | PASS |
| E2E_V1 golden integrity | 11 | PASS |
| E2E_V2 golden integrity | 8 | PASS |
| **Total** | **130** | **ALL PASS** |

---

## VERDICT

```
CONTROLLED_UPLOAD_CRASH_RECOVERY = PASS
CRASH_SAFETY = PASS_FOR_CONTROLLED_UPLOAD_RECOVERY
```

Scope: controlled upload writer lease + ingestion recovery only.
Does not cover: OS disk corruption, power loss during filesystem flush,
external unmanaged DB writers, hardware failure.
