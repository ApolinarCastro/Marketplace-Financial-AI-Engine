"""Filesystem writer lease for controlled database writes.

Guarantees MAX_ACTIVE_CONTROLLED_WRITERS = 1 per physical database file,
across threads AND processes, using atomic exclusive file creation
(O_CREAT | O_EXCL). A threading.Lock alone cannot do this: each
DatabaseV4 instance owns a private lock, and separate processes share
nothing.

Lease identity derives from the resolved absolute DB path only —
never marketplace, filename, or execution_id. Different DB files never
block each other.

Fail-closed semantics:
- lease present (by anyone) -> second writer REJECTED (no waiting, no retry);
- stale leases are NEVER auto-deleted (fail closed beats double writer);
- release always runs in try/finally by the holder.

Lease files carry operational metadata only (pid, timestamps, db path,
request id). No financial data, tokens, or credentials.
"""
from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import Any


def lock_path_for(db_path: str | Path) -> Path:
    """Deterministic lease path for a database file (never versioned)."""
    resolved = Path(db_path).resolve()
    return resolved.parent / (resolved.name + ".writer.lock")


def _metadata(db_path: str | Path, request_id: str | None) -> dict[str, Any]:
    return {
        "pid": os.getpid(),
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "db_path": str(Path(db_path).resolve()),
        "request_id": request_id,
    }


def acquire(db_path: str | Path, request_id: str | None = None) -> dict[str, Any]:
    """Atomically acquire the writer lease. Returns status dict.

    Outcomes: ACQUIRED | BUSY | ERROR. Never blocks, never retries.
    """
    lock_path = lock_path_for(db_path)
    try:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return {"status": "ERROR", "detail": f"lock dir unavailable: {e}",
                "lock_path": str(lock_path)}
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    try:
        fd = os.open(str(lock_path), flags)
    except FileExistsError:
        return {"status": "BUSY", "detail": "WRITE_IN_PROGRESS",
                "lock_path": str(lock_path)}
    except Exception as e:
        return {"status": "ERROR", "detail": f"{type(e).__name__}: {e}",
                "lock_path": str(lock_path)}
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(_metadata(db_path, request_id), f)
    except Exception:
        try:
            lock_path.unlink(missing_ok=True)
        except Exception:
            pass
        return {"status": "ERROR", "detail": "lease metadata write failed",
                "lock_path": str(lock_path)}
    return {"status": "ACQUIRED", "lock_path": str(lock_path)}


def release(db_path: str | Path) -> bool:
    """Remove the lease file. Best-effort; returns True when absent afterwards."""
    try:
        lock_path_for(db_path).unlink(missing_ok=True)
    except Exception:
        pass
    return not lock_path_for(db_path).exists()


def is_locked(db_path: str | Path) -> bool:
    """True when a lease file currently exists (holder unknown)."""
    return lock_path_for(db_path).exists()


def read_lease(db_path: str | Path) -> dict[str, Any] | None:
    """Read lease metadata for evidence/logging. Never exposes secrets (none stored)."""
    try:
        return json.loads(lock_path_for(db_path).read_text(encoding="utf-8"))
    except Exception:
        return None
