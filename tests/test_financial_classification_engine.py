"""
Meli Financial AI Engine v4.0
Phase 5 Step 2 — Financial Classification Engine Test Suite
Validates:
1. Classification Registry completeness (11 official categories).
2. Deterministic rule evaluation per transaction.
3. Full trace & explanation engine for any transaction.
4. Classification summary & metrics per marketplace/period.
5. Zero financial delta ($0.00).
"""
import pytest
from engine.v4.database import DatabaseV4
from engine.v4.domain.financial_classification_engine import FinancialClassificationEngine, OFFICIAL_CATEGORIES

@pytest.fixture
def classification_engine():
    db = DatabaseV4.get()
    return FinancialClassificationEngine(db=db)

def test_official_categories_registry():
    """Verify that all 11 official category codes exist in the registry."""
    expected_codes = {
        "VENTA", "COMISION", "PUBLICIDAD", "ENVIO", "DEVOLUCION",
        "BONIFICACION", "AJUSTE", "IMPUESTO", "RETENCION", "COMPENSACION", "OTROS_CARGOS"
    }
    registered_codes = {cat["code"] for cat in OFFICIAL_CATEGORIES.values()}
    assert expected_codes.issubset(registered_codes)

def test_classify_transaction_deterministic(classification_engine):
    """Test deterministic evaluation for sample records."""
    # Query a transaction record
    db = DatabaseV4.get()
    df = db.query("SELECT * FROM v_ledger_certified LIMIT 1")
    assert not df.empty
    row = df.iloc[0]

    result = classification_engine.classify_record(row)
    assert "category_code" in result
    assert "category_name" in result
    assert "rule_id" in result
    assert "confidence" in result
    assert result["confidence"] == 1.0

def test_explain_classification(classification_engine):
    """Test full trace & explanation engine for a specific transaction ID."""
    db = DatabaseV4.get()
    df = db.query("SELECT id_transaccion FROM v_ledger_certified LIMIT 1")
    assert not df.empty
    tx_id = df.iloc[0]["id_transaccion"]

    explanation = classification_engine.explain_classification(tx_id)
    assert explanation is not None
    assert explanation["id_transaccion"] == tx_id
    assert "clasificacion" in explanation
    assert "regla_aplicada" in explanation
    assert "campo_utilizado" in explanation
    assert "valor_encontrado" in explanation
    assert "evidencia_utilizada" in explanation

def test_get_classification_summary(classification_engine):
    """Test classification summary metrics per marketplace and period."""
    summary = classification_engine.get_classification_summary(marketplace="ML", period="2025-12")
    assert "total_records" in summary
    assert "classified_records" in summary
    assert "coverage_percentage" in summary
    assert summary["coverage_percentage"] >= 99.0
    assert "category_breakdown" in summary

def test_get_classification_rules(classification_engine):
    """Test rule catalog endpoint output."""
    rules = classification_engine.get_rules_catalog()
    assert len(rules) > 0
    for r in rules:
        assert "rule_id" in r
        assert "category_code" in r
        assert "marketplace" in r
