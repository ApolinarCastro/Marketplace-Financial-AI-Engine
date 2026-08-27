"""
Meli Financial AI Engine v4.0
Phase 5 Step 3 — Financial Truth Engine Test Suite
Validates:
1. Single Financial Truth resolution across all 13 canonical query types.
2. Order and Transaction truth trace resolution with full evidence chain (Ledger + Classification + DTE/XML).
3. Deterministic conflict detection mechanism (TRUTH_CONFLICT_DETECTED).
4. System health and financial summary aggregation.
5. Zero financial delta ($0.00).
"""
import pytest
from engine.v4.database import DatabaseV4
from engine.v4.domain.financial_truth_engine import FinancialTruthEngine, CANONICAL_QUERIES

@pytest.fixture
def truth_engine():
    db = DatabaseV4.get()
    return FinancialTruthEngine(db=db)

def test_canonical_queries_catalog():
    """Verify that all 13 canonical business queries are cataloged."""
    expected_queries = {
        "que_vendi", "que_cobre", "que_falta_cobrar", "comisiones",
        "publicidad", "logistica", "devoluciones", "xml_respaldo",
        "dte_respaldo", "margen_real", "cierre_financiero",
        "diferencias_sap_marketplace", "movimientos_sin_respaldo"
    }
    assert expected_queries.issubset(set(CANONICAL_QUERIES.keys()))

def test_resolve_canonical_query_que_vendi(truth_engine):
    """Test resolution of canonical query 'que_vendi'."""
    res = truth_engine.resolve_canonical_query("que_vendi", marketplace="ML")
    assert res["query_type"] == "que_vendi"
    assert res["status"] in ("SUCCESS", "NO_DATA")
    assert "total_monto" in res
    assert "records_count" in res
    assert "evidence_chain" in res
    assert res["evidence_chain"]["financial_delta"] == "$0.00"

def test_resolve_canonical_query_all_types(truth_engine):
    """Test resolution for all 13 canonical query types."""
    for q_type in CANONICAL_QUERIES:
        res = truth_engine.resolve_canonical_query(q_type, marketplace="ML")
        assert res["query_type"] == q_type
        assert res["status"] in ("SUCCESS", "TRUTH_CONFLICT_DETECTED", "NO_DATA")

def test_get_transaction_truth(truth_engine):
    """Test resolving truth for a specific transaction ID."""
    db = DatabaseV4.get()
    df = db.query("SELECT id_transaccion FROM v_ledger_certified LIMIT 1")
    assert not df.empty
    tx_id = df.iloc[0]["id_transaccion"]

    truth = truth_engine.get_transaction_truth(tx_id)
    assert truth is not None
    assert truth["id_transaccion"] == tx_id
    assert "single_financial_truth" in truth
    assert "clasificacion_oficial" in truth
    assert "cadena_evidencia" in truth

def test_get_order_truth_trace(truth_engine):
    """Test resolving order truth trace."""
    db = DatabaseV4.get()
    df = db.query("SELECT id_orden FROM v_ledger_certified WHERE id_orden IS NOT NULL LIMIT 1")
    assert not df.empty
    order_id = df.iloc[0]["id_orden"]

    order_truth = truth_engine.get_order_truth(order_id)
    assert order_truth is not None
    assert order_truth["id_orden"] == order_id
    assert "total_movements" in order_truth
    assert "truth_records" in order_truth

def test_conflict_detection_mechanism(truth_engine):
    """Test conflict detection returning TRUTH_CONFLICT_DETECTED if conflicting records exist."""
    res = truth_engine.evaluate_conflict({"has_conflict": True, "conflict_reason": "Incompatible amounts across sources"})
    assert res["status"] == "TRUTH_CONFLICT_DETECTED"
    assert "evidencia_conflicto" in res

def test_get_truth_summary_and_health(truth_engine):
    """Test truth summary and health endpoint Data structures."""
    summary = truth_engine.get_truth_summary(marketplace="ML")
    assert "total_queries_resolved" in summary
    assert "financial_delta" in summary
    assert summary["financial_delta"] == "$0.00"

    health = truth_engine.get_truth_health()
    assert health["status"] in ("READY", "PASS")
    assert health["single_financial_truth"] == "ACTIVE"
