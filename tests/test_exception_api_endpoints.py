"""
Meli Financial AI Engine v4.0
Phase 5 Step 5 — Exception Engine API Integration Tests
Tests:
- GET /api/v4/exceptions/health
- GET /api/v4/exceptions/summary
- GET /api/v4/exceptions/sla
- GET /api/v4/exceptions
- POST /api/v4/exceptions/rebuild
- GET /api/v4/exceptions/transaction/{transaction_id}
- GET /api/v4/exceptions/order/{id_orden}
- GET /api/v4/exceptions/{exception_id}
- GET /api/v4/exceptions/statistics
- GET /api/v4/exceptions/marketplace/{marketplace}
- POST /api/v4/exceptions/evaluate
"""
import pytest
from fastapi.testclient import TestClient
from api.api import app

@pytest.fixture
def client():
    return TestClient(app)

def test_api_get_exceptions_health(client):
    response = client.get("/api/v4/exceptions/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("READY", "PASS")
    assert data["exception_engine"] == "ACTIVE"

def test_api_get_exceptions_summary(client):
    response = client.get("/api/v4/exceptions/summary?marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert "total_exceptions" in data
    assert "open_exceptions" in data
    assert data["financial_delta"] == "$0.00"

def test_api_get_exceptions_sla(client):
    response = client.get("/api/v4/exceptions/sla?marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert "total_exceptions" in data
    assert "within_sla" in data
    assert "sla_breached" in data

def test_api_get_exceptions_list(client):
    response = client.get("/api/v4/exceptions?page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert "total_exceptions" in data
    assert "exceptions" in data

def test_api_post_exceptions_rebuild(client):
    response = client.post("/api/v4/exceptions/rebuild", json={"marketplace": "ML"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["financial_delta"] == "$0.00"

def test_api_get_transaction_exceptions(client):
    res = client.get("/api/v4/ledger/records?limit=1").json()
    assert res["records"]
    tx_id = res["records"][0]["id_transaccion"]

    response = client.get(f"/api/v4/exceptions/transaction/{tx_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_id"] == tx_id
    assert "exceptions" in data

def test_api_get_order_exceptions(client):
    res = client.get("/api/v4/ledger/records?limit=50").json()
    rec_with_order = next((r for r in res["records"] if r.get("id_orden")), None)

    if rec_with_order:
        order_id = rec_with_order["id_orden"]
        response = client.get(f"/api/v4/exceptions/order/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id_orden"] == order_id
        assert "exceptions" in data

def test_api_get_exception_by_id(client):
    res = client.get("/api/v4/exceptions?page_size=10").json()
    if res["exceptions"]:
        exc_id = res["exceptions"][0]["exception_id"]
        response = client.get(f"/api/v4/exceptions/{exc_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["exception_id"] == exc_id

def test_api_get_exceptions_statistics(client):
    response = client.get("/api/v4/exceptions/statistics?marketplace=ML")
    assert response.status_code == 200
    data = response.json()
    assert "total_exceptions_detected" in data
    assert "exceptions_by_type" in data
    assert "exceptions_by_marketplace" in data
    assert data["financial_delta"] == "$0.00"

def test_api_get_marketplace_exceptions(client):
    response = client.get("/api/v4/exceptions/marketplace/PARIS")
    assert response.status_code == 200
    data = response.json()
    assert data["marketplace"] == "PARIS"
    assert "total_exceptions_detected" in data
    assert "active_types" in data
    assert data["financial_delta"] == "$0.00"

def test_api_post_exceptions_evaluate(client):
    response = client.post("/api/v4/exceptions/evaluate", json={
        "id_transaccion": "TX_EVAL",
        "marketplace": "ML",
        "id_orden": "ORD_EVAL",
        "fecha": "2025-12-01",
        "monto": 15000.0,
        "folio_xml": None,
        "financial_group": "ingresos",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "EVALUATED"
    assert data["financial_delta"] == "$0.00"
    assert isinstance(data["exceptions"], list)

def test_api_post_exceptions_evaluate_invalid(client):
    response = client.post("/api/v4/exceptions/evaluate", json={"id_transaccion": "TX_ONLY"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "INVALID_RECORD"
    assert "marketplace" in data["missing_fields"]
    assert data["financial_delta"] == "$0.00"
