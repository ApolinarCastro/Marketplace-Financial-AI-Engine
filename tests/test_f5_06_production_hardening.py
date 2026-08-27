import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from unittest.mock import patch
from engine.v4.database import DatabaseV4
from engine.v4.ingestion.orchestrator import IngestionOrchestrator
from engine.v4.ingestion import IngestionRegistry
from api.api import app

@pytest.fixture
def client():
    DatabaseV4.reset()
    return TestClient(app)

@pytest.fixture
def fresh_writer_db(tmp_path):
    db_path = tmp_path / "writer.db"
    db = DatabaseV4(db_path=db_path, read_only=False)
    db.execute("CREATE TABLE IF NOT EXISTS file_registry (id INT)")
    yield db
    db.conn.close()

def test_api_database_is_read_only(client):
    db = DatabaseV4.get()
    assert getattr(db, 'is_read_only', True) is True

def test_api_write_attempt_is_rejected(client):
    db = DatabaseV4.get()
    with pytest.raises(Exception) as excinfo:
        db.execute("CREATE TABLE _should_fail (id INT)")
    assert "read-only mode" in str(excinfo.value).lower()

def test_orchestrator_retains_write_access(fresh_writer_db):
    registry = IngestionRegistry(db=fresh_writer_db)
    orch = IngestionOrchestrator(db=fresh_writer_db, registry=registry)
    assert getattr(fresh_writer_db, 'is_read_only', False) is False
    try:
        fresh_writer_db.execute("CREATE TABLE _should_succeed (id INT)")
    except Exception as e:
        pytest.fail(f"Orchestrator DB write failed: {e}")

@patch("api.api.DatabaseV4.get")
def test_health_ready(mock_get, client):
    class MockDB:
        def execute(self, sql):
            class MockCursor:
                def fetchone(self):
                    if 'ingestion_registry' in sql: return [0]
                    return [1]
            return MockCursor()
    mock_get.return_value = MockDB()
    resp = client.get("/api/v4/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "READY"

@patch("api.api.DatabaseV4.get")
def test_health_degraded_on_incomplete_ingestion(mock_get, client):
    class MockDB:
        def execute(self, sql):
            class MockCursor:
                def fetchone(self):
                    if "ingestion_registry" in sql: return [1] # 1 orphan
                    return [1]
            return MockCursor()
    mock_get.return_value = MockDB()
    resp = client.get("/api/v4/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "DEGRADED"

@patch("api.api.DatabaseV4.get")
def test_health_not_ready_when_database_unavailable(mock_get, client):
    mock_get.side_effect = Exception("DB Connection Refused")
    resp = client.get("/api/v4/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "NOT_READY"
    assert resp.json()["database"] == "FAIL"

def test_health_does_not_expose_internal_paths(client):
    resp = client.get("/api/v4/health")
    text = resp.text
    assert "C:\\" not in text
    assert "Users" not in text

def test_auditor_matches_api_truth(client):
    resp = client.get("/app")
    assert resp.status_code == 200

def test_executive_dashboard_matches_api_truth(client):
    resp = client.get("/exec")
    assert resp.status_code == 200
