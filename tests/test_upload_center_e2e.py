"""Upload hardening tests — corrected contract (PFO-UPLOAD-CONFIG-GUARD-001).

Default upload is a NON-WRITING dry run. Confirmed writes require
dry_run=false + confirm_write=true and run the real IngestionOrchestrator.
Registry endpoints never fabricate records. All tests isolated (temp DB +
temp uploads + temp knowledge index). Production never touched.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
E2E_V1_INPUT = ROOT / "tests" / "golden" / "e2e_v1" / "input" / "ML_Facturacion_E2E_V1.xlsx"


def _make_csv(tmp_path, name, content=None):
    if content is None:
        content = "col1,col2\n1,test\n"
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


def _copy_e2e_v1(tmp_path, name="ML_Facturacion_E2E_V1.xlsx"):
    dest = tmp_path / name
    shutil.copy2(E2E_V1_INPUT, dest)
    return dest


@pytest.fixture
def isolated_uploads(tmp_path):
    uploads = tmp_path / "uploads"
    uploads.mkdir()
    return uploads


@pytest.fixture
def isolated_db(tmp_path):
    from engine.v4.database import DatabaseV4

    DatabaseV4.reset()
    db = DatabaseV4(db_path=tmp_path / "upload_center.duckdb", read_only=False)
    db.is_read_only = False
    DatabaseV4._instance = db
    try:
        yield db
    finally:
        DatabaseV4.reset()


@pytest.fixture
def isolated_app(isolated_db, isolated_uploads, tmp_path, monkeypatch):
    import api.api as api_module
    import engine.v4.knowledge.knowledge_indexer as knowledge_indexer_module

    monkeypatch.setattr(api_module, "UPLOAD_DIR", isolated_uploads)
    monkeypatch.setattr(
        knowledge_indexer_module,
        "DEFAULT_PATH",
        tmp_path / "knowledge_index.yaml",
    )
    monkeypatch.setenv("MF_RUNTIME_MODE", "CONTROLLED")
    with TestClient(api_module.app) as client:
        yield client


def _ledger_count(isolated_db):
    return int(isolated_db.query(
        "SELECT COUNT(*) AS n FROM marketplace_ledger_v1")["n"].iloc[0])


class TestUploadHardenedContract:
    def test_upload_page_served(self, isolated_app):
        resp = isolated_app.get("/upload")
        assert resp.status_code == 200
        assert "Upload Center" in resp.text

    def test_a_default_request_is_dry_run_no_write(self, isolated_app, tmp_path, isolated_db):
        src = _copy_e2e_v1(tmp_path)
        before = _ledger_count(isolated_db)
        with open(src, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (src.name, f, "application/vnd.ms-excel")},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "DRY_RUN"
        assert data["status"] != "COMPLETED"
        assert "DETECT" in data["details"]["stages_completed"]
        assert "PERSIST" not in data["details"]["stages_completed"]
        assert _ledger_count(isolated_db) == before
        # registry holds no record for dry runs
        reg = isolated_app.get(f"/api/v4/ingestion/registry/{data['execution_id']}")
        assert reg.status_code == 404

    def test_b_write_without_confirmation_rejected(self, isolated_app, tmp_path, isolated_db):
        src = _copy_e2e_v1(tmp_path)
        before = _ledger_count(isolated_db)
        with open(src, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload?dry_run=false",
                files={"file": (src.name, f, "application/vnd.ms-excel")},
            )
        assert resp.status_code == 409
        assert resp.json()["detail"] == "WRITE_NOT_CONFIRMED"
        assert _ledger_count(isolated_db) == before

    def test_c_controlled_confirmed_runs_real_orchestrator(self, isolated_app, tmp_path, isolated_db):
        from engine.v4.ingestion.handlers.marketplace_classifier import MarketplaceClassifier

        src = _copy_e2e_v1(tmp_path)
        with open(src, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
                files={"file": (src.name, f, "application/vnd.ms-excel")},
            )
        assert resp.status_code == 200
        data = resp.json()
        expected = MarketplaceClassifier().classify(str(src), src.name)
        assert data["marketplace"] == expected["marketplace"]
        assert data["document_type"] == expected["document_type"]
        assert (data["period"] or "") == (expected["period"] or "")
        stages = data["details"]["stages_completed"]
        for s in ("DETECT", "VALIDATE", "CLASSIFY", "PERSIST"):
            assert s in stages
        assert data["status"] == "COMPLETED"
        assert _ledger_count(isolated_db) == 8

    def test_d_test_mode_blocks_production_path(self, isolated_app, tmp_path, isolated_db, monkeypatch):
        import api.api as api_module
        from engine.v4 import config_guard

        monkeypatch.setenv("MF_RUNTIME_MODE", "TEST")
        monkeypatch.setattr(
            config_guard, "is_production_db_path", lambda p: True)
        src = _copy_e2e_v1(tmp_path)
        with open(src, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
                files={"file": (src.name, f, "application/vnd.ms-excel")},
            )
        assert resp.status_code == 403
        assert resp.json()["detail"] == "PRODUCTION_WRITE_BLOCKED_IN_TEST"
        assert _ledger_count(isolated_db) == 0

    def test_e_classification_comes_from_classifier(self, isolated_app, tmp_path, isolated_db):
        from engine.v4.ingestion.handlers.marketplace_classifier import MarketplaceClassifier

        src = _copy_e2e_v1(tmp_path)
        expected = MarketplaceClassifier().classify(str(src), src.name)
        with open(src, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (src.name, f, "application/vnd.ms-excel")},
            )
        data = resp.json()
        assert (data["marketplace"], data["document_type"], data["period"] or "") == (
            expected["marketplace"], expected["document_type"], expected["period"] or "")

    def test_f_pipeline_failure_never_completed(self, isolated_app, tmp_path, isolated_db):
        bad = _make_csv(tmp_path, "BAD_ML.csv", content="Nope\n")
        with open(bad, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
                files={"file": (bad.name, f, "text/csv")},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "FAILED"
        assert data["status"] != "COMPLETED"
        assert "PERSIST" not in data["details"]["stages_completed"]

    def test_g_unknown_execution_returns_404(self, isolated_app):
        resp = isolated_app.get("/api/v4/ingestion/registry/does-not-exist-123")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "EXECUTION_NOT_FOUND"

    def test_h_list_error_returns_500_without_fake(self, isolated_app, monkeypatch):
        import api.api as api_module

        class Boom:
            def __init__(self, *a, **k):
                raise RuntimeError("controlled registry failure")

        monkeypatch.setattr(api_module, "IngestionRegistry", Boom)
        resp = isolated_app.get("/api/v4/ingestion/registry?limit=10")
        assert resp.status_code == 500
        body = resp.json()
        assert body.get("detail") == "Registry unavailable"

    def test_upload_invalid_extension_rejected(self, isolated_app, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("hello")
        with open(p, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (p.name, f, "text/plain")},
            )
        assert resp.status_code == 400
        assert "not allowed" in resp.text.lower()

    def test_upload_no_file_returns_400(self, isolated_app):
        resp = isolated_app.post("/api/v4/ingestion/upload")
        assert resp.status_code == 400

    def test_staged_files_cleaned_up(self, isolated_app, tmp_path, isolated_uploads):
        src = _copy_e2e_v1(tmp_path)
        with open(src, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (src.name, f, "application/vnd.ms-excel")},
            )
        assert resp.status_code == 200
        leftover = list(isolated_uploads.iterdir())
        assert leftover == [], f"staged artifacts left: {leftover}"

    def test_registry_returns_real_record_after_confirmed_write(
        self, isolated_app, tmp_path, isolated_db
    ):
        src = _copy_e2e_v1(tmp_path)
        with open(src, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload?dry_run=false&confirm_write=true",
                files={"file": (src.name, f, "application/vnd.ms-excel")},
            )
        execution_id = resp.json()["execution_id"]
        reg_resp = isolated_app.get(f"/api/v4/ingestion/registry/{execution_id}")
        assert reg_resp.status_code == 200
        reg_data = reg_resp.json()
        assert reg_data["execution_id"] == execution_id
        assert reg_data["file_name"].endswith(src.name)
        assert reg_data["status"] == "COMPLETED"

        reg_list = isolated_app.get("/api/v4/ingestion/registry?limit=100")
        ids = [r["execution_id"] for r in reg_list.json().get("records", [])]
        assert execution_id in ids
