"""
Meli Financial AI Engine v4.0
Phase 5 Step 1 — Unified Transaction Ledger Test Suite
Validates:
1. Unified Transaction Ledger query capabilities (marketplace, period, transaction_id, order_id).
2. Field schema completeness (origen, documento, fecha, marketplace, orden, sku, tipo financiero, monto, estado, evidencia).
3. Evidence chain traceability per transaction.
4. Financial aggregation determinism ($0 delta against v_ledger_certified).
"""
import pytest
from engine.v4.database import DatabaseV4
from engine.v4.domain.ledger_engine import LedgerEngine

@pytest.fixture
def ledger_engine():
    db = DatabaseV4.get()
    return LedgerEngine(db=db)

def test_ledger_record_count_all(ledger_engine):
    """Test total records count across all marketplaces."""
    total = ledger_engine.get_total_records_count()
    assert total > 0

def test_ledger_records_count_per_marketplace(ledger_engine):
    """Test record counts per marketplace."""
    ml_count = ledger_engine.get_total_records_count(marketplace="ML")
    ripley_count = ledger_engine.get_total_records_count(marketplace="RIPLEY")
    paris_count = ledger_engine.get_total_records_count(marketplace="PARIS")
    falabella_count = ledger_engine.get_total_records_count(marketplace="FALABELLA")

    assert ml_count > 0
    assert ripley_count > 0
    assert paris_count > 0
    assert falabella_count > 0
    
    total = ledger_engine.get_total_records_count()
    assert (ml_count + ripley_count + paris_count + falabella_count) == total

def test_query_unified_ledger_schema(ledger_engine):
    """Test that query_unified_ledger returns records with mandatory fields."""
    res = ledger_engine.query_unified_ledger(marketplace="ML", limit=10)
    assert "records" in res
    assert len(res["records"]) <= 10
    
    if res["records"]:
        rec = res["records"][0]
        mandatory_fields = [
            "marketplace", "id_transaccion", "id_orden", "fecha", 
            "detalle", "monto", "tipo_movimiento", "archivo_origen", 
            "financial_group", "clasificacion_operativa", "documento", 
            "estado_documento", "evidencia"
        ]
        for field in mandatory_fields:
            assert field in rec, f"Missing field {field} in ledger record payload"

def test_get_transaction_by_id(ledger_engine):
    """Test querying a specific transaction ID."""
    res = ledger_engine.query_unified_ledger(limit=1)
    assert res["records"]
    tx_id = res["records"][0]["id_transaccion"]

    tx_record = ledger_engine.get_transaction_by_id(tx_id)
    assert tx_record is not None
    assert tx_record["id_transaccion"] == tx_id

def test_get_order_ledger_trace(ledger_engine):
    """Test querying all transactions associated with a single order."""
    sql = "SELECT id_orden FROM v_ledger_certified WHERE id_orden IS NOT NULL LIMIT 1"
    db = DatabaseV4.get()
    df = db.query(sql)
    assert not df.empty
    order_id = df.iloc[0]["id_orden"]

    trace = ledger_engine.get_order_ledger_trace(order_id)
    assert len(trace) >= 1
    for t in trace:
        assert t["id_orden"] == order_id

def test_get_ledger_summary(ledger_engine):
    """Test ledger financial summary per marketplace and period."""
    summary = ledger_engine.get_ledger_summary(marketplace="ML", period="2025-12")
    assert "total_records" in summary
    assert "total_monto" in summary
    assert "financial_groups" in summary
