"""CAP-001: Upload Center E2E Test — Isolated with temp DB and temp uploads.

Verifies the complete upload flow end-to-end:
1. File upload via POST /api/v4/ingestion/upload returns execution_id
2. File is physically saved in temp uploads/
3. Ingestion registry has the record in temp DB
4. File registry has the record in temp DB
5. Upload page HTML is served correctly
"""
from __future__ import annotations
from pathlib import Path
import uuid
from unittest.mock import patch

import pytest

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent


def _make_csv(tmp_path, name, content=None):
    if content is None:
        content = "col1,col2\n1,test\n"
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return p


@pytest.fixture
def mock_loader():
    with patch("engine.v4.ingestion.handlers.persistence_engine.SurgicalLoader") as m:
        instance = m.return_value
        instance.load_file.return_value = 4
        yield instance


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
def isolated_app(isolated_db, isolated_uploads, tmp_path, monkeypatch, mock_loader):
    import api.api as api_module
    import engine.v4.knowledge.knowledge_indexer as knowledge_indexer_module

    monkeypatch.setattr(api_module, "UPLOAD_DIR", isolated_uploads)
    monkeypatch.setattr(
        knowledge_indexer_module,
        "DEFAULT_PATH",
        tmp_path / "knowledge_index.yaml",
    )
    with TestClient(api_module.app) as client:
        yield client


class TestUploadCenterE2E:

    def test_upload_page_served(self, isolated_app):
        resp = isolated_app.get("/upload")
        assert resp.status_code == 200
        assert "Upload Center" in resp.text
        assert "Subir Archivos" in resp.text

    def test_upload_file_returns_execution_id(self, isolated_app, tmp_path):
        csv = _make_csv(tmp_path, "ML_Facturacion_2026-01_A.csv")
        with open(csv, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (csv.name, f, "text/csv")},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert "execution_id" in data
        assert data["execution_id"] is not None
        assert len(data["execution_id"]) > 0

    def test_upload_response_has_metadata(self, isolated_app, tmp_path, mock_loader):
        csv = _make_csv(tmp_path, "ML_Facturacion_2026-01_B.csv")
        with open(csv, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (csv.name, f, "text/csv")},
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data.get("marketplace") == "ML"
        assert data.get("document_type") == "facturacion"
        assert data.get("period") == "2026-01"
        assert data.get("file_name") == csv.name
        assert data.get("status") == "COMPLETED"

    def test_upload_creates_file_in_uploads(self, isolated_app, tmp_path, isolated_uploads):
        csv = _make_csv(tmp_path, "ML_Facturacion_2026-01_C.csv")
        with open(csv, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (csv.name, f, "text/csv")},
            )
        assert resp.status_code == 200
        candidates = list(isolated_uploads.glob(f"*{csv.name}"))
        assert len(candidates) >= 1
        saved = candidates[0]
        assert saved.exists()
        assert saved.stat().st_size > 0

    def test_upload_registry_has_record(self, isolated_app, tmp_path, mock_loader):
        csv = _make_csv(tmp_path, "ML_Facturacion_2026-01_D.csv")
        with open(csv, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (csv.name, f, "text/csv")},
            )
        assert resp.status_code == 200
        execution_id = resp.json()["execution_id"]

        reg_resp = isolated_app.get(f"/api/v4/ingestion/registry/{execution_id}")
        assert reg_resp.status_code == 200
        reg_data = reg_resp.json()
        assert reg_data["execution_id"] == execution_id
        assert reg_data["file_name"] == csv.name
        assert reg_data["marketplace"] == "ML"
        assert reg_data["status"] == "COMPLETED"

    def test_upload_registry_list_includes_record(self, isolated_app, tmp_path):
        csv = _make_csv(tmp_path, "ML_Facturacion_2026-01_E.csv")
        with open(csv, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (csv.name, f, "text/csv")},
            )
        assert resp.status_code == 200
        execution_id = resp.json()["execution_id"]

        reg_resp = isolated_app.get("/api/v4/ingestion/registry?limit=100")
        assert reg_resp.status_code == 200
        body = reg_resp.json()
        ids = [r["execution_id"] for r in body.get("records", [])]
        assert execution_id in ids

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

    def test_loader_called_with_marketplace(self, isolated_app, tmp_path):
        from unittest.mock import patch
        csv = _make_csv(tmp_path, "ML_Facturacion_2026-01_F.csv")
        with patch("engine.v4.ingestion.handlers.persistence_engine.SurgicalLoader") as MockLoader:
            instance = MockLoader.return_value
            instance.load_file.return_value = 4

            with open(csv, "rb") as f:
                isolated_app.post(
                    "/api/v4/ingestion/upload",
                    files={"file": (csv.name, f, "text/csv")},
                )

            instance.load_file.assert_called_once()
            args, kwargs = instance.load_file.call_args
            assert args[1] == "ML"
            assert kwargs["execution_id"]

    def test_upload_pipeline_completes_all_stages(self, isolated_app, tmp_path, mock_loader):
        csv = _make_csv(tmp_path, "ML_Facturacion_2026-01_G.csv")
        with open(csv, "rb") as f:
            resp = isolated_app.post(
                "/api/v4/ingestion/upload",
                files={"file": (csv.name, f, "text/csv")},
            )
        assert resp.status_code == 200
        data = resp.json()
        stages = data.get("details", {}).get("stages_completed", [])
        expected = ["DETECT", "VALIDATE", "CLASSIFY", "PERSIST", "CERTIFY", "KNOWLEDGE"]
        for s in expected:
            assert s in stages, f"Stage {s} not completed"
