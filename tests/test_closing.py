"""Tests for Phase 12.4 — Closing Engine."""
from __future__ import annotations
import pytest
from engine.v4.closing import ClosingEngine, CloseReport


@pytest.fixture
def engine():
    return ClosingEngine()


def test_run_period_close_ml(engine):
    report = engine.run_period_close("ML", "2026-01", dry_run=True)
    assert isinstance(report, CloseReport)
    assert report.marketplace == "ML"
    assert report.period == "2026-01"
    assert len(report.results) >= 1


def test_run_period_close_reconcile_only(engine):
    report = engine.run_period_close("ML", "2026-01", phases=["reconcile"], dry_run=True)
    assert any(r.phase == "RECONCILE" for r in report.results)


def test_run_period_close_certify_only(engine):
    report = engine.run_period_close("ML", "2026-01", phases=["certify"], dry_run=True)
    assert any(r.phase == "CERTIFY" for r in report.results)


def test_run_period_close_dry_run_preserves_data(engine):
    """Dry run should not modify any data."""
    db = engine.db
    before = db.query("SELECT COUNT(*) as n FROM marketplace_cierre_financiero_v1").iloc[0]["n"]
    engine.run_period_close("ML", "2026-05", dry_run=True)
    after = db.query("SELECT COUNT(*) as n FROM marketplace_cierre_financiero_v1").iloc[0]["n"]
    assert before == after
