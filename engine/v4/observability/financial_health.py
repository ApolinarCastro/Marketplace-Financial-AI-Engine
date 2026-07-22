"""
financial_health.py — Financial Health Score computation.

Produces a single 0-100 score per marketplace from weighted metrics.
Consumes FinancialMetricsCollector — no direct DB access.
"""
from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field

from engine.v4.observability.financial_metrics import FinancialMetricsCollector, FinancialMetricsSnapshot


@dataclass
class FinancialHealthReport:
    marketplace: str
    period: str
    health_score: float
    status: str  # SALUDABLE|ATENCIÓN|CRÍTICO
    metrics: FinancialMetricsSnapshot | None = None
    sub_scores: dict[str, float] = field(default_factory=dict)
    timestamp: str = ""


class FinancialHealthScore:
    """Computes financial health scores per marketplace."""

    def __init__(self, collector: FinancialMetricsCollector | None = None):
        self.collector = collector or FinancialMetricsCollector()

    def evaluate(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
    ) -> FinancialHealthReport:
        """Evaluate financial health for a marketplace/period."""
        metrics = self.collector.collect(marketplace, periodo)
        return self._build_report(metrics)

    def evaluate_all(self, periodo: str | None = None) -> dict[str, FinancialHealthReport]:
        """Evaluate all marketplaces."""
        all_metrics = self.collector.collect_all_marketplaces(periodo)
        return {mp: self._build_report(m) for mp, m in all_metrics.items()}

    def _build_report(self, metrics: FinancialMetricsSnapshot) -> FinancialHealthReport:
        score = metrics.marketplace_health_score
        if score >= 80:
            status = "SALUDABLE"
        elif score >= 50:
            status = "ATENCIÓN"
        else:
            status = "CRÍTICO"

        return FinancialHealthReport(
            marketplace=metrics.marketplace,
            period=metrics.period,
            health_score=score,
            status=status,
            metrics=metrics,
            sub_scores={
                "reconciliation_delta": max(0, 100 - min(metrics.reconciliation_delta / 100000, 100)),
                "taxonomy_coverage": metrics.taxonomy_coverage,
                "document_coverage": metrics.document_coverage,
                "classification": max(0, 100 - metrics.unclassified_records),
                "audit_health": max(0, 100 - min(metrics.audit_alerts / 1000, 100)),
            },
            timestamp=datetime.now().isoformat(),
        )
