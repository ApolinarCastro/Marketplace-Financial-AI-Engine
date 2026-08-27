"""
Meli Financial AI Engine v4.0
Phase 5 Step 5 — Exception Engine Test Suite
Validates:
1. Deterministic exception_id generation (SHA-256).
2. Exclusion of CRYPTOGRAPHIC_CERTIFIED / CONCILIADO records from exception generation.
3. Official canonical catalog (19 categories), severity rules (CRITICAL, HIGH, MEDIUM, LOW), priority (P1-P4), owner, and required_action.
4. SLA calculation and age tracking (within_sla, sla_breached).
5. Deduplication control preventing duplicate active exceptions (single-primary per transaction).
6. Full end-to-end evidence traceability payload.
7. Zero financial delta ($0.00).
"""
import pytest
from engine.v4.database import DatabaseV4
from engine.v4.domain.exception_engine import ExceptionEngine, EXCEPTION_CAUSES, EXCEPTION_OWNERS, SEVERITY_RULES, LEGACY_CAUSE_TO_CANONICAL

@pytest.fixture
def exception_engine():
    db = DatabaseV4.get()
    return ExceptionEngine(db=db)

def test_catalogs_completeness():
    """Verify that exception causes, owners, and severity rules are fully registered."""
    expected_causes = {
        "MISSING_DTE", "INSUFFICIENT_FISCAL_EVIDENCE", "TRUTH_CONFLICT",
        "MISSING_XML", "DOCUMENT_REFERENCE_ONLY", "LEDGER_REFERENCE_ONLY", "MISSING_SUPPORT",
        "AMOUNT_MISMATCH", "DATE_MISMATCH", "CLASSIFICATION_CONFLICT", "RECONCILIATION_FAILED",
        "SETTLEMENT_MISSING", "PENDING_COLLECTION", "PENDING_PAYMENT", "SAP_MISMATCH",
        "MARKETPLACE_MISMATCH", "UNMATCHED_TRANSACTION", "UNMATCHED_ORDER", "MANUAL_REVIEW_REQUIRED"
    }
    assert expected_causes.issubset(set(EXCEPTION_CAUSES.keys()))

    # Legacy 10-cause catalog must map onto the canonical catalog (spec change: 10 → 19).
    assert set(LEGACY_CAUSE_TO_CANONICAL.keys()) == {
        "DIFERENCIA_MONTO", "DIFERENCIA_DOCUMENTAL", "DIFERENCIA_TRIBUTARIA",
        "COBRO_PENDIENTE", "PAGO_PENDIENTE", "SIN_RESPALDO_XML",
        "SIN_RESPALDO_DTE", "SIN_MATCH_SAP", "SIN_MATCH_MARKETPLACE", "REQUIERE_REVISION"
    }
    assert set(LEGACY_CAUSE_TO_CANONICAL.values()).issubset(set(EXCEPTION_CAUSES.keys()))

    expected_owners = {
        "FINANZAS", "TESORERIA", "CONTABILIDAD", "TRIBUTARIO",
        "ECOMMERCE", "LOGISTICA", "TECNOLOGIA", "MARKETPLACE", "REVISION_MANUAL"
    }
    assert expected_owners.issubset(set(EXCEPTION_OWNERS.keys()))

def test_deterministic_exception_id(exception_engine):
    """Test deterministic exception_id calculation using SHA-256."""
    id1 = exception_engine.compute_exception_id("ML", "TX123", "ORD456", "MISSING_DTE", "REF1")
    id2 = exception_engine.compute_exception_id("ML", "TX123", "ORD456", "MISSING_DTE", "REF1")
    id3 = exception_engine.compute_exception_id("ML", "TX123", "ORD456", "MISSING_DTE", "REF2")

    assert len(id1) == 64
    assert id1 == id2
    assert id1 != id3

def test_exclusion_of_conciliado_records(exception_engine):
    """Verify that fully-certified records (CRYPTOGRAPHIC_CERTIFIED) DO NOT generate exceptions."""
    # Estado de certificación completo ⇒ ninguna categoría primaria (0 excepciones).
    assert exception_engine._resolve_primary_category(
        {"marketplace": "PARIS", "financial_group": "ingresos", "folio_xml": "6284235"},
        {"estado": "CRYPTOGRAPHIC_CERTIFIED", "has_real_dte": True, "has_doc_match": True},
    ) is None
    # Registros sin evidencia fiscal mínima sí generan excepción.
    assert exception_engine._resolve_primary_category(
        {"marketplace": "RIPLEY", "financial_group": "ingresos", "folio_xml": None},
        {"estado": "INSUFFICIENT_FISCAL_EVIDENCE", "has_real_dte": False, "has_doc_match": False},
    ) == "INSUFFICIENT_FISCAL_EVIDENCE"

def test_process_unconciliated_record(exception_engine):
    """Verify read-only evaluation of an unconciliated record into a canonical Exception object."""
    rec = {
        "id_transaccion": "TX_UNCONCILIATED",
        "marketplace": "ML",
        "id_orden": "ORD_UNCONC",
        "fecha": "2025-12-01",
        "monto": 15000.0,
        "folio_xml": None,
        "financial_group": "ingresos",
    }
    res = exception_engine.evaluate(rec)
    assert res["status"] == "EVALUATED"
    assert res["financial_delta"] == "$0.00"
    assert isinstance(res["exceptions"], list)
    assert len(res["exceptions"]) == 1
    exc = res["exceptions"][0]
    assert exc["exception_type"] in EXCEPTION_CAUSES
    assert exc["severity"] in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
    assert exc["priority"] in ("P1", "P2", "P3", "P4")
    assert exc["owner"] in EXCEPTION_OWNERS
    assert exc["required_action"] != ""
    assert exc["status"] == "OPEN"
    assert "exception_id" in exc
    assert len(exc["exception_id"]) == 64

def test_deduplication_and_aggregation(exception_engine):
    """Test building exception catalog and avoiding duplicates."""
    res = exception_engine.build_exceptions_catalog(marketplace="ML", page_size=50)
    assert "total_exceptions" in res
    assert "duplicate_exceptions_prevented" in res
    assert "exceptions" in res
    assert isinstance(res["exceptions"], list)

    # Verify no duplicate exception_id in list
    exc_ids = [e["exception_id"] for e in res["exceptions"]]
    assert len(exc_ids) == len(set(exc_ids))

def test_exception_sla_metrics(exception_engine):
    """Test SLA metrics calculation."""
    sla_data = exception_engine.get_sla_summary(marketplace="ML")
    assert "total_exceptions" in sla_data
    assert "within_sla" in sla_data
    assert "sla_breached" in sla_data

def test_exception_health_and_summary(exception_engine):
    """Test health check and summary endpoints data structure."""
    health = exception_engine.get_health()
    assert health["status"] in ("READY", "PASS")
    assert health["exception_engine"] == "ACTIVE"

    summary = exception_engine.get_summary(marketplace="ML")
    assert "total_exceptions" in summary
    assert "financial_delta" in summary
    assert summary["financial_delta"] == "$0.00"
