"""
operational_insights.py — SQL-based operational insights.

Every insight includes: evidence SQL, row count, financial impact.
No LLM, no mock data, no placeholders.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from engine.v4.database import DatabaseV4


@dataclass
class OperationalInsight:
    title: str
    description: str
    impact_amount: float
    record_count: int
    sql_query: str
    evidence: str
    insight_type: str = "trend"


@dataclass
class OperationalInsightsReport:
    marketplace: str
    period: str
    insights: list[OperationalInsight] = field(default_factory=list)
    total_insights: int = 0


class OperationalInsights:
    """SQL-based operational insights generator.

    All queries deterministic. No LLM. No mock data.
    """

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()

    def analyze(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
    ) -> OperationalInsightsReport:
        """Generate operational insights for a marketplace/period."""
        mp = marketplace.upper() if marketplace else "ALL"
        period_label = periodo or "YTD"
        insights: list[OperationalInsight] = []

        # Insight 1: Top operational cost drivers
        insights.append(self._top_cost_drivers(mp, periodo))

        # Insight 2: Period-over-period change in operational P&L
        insights.append(self._period_change(mp, periodo))

        # Insight 3: Tax impact
        insights.append(self._tax_impact(mp, periodo))

        # Insight 4: Returns as % of gross sales
        insights.append(self._return_rate(mp, periodo))

        return OperationalInsightsReport(
            marketplace=mp,
            period=period_label,
            insights=[i for i in insights if i is not None],
            total_insights=len(insights),
        )

    def _top_cost_drivers(self, marketplace: str, periodo: str | None) -> OperationalInsight | None:
        """Top 5 cost drivers by financial group."""
        mp_filter = "AND marketplace = ?" if marketplace != "ALL" else ""
        mp_params = [marketplace] if marketplace != "ALL" else []

        date_sql, date_params = self._date_clause(periodo)

        sql = f"""
            SELECT financial_group, SUM(COALESCE(monto, 0)) as total
            FROM marketplace_ledger_clasificado_v1
            WHERE financial_group IN ('costos_operacionales', 'costos_comerciales')
              {mp_filter}
              {date_sql}
            GROUP BY financial_group
            ORDER BY total ASC
        """
        params = mp_params + date_params
        df = self.db.query(sql, params)

        if df.empty:
            return None

        total_cost = sum(float(r["total"]) for _, r in df.iterrows())
        groups = [f"{r['financial_group']}={float(r['total']):.2f}" for _, r in df.iterrows()]

        return OperationalInsight(
            title="Top Cost Drivers",
            description=f"Operational costs total ${abs(total_cost):,.2f} across {len(groups)} groups: {', '.join(groups)}",
            impact_amount=abs(total_cost),
            record_count=len(df),
            sql_query=sql,
            evidence=f"Total cost: ${abs(total_cost):,.2f}, Groups: {', '.join(groups)}",
            insight_type="cost_analysis",
        )

    def _period_change(self, marketplace: str, periodo: str | None) -> OperationalInsight | None:
        """Period-over-period change in operational P&L."""
        if not periodo or periodo.upper() == "YTD":
            return OperationalInsight(
                title="Period Comparison",
                description="YTD period: no previous period available for comparison.",
                impact_amount=0, record_count=0, sql_query="N/A",
                evidence="YTD period selected; comparison requires specific month.",
                insight_type="period_change",
            )

        y, m = map(int, periodo.split("-"))
        prev_m = 12 if m == 1 else m - 1
        prev_y = y - 1 if m == 1 else y
        prev_periodo = f"{prev_y}-{prev_m:02d}"
        prev_label = f"{prev_y}-{prev_m:02d}"

        import calendar
        cur_start = f"{y}-{m:02d}-01"
        cur_end = f"{y}-{m:02d}-{calendar.monthrange(y, m)[1]}"
        prev_start = f"{prev_y}-{prev_m:02d}-01"
        prev_end = f"{prev_y}-{prev_m:02d}-{calendar.monthrange(prev_y, prev_m)[1]}"

        mp_filter = "AND marketplace = ?" if marketplace != "ALL" else ""
        mp = [marketplace] if marketplace != "ALL" else []

        sql_cur = f"""
            SELECT COALESCE(SUM(COALESCE(monto, 0)), 0) as total
            FROM marketplace_ledger_clasificado_v1
            WHERE fecha BETWEEN ? AND ?
              AND COALESCE(include_in_operational_pnl, 1) = 1
              {mp_filter}
        """
        sql_prev = sql_cur

        cur_total = float(self.db.query(sql_cur, [cur_start, cur_end] + mp).iloc[0]["total"])
        prev_total = float(self.db.query(sql_prev, [prev_start, prev_end] + mp).iloc[0]["total"])

        change = cur_total - prev_total
        pct = (change / prev_total * 100) if prev_total != 0 else 0

        return OperationalInsight(
            title="Period P&L Change",
            description=f"Operational P&L went from ${prev_total:,.2f} ({prev_label}) to ${cur_total:,.2f} (current). Change: ${change:,.2f} ({pct:+.1f}%)",
            impact_amount=change,
            record_count=2,
            sql_query=sql_cur,
            evidence=f"Previous: ${prev_total:,.2f}, Current: ${cur_total:,.2f}, Delta: ${change:,.2f} ({pct:+.1f}%)",
            insight_type="period_change",
        )

    def _tax_impact(self, marketplace: str, periodo: str | None) -> OperationalInsight | None:
        """Total tax impact."""
        mp_filter = "AND marketplace = ?" if marketplace != "ALL" else ""
        mp_params = [marketplace] if marketplace != "ALL" else []
        date_sql, date_params = self._date_clause(periodo)

        sql = f"""
            SELECT COALESCE(SUM(COALESCE(monto, 0)), 0) as total
            FROM marketplace_ledger_clasificado_v1
            WHERE financial_group = 'impuestos'
              {mp_filter}
              {date_sql}
        """
        df = self.db.query(sql, mp_params + date_params)
        total_tax = float(df.iloc[0]["total"]) if not df.empty else 0

        if total_tax == 0:
            return None

        return OperationalInsight(
            title="Tax Impact",
            description=f"Total tax impact: ${abs(total_tax):,.2f}",
            impact_amount=abs(total_tax),
            record_count=1,
            sql_query=sql,
            evidence=f"Tax total: ${abs(total_tax):,.2f}",
            insight_type="tax_analysis",
        )

    def _return_rate(self, marketplace: str, periodo: str | None) -> OperationalInsight | None:
        """Returns as % of gross sales."""
        mp_filter = "AND marketplace = ?" if marketplace != "ALL" else ""
        mp_params = [marketplace] if marketplace != "ALL" else []
        date_sql, date_params = self._date_clause(periodo)

        sql = f"""
            SELECT 
                COALESCE(SUM(CASE WHEN financial_group = 'ingresos' THEN COALESCE(monto, 0) ELSE 0 END), 0) as gross,
                COALESCE(SUM(CASE WHEN financial_group = 'devoluciones' THEN COALESCE(monto, 0) ELSE 0 END), 0) as returns
            FROM marketplace_ledger_clasificado_v1
            WHERE COALESCE(include_in_operational_pnl, 1) = 1
              {mp_filter}
              {date_sql}
        """
        df = self.db.query(sql, mp_params + date_params)
        if df.empty:
            return None

        gross = float(df.iloc[0]["gross"])
        returns = float(df.iloc[0]["returns"])
        rate = (abs(returns) / abs(gross) * 100) if gross != 0 else 0

        return OperationalInsight(
            title="Return Rate",
            description=f"Returns represent {rate:.1f}% of gross sales (${abs(returns):,.2f} returns on ${abs(gross):,.2f} sales)",
            impact_amount=abs(returns),
            record_count=1,
            sql_query=sql,
            evidence=f"Gross: ${abs(gross):,.2f}, Returns: ${abs(returns):,.2f}, Rate: {rate:.1f}%",
            insight_type="return_analysis",
        )

    def _date_clause(self, periodo: str | None) -> tuple[str, list]:
        if not periodo or periodo.upper() == "YTD":
            return "", []
        y, m = map(int, periodo.split("-"))
        import calendar
        last = calendar.monthrange(y, m)[1]
        return "AND fecha BETWEEN ? AND ?", [f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last}"]
