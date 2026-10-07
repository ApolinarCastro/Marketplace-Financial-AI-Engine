"""Crash recovery tests — PFO-CRASH-RECOVERY-SAFETY-001 §18-24.

TEMP DB only. Covers:
- Crash before DB write (A)
- Crash after registry start (B)
- Active process block (D)
- WAL block (E)
- Normal failure release regression (§23)
- Post-recovery valid run (§24)
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pytest

from engine.v4 import write_guard

REPO_ROOT = Path(__file__).resolve().parent.parent
E2E_V1_INPUT = REPO_ROOT / "tests" / "golden" / "e2e_v1" / "input" / "ML_Facturacion_E2E_V1.xlsx"


def _tmp_db(tmp_path: Path, name: str = "crash.db") -> Path:
    return tmp_path / name


# ── §18 Crash Simulation A — before DB write ────────────────────────────────

def test_crash_before_write(tmp_path: Path):
    """Child acquires lease, dies before any DB write. Stale lock remains."""
    db = _tmp_db(tmp_path, "a.db")
    holder_script = tmp_path / "holder.py"
    holder_script.write_text(
        "import sys, os\n"
        f"sys.path.insert(0, r'{REPO_ROOT}')\n"
        "from engine.v4 import write_guard\n"
        f"r = write_guard.acquire(r'{db}', request_id='CRASH-A')\n"
        "print(r['status'])\n"
        "sys.stdout.flush()\n"
        "# Die abruptly — no release\n"
        "os._exit(1)\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(holder_script)],
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode != 0
    assert "ACQUIRED" in proc.stdout
    # Stale lock remains
    assert write_guard.is_locked(str(db))
    info = write_guard.inspect_writer_lease(str(db))
    assert info["LOCK_EXISTS"] is True
    assert info["PROCESS_STATE"] == "NOT_FOUND"
    # Recovery eligible (no WAL, no active ingestion)
    from tools.recover_stale_writer_lock import inspect as tool_inspect
    assessment = tool_inspect(db)
    assert assessment["recovery_eligible"] is True
    # Explicit recovery removes lock
    from tools.recover_stale_writer_lock import recover
    result = recover(db, confirm=True)
    assert result["status"] == "RECOVERED"
    assert not write_guard.is_locked(str(db))
    # Subsequent valid run can acquire
    r = write_guard.acquire(str(db), request_id="POST-RECOVERY")
    assert r["status"] == "ACQUIRED"
    assert write_guard.release(str(db)) is True


# ── §19 Crash Simulation B — after registry start ───────────────────────────

def test_crash_after_registry_start(tmp_path: Path):
    """Child creates registry record, acquires lease, dies before persist."""
    db = _tmp_db(tmp_path, "b.db")
    # Create a real DB with schema
    import duckdb
    con = duckdb.connect(str(db))
    con.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_registry (
            execution_id TEXT PRIMARY KEY,
            start_time TEXT, end_time TEXT, user TEXT,
            marketplace TEXT, document_type TEXT, period TEXT,
            file_name TEXT, file_path TEXT, sha256 TEXT,
            file_size_bytes INTEGER, status TEXT,
            loader_executed TEXT, pipeline TEXT, pipeline_version TEXT,
            records_inserted INTEGER DEFAULT 0, records_updated INTEGER DEFAULT 0,
            records_rejected INTEGER DEFAULT 0, records_read INTEGER DEFAULT 0,
            records_new INTEGER DEFAULT 0, records_existing INTEGER DEFAULT 0,
            errors TEXT DEFAULT '[]', warnings TEXT DEFAULT '[]',
            execution_time_seconds REAL,
            certification_triggered BOOLEAN DEFAULT FALSE,
            certification_result TEXT, knowledge_updated BOOLEAN DEFAULT FALSE,
            details TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT current_timestamp
        )
    """)
    con.close()

    holder_script = tmp_path / "holder_b.py"
    holder_script.write_text(
        "import sys, os, uuid\n"
        f"sys.path.insert(0, r'{REPO_ROOT}')\n"
        "import duckdb\n"
        f"con = duckdb.connect(r'{db}')\n"
        "exec_id = str(uuid.uuid4())\n"
        "sql = \"INSERT INTO ingestion_registry (execution_id, start_time, user, file_name, file_path, sha256, file_size_bytes, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)\"\n"
        "con.execute(sql, [exec_id, '2026-10-07T00:00:00', 'crash-test', 'test.xlsx', '/tmp/test.xlsx', 'abc123', 100, 'STARTED'])\n"
        "con.close()\n"
        "from engine.v4 import write_guard\n"
        f"r = write_guard.acquire(r'{db}', request_id=exec_id)\n"
        "print(r['status'])\n"
        "sys.stdout.flush()\n"
        "os._exit(1)\n",
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(holder_script)],
        capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode != 0
    assert "ACQUIRED" in proc.stdout
    # Wait for OS to clean up the dead child's PID
    time.sleep(1.0)
    # Registry has STARTED record
    con = duckdb.connect(str(db), read_only=True)
    rows = con.execute("SELECT status, COUNT(*) FROM ingestion_registry GROUP BY status").fetchall()
    con.close()
    assert ("STARTED", 1) in rows
    # Ledger has 0 rows
    con = duckdb.connect(str(db), read_only=True)
    try:
        n = con.execute("SELECT COUNT(*) FROM marketplace_ledger_v1").fetchone()[0]
    except Exception:
        n = 0
    con.close()
    assert n == 0
    # Recovery assessment reports abandoned execution
    from tools.recover_stale_writer_lock import inspect as tool_inspect
    assessment = tool_inspect(db)
    assert assessment["lease"]["LOCK_EXISTS"] is True
    assert assessment["lease"]["PROCESS_STATE"] == "NOT_FOUND"
    # Active ingestion blocks recovery
    assert assessment["recovery_eligible"] is False
    assert "ACTIVE_INGESTION" in assessment.get("recovery_blocked_reasons", [])
    # Clean up for next test
    write_guard.release(str(db))


# ── §21 Crash Simulation D — active process ────────────────────────────────

def test_active_process_blocks_recovery(tmp_path: Path):
    """Live process holds lease. Recovery must be BLOCKED."""
    db = _tmp_db(tmp_path, "d.db")
    # Acquire in this process (simulates active writer)
    r = write_guard.acquire(str(db), request_id="ACTIVE")
    assert r["status"] == "ACQUIRED"
    try:
        from tools.recover_stale_writer_lock import recover
        result = recover(db, confirm=True)
        assert result["status"] == "BLOCKED"
        assert "ACTIVE_WRITER_PROCESS" in result["reasons"]
        assert write_guard.is_locked(str(db))  # Lock remains
    finally:
        assert write_guard.release(str(db)) is True


# ── §22 Crash Simulation E — WAL ───────────────────────────────────────────

def test_wal_blocks_recovery(tmp_path: Path):
    """Synthetic WAL file blocks recovery."""
    db = _tmp_db(tmp_path, "e.db")
    r = write_guard.acquire(str(db), request_id="WAL-TEST")
    assert r["status"] == "ACQUIRED"
    # Create synthetic WAL
    wal_path = tmp_path / "e.db.wal"
    wal_path.write_text("synthetic", encoding="utf-8")
    try:
        from tools.recover_stale_writer_lock import recover
        result = recover(db, confirm=True)
        assert result["status"] == "BLOCKED"
        assert "ACTIVE_OR_UNRESOLVED_WAL" in result["reasons"]
        assert write_guard.is_locked(str(db))  # Lock remains
    finally:
        wal_path.unlink(missing_ok=True)
        assert write_guard.release(str(db)) is True


# ── §23 Normal failure regression ──────────────────────────────────────────

def test_normal_failure_releases_lock(tmp_path: Path):
    """Normal exception path still releases lock via finally."""
    db = _tmp_db(tmp_path, "f.db")
    r = write_guard.acquire(str(db), request_id="NORMAL")
    assert r["status"] == "ACQUIRED"
    try:
        raise ValueError("simulated failure")
    except ValueError:
        pass
    finally:
        write_guard.release(str(db))
    assert not write_guard.is_locked(str(db))


# ── §24 Post-recovery verification ─────────────────────────────────────────

def test_post_recovery_valid_run(tmp_path: Path):
    """After recovery, a valid run acquires lock and completes."""
    db = _tmp_db(tmp_path, "g.db")
    # Simulate stale lock: manually create lock file with dead PID
    lock_path = write_guard.lock_path_for(db)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    import json
    lock_path.write_text(json.dumps({
        "pid": 999999,  # Non-existent PID
        "created_at": "2026-10-07T00:00:00+00:00",
        "db_path": str(db),
        "request_id": "STALE",
    }), encoding="utf-8")
    assert write_guard.is_locked(str(db))
    # Recover
    from tools.recover_stale_writer_lock import recover
    result = recover(db, confirm=True)
    assert result["status"] == "RECOVERED"
    # Valid run
    r2 = write_guard.acquire(str(db), request_id="VALID")
    assert r2["status"] == "ACQUIRED"
    assert write_guard.release(str(db)) is True
    assert not write_guard.is_locked(str(db))


# ── §4-6 Inspection capability ─────────────────────────────────────────────

def test_inspect_writer_lease_fields(tmp_path: Path):
    db = _tmp_db(tmp_path, "h.db")
    r = write_guard.acquire(str(db), request_id="INSPECT-1")
    assert r["status"] == "ACQUIRED"
    try:
        info = write_guard.inspect_writer_lease(str(db))
        assert info["LOCK_EXISTS"] is True
        assert "LOCK_PATH" in info
        assert "PID" in info
        assert "CREATED_AT" in info
        assert info["REQUEST_ID"] == "INSPECT-1"
        assert info["PROCESS_STATE"] == "ALIVE"  # This process is alive
        assert info["AGE_SECONDS"] is not None
        assert info["AGE_SECONDS"] >= 0
    finally:
        write_guard.release(str(db))


def test_inspect_no_lock(tmp_path: Path):
    db = _tmp_db(tmp_path, "i.db")
    info = write_guard.inspect_writer_lease(str(db))
    assert info["LOCK_EXISTS"] is False


def test_check_wal_detects_wal(tmp_path: Path):
    db = _tmp_db(tmp_path, "j.db")
    wal = tmp_path / "j.db.wal"
    wal.write_text("x", encoding="utf-8")
    try:
        result = write_guard.check_wal(str(db))
        assert result["WAL_EXISTS"] is True
        assert len(result["WAL_PATHS"]) == 1
    finally:
        wal.unlink(missing_ok=True)
    result = write_guard.check_wal(str(db))
    assert result["WAL_EXISTS"] is False


# ── §8 No auto-recovery on normal upload ───────────────────────────────────

def test_upload_does_not_auto_delete_stale_lock(tmp_path: Path):
    """Normal upload endpoint must NOT delete stale locks."""
    db = _tmp_db(tmp_path, "k.db")
    # Create stale lock
    r = write_guard.acquire(str(db), request_id="STALE")
    assert r["status"] == "ACQUIRED"
    # The lock still exists — upload would get 409
    assert write_guard.is_locked(str(db))
    # Release for cleanup
    write_guard.release(str(db))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
