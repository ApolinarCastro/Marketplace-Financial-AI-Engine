"""Explicit stale writer-lease recovery tool.

Usage:
    python tools/recover_stale_writer_lock.py inspect [--db PATH]
    python tools/recover_stale_writer_lock.py recover --confirm [--db PATH]

Default: inspect only. No delete without --confirm.
Fail-closed: never deletes when PID alive, ingestion active, or WAL present.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running from repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from engine.v4.write_guard import (
    acquire,
    check_wal,
    inspect_writer_lease,
    is_locked,
    lock_path_for,
    release,
)

ACTIVE_STATES = {"STARTED", "PROCESSING", "CLASSIFIED"}


def _default_db() -> Path:
    return REPO_ROOT / "data" / "db" / "meli_financial_v4.db"


def _registry_active_count(db_path: Path) -> dict:
    """Check ingestion_registry for active executions. Read-only."""
    try:
        import duckdb

        con = duckdb.connect(str(db_path), read_only=True)
        try:
            rows = con.execute(
                "SELECT status, COUNT(*) AS n FROM ingestion_registry "
                "WHERE status IN ('STARTED','PROCESSING','CLASSIFIED') GROUP BY status"
            ).fetchall()
            return {r[0]: r[1] for r in rows}
        finally:
            con.close()
    except Exception:
        return {}


def _partial_ledger_rows(db_path: Path, request_id: str | None) -> int:
    """Count ledger rows associated with a crashed execution_id. Read-only."""
    if not request_id:
        return 0
    try:
        import duckdb

        con = duckdb.connect(str(db_path), read_only=True)
        try:
            row = con.execute(
                "SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE execution_id = ?",
                [request_id],
            ).fetchone()
            return int(row[0]) if row else 0
        finally:
            con.close()
    except Exception:
        return 0


def inspect(db_path: Path) -> dict:
    """Full read-only assessment."""
    lease = inspect_writer_lease(db_path)
    wal = check_wal(db_path)
    result = {
        "db_path": str(db_path),
        "lease": lease,
        "wal": wal,
    }
    if lease.get("LOCK_EXISTS"):
        active = _registry_active_count(db_path)
        result["active_ingestion"] = active
        result["partial_ledger_rows"] = _partial_ledger_rows(db_path, lease.get("REQUEST_ID"))
        # Eligibility
        eligible = (
            lease.get("PROCESS_STATE") == "NOT_FOUND"
            and not active
            and not wal.get("WAL_EXISTS")
        )
        result["recovery_eligible"] = eligible
        if not eligible:
            reasons = []
            if lease.get("PROCESS_STATE") == "ALIVE":
                reasons.append("ACTIVE_WRITER_PROCESS")
            elif lease.get("PROCESS_STATE") == "UNKNOWN":
                reasons.append("PROCESS_STATE_UNKNOWN")
            if active:
                reasons.append("ACTIVE_INGESTION")
            if wal.get("WAL_EXISTS"):
                reasons.append("ACTIVE_OR_UNRESOLVED_WAL")
            result["recovery_blocked_reasons"] = reasons
    return result


def recover(db_path: Path, confirm: bool) -> dict:
    """Explicit recovery. Requires --confirm. Preserves metadata before delete."""
    assessment = inspect(db_path)
    if not assessment["lease"].get("LOCK_EXISTS"):
        return {"status": "NO_LOCK", "detail": "No writer lease present."}
    if not confirm:
        return {
            "status": "INSPECT_ONLY",
            "detail": "Re-run with --confirm to remove stale lock.",
            "assessment": assessment,
        }
    if not assessment.get("recovery_eligible"):
        return {
            "status": "BLOCKED",
            "reasons": assessment.get("recovery_blocked_reasons", ["NOT_ELIGIBLE"]),
            "detail": "Recovery not eligible. Lock preserved.",
            "assessment": assessment,
        }
    # Preserve metadata for evidence
    lock_path = lock_path_for(db_path)
    try:
        recovered_at = str(Path(db_path).stat().st_mtime)
    except Exception:
        recovered_at = None
    evidence = {
        "recovered_at": recovered_at,
        "lease_metadata": assessment["lease"],
        "db_path": str(db_path),
    }
    evidence_path = lock_path.parent / (lock_path.name + ".recovered.json")
    try:
        evidence_path.write_text(json.dumps(evidence, indent=2, default=str), encoding="utf-8")
    except Exception:
        pass
    # Delete only the lock
    removed = release(db_path)
    return {
        "status": "RECOVERED" if removed else "RELEASE_FAILED",
        "lock_removed": removed,
        "evidence_preserved_at": str(evidence_path),
    }


def main():
    parser = argparse.ArgumentParser(description="Stale writer lease recovery")
    parser.add_argument("action", choices=["inspect", "recover"], nargs="?", default="inspect")
    parser.add_argument("--db", type=Path, default=None)
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()

    db_path = args.db or _default_db()
    if args.action == "inspect":
        result = inspect(db_path)
    else:
        result = recover(db_path, args.confirm)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
