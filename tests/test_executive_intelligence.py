"""Tests for ExecutiveIntelligence engine."""
import pytest
import sys; sys.path.insert(0, '.')
from engine.v4.intelligence.executive_intelligence import ExecutiveIntelligence


@pytest.fixture
def engine():
    return ExecutiveIntelligence()


def test_analyze_returns_report(engine):
    report = engine.analyze("ML", "2026-01")
    assert report.marketplace == "ML"
    assert report.period == "2026-01"
    assert report.total_insights > 0
    assert report.executive_summary != ""


def test_analyze_all_mps(engine):
    report = engine.analyze("ALL")
    assert report.marketplace == "ALL"
    assert report.total_insights > 0
    insights_by_type = {i.insight_type for i in report.insights}
    assert "contribution" in insights_by_type  # Only ALL has contribution
    assert "risk" in insights_by_type


def test_analyze_per_mp(engine):
    for mp in ["ML", "PARIS", "RIPLEY", "FALABELLA"]:
        report = engine.analyze(mp)
        assert report.marketplace == mp
        assert report.total_insights > 0, f"No insights for {mp}"
        # Verify no contribution data for per-MP
        for ins in report.insights:
            assert ins.insight_type != "contribution"  # Only for ALL


def test_risk_insight(engine):
    report = engine.analyze("RIPLEY")
    risks = [i for i in report.insights if i.insight_type == "risk"]
    assert len(risks) >= 1
    assert risks[0].impact_amount > 0


def test_coverage_insight(engine):
    report = engine.analyze("ALL")
    coverage = [i for i in report.insights if i.insight_type == "coverage"]
    assert len(coverage) >= 1
    assert coverage[0].impact_amount >= 0  # coverage percentage


def test_driver_insight(engine):
    report = engine.analyze("ML")
    drivers = [i for i in report.insights if i.insight_type == "driver"]
    assert len(drivers) >= 1
    assert drivers[0].impact_amount > 0


def test_summary_includes_marketplace(engine):
    report = engine.analyze("PARIS")
    assert "PARIS" in report.executive_summary


def test_insights_have_all_required_fields(engine):
    report = engine.analyze("ALL")
    for ins in report.insights:
        assert ins.title
        assert ins.description
        assert ins.insight_type
        assert isinstance(ins.marketplaces, list)
