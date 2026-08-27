"""
Meli Financial AI Engine v4.0
Phase 5 Step 1 — Unified Transaction Ledger API Integration Tests
Tests:
- GET /api/v4/ledger/records
- GET /api/v4/ledger/transaction/{id_transaccion}
- GET /api/v4/ledger/order/{id_orden}
- GET /api/v4/ledger/summary
"""
import pytest
from fastapi.testclient import TestClient
from api.api import app

@pytest.fixture
def client():
    return TestClient(app)

def test_api_get_ledger_records(client):
    response = client.get("/api/v4/ledger/records?marketplace=ML&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert "records" in data
    assert len(data["records"]) <= 5

def test_api_get_ledger_summary(client):
    response = client.get("/api/v4/ledger/summary?marketplace=ML&periodo=2025-12")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert "total_monto" in data
    assert "financial_groups" in data

def test_api_get_ledger_transaction(client):
    # Fetch 1 record to get a valid id_transaccion
    res = client.get("/api/v4/ledger/records?limit=1").json()
    assert res["records"]
    tx_id = res["records"][0]["id_transaccion"]

    response = client.get(f"/api/v4/ledger/transaction/{tx_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id_transaccion"] == tx_id

def test_api_get_order_trace(client):
    # Fetch 1 record with id_orden
    res = client.get("/api/v4/ledger/records?limit=50").json()
    record_with_order = next((r for r in res["records"] if r.get("id_orden")), None)
    
    if record_with_order:
        order_id = record_with_order["id_orden"]
        response = client.get(f"/api/v4/ledger/order/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id_orden"] == order_id
        assert "trace" in data
        assert len(data["trace"]) >= 1
