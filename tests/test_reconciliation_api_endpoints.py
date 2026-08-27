"""
Meli Financial AI Engine v4.0
Phase 5 Step 4 — Reconciliation Engine API Integration Tests
Tests:
- GET /api/v4/reconciliation/health
- GET /api/v4/reconciliation/summary
- GET /api/v4/reconciliation/statistics
- GET /api/v4/reconciliation/exceptions
- POST /api/v4/reconciliation/execute
- GET /api/v4/reconciliation/transaction/{transaction_id}
- GET /api/v4/reconciliation/order/{id_orden}
"""
import pytest
from fastapi.testclient import TestClient
from api.api import app

@pytest.fixture
def client():
    return TestClient(app)

def test_api_get_reconciliation_health(client):
    response = client.get("/api/v4/reconciliation/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("READY", "PASS")
    assert data["reconciliation_engine"] == "ACTIVE"

def test_api_get_reconciliation_summary(client):
    response = client.get("/api/v4/reconciliation/summary?marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert "total_reconciled" in data
    assert "reconciliation_rate_pct" in data
    assert data["financial_delta"] == "$0.00"

def test_api_get_reconciliation_statistics(client):
    response = client.get("/api/v4/reconciliation/statistics?marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert "exception_breakdown" in data

def test_api_get_reconciliation_exceptions(client):
    response = client.get("/api/v4/reconciliation/exceptions?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "total_exceptions" in data
    assert "exceptions" in data

def test_api_post_reconciliation_execute(client):
    response = client.post("/api/v4/reconciliation/execute", json={"marketplace": "ML", "limit": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["financial_delta"] == "$0.00"

def test_api_get_reconciled_transaction(client):
    res = client.get("/api/v4/ledger/records?limit=1").json()
    assert res["records"]
    tx_id = res["records"][0]["id_transaccion"]

    response = client.get(f"/api/v4/reconciliation/transaction/{tx_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_transaccion"] == tx_id
    assert "status_reconciliacion" in data

def test_api_get_reconciled_order(client):
    res = client.get("/api/v4/ledger/records?limit=50").json()
    rec_with_order = next((r for r in res["records"] if r.get("id_orden")), None)

    if rec_with_order:
        order_id = rec_with_order["id_orden"]
        response = client.get(f"/api/v4/reconciliation/order/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id_orden"] == order_id
        assert "status_reconciliacion" in data
