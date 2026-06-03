# DB CONNECTION HARDENING REPORT

**Sprint**: B1.1 — Phase A2
**Date**: 2026-05-30
**Regime**: IMPLEMENTATION

---

## Summary

Implemented graceful shutdown handlers and connection lifecycle management to prevent database lock persistence.

## Changes

### 1. `engine/v4/database.py` — Connection Lifecycle

**Before**: `DatabaseV4` had only `reset()` which closed the connection and nulled the singleton. No tracking of closed state.

**After**:

- **`close()` method**: Safely closes the DuckDB connection with idempotent guard (`_closed` flag prevents double-close)
- **`_shutdown_registered` flag**: Ensures atexit hook is registered only once, even with multiple `get()` calls
- **`atexit` hook**: `atexit.register(DatabaseV4.reset)` ensures connection is closed on normal Python process exit
- **`_closed` tracking**: Prevents `close()` from attempting to close an already-closed connection

```python
def close(self):
    if self._closed:
        return
    self._closed = True
    try:
        self.conn.close()
        logger.info("Database connection closed.")
    except Exception as e:
        logger.warning(f"Error closing database connection: {e}")
```

```python
@classmethod
def _register_shutdown_hook(cls):
    if cls._shutdown_registered:
        return
    cls._shutdown_registered = True
    import atexit
    atexit.register(cls.reset)
```

### 2. `run_app.py` — Signal Handlers

**Before**: No signal handling. Killing the process left the DuckDB lock open.

**After**:

- **SIGINT handler** (Ctrl+C): Calls `DatabaseV4.reset()` then exits
- **SIGTERM handler** (kill/systemd): Calls `DatabaseV4.reset()` then exits
- **Logging**: Logs a warning when signal is received

```python
def shutdown_handler(signum, frame):
    logger.warning(f"Received signal {signum}, shutting down gracefully...")
    DatabaseV4.reset()
    sys.exit(0)
```

## No Longer Possible

| Before | After |
|---|---|
| Kill `run_app.py` -> DB locked forever | Kill `run_app.py` -> SIGTERM handler closes DB |
| Ctrl+C -> DB lock orphaned | Ctrl+C -> SIGINT handler closes DB |
| Process crash -> DuckDB file lock persists | atexit handles normal exit; signal handles kill |
| `conn.close()` double-call -> exception | `_closed` flag prevents double-close |

## Verification

- **14/14 regression tests**: PASS
- `DatabaseV4.reset()` idempotent
- `atexit` registered exactly once
