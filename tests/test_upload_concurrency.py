"""Upload endpoint concurrency tests (PFO-CONCURRENT-WRITE-SAFETY-001 §16-22).

TEMP DB + TEMP uploads only. Verifies second confirmed writer is rejected
with 409 WRITE_IN_PROGRESS and zero writes, locks release on all outcomes,
and dry-run/unconfirmed paths never create leases.
"""
from __future__ import annotations

import shutil
import threading
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
E2E_V1_INPUT = ROOT / "tests" / "golden" / "e2e_v1" / "input" / "ML_Facturacion_E2E_V1.xlsx"


@pytest.fixture
def isolated_stack(tmp_path, monkeypatch):
    from engine.v4.database import DatabaseV4
    import api.api as api_module
    import engine.v4.knowledge.knowledge_indexer as knowledge_indexer_module

    DatabaseV4.reset()
    db = DatabaseV4(db_path=tmp_path / "conc.duckdb", read_only=False)
    db.is_read_only = False
    DatabaseV4._instance = db
    uploads = tmp_path / "uploads"
    uploads.mkdir()
    monkeypatch.setattr(api_module, "UPLOAD_DIR", uploads)
    monkeypatch.setattr(
        knowledge_indexer_module, "DEFAULT_PATH", tmp_path / "knowledge_index.yaml")
    monkeypatch.setenv("MF_RUNTIME_MODE", "CONTROLLED")
    try:
        with TestClient(api_module.app) as client:
            yield client, tmp_path, db
    finally:
        DatabaseV4.reset()


def _post(client, src, query):
    with open(src, "rb") as f:
        return client.post(
            "/api/v4/ingestion/upload" + query,
            files={"file": (src.name, f, "application/vnd.ms-excel")},
        )


def _lock_path(tmp_path):
    from engine.v4.write_guard import lock_path_for

    return lock_path_for(tmp_path / "conc.duckdb")


def _ledger_count(tmp_path):
    import duckdb

    try:
        con = duckdb.connect(str(tmp_path / "conc.duckdb"), read_only=True)
    except Exception:
        return -1
    try:
        return int(con.execute("SELECT COUNT(*) FROM marketplace_ledger_v1").fetchone()[0])
    except Exception:
        return -1
    finally:
        try:
            con.close()
        except Exception:
            pass


def _copy_src(tmp_path, tag):
    dest = tmp_path / f"SRC_{tag}.xlsx"
    shutil.copy2(E2E_V1_INPUT, dest)
    return dest


def test_api_second_writer_rejected_while_first_active(isolated_stack):
    # Deterministic: an externally held lease simulates an in-flight writer.
    # The endpoint must honor it (the guard itself is timing-independent;
    # proven separately to be held across real pipeline runs below).
    from engine.v4 import write_guard

    client, tmp_path, _db = isolated_stack
    src_b = _copy_src(tmp_path, "B")
    db_path = tmp_path / "conc.duckdb"
    assert write_guard.acquire(str(db_path), request_id="SIMULATED-ACTIVE-WRITER")["status"] == "ACQUIRED"
    try:
        with open(src_b, "rb") as f:
            resp_b = client.post(
                "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
                files={"file": (src_b.name, f, "application/vnd.ms-excel")},
            )
        assert resp_b.status_code == 409
        assert resp_b.json()["detail"] == "WRITE_IN_PROGRESS"
    finally:
        assert write_guard.release(str(db_path)) is True

    # Rejected writer wrote nothing: no registry record, no ledger rows.
    from engine.v4.database import DatabaseV4

    DatabaseV4.reset()
    import duckdb

    con = duckdb.connect(str(tmp_path / "conc.duckdb"), read_only=True)
    try:
        assert int(con.execute("SELECT COUNT(*) FROM marketplace_ledger_v1").fetchone()[0]) == 0
        try:
            reg_n = int(con.execute("SELECT COUNT(*) FROM ingestion_registry").fetchone()[0])
        except Exception:
            reg_n = 0  # table lazily created on first real write; absent == zero records
        assert reg_n == 0
    finally:
        con.close()
    assert not _lock_path(tmp_path).exists()


def test_lease_held_across_real_pipeline_and_released(isolated_stack):
    client, tmp_path, _db = isolated_stack
    src_a = _copy_src(tmp_path, "A")
    results = {}
    observed_during_run = {}

    def run_a():
        with open(src_a, "rb") as f:
            results["a"] = client.post(
                "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
                files={"file": (src_a.name, f, "application/vnd.ms-excel")},
            )

    thread = threading.Thread(target=run_a, daemon=True)
    thread.start()
    deadline = time.time() + 60
    while not _lock_path(tmp_path).exists() and time.time() < deadline:
        time.sleep(0.1)
    observed_during_run["held"] = _lock_path(tmp_path).exists()
    thread.join(timeout=180)

    assert observed_during_run["held"] is True
    assert results["a"].status_code == 200
    assert results["a"].json()["status"] == "COMPLETED"
    assert not _lock_path(tmp_path).exists()

    from engine.v4.database import DatabaseV4

    DatabaseV4.reset()
    import duckdb

    con = duckdb.connect(str(tmp_path / "conc.duckdb"), read_only=True)
    try:
        assert int(con.execute("SELECT COUNT(*) FROM marketplace_ledger_v1").fetchone()[0]) == 8
        assert int(con.execute(
            "SELECT COUNT(*) FROM ingestion_registry WHERE status = 'COMPLETED'").fetchone()[0]) == 1
    finally:
        con.close()


def test_dry_run_creates_no_lease(isolated_stack):
    client, tmp_path, _db = isolated_stack
    src = _copy_src(tmp_path, "D")
    with open(src, "rb") as f:
        resp = client.post(
            "/api/v4/ingestion/upload?dry_run=true",
            files={"file": (src.name, f, "application/vnd.ms-excel")},
        )
    assert resp.status_code == 200
    assert resp.json()["status"] == "DRY_RUN"
    assert not _lock_path(tmp_path).exists()


def test_unconfirmed_write_creates_no_lease(isolated_stack):
    client, tmp_path, _db = isolated_stack
    src = _copy_src(tmp_path, "U")
    with open(src, "rb") as f:
        resp = client.post(
            "/api/v4/ingestion/upload?dry_run=false",
            files={"file": (src.name, f, "application/vnd.ms-excel")},
        )
    assert resp.status_code == 409
    assert not _lock_path(tmp_path).exists()


def test_failed_run_releases_lease(isolated_stack):
    client, tmp_path, _db = isolated_stack
    bad = tmp_path / "BAD_ML.csv"
    bad.write_text("Nope\n", encoding="utf-8")
    with open(bad, "rb") as f:
        resp = client.post(
            "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
            files={"file": (bad.name, f, "text/csv")},
        )
    assert resp.status_code == 200
    assert resp.json()["status"] == "FAILED"
    assert not _lock_path(tmp_path).exists()
    # A later valid run can still acquire the lease.
    src = _copy_src(tmp_path, "V")
    with open(src, "rb") as f:
        resp2 = client.post(
            "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
            files={"file": (src.name, f, "application/vnd.ms-excel")},
        )
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "COMPLETED"
    assert not _lock_path(tmp_path).exists()


def test_duplicate_run_releases_lease(isolated_stack):
    client, tmp_path, _db = isolated_stack
    src = _copy_src(tmp_path, "W")
    with open(src, "rb") as f:
        first = client.post(
            "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
            files={"file": (src.name, f, "application/vnd.ms-excel")},
        )
    assert first.json()["status"] == "COMPLETED"
    with open(src, "rb") as f:
        second = client.post(
            "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
            files={"file": (src.name, f, "application/vnd.ms-excel")},
        )
    assert second.json()["status"] == "SKIPPED_DUPLICATE"
    assert not _lock_path(tmp_path).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
