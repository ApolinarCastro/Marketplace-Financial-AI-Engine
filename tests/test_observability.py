"""Tests for Observability (Phase 5) — health score and metrics."""
from __future__ import annotations
import pytest
from engine.v4.observability import FinancialHealthScore, FinancialMetricsCollector


class TestFinancialHealthScore:
    def test_evaluate_returns_report(self):
        health = FinancialHealthScore()
        result = health.evaluate()
        assert result.health_score >= 0
        assert result.status in ("SALUDABLE", "ATENCIÓN", "CRÍTICO")
        assert result.marketplace == "ALL"

    def test_evaluate_ml_returns_score(self):
        health = FinancialHealthScore()
        result = health.evaluate(marketplace="ML")
        assert result.health_score >= 0
        assert result.health_score <= 100

    def test_evaluate_paris_returns_score(self):
        health = FinancialHealthScore()
        result = health.evaluate(marketplace="PARIS")
        assert result.health_score >= 0
        assert result.health_score <= 100

    def test_evaluate_ripley_returns_score(self):
        health = FinancialHealthScore()
        result = health.evaluate(marketplace="RIPLEY")
        assert result.health_score >= 0
        assert result.health_score <= 100

    def test_evaluate_falabella_returns_score(self):
        health = FinancialHealthScore()
        result = health.evaluate(marketplace="FALABELLA")
        assert result.health_score >= 0
        assert result.health_score <= 100

    def test_evaluate_with_period(self):
        health = FinancialHealthScore()
        result = health.evaluate(periodo="2026-01")
        assert result.period == "2026-01"
        assert result.health_score >= 0


class TestFinancialMetricsCollector:
    def test_collect_returns_snapshot(self):
        collector = FinancialMetricsCollector()
        result = collector.collect()
        assert result.marketplace == "ALL"
        assert result.ledger_rows > 0

    def test_collect_ml(self):
        collector = FinancialMetricsCollector()
        result = collector.collect(marketplace="ML")
        assert result is not None

    def test_collect_paris(self):
        collector = FinancialMetricsCollector()
        result = collector.collect(marketplace="PARIS")
        assert result is not None

    def test_collect_ripley(self):
        collector = FinancialMetricsCollector()
        result = collector.collect(marketplace="RIPLEY")
        assert result is not None
