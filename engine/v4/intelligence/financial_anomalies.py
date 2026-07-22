"""
financial_anomalies.py — SQL-based anomaly detection.

Detects: delta spikes, coverage drops, sudden changes in audit volume.
Every anomaly includes SQL evidence and financial impact.
"""
from __future__ import annotations
from dataclasses import dataclass, field

from engine.v4.database import DatabaseV4
from engine.v4.reconciliation.reconciliation_engine import ReconciliationEngine


@dataclass
class FinancialAnomaly:
    anomaly_type: str
    severity: str  # ALTA|MEDIA|BAJA
    description: str
    impact_amount: float
    record_count: int
    sql_query: str
    evidence: str


@dataclass
class AnomalyReport:
    marketplace: str
    period: str
    anomalies: list[FinancialAnomaly] = field(default_factory=list)
    total_anomalies: int = 0
    total_impact: float = 0.0


class FinancialAnomalyDetector:
    """Detect financial anomalies from certified sources."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self.recon = ReconciliationEngine(self.db)

    def detect(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
    ) -> AnomalyReport:
        mp = marketplace.upper() if marketplace else "ALL"
        period_label = periodo or "YTD"
        anomalies: list[FinancialAnomaly] = []

        # Anomaly 1: Reconciliation delta exceeds threshold
        anomalies.extend(self._check_reconciliation_delta(mp, periodo))

        # Anomaly 2: Unclassified records
        anomalies.append(self._check_unclassified(mp, periodo))

        # Anomaly 3: Orphan records
        anomalies.append(self._check_orphans(mp, periodo))

        # Anomaly 4: Zero revenue (possible data gap)
        anomalies.append(self._check_zero_revenue(mp, periodo))

        anomalies = [a for a in anomalies if a is not None]
        total_impact = sum(a.impact_amount for a in anomalies)

        return AnomalyReport(
            marketplace=mp,
            period=period_label,
            anomalies=anomalies,
            total_anomalies=len(anomalies),
            total_impact=round(total_impact, 2),
        )

    def _check_reconciliation_delta(self, mp: str, periodo: str | None) -> list[FinancialAnomaly]:
        result = []
        if mp == "ALL":
            return result

        recon = self.recon.validate_marketplace_consistency(mp, periodo)
        if recon.delta > 1000:
            result.append(FinancialAnomaly(
                anomaly_type="CRITICAL_DELTA",
                severity="ALTA",
                description=f"Reconciliation delta ${recon.delta:,.2f} exceeds critical threshold",
                impact_amount=recon.delta,
                record_count=1,
                sql_query="ReconciliationEngine.validate_marketplace_consistency()",
                evidence=f"Delta=${recon.delta:,.2f}, Status={recon.certification_status}",
            ))
        elif recon.delta > 1:
            result.append(FinancialAnomaly(
                anomaly_type="ELEVATED_DELTA",
                severity="MEDIA",
                description=f"Reconciliation delta ${recon.delta:,.2f} above allowed threshold",
                impact_amount=recon.delta,
                record_count=1,
                sql_query="ReconciliationEngine.validate_marketplace_consistency()",
                evidence=f"Delta=${recon.delta:,.2f}",
            ))
        return result

    def _check_unclassified(self, mp: str, periodo: str | None) -> FinancialAnomaly | None:
        mp_filter = "AND marketplace = ?" if mp != "ALL" else ""
        mp_params = [mp] if mp != "ALL" else []
        date_sql, date_params = self._date_clause(periodo)

        sql = f"""
            SELECT COUNT(*) as n
            FROM marketplace_ledger_clasificado_v1
            WHERE (financial_group IS NULL OR financial_group = '')
              {mp_filter}
              {date_sql}
        """
        df = self.db.query(sql, mp_params + date_params)
        n = int(df.iloc[0]["n"]) if not df.empty else 0

        if n > 0:
            return FinancialAnomaly(
                anomaly_type="UNCLASSIFIED_RECORDS",
                severity="ALTA" if n > 100 else "MEDIA",
                description=f"{n} records without financial_group classification",
                impact_amount=float(n),
                record_count=n,
                sql_query=sql,
                evidence=f"{n} unclassified records found",
            )
        return None

    def _check_orphans(self, mp: str, periodo: str | None) -> FinancialAnomaly | None:
        # Build params in SQL order: date_join ? first, then mp_filter ?
        date_sql, date_params = self._date_clause(periodo)
        params: list = list(date_params)

        mp_filter = ""
        mp_params_list: list = []
        if mp != "ALL":
            mp_filter = " AND d.marketplace = ?"
            mp_params_list = [mp]

        # document_match_v1 has no fecha column — use ledger subquery to filter by date
        date_join = f" AND c.fecha BETWEEN ? AND ?" if date_sql else ""

        sql = f"""
            SELECT COUNT(*) as orphans
            FROM document_match_v1 d
            WHERE NOT EXISTS (
                SELECT 1 FROM marketplace_ledger_clasificado_v1 c
                WHERE c.marketplace = d.marketplace AND c.id_transaccion = d.ledger_id
                {date_join}
            )
            {mp_filter}
        """
        params.extend(mp_params_list)
        df = self.db.query(sql, params)
        n = int(df.iloc[0]["orphans"]) if not df.empty else 0

        if n > 0:
            return FinancialAnomaly(
                anomaly_type="ORPHAN_DOCUMENTS",
                severity="ALTA" if n > 100 else "MEDIA",
                description=f"{n} orphan document records without ledger match",
                impact_amount=float(n),
                record_count=n,
                sql_query=sql,
                evidence=f"{n} orphan documents found",
            )
        return None

    def _check_zero_revenue(self, mp: str, periodo: str | None) -> FinancialAnomaly | None:
        mp_filter = "AND marketplace = ?" if mp != "ALL" else ""
        mp_params = [mp] if mp != "ALL" else []
        date_sql, date_params = self._date_clause(periodo)

        sql = f"""
            SELECT COALESCE(SUM(COALESCE(monto, 0)), 0) as total_ingresos
            FROM marketplace_ledger_clasificado_v1
            WHERE financial_group = 'ingresos'
              {mp_filter}
              {date_sql}
        """
        df = self.db.query(sql, mp_params + date_params)
        total = float(df.iloc[0]["total_ingresos"]) if not df.empty else 0

        if total == 0:
            mp_name = mp if mp != "ALL" else "ALL MARKETPLACES"
            return FinancialAnomaly(
                anomaly_type="ZERO_REVENUE",
                severity="ALTA",
                description=f"{mp_name} has $0 revenue for the period — possible data gap",
                impact_amount=0.0,
                record_count=1,
                sql_query=sql,
                evidence=f"Zero ingresos for {mp_name} in period {periodo or 'YTD'}",
            )
        return None

    def _date_clause(self, periodo: str | None) -> tuple[str, list]:
        if not periodo or periodo.upper() == "YTD":
            return "", []
        y, m = map(int, periodo.split("-"))
        import calendar
        last = calendar.monthrange(y, m)[1]
        return "AND fecha BETWEEN ? AND ?", [f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last}"]
