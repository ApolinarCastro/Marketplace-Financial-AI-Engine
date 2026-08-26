"""
Meli Financial AI Engine v4.0
Phase 5 Step 4 — Reconciliation Engine Test Suite
Validates:
1. Reconciliation Exception Catalog completeness (11 official exception states).
2. Deterministic exact matching for transactions and orders.
3. Full reconciliation execution with statistics and coverage metrics.
4. Health check and exception query capabilities.
5. Zero financial delta ($0.00).
"""
import pytest
from engine.v4.database import DatabaseV4
from engine.v4.domain.reconciliation_engine import ReconciliationEngine, RECONCILIATION_EXCEPTIONS

@pytest.fixture
def reconciliation_engine():
    db = DatabaseV4.get()
    return ReconciliationEngine(db=db)

def test_exception_catalog_completeness():
    """Verify that all 11 official reconciliation exception states exist."""
    expected_states = {
        "CONCILIADO", "DIFERENCIA_MONTO", "DIFERENCIA_DOCUMENTAL",
        "DIFERENCIA_TRIBUTARIA", "COBRO_PENDIENTE", "PAGO_PENDIENTE",
        "SIN_RESPALDO_XML", "SIN_RESPALDO_DTE", "SIN_MATCH_SAP",
        "SIN_MATCH_MARKETPLACE", "REQUIERE_REVISION"
    }
    registered_states = set(RECONCILIATION_EXCEPTIONS.keys())
    assert expected_states.issubset(registered_states)

def test_reconcile_transaction(reconciliation_engine):
    """Test reconciliation matching for a single transaction ID."""
    db = DatabaseV4.get()
    df = db.query("SELECT id_transaccion FROM v_ledger_certified LIMIT 1")
    assert not df.empty
    tx_id = df.iloc[0]["id_transaccion"]

    rec_res = reconciliation_engine.reconcile_transaction(tx_id)
    assert rec_res is not None
    assert rec_res["id_transaccion"] == tx_id
    assert "status_reconciliacion" in rec_res
    assert rec_res["status_reconciliacion"] in RECONCILIATION_EXCEPTIONS
    assert "cadena_evidencia" in rec_res

def test_reconcile_order(reconciliation_engine):
    """Test order-level reconciliation for multi-movement order."""
    db = DatabaseV4.get()
    df = db.query("SELECT id_orden FROM v_ledger_certified WHERE id_orden IS NOT NULL LIMIT 1")
    assert not df.empty
    order_id = df.iloc[0]["id_orden"]

    order_res = reconciliation_engine.reconcile_order(order_id)
    assert order_res is not None
    assert order_res["id_orden"] == order_id
    assert "status_reconciliacion" in order_res
    assert "movements_count" in order_res

def test_execute_reconciliation(reconciliation_engine):
    """Test full reconciliation execution for marketplace and period."""
    exec_res = reconciliation_engine.execute_reconciliation(marketplace="ML", limit=20)
    assert exec_res["status"] == "COMPLETED"
    assert "total_audited" in exec_res
    assert "reconciliation_summary" in exec_res
    assert exec_res["financial_delta"] == "$0.00"

def test_get_reconciliation_exceptions(reconciliation_engine):
    """Test querying reconciliation exceptions filter."""
    res = reconciliation_engine.get_exceptions(limit=10)
    assert "total_exceptions" in res
    assert "exceptions" in res
    assert isinstance(res["exceptions"], list)

def test_reconciliation_health_and_statistics(reconciliation_engine):
    """Test health and statistics endpoints data structures."""
    health = reconciliation_engine.get_health()
    assert health["status"] in ("READY", "PASS")
    assert health["reconciliation_engine"] == "ACTIVE"

    stats = reconciliation_engine.get_statistics(marketplace="ML")
    assert "total_reconciled" in stats
    assert "reconciliation_rate_pct" in stats
    assert stats["financial_delta"] == "$0.00"
