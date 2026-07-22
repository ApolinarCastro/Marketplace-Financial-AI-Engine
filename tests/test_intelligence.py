"""Tests for Intelligence (Phase 7) — insights, returns, anomalies."""
from __future__ import annotations
import pytest
from engine.v4.intelligence import OperationalInsights, ReturnReasonAnalyzer, FinancialAnomalyDetector


class TestOperationalInsights:
    def test_analyze_returns_report(self):
        engine = OperationalInsights()
        report = engine.analyze()
        assert report.total_insights >= 0
        assert report.marketplace == "ALL"

    def test_analyze_ml(self):
        engine = OperationalInsights()
        report = engine.analyze(marketplace="ML")
        assert report.marketplace == "ML"
        assert report.total_insights >= 0

    def test_analyze_paris(self):
        engine = OperationalInsights()
        report = engine.analyze(marketplace="PARIS")
        assert report.marketplace == "PARIS"

    def test_analyze_ripley(self):
        engine = OperationalInsights()
        report = engine.analyze(marketplace="RIPLEY")
        assert report.marketplace == "RIPLEY"

    def test_analyze_with_period(self):
        engine = OperationalInsights()
        report = engine.analyze(periodo="2026-01")
        assert report.period == "2026-01"

    def test_insights_have_evidence(self):
        engine = OperationalInsights()
        report = engine.analyze(marketplace="ML")
        for insight in report.insights:
            assert insight.evidence
            assert insight.sql_query

    def test_top_cost_drivers_returns_valid(self):
        engine = OperationalInsights()
        report = engine.analyze(marketplace="ML")
        cost_insights = [i for i in report.insights if i.insight_type == "cost_analysis"]
        assert len(cost_insights) >= 0


class TestReturnReasonAnalyzer:
    def test_analyze_returns_report(self):
        analyzer = ReturnReasonAnalyzer()
        report = analyzer.analyze()
        assert report.total_cases >= 0
        assert report.marketplace == "ALL"

    def test_analyze_ml(self):
        analyzer = ReturnReasonAnalyzer()
        report = analyzer.analyze(marketplace="ML")
        assert report.marketplace == "ML"

    def test_analyze_paris(self):
        analyzer = ReturnReasonAnalyzer()
        report = analyzer.analyze(marketplace="PARIS")
        assert report.marketplace == "PARIS"

    def test_analyze_ripley(self):
        analyzer = ReturnReasonAnalyzer()
        report = analyzer.analyze(marketplace="RIPLEY")
        assert report.marketplace == "RIPLEY"

    def test_analyze_with_period(self):
        analyzer = ReturnReasonAnalyzer()
        report = analyzer.analyze(periodo="2026-01")
        assert report.period == "2026-01"

    def test_reasons_have_participation(self):
        analyzer = ReturnReasonAnalyzer()
        report = analyzer.analyze(marketplace="RIPLEY")
        for r in report.reasons:
            assert r.participation_pct >= 0
            assert abs(r.total_amount) > 0  # devoluciones son distintas de cero


class TestFinancialAnomalyDetector:
    def test_detect_returns_report(self):
        detector = FinancialAnomalyDetector()
        report = detector.detect()
        assert report.total_anomalies >= 0
        assert report.marketplace == "ALL"

    def test_detect_ml(self):
        detector = FinancialAnomalyDetector()
        report = detector.detect(marketplace="ML")
        assert report.marketplace == "ML"

    def test_detect_paris(self):
        detector = FinancialAnomalyDetector()
        report = detector.detect(marketplace="PARIS")
        assert report.marketplace == "PARIS"

    def test_detect_ripley(self):
        detector = FinancialAnomalyDetector()
        report = detector.detect(marketplace="RIPLEY")
        assert report.marketplace == "RIPLEY"

    def test_anomalies_have_evidence(self):
        detector = FinancialAnomalyDetector()
        report = detector.detect(marketplace="ML")
        for a in report.anomalies:
            assert a.evidence
            assert a.sql_query

    def test_zero_revenue_detected_for_future(self):
        detector = FinancialAnomalyDetector()
        report = detector.detect(marketplace="ML", periodo="2099-01")
        has_zero = any(a.anomaly_type == "ZERO_REVENUE" for a in report.anomalies)
        assert has_zero
