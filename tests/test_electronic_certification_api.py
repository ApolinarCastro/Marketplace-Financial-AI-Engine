"""
Unit test for /api/v4/electronic_certification/status/{tx_id} endpoint.
Fulfills CAP_PRODUCT_CONSISTENCY_001 Accion Correctiva 2.
CORRECTED 2026-08-06 (LOOP_P0_1): RIPLEY liquidation folios are NOT SII DTE.
LEDGER_EXISTING must never produce CRYPTOGRAPHIC_CERTIFIED.
"""
import pytest
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

def test_electronic_certification_status_ripley_not_certified():
    # RIPLEY transaction: ledger folio is a liquidation number, not an SII DTE.
    # Must NEVER be reported as fiscal certificate.
    res = client.get("/api/v4/electronic_certification/status/RIP_596684_24751081101-A_importedelpedido")
    assert res.status_code == 200
    data = res.json()
    assert data["estado"] == "INSUFFICIENT_FISCAL_EVIDENCE"
    assert data["certification_scope"] == "UNKNOWN"
    assert data["evidence_source"] == "NONE"
    assert data["blocking_reason"] == "RIPLEY_LIQUIDATION_IS_NOT_SII_DTE"
    assert data["pipeline"]["xml"] == "FAIL"
    assert data["pipeline"]["xsd"] == "FAIL"
    assert data["pipeline"]["sig"] == "FAIL"
    assert data["pipeline"]["caf"] == "FAIL"
    assert data["folio"] == "596684"
    assert data["evidencia"]["confidence"] == "0%"
    assert data["evidencia"]["level"] == "INSUFFICIENT_FISCAL_EVIDENCE"
    assert data["evidencia"]["level"] != "CRYPTOGRAPHIC_CERTIFIED"

def test_electronic_certification_status_unknown_tx():
    res = client.get("/api/v4/electronic_certification/status/NON_EXISTENT_TX_99999")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "INSUFFICIENT_FISCAL_EVIDENCE"
    assert data["pipeline"]["xml"] == "FAIL"
    assert data["evidencia"]["confidence"] == "0%"
