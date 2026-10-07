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


def _pid_alive(pid: int) -> str:
    """Minimal Windows PID liveness check. Returns ALIVE | NOT_FOUND | UNKNOWN."""
    if not isinstance(pid, int) or pid <= 0:
        return "UNKNOWN"
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # Try PROCESS_QUERY_LIMITED_INFORMATION (0x1000) first
        handle = kernel32.OpenProcess(0x1000, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return "ALIVE"
        # If that fails, try PROCESS_QUERY_INFORMATION (0x0400)
        handle = kernel32.OpenProcess(0x0400, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return "ALIVE"
        # Process cannot be opened — check error code
        err = ctypes.get_last_error()
        # ERROR_INVALID_PARAMETER (87) or error 0 (ctypes quirk) → not found
        # ERROR_ACCESS_DENIED (5) → process exists but we can't query it
        if err in (0, 87):
            return "NOT_FOUND"
        if err == 5:  # ACCESS_DENIED → process likely exists
            return "ALIVE"
        return "UNKNOWN"
    except Exception:
        return "UNKNOWN"


def inspect_writer_lease(db_path: str | Path) -> dict[str, Any]:
    """Read-only assessment of a writer lease. Never modifies the lock.

    Returns: LOCK_EXISTS, LOCK_PATH, PID, CREATED_AT, REQUEST_ID,
             PROCESS_STATE, AGE_SECONDS
    """
    lock_path = lock_path_for(db_path)
    if not lock_path.exists():
        return {"LOCK_EXISTS": False, "LOCK_PATH": str(lock_path)}
    meta = read_lease(db_path) or {}
    pid = meta.get("pid")
    created_at = meta.get("created_at")
    age_seconds = None
    if created_at:
        try:
            dt = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            age_seconds = (datetime.datetime.now(datetime.timezone.utc) - dt).total_seconds()
        except Exception:
            pass
    return {
        "LOCK_EXISTS": True,
        "LOCK_PATH": str(lock_path),
        "PID": pid,
        "CREATED_AT": created_at,
        "REQUEST_ID": meta.get("request_id"),
        "PROCESS_STATE": _pid_alive(pid) if pid else "UNKNOWN",
        "AGE_SECONDS": age_seconds,
    }


def check_wal(db_path: str | Path) -> dict[str, Any]:
    """Check for WAL/journal files near the DB. Returns WAL_EXISTS + paths."""
    resolved = Path(db_path).resolve()
    parent = resolved.parent
    name = resolved.name
    candidates = [
        parent / (name + ".wal"),
        parent / (name + "-wal"),
        parent / (name + ".db-wal"),
        parent / (name + ".journal"),
    ]
    found = [str(p) for p in candidates if p.exists()]
    return {"WAL_EXISTS": bool(found), "WAL_PATHS": found}
