"""
financial_metrics.py — Certified financial metrics collector.

Computes the 10 mandatory observability metrics from certified sources.
All metrics are deterministic, traceable, and reproducible.
"""
from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any

from engine.v4.database import DatabaseV4
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine
from engine.v4.reconciliation.reconciliation_contracts import ReconciliationResult


@dataclass
class FinancialMetricsSnapshot:
    reconciliation_delta: float = 0.0
    taxonomy_coverage: float = 100.0
    document_coverage: float = 0.0
    orphan_records: int = 0
    unclassified_records: int = 0
    ledger_rows: int = 0
    classified_rows: int = 0
    audit_alerts: int = 0
    certification_status: str = "PENDIENTE"
    marketplace_health_score: float = 0.0
    timestamp: str = ""
    marketplace: str = "ALL"
    period: str = ""


class FinancialMetricsCollector:
    """Collects all 10 mandatory metrics from certified sources."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self.recon = ReconciliationEngine(self.db)

    def collect(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
    ) -> FinancialMetricsSnapshot:
        """Collect all metrics for a given marketplace and period."""
        mp = marketplace.upper() if marketplace else "ALL"
        recon_result = self.recon.validate_marketplace_consistency(mp, periodo) if mp != "ALL" else None

        if recon_result:
            rd = recon_result.delta
            tc = recon_result.taxonomy_coverage
            dc = recon_result.document_coverage
            orphans = recon_result.orphan_records
            cs = recon_result.certification_status
            period_label = recon_result.period
        else:
            rd = 0.0
            tc = 100.0
            dc = 0.0
            orphans = 0
            cs = "PENDIENTE"
            period_label = periodo or "YTD"

        # Unclassified records
        start, end, _ = self.recon.fe.resolve_period_range(periodo)
        date_sql = "AND fecha >= ?" if end is None else "AND fecha BETWEEN ? AND ?"
        date_params = [start] if end is None else [start, end]

        base_where = "1=1"
        base_params: list = []

        if mp != "ALL":
            base_where += " AND marketplace = ?"
            base_params.append(mp)

        if date_sql:
            base_where += f" {date_sql}"
            base_params.extend(date_params)

        # Count records without financial_group
        df_uncl = self.db.query(
            f"SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE {base_where} AND (financial_group IS NULL OR financial_group = '')",
            base_params)
        unclassified = int(df_uncl.iloc[0]["n"]) if not df_uncl.empty else 0

        df_total = self.db.query(
            f"SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE {base_where}",
            base_params)
        total_ledger = int(df_total.iloc[0]["n"]) if not df_total.empty else 0

        # Classified rows (have financial_group)
        df_cl = self.db.query(
            f"SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE financial_group IS NOT NULL AND financial_group != '' AND {base_where}",
            base_params)
        classified = int(df_cl.iloc[0]["n"]) if not df_cl.empty else 0

        # Audit alerts count
        if mp != "ALL":
            audit_params = [mp]
            audit_where = "WHERE marketplace = ?"
        else:
            audit_params = []
            audit_where = ""

        df_audit = self.db.query(
            f"SELECT COUNT(*) as n FROM marketplace_auditoria_v1 {audit_where}", audit_params)
        audit_count = int(df_audit.iloc[0]["n"]) if not df_audit.empty else 0

        # Health score (0-100)
        health = self._compute_health_score(rd, tc, dc, orphans, unclassified, audit_count)

        return FinancialMetricsSnapshot(
            reconciliation_delta=round(rd, 2),
            taxonomy_coverage=round(tc, 2),
            document_coverage=round(dc, 2),
            orphan_records=orphans,
            unclassified_records=unclassified,
            ledger_rows=total_ledger,
            classified_rows=classified,
            audit_alerts=audit_count,
            certification_status=cs,
            marketplace_health_score=round(health, 2),
            timestamp=datetime.now().isoformat(),
            marketplace=mp,
            period=period_label,
        )

    def collect_all_marketplaces(self, periodo: str | None = None) -> dict[str, FinancialMetricsSnapshot]:
        """Collect metrics for each marketplace individually."""
        results = {}
        for mp in ["ML", "PARIS", "RIPLEY", "FALABELLA"]:
            results[mp] = self.collect(mp, periodo)
        results["ALL"] = self.collect(None, periodo)
        return results

    def _compute_health_score(
        self,
        delta: float,
        taxonomy_cov: float,
        document_cov: float,
        orphans: int,
        unclassified: int,
        audit_alerts: int,
    ) -> float:
        """Compute a 0-100 health score from weighted sub-scores.

        Weights:
          - reconciliation delta (35%): 100 - normalized_delta
          - taxonomy coverage  (25%): taxonomy_cov
          - document coverage  (20%): document_cov
          - unclassified       (10%): 100 - normalized_uncl
          - orphans            (5%):  100 - normalized_orphans
          - audit alerts       (5%):  100 - normalized_audit
        """
        norm_delta = max(0, 100 - min(delta / 100000, 100))
        norm_uncl = max(0, 100 - unclassified) if unclassified <= 100 else 0
        norm_orphans = max(0, 100 - orphans) if orphans <= 100 else 0
        norm_audit = max(0, 100 - min(audit_alerts / 1000, 100))

        score = (
            0.35 * norm_delta
            + 0.25 * taxonomy_cov
            + 0.20 * document_cov
            + 0.10 * norm_uncl
            + 0.05 * norm_orphans
            + 0.05 * norm_audit
        )
        return max(0, min(100, score))
