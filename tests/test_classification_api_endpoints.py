"""
Meli Financial AI Engine v4.0
Phase 5 Step 2 — Financial Classification Engine API Integration Tests
Tests:
- GET /api/v4/classification/summary
- GET /api/v4/classification/rules
- GET /api/v4/classification/{transaction_id}
- POST /api/v4/classification/rebuild
"""
import pytest
from fastapi.testclient import TestClient
from api.api import app

@pytest.fixture
def client():
    return TestClient(app)

def test_api_get_classification_summary(client):
    response = client.get("/api/v4/classification/summary?marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert "classified_records" in data
    assert "coverage_percentage" in data
    assert "category_breakdown" in data

def test_api_get_classification_rules(client):
    response = client.get("/api/v4/classification/rules")
    assert response.status_code == 200
    data = response.json()
    assert "official_categories" in data
    assert "rules_catalog" in data
    assert len(data["official_categories"]) == 11

def test_api_explain_transaction_classification(client):
    # Fetch 1 transaction ID from ledger API
    res = client.get("/api/v4/ledger/records?limit=1").json()
    assert res["records"]
    tx_id = res["records"][0]["id_transaccion"]

    response = client.get(f"/api/v4/classification/{tx_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_transaccion"] == tx_id
    assert "clasificacion" in data
    assert "regla_aplicada" in data
    assert "evidencia_utilizada" in data

def test_api_rebuild_classification(client):
    response = client.post("/api/v4/classification/rebuild?marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["delta_verified"] == "$0.00"
