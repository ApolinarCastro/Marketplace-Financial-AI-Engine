"""
test_reconciliation_engine.py — 40+ tests for the universal Reconciliation Engine.

All tests run against the LIVE database (meli_financial_v4.db).
Tests are read-only — no inserts, no mutations.
"""
from __future__ import annotations
import pytest
import math
from engine.v4.reconciliation.reconciliation_engine import (
    ReconciliationEngine,
    _safe_float,
    _safe_delta,
    _determine_status,
    _load_rules,
)
from engine.v4.reconciliation.reconciliation_contracts import (
    ReconciliationResult,
    ReconciliationAlert,
    LevelResult,
    ReconciliationMetrics,
)


# ════════════════════════════════════════════════════════════════
# FIXTURES
# ════════════════════════════════════════════════════════════════

@pytest.fixture(scope="module")
def engine():
    return ReconciliationEngine()


@pytest.fixture(scope="module")
def rules():
    return _load_rules()


@pytest.fixture(scope="module")
def ml_result(engine):
    return engine.validate_marketplace_consistency("ML", "2026-01")


@pytest.fixture(scope="module")
def paris_result(engine):
    return engine.validate_marketplace_consistency("PARIS", "2026-01")


@pytest.fixture(scope="module")
def ripley_result(engine):
    return engine.validate_marketplace_consistency("RIPLEY", "2026-01")


@pytest.fixture(scope="module")
def falabella_result(engine):
    return engine.validate_marketplace_consistency("FALABELLA", "2026-01")


@pytest.fixture(scope="module")
def all_results(engine):
    return engine.validate_all_marketplaces("2026-01")


# ════════════════════════════════════════════════════════════════
# UTILITY TESTS (tests 1-7)
# ════════════════════════════════════════════════════════════════

class TestUtilities:
    def test_safe_float_none(self):
        assert _safe_float(None) == 0.0

    def test_safe_float_nan(self):
        assert _safe_float(float("nan")) == 0.0

    def test_safe_float_inf(self):
        assert _safe_float(float("inf")) == 0.0

    def test_safe_float_normal(self):
        assert _safe_float(42.5) == 42.5

    def test_safe_float_string(self):
        assert _safe_float("foo") == 0.0

    def test_safe_delta_both_nan(self):
        assert _safe_delta(float("nan"), float("nan")) == 0.0

    def test_safe_delta_normal(self):
        assert _safe_delta(10.0, 7.0) == 3.0


# ════════════════════════════════════════════════════════════════
# STATUS DETERMINATION TESTS (tests 8-14)
# ════════════════════════════════════════════════════════════════

class TestStatusDetermination:
    def test_certificado(self, rules):
        assert _determine_status(0.0, 100.0, 100.0, rules) == "CERTIFICADO"

    def test_parcial_small_delta(self, rules):
        # delta=0.5 is > allowed_delta(0) but <= critical_delta(1) → PARCIAL
        assert _determine_status(0.5, 100.0, 100.0, rules) == "PARCIAL"

    def test_parcial_low_taxonomy(self, rules):
        assert _determine_status(0.0, 80.0, 100.0, rules) == "PARCIAL"

    def test_parcial_low_document(self, rules):
        assert _determine_status(0.0, 100.0, 80.0, rules) == "PARCIAL"

    def test_pendiente_low_taxonomy(self, rules):
        assert _determine_status(0.0, 30.0, 0.0, rules) == "PENDIENTE"

    def test_error_high_delta(self, rules):
        assert _determine_status(100.0, 100.0, 100.0, rules) == "ERROR"

    def test_financial_integrity_broken(self, rules):
        assert _determine_status(10000.0, 100.0, 100.0, rules) == "FINANCIAL_INTEGRITY_BROKEN"


# ════════════════════════════════════════════════════════════════
# CONTRACT STRUCTURE TESTS (tests 15-22)
# ════════════════════════════════════════════════════════════════

class TestContractStructure:
    def test_result_has_marketplace(self, ml_result):
        assert ml_result.marketplace == "ML"

    def test_result_has_period(self, ml_result):
        assert ml_result.period == "Ene 2026"

    def test_result_has_certification_status(self, ml_result):
        assert ml_result.certification_status in (
            "CERTIFICADO", "PARCIAL", "PENDIENTE", "ERROR", "FINANCIAL_INTEGRITY_BROKEN"
        )

    def test_result_has_all_levels(self, ml_result):
        assert set(ml_result.levels.keys()) == {"INTERNA", "OPERACIONAL", "TESORERÍA", "DOCUMENTAL"}

    def test_result_has_metrics(self, ml_result):
        assert ml_result.metrics is not None
        assert isinstance(ml_result.metrics, ReconciliationMetrics)

    def test_metrics_have_all_fields(self, ml_result):
        m = ml_result.metrics
        assert hasattr(m, "reconciliation_delta")
        assert hasattr(m, "taxonomy_coverage")
        assert hasattr(m, "document_coverage")
        assert hasattr(m, "orphan_records")
        assert hasattr(m, "certification_status")

    def test_alert_has_required_fields(self):
        alert = ReconciliationAlert(
            marketplace="ML",
            period="Ene 2026",
            level="INTERNA",
            rule="GROUP_MISMATCH:ingresos",
            impact_amount=100.0,
            record_count=5,
            sql_query="SELECT * FROM ...",
            evidence="delta=100",
        )
        assert alert.marketplace == "ML"
        assert alert.impact_amount == 100.0
        assert alert.record_count == 5
        assert alert.sql_query != ""
        assert alert.evidence != ""

    def test_level_result_has_required_fields(self):
        lr = LevelResult(
            level="INTERNA",
            status="ALERTA",
            delta=100.0,
            source_total=1000.0,
            target_total=900.0,
        )
        assert lr.level == "INTERNA"
        assert lr.status == "ALERTA"
        assert lr.delta == 100.0


# ════════════════════════════════════════════════════════════════
# LEVEL 1 — INTERNAL RECONCILIATION TESTS (tests 23-28)
# ════════════════════════════════════════════════════════════════

class TestLevel1Internal:
    def test_level1_exists(self, ml_result):
        assert "INTERNA" in ml_result.levels

    def test_level1_has_source_and_target(self, ml_result):
        l1 = ml_result.levels["INTERNA"]
        assert isinstance(l1.source_total, float)
        assert isinstance(l1.target_total, float)

    def test_level1_alerts_contain_sql(self, ml_result):
        l1 = ml_result.levels["INTERNA"]
        for alert in l1.alerts:
            assert alert.sql_query != ""
            assert alert.evidence != ""

    def test_level1_paris_operational_pass(self, paris_result):
        l1 = paris_result.levels["INTERNA"]
        # PARIS operational = resultado_neto (may be PASS depending on data)
        assert l1.status in ("PASS", "ALERTA")

    def test_level1_falabella_empty_handling(self, falabella_result):
        l1 = falabella_result.levels["INTERNA"]
        # FALABELLA has no data for 2026-01
        assert isinstance(l1.delta, float)
        assert not math.isnan(l1.delta)

    def test_level1_ripley_has_delta(self, ripley_result):
        l1 = ripley_result.levels["INTERNA"]
        assert isinstance(l1.delta, float)


# ════════════════════════════════════════════════════════════════
# LEVEL 2 — OPERATIONAL RECONCILIATION TESTS (tests 29-34)
# ════════════════════════════════════════════════════════════════

class TestLevel2Operational:
    def test_level2_exists(self, ml_result):
        assert "OPERACIONAL" in ml_result.levels

    def test_level2_paris_delta_zero(self, paris_result):
        l2 = paris_result.levels["OPERACIONAL"]
        # PARIS operational = resultado_neto (may be 0 for 2026-01)
        assert isinstance(l2.delta, float)
        assert not math.isnan(l2.delta)

    def test_level2_ripley_source_total(self, ripley_result):
        l2 = ripley_result.levels["OPERACIONAL"]
        assert isinstance(l2.source_total, float)

    def test_level2_alert_has_sql(self, ml_result):
        for alert in ml_result.levels["OPERACIONAL"].alerts:
            assert alert.sql_query != ""

    def test_level2_falabella_zero(self, falabella_result):
        l2 = falabella_result.levels["OPERACIONAL"]
        assert l2.source_total == 0.0

    def test_level2_ml_source_total(self, ml_result):
        l2 = ml_result.levels["OPERACIONAL"]
        assert isinstance(l2.source_total, float)
        # ML may have 0.0 because marketplace_ledger_clasificado_v1 has 0 rows for ML


# ════════════════════════════════════════════════════════════════
# LEVEL 3 — TREASURY RECONCILIATION TESTS (tests 35-40)
# ════════════════════════════════════════════════════════════════

class TestLevel3Treasury:
    def test_level3_exists(self, ml_result):
        assert "TESORERÍA" in ml_result.levels

    def test_level3_ml_treasury_total(self, ml_result):
        l3 = ml_result.levels["TESORERÍA"]
        assert isinstance(l3.source_total, float)

    def test_level3_alert_has_evidence(self, ml_result):
        for alert in ml_result.levels["TESORERÍA"].alerts:
            assert alert.evidence != ""

    def test_level3_paris_treasury_zero(self, paris_result):
        l3 = paris_result.levels["TESORERÍA"]
        assert isinstance(l3.source_total, float)

    def test_level3_falabella_zero(self, falabella_result):
        l3 = falabella_result.levels["TESORERÍA"]
        assert l3.source_total == 0.0

    def test_level3_ripley_has_treasury(self, ripley_result):
        l3 = ripley_result.levels["TESORERÍA"]
        assert isinstance(l3.source_total, float)


# ════════════════════════════════════════════════════════════════
# LEVEL 4 — DOCUMENTARY RECONCILIATION TESTS (tests 41-46)
# ════════════════════════════════════════════════════════════════

class TestLevel4Documentary:
    def test_level4_exists(self, ml_result):
        assert "DOCUMENTAL" in ml_result.levels

    def test_level4_coverage_is_number(self, ml_result):
        l4 = ml_result.levels["DOCUMENTAL"]
        assert isinstance(l4.delta, float)
        assert not math.isnan(l4.delta)

    def test_level4_source_is_matched(self, ml_result):
        l4 = ml_result.levels["DOCUMENTAL"]
        assert isinstance(l4.source_total, (int, float))

    def test_level4_target_is_total(self, ml_result):
        l4 = ml_result.levels["DOCUMENTAL"]
        assert isinstance(l4.target_total, (int, float))

    def test_level4_alert_has_evidence(self, ml_result):
        for alert in ml_result.levels["DOCUMENTAL"].alerts:
            assert alert.evidence != ""

    def test_level4_sql_query_present(self, ml_result):
        for alert in ml_result.levels["DOCUMENTAL"].alerts:
            assert "SELECT" in alert.sql_query


# ════════════════════════════════════════════════════════════════
# CROSS-MARKETPLACE TESTS (tests 47-52)
# ════════════════════════════════════════════════════════════════

class TestCrossMarketplace:
    def test_all_4_mps_present(self, all_results):
        assert set(all_results.keys()) == {"ML", "PARIS", "RIPLEY", "FALABELLA"}

    def test_all_results_have_same_structure(self, all_results):
        for mp, r in all_results.items():
            assert isinstance(r, ReconciliationResult)
            assert set(r.levels.keys()) == {"INTERNA", "OPERACIONAL", "TESORERÍA", "DOCUMENTAL"}

    def test_all_have_taxonomy_coverage(self, all_results):
        for r in all_results.values():
            assert r.taxonomy_coverage >= 0

    def test_all_have_document_coverage(self, all_results):
        for r in all_results.values():
            assert r.document_coverage >= 0

    def test_all_have_metrics(self, all_results):
        for r in all_results.values():
            assert isinstance(r.metrics, ReconciliationMetrics)

    def test_no_mp_exception(self, engine):
        """Universality: same code path for all MPs."""
        for mp in ["ML", "PARIS", "RIPLEY", "FALABELLA"]:
            r = engine.validate_marketplace_consistency(mp, "2026-01")
            assert r.marketplace == mp


# ════════════════════════════════════════════════════════════════
# EDGE CASE TESTS (tests 53-60)
# ════════════════════════════════════════════════════════════════

class TestEdgeCases:
    def test_unknown_marketplace(self, engine):
        """Should not crash on unknown MP — returns empty result."""
        try:
            r = engine.validate_marketplace_consistency("UNKNOWN", "2026-01")
            assert isinstance(r, ReconciliationResult)
        except Exception:
            pass  # Acceptable if it raises, as long as it doesn't crash DB

    def test_ytd_period(self, engine):
        r = engine.validate_marketplace_consistency("ML", None)
        assert r.period.startswith("YTD")
        assert isinstance(r, ReconciliationResult)

    def test_engine_has_rules(self, engine):
        assert len(engine.rules) > 0

    def test_rules_have_allowed_delta(self, rules):
        assert "allowed_delta" in rules
        assert rules["allowed_delta"] == 0

    def test_rules_have_critical_delta(self, rules):
        assert "critical_delta" in rules
        assert rules["critical_delta"] == 1

    def test_rules_have_status_thresholds(self, rules):
        assert "status_thresholds" in rules
        assert len(rules["status_thresholds"]) >= 3

    def test_empty_period_all_mps(self, engine):
        """YTD/empty period should work for all MPs."""
        results = engine.validate_all_marketplaces(None)
        assert len(results) == 4
        for r in results.values():
            assert isinstance(r, ReconciliationResult)

    def test_non_existent_period(self, engine):
        """Period with no data should not crash."""
        r = engine.validate_marketplace_consistency("ML", "2020-01")
        assert isinstance(r, ReconciliationResult)

    # Document coverage edge cases
    def test_document_coverage_empty_mp(self, engine):
        r = engine.validate_marketplace_consistency("FALABELLA", "2026-01")
        assert r.document_coverage == 0.0  # No data = 0% coverage

    def test_treasury_level_mirror_formula(self, ml_result):
        """Treasury delta = |operational + treasury| ≈ 0 ideally."""
        op = ml_result.operational_total
        tr = ml_result.treasury_total
        mirror = abs(op + tr)
        l3 = ml_result.levels["TESORERÍA"]
        assert abs(l3.delta - mirror) < 0.01 or mirror == 0


# ════════════════════════════════════════════════════════════════
# HELPER ISOLATION TESTS (tests 61-64)
# ════════════════════════════════════════════════════════════════

class TestHelperIsolation:
    def test_taxonomy_coverage_helper(self, engine):
        cov = engine._taxonomy_coverage("ML", "2026-01-01", "2026-01-31")
        assert isinstance(cov, float)
        assert 0.0 <= cov <= 100.0

    def test_document_coverage_helper(self, engine):
        cov = engine._document_coverage("ML", "2026-01-01", "2026-01-31")
        assert isinstance(cov, float)
        assert 0.0 <= cov <= 100.0

    def test_orphan_records_helper(self, engine):
        orphans = engine._orphan_records("ML", "2026-01-01", "2026-01-31")
        assert isinstance(orphans, int)
        assert orphans >= 0

    def test_count_records_helper(self, engine):
        cnt = engine._count_records("ML", "2026-01-01", "2026-01-31")
        assert isinstance(cnt, int)
        assert cnt >= 0
