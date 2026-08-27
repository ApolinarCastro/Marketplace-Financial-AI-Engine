"""
Meli Financial AI Engine v4.0
Phase 5 Step 3 — Financial Truth Engine API Integration Tests
Tests:
- GET /api/v4/truth/health
- GET /api/v4/truth/summary
- GET /api/v4/truth/query
- POST /api/v4/truth/query
- GET /api/v4/truth/transaction/{transaction_id}
- GET /api/v4/truth/order/{id_orden}
"""
import pytest
from fastapi.testclient import TestClient
from api.api import app

@pytest.fixture
def client():
    return TestClient(app)

def test_api_get_truth_health(client):
    response = client.get("/api/v4/truth/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("READY", "PASS")
    assert data["single_financial_truth"] == "ACTIVE"

def test_api_get_truth_summary(client):
    response = client.get("/api/v4/truth/summary?marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert "total_queries_resolved" in data
    assert "financial_delta" in data
    assert data["financial_delta"] == "$0.00"

def test_api_get_truth_query(client):
    response = client.get("/api/v4/truth/query?query_type=que_vendi&marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert data["query_type"] == "que_vendi"
    assert "records" in data
    assert "evidence_chain" in data

def test_api_post_truth_query(client):
    response = client.post("/api/v4/truth/query", json={"query_type": "comisiones", "marketplace": "ML", "page": 1, "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["query_type"] == "comisiones"
    assert "records" in data

def test_api_get_transaction_truth(client):
    res = client.get("/api/v4/ledger/records?limit=1").json()
    assert res["records"]
    tx_id = res["records"][0]["id_transaccion"]

    response = client.get(f"/api/v4/truth/transaction/{tx_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_transaccion"] == tx_id
    assert "single_financial_truth" in data
    assert "cadena_evidencia" in data

def test_api_get_order_truth(client):
    res = client.get("/api/v4/ledger/records?limit=50").json()
    rec_with_order = next((r for r in res["records"] if r.get("id_orden")), None)

    if rec_with_order:
        order_id = rec_with_order["id_orden"]
        response = client.get(f"/api/v4/truth/order/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id_orden"] == order_id
        assert "truth_records" in data
