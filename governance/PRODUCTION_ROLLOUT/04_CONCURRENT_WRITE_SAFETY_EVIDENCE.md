# 04 — Concurrent Write Safety Evidence

**TASK_ID:** PFO-CONCURRENT-WRITE-SAFETY-001
**DATE:** 2026-10-07
**BRANCH:** main
**HEAD_BEFORE:** af64e4523987b8ecd10247bb1f25469b51b0bfcf

---

## RCA

### LOCK_SCOPE_BEFORE

`DatabaseV4.__init__` creates `self.lock = threading.Lock()` — a **per-instance** lock.
`execute()` / `query()` / `insert_df()` acquire `self.lock`, so two `DatabaseV4` instances
pointing at the same physical DuckDB file **do not share the lock**.

```
DatabaseV4(path, read_only=False) instance A  →  self.lock = Lock_A
DatabaseV4(path, read_only=False) instance B  →  self.lock = Lock_B
```

`Lock_A` and `Lock_B` are different objects. Concurrent writes from two instances (or two
processes) are **not serialized** by this mechanism.

**CURRENT_LOCK_SCOPE = CONNECTION_INSTANCE_ONLY**

DuckDB's single-writer constraint is enforced at the file-handle level, but the application
layer had no operational policy to prevent two confirmed upload requests from both opening
writers simultaneously.

---

## LOCK_MECHANISM_AFTER

**File:** `engine/v4/write_guard.py`

Filesystem-based writer lease using atomic exclusive file creation (`O_CREAT | O_EXCL`).
Cross-process safe (not limited to threads). No queue, Redis, Celery, or external service.

### LOCK_PATH_RULE

```
lock_path = <resolved absolute DB path>.parent / (<DB filename>.writer.lock)
```

Identity derives **only** from the resolved absolute DB path — never marketplace, filename
pattern, or execution_id. Different DB files never block each other.

### LOCK_ATOMIC_ACQUIRE

```python
fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
```

Atomic on Windows. No `if not exists: create` race. Outcomes: `ACQUIRED | BUSY | ERROR`.

### LOCK_METADATA

Lease file contains only: `pid`, `created_at`, `db_path`, `request_id`.
No financial data, tokens, or credentials.

### STALE_LOCK_AUTO_RECOVERY

**NOT_IMPLEMENTED.** Stale leases are never auto-deleted. Fail closed is preferred to
double writer. A crash may leave a lease file; manual intervention required.

---

## Test Evidence

### SAME_PROCESS_TEST (§14)

**File:** `tests/test_write_guard.py::test_same_process_second_writer_rejected`

| Step | Result |
|------|--------|
| A acquires lease on TEMP DB | ACQUIRED |
| B attempts acquire on same DB | BUSY (WRITE_IN_PROGRESS) |
| B DB writes | 0 |
| A releases | TRUE |
| B retry after release | ACQUIRED |

**PASS**

### CROSS_PROCESS_TEST (§15)

**File:** `tests/test_write_guard.py::test_cross_process_second_writer_rejected`

Two independent OS processes via `subprocess.Popen`:

| Step | Result |
|------|--------|
| Process A acquires lease | ACQUIRED |
| Process B attempts while A holds | BUSY (WRITE_IN_PROGRESS) |
| A releases | TRUE |
| Process B new attempt | ACQUIRED |

**PASS** — proves no dependency on `threading.Lock`.

### API_CONCURRENT_TEST (§16)

**File:** `tests/test_upload_concurrency.py`

| Test | Result |
|------|--------|
| `test_api_second_writer_rejected_while_first_active` | 409 WRITE_IN_PROGRESS, 0 registry records, 0 ledger rows |
| `test_lease_held_across_real_pipeline_and_released` | Lease held during full pipeline, released after |

**PASS**

### DIFFERENT_DB_TEST (§17)

**File:** `tests/test_write_guard.py::test_different_db_concurrent_allowed`

| DB A | DB B |
|------|------|
| ACQUIRED | ACQUIRED (not blocked) |

**PASS** — lock is per-DB-path, not a global mutex.

### DRY_RUN_TEST (§18)

**File:** `tests/test_upload_concurrency.py::test_dry_run_creates_no_lease`

`dry_run=true` → no lease created, 0 DB writes. **PASS**

### UNCONFIRMED_TEST (§19)

**File:** `tests/test_upload_concurrency.py::test_unconfirmed_write_creates_no_lease`

`dry_run=false&confirm_write=false` → HTTP 409 WRITE_NOT_CONFIRMED, no lease, 0 writes. **PASS**

### FAILURE_RELEASE_TEST (§21)

**File:** `tests/test_upload_concurrency.py::test_failed_run_releases_lease`

Invalid input after lease acquire → status=FAILED, lease released, subsequent valid run acquires. **PASS**

### EXCEPTION_RELEASE_TEST (§11)

`try/finally` in `api/api.py` guarantees release on COMPLETED, FAILED, and exception paths.
Verified by `test_failed_run_releases_lease` and `test_duplicate_run_releases_lease`. **PASS**

### DUPLICATE_RELEASE_TEST (§22)

**File:** `tests/test_upload_concurrency.py::test_duplicate_run_releases_lease`

`SKIPPED_DUPLICATE` → lease released normally. **PASS**

### PRODUCTION_TEST_MODE_BEHAVIOR (§20)

`authorize_db_write()` blocks production writes in TEST mode before lease acquisition.
No production DB modification. **PASS**

---

## UI_BUSY_BEHAVIOR (§24)

**File:** `templates/upload_center.html`

On HTTP 409 `WRITE_IN_PROGRESS`:
- File reverts to `validated` state (user decides when to retry)
- Message: "Otro procesamiento está en curso. Intenta nuevamente cuando finalice."
- No auto-retry, no `setTimeout`/`setInterval`, no `Promise.all`

**UI_WRITE_MODE = SEQUENTIAL** — `confirmProcess()` uses `for...await`, not parallel writes.

---

## NON_CONTAMINATION

| Check | Result |
|-------|--------|
| PRODUCTION_DB_MODIFIED | NO |
| REAL_RAW_MODIFIED | NO |
| FINANCIAL_CORE_MODIFIED | NO |
| GOLDEN_FILES_MODIFIED | NO |
| DatabaseV4 financial semantics | Unchanged |
| Ledger/classification/closing/reconciliation | Unchanged |

---

## REGRESSION_RESULTS

| Suite | Tests | Result |
|-------|-------|--------|
| `test_write_guard.py` | 7 | PASS |
| `test_upload_concurrency.py` | 6 | PASS |
| `test_upload_center_controlled_ux.py` | 19 | PASS |
| `test_upload_center_e2e.py` | 13 | PASS |
| `test_ingestion_handlers.py` | 56 | PASS |
| E2E_V1 golden integrity (isolated) | 11 | PASS |
| E2E_V2 golden integrity | 8 | PASS |
| **Total** | **120** | **ALL PASS** |

---

## CRASH_BOUNDARY

Abrupt process death may leave a lease file. The system **fails closed**: subsequent writes
are rejected with `WRITE_IN_PROGRESS` until manual intervention.

**CRASH_SAFETY = PARTIAL** (unchanged)

---

## VERDICT

```
CONTROLLED_UPLOAD_CONCURRENT_WRITE_SAFETY = PASS
CONCURRENT_WRITE_SAFETY = PASS_FOR_CONTROLLED_UPLOAD_PATH
```

Scope: `POST /api/v4/ingestion/upload` with `dry_run=false&confirm_write=true` only.
External scripts opening DuckDB directly are not covered.
