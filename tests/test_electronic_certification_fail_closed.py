"""Electronic certification fail-closed semantics (PFO-ELECTRONIC-SIGNATURE-HARDENING-001).

Proves missing dependencies / unexecuted validation can never yield PASS,
and that unsigned XML fails hard. No production state touched.
"""
from __future__ import annotations

from pathlib import Path

from engine.v4.certification.electronic_certification import ElectronicCertificationEngine
from engine.v4.certification.electronic_certification.electronic_certification_engine import (
    can_claim_electronic_certification,
)
from engine.v4.certification.electronic_certification.caf_validator import CafValidator
from engine.v4.certification.electronic_certification.signature_validator import SignatureValidator
from engine.v4.certification.electronic_certification.vat_validator import VatValidator
from engine.v4.certification.electronic_certification.xsd_validator import XsdValidator

GOLDEN_XML = Path("tests/golden/xml_dte_e2e/input/PFO_SYNTH_DTE_90000001.xml").read_text(encoding="utf-8")


def _force_no_deps(validator):
    validator.has_deps = False
    if hasattr(validator, "safe_mode"):
        validator.safe_mode = False
    if hasattr(validator, "xmlschema"):
        validator.xmlschema = None
    if hasattr(validator, "etree"):
        validator.etree = None
    return validator


def test_case_a_signature_missing_deps_is_not_implemented():
    v = _force_no_deps(SignatureValidator())
    r = v.validate(GOLDEN_XML)
    assert r["status"] == "NOT_IMPLEMENTED", r["status"]
    assert r["status"] != "PASS"

    eng = ElectronicCertificationEngine()
    eng.signature_validator = _force_no_deps(SignatureValidator())
    out = eng.certify(GOLDEN_XML)
    assert out["overall_status"] != "PASS"
    assert can_claim_electronic_certification(out) is False


def test_case_b_xsd_unavailable_is_not_implemented():
    v = _force_no_deps(XsdValidator())
    r = v.validate(GOLDEN_XML)
    assert r["status"] == "NOT_IMPLEMENTED", r["status"]

    eng = ElectronicCertificationEngine()
    eng.xsd_validator = _force_no_deps(XsdValidator())
    out = eng.certify(GOLDEN_XML)
    assert out["overall_status"] != "PASS"
    assert can_claim_electronic_certification(out) is False


def test_case_c_caf_unavailable_is_not_implemented():
    v = _force_no_deps(CafValidator())
    r = v.validate(GOLDEN_XML, {})
    assert r["status"] == "NOT_IMPLEMENTED", r["status"]

    v2 = _force_no_deps(VatValidator())
    r2 = v2.validate(GOLDEN_XML, {})
    assert r2["status"] == "NOT_IMPLEMENTED", r2["status"]


def test_case_d_unsigned_xml_fails_never_passes():
    # Synthetic fixture carries no ds:Signature node by design.
    v = SignatureValidator()
    r = v.validate(GOLDEN_XML)
    assert r["status"] != "PASS", r["status"]
    assert r["status"] in ("NOT_IMPLEMENTED", "FAIL", "INVALID_CERTIFICATE",
                           "INVALID_SIGNATURE", "EXPIRED_CERTIFICATE")

    eng = ElectronicCertificationEngine()
    out = eng.certify(GOLDEN_XML)
    assert out["overall_status"] != "PASS"
    assert can_claim_electronic_certification(out) is False


def test_gate_requires_real_pass():
    assert can_claim_electronic_certification(None) is False
    assert can_claim_electronic_certification({}) is False
    assert can_claim_electronic_certification({"overall_status": "PARTIAL"}) is False
    assert can_claim_electronic_certification({"overall_status": "FAIL"}) is False
    assert can_claim_electronic_certification({"overall_status": "PASS"}) is True


def test_engine_partial_when_incomplete_no_hard_failure():
    # XML structure passes; XSD+signature NOT_IMPLEMENTED; CAF sees no CAF
    # node in the minimal fixture -> hard INVALID_CAF. Overall must not be PASS.
    # (With a CAF-bearing fixture the aggregate would be PARTIAL instead.)
    eng = ElectronicCertificationEngine()
    out = eng.certify(GOLDEN_XML)
    assert out["overall_status"] in ("PARTIAL", "FAIL")
    assert out["overall_status"] != "PASS"
