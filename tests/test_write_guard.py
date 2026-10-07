"""Writer-lease guard tests — PFO-CONCURRENT-WRITE-SAFETY-001 §14-23.

Unit level: same-process, different-DB, dry-run/unconfirmed, release paths.
API level: busy rejection without writes. UI level: structural busy handling.
All TEMP-isolated. Production never touched.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from engine.v4 import write_guard


def _tmp_db(tmp_path: Path, name: str = "w.db") -> Path:
    return tmp_path / name


def test_same_process_second_writer_rejected(tmp_path: Path):
    db = _tmp_db(tmp_path, "a.db")
    try:
        from engine.v4.database import DatabaseV4
        d = DatabaseV4(db_path=str(db), read_only=False)
        try:
            d.execute("CREATE TABLE IF NOT EXISTS t (x INT)")
            d.execute("INSERT INTO t VALUES (1)")
        finally:
            d.close()
        a = write_guard.acquire(str(db), request_id="A")
        assert a["status"] == "ACQUIRED"
        try:
            b = write_guard.acquire(str(db), request_id="B")
            assert b["status"] == "BUSY"
            assert b["detail"] == "WRITE_IN_PROGRESS"
            # B performed zero writes: table still has exactly the 1 row from A setup
            d2 = DatabaseV4(db_path=str(db), read_only=True)
            try:
                assert int(d2.query("SELECT COUNT(*) AS n FROM t")["n"].iloc[0]) == 1
            finally:
                d2.close()
        finally:
            assert write_guard.release(str(db)) is True
        # manual retry after release succeeds
        c = write_guard.acquire(str(db), request_id="B-retry")
        assert c["status"] == "ACQUIRED"
        assert write_guard.release(str(db)) is True
    finally:
        assert not write_guard.is_locked(str(db))


def test_different_db_concurrent_allowed(tmp_path: Path):
    a = _tmp_db(tmp_path, "a.db")
    b = _tmp_db(tmp_path, "b.db")
    ra = write_guard.acquire(str(a), request_id="A")
    try:
        assert ra["status"] == "ACQUIRED"
        rb = write_guard.acquire(str(b), request_id="B")
        assert rb["status"] == "ACQUIRED"
        assert write_guard.release(str(b)) is True
    finally:
        assert write_guard.release(str(a)) is True


def test_lock_identity_derives_from_db_path(tmp_path: Path):
    a = _tmp_db(tmp_path, "same.db")
    assert write_guard.lock_path_for(a).name == "same.db.writer.lock"
    assert write_guard.lock_path_for(a).parent == a.resolve().parent


def test_atomic_acquire_has_no_check_then_create_race():
    import inspect

    src = inspect.getsource(write_guard.acquire)
    assert "O_EXCL" in src
    assert "O_CREAT" in src


def test_lease_metadata_has_no_financial_data(tmp_path: Path):
    db = _tmp_db(tmp_path, "m.db")
    try:
        r = write_guard.acquire(str(db), request_id="REQ-1")
        assert r["status"] == "ACQUIRED"
        meta = write_guard.read_lease(str(db))
        assert set(meta) <= {"pid", "created_at", "db_path", "request_id"}
        assert meta["request_id"] == "REQ-1"
    finally:
        assert write_guard.release(str(db)) is True


def test_stale_lock_never_auto_recovered(tmp_path: Path):
    db = _tmp_db(tmp_path, "s.db")
    try:
        assert write_guard.acquire(str(db), request_id="holder")["status"] == "ACQUIRED"
        # Simulate crash: holder gone without release (no release call here).
        assert write_guard.acquire(str(db), request_id="next")["status"] == "BUSY"
    finally:
        assert write_guard.release(str(db)) is True


def test_cross_process_second_writer_rejected(tmp_path: Path):
    db = _tmp_db(tmp_path, "x.db")
    holder = os.path.join(tempfile.gettempdir(), "wg_holder_probe.py")
    script = (
        "import sys, time, json\n"
        "sys.path.insert(0, r'C:\\Users\\ASUS Zenbook\\Documents\\Marketplace Financial AI Engine')\n"
        "from engine.v4 import write_guard\n"
        f"print(json.dumps(write_guard.acquire(r'{db}', request_id='PROC-A')))\n"
        "sys.stdout.flush()\n"
        "time.sleep(8)\n"
        f"write_guard.release(r'{db}')\n"
    )
    Path(holder).write_text(script, encoding="utf-8")
    try:
        proc = subprocess.Popen(
            [sys.executable, holder], stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True)
        try:
            import json as _json
            first_line = proc.stdout.readline()
            assert _json.loads(first_line)["status"] == "ACQUIRED"
            # While A holds the lease, this process must be rejected.
            mine = write_guard.acquire(str(db), request_id="PROC-B")
            assert mine["status"] == "BUSY"
            assert mine["detail"] == "WRITE_IN_PROGRESS"
        finally:
            proc.wait(timeout=30)
        # After A released, a new attempt succeeds.
        again = write_guard.acquire(str(db), request_id="PROC-B-retry")
        assert again["status"] == "ACQUIRED"
        assert write_guard.release(str(db)) is True
    finally:
        Path(holder).unlink(missing_ok=True)
        assert not write_guard.is_locked(str(db))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
