"""Tests for Certification Engine (Phase 9)."""
from __future__ import annotations
import pytest
from engine.v4.certification import CertificationEngine


class TestCertificationEngine:
    def test_certify_returns_certification(self):
        engine = CertificationEngine()
        cert = engine.certify()
        assert cert.marketplace == "ALL"
        assert cert.status in ("CERTIFIED", "DEGRADED", "FAILED")
        assert len(cert.claims) > 0

    def test_certify_ml(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="ML")
        assert cert.marketplace == "ML"
        assert len(cert.claims) > 0

    def test_certify_paris(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="PARIS")
        assert cert.marketplace == "PARIS"

    def test_certify_ripley(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="RIPLEY")
        assert cert.marketplace == "RIPLEY"

    def test_certify_falabella(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="FALABELLA")
        assert cert.marketplace == "FALABELLA"

    def test_certify_with_period(self):
        engine = CertificationEngine()
        cert = engine.certify(periodo="2026-01")
        assert cert.period == "2026-01"

    def test_all_claims_have_evidence(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="ML")
        for claim in cert.claims:
            assert claim.evidence_sql
            assert claim.kpi

    def test_pass_rate_between_0_and_100(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="ML")
        assert 0 <= cert.pass_rate <= 100

    def test_ingresos_claim_present(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="ML")
        kpis = [c.kpi for c in cert.claims]
        assert "INGRESOS" in kpis

    def test_devoluciones_claim_present(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="ML")
        kpis = [c.kpi for c in cert.claims]
        assert "DEVOLUCIONES" in kpis

    def test_classification_coverage_claim_present(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="ML")
        kpis = [c.kpi for c in cert.claims]
        assert "CLASSIFICATION_COVERAGE" in kpis

    def test_operational_pnl_claim_present(self):
        engine = CertificationEngine()
        cert = engine.certify(marketplace="ML")
        kpis = [c.kpi for c in cert.claims]
        assert "OPERATIONAL_PNL" in kpis
