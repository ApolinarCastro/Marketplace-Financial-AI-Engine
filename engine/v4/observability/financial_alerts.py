"""
financial_alerts.py — Certified financial alert aggregator.

Consumes ReconciliationEngine alerts + audit data.
Every alert includes evidence: amount, source, SQL, record count.
"""
from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any

from engine.v4.database import DatabaseV4
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
from engine.v4.reconciliation.reconciliation_contracts import ReconciliationAlert


@dataclass
class FinancialAlertSummary:
    total_alerts: int = 0
    alerts_by_level: dict[str, int] = field(default_factory=dict)
    alerts_by_rule: dict[str, int] = field(default_factory=dict)
    total_impact: float = 0.0
    alerts: list[dict[str, Any]] = field(default_factory=list)
    marketplace: str = "ALL"
    period: str = ""
    timestamp: str = ""


class FinancialAlertAggregator:
    """Aggregates reconciliation alerts + audit data into single view."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self.recon = ReconciliationEngine(self.db)

    def aggregate(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
        limit: int = 100,
    ) -> FinancialAlertSummary:
        """Aggregate all alerts for a marketplace/period."""
        mp = marketplace.upper() if marketplace else "ALL"

        if mp != "ALL":
            recon_result = self.recon.validate_marketplace_consistency(mp, periodo)
            recon_alerts = recon_result.alerts
            period_label = recon_result.period
        else:
            recon_alerts = []
            period_label = periodo or "YTD"

        # Convert reconciliation alerts to dicts
        alert_dicts = []
        for a in recon_alerts:
            alert_dicts.append({
                "marketplace": a.marketplace,
                "period": a.period,
                "level": a.level,
                "rule": a.rule,
                "impact_amount": a.impact_amount,
                "record_count": a.record_count,
                "sql_query": a.sql_query,
                "evidence": a.evidence,
                "source": "reconciliation",
            })

        # Count by level and rule
        by_level: dict[str, int] = {}
        by_rule: dict[str, int] = {}
        total_impact = 0.0
        for a in alert_dicts:
            by_level[a["level"]] = by_level.get(a["level"], 0) + 1
            by_rule[a["rule"]] = by_rule.get(a["rule"], 0) + 1
            total_impact += a["impact_amount"]

        return FinancialAlertSummary(
            total_alerts=len(alert_dicts),
            alerts_by_level=by_level,
            alerts_by_rule=by_rule,
            total_impact=round(total_impact, 2),
            alerts=alert_dicts[:limit],
            marketplace=mp,
            period=period_label,
            timestamp=datetime.now().isoformat(),
        )
