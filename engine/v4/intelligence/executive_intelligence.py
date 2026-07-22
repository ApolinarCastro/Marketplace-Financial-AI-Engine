"""executive_intelligence.py — Executive intelligence layer.

SQL-based executive insights: risks, opportunities, drivers, contributions, coverage.
No LLM, no mock data, no placeholders. Every insight traces to marketplace_ledger_v1.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from engine.v4.database import DatabaseV4


@dataclass
class ExecutiveInsight:
    title: str
    description: str
    impact_amount: float
    detail: str
    marketplaces: list[str]
    insight_type: str  # risk / opportunity / driver / contribution / coverage / summary


@dataclass
class ExecutiveIntelligenceReport:
    marketplace: str
    period: str
    insights: list[ExecutiveInsight] = field(default_factory=list)
    total_insights: int = 0
    executive_summary: str = ""


class ExecutiveIntelligence:
    """SQL-based executive intelligence generator.

    Generates top risk, top opportunity, principal driver,
    marketplace contribution, coverage analysis, and executive summary.
    """

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()

    def analyze(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
    ) -> ExecutiveIntelligenceReport:
        mp = marketplace.upper() if marketplace else "ALL"
        period_label = periodo or "YTD"
        insights: list[ExecutiveInsight] = []

        insights.append(self._top_risk(mp, periodo))
        insights.append(self._top_opportunity(mp, periodo))
        insights.append(self._principal_driver(mp, periodo))
        insights.append(self._marketplace_contribution(mp, periodo))
        insights.append(self._coverage_analysis(mp, periodo))

        valid = [i for i in insights if i is not None]
        summary = self._build_summary(valid, mp, period_label)

        return ExecutiveIntelligenceReport(
            marketplace=mp,
            period=period_label,
            insights=valid,
            total_insights=len(valid),
            executive_summary=summary,
        )

    def _date_clause(self, periodo: str | None) -> tuple[str, list]:
        if not periodo or periodo.upper() == "YTD":
            return "", []
        y, m = map(int, periodo.split("-"))
        import calendar
        last = calendar.monthrange(y, m)[1]
        return "AND l.fecha BETWEEN ? AND ?", [f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last}"]

    def _mp_filter(self, marketplace: str) -> tuple[str, list]:
        if marketplace != "ALL":
            return "AND LOWER(l.marketplace) = ?", [marketplace.lower()]
        return "", []

    def _top_risk(self, marketplace: str, periodo: str | None) -> ExecutiveInsight | None:
        """Identify the largest financial risk — highest negative-impact group."""
        date_sql, date_params = self._date_clause(periodo)
        mp_sql, mp_params = self._mp_filter(marketplace)

        df = self.db.query(f"""
            SELECT LOWER(l.financial_group) as fg,
                   SUM(l.monto) as total,
                   COUNT(*) as cnt
            FROM marketplace_ledger_v1 l
            WHERE COALESCE(l.include_in_operational_pnl, 1) = 1
              AND l.financial_group IS NOT NULL
              {date_sql}
              {mp_sql}
            GROUP BY fg
            ORDER BY ABS(SUM(l.monto)) ASC
            LIMIT 5
        """, date_params + mp_params)

        if df.empty:
            return None

        # Largest negative is the top risk
        neg = df[df['total'] < 0].sort_values('total')
        if neg.empty:
            return ExecutiveInsight(
                title="No Financial Risks Detected",
                description="All financial groups have positive balances.",
                impact_amount=0, detail="No negative groups found.",
                marketplaces=[marketplace] if marketplace != "ALL" else [],
                insight_type="risk",
            )

        top = neg.iloc[0]
        fg = str(top['fg'])
        total = float(top['total'])
        fg_pct = abs(total) / max(abs(float(df['total'].sum())), 1) * 100

        return ExecutiveInsight(
            title=f"Top Risk: {fg}",
            description=f"{fg} represents ${abs(total):,.2f} ({fg_pct:.1f}% of net) — highest cost center.",
            impact_amount=abs(total),
            detail=f"{fg}: ${abs(total):,.2f} across {int(top['cnt'])} transactions ({fg_pct:.1f}% of P&L)",
            marketplaces=[marketplace] if marketplace != "ALL" else list(df['fg'].unique()),
            insight_type="risk",
        )

    def _top_opportunity(self, marketplace: str, periodo: str | None) -> ExecutiveInsight | None:
        """Identify the largest positive-impact adjustment or recovery."""
        date_sql, date_params = self._date_clause(periodo)
        mp_sql, mp_params = self._mp_filter(marketplace)

        df = self.db.query(f"""
            SELECT LOWER(l.financial_group) as fg,
                   SUM(l.monto) as total,
                   COUNT(*) as cnt
            FROM marketplace_ledger_v1 l
            WHERE COALESCE(l.include_in_operational_pnl, 1) = 1
              AND l.financial_group IS NOT NULL
              AND LOWER(l.financial_group) IN ('recuperaciones_y_bonificaciones', 'ajustes')
              AND l.monto > 0
              {date_sql}
              {mp_sql}
            GROUP BY fg
            ORDER BY SUM(l.monto) DESC
            LIMIT 3
        """, date_params + mp_params)

        if df.empty:
            return None

        top = df.iloc[0]
        total = float(top['total'])
        fg = str(top['fg'])

        return ExecutiveInsight(
            title=f"Top Opportunity: {fg}",
            description=f"Positive recoveries of ${total:,.2f} from {int(top['cnt'])} transactions.",
            impact_amount=total,
            detail=f"{fg}: ${total:,.2f} positive impact ({int(top['cnt'])} transactions)",
            marketplaces=[marketplace] if marketplace != "ALL" else [],
            insight_type="opportunity",
        )

    def _principal_driver(self, marketplace: str, periodo: str | None) -> ExecutiveInsight | None:
        """Identify the principal P&L driver (largest revenue contributor)."""
        date_sql, date_params = self._date_clause(periodo)
        mp_sql, mp_params = self._mp_filter(marketplace)

        df = self.db.query(f"""
            SELECT l.detalle,
                   SUM(l.monto) as total,
                   COUNT(*) as cnt
            FROM marketplace_ledger_v1 l
            WHERE COALESCE(l.include_in_operational_pnl, 1) = 1
              AND l.monto > 0
              {date_sql}
              {mp_sql}
            GROUP BY l.detalle
            ORDER BY SUM(l.monto) DESC
            LIMIT 1
        """, date_params + mp_params)

        if df.empty:
            return None

        top = df.iloc[0]
        total = float(top['total'])
        detalle = str(top['detalle'])

        # Total ingresos for percentage
        ing_df = self.db.query(f"""
            SELECT COALESCE(SUM(l.monto), 0) as total
            FROM marketplace_ledger_v1 l
            WHERE COALESCE(l.include_in_operational_pnl, 1) = 1
              AND LOWER(l.financial_group) = 'ingresos'
              AND l.monto > 0
              {date_sql}
              {mp_sql}
        """, date_params + mp_params)

        ing_total = float(ing_df.iloc[0]['total']) if not ing_df.empty else 1
        pct = total / ing_total * 100 if ing_total > 0 else 0

        return ExecutiveInsight(
            title=f"Principal Driver: {detalle}",
            description=f"{detalle} generates ${total:,.2f} ({pct:.1f}% of gross revenue).",
            impact_amount=total,
            detail=f"{detalle}: ${total:,.2f} across {int(top['cnt'])} orders ({pct:.1f}% of revenue)",
            marketplaces=[marketplace] if marketplace != "ALL" else [],
            insight_type="driver",
        )

    def _marketplace_contribution(self, marketplace: str, periodo: str | None) -> ExecutiveInsight | None:
        """Analyze each marketplace's contribution to total P&L."""
        if marketplace != "ALL":
            return None  # Only for consolidated view

        date_sql, date_params = self._date_clause(periodo)

        df = self.db.query(f"""
            SELECT LOWER(l.marketplace) as mp,
                   SUM(l.monto) as neto,
                   COUNT(*) as cnt
            FROM marketplace_ledger_v1 l
            WHERE COALESCE(l.include_in_operational_pnl, 1) = 1
              AND l.financial_group IS NOT NULL
              {date_sql}
            GROUP BY mp
            ORDER BY SUM(l.monto) DESC
        """, date_params)

        if df.empty:
            return None

        total_neto = float(df['neto'].sum())
        contributions = []
        for _, r in df.iterrows():
            mp = str(r['mp']).upper()
            neto = float(r['neto'])
            pct = abs(neto) / abs(total_neto) * 100 if total_neto != 0 else 0
            contributions.append(f"{mp}={neto:,.2f} ({pct:.1f}%)")

        top_mp = df.iloc[0]
        top_name = str(top_mp['mp']).upper()
        top_value = float(top_mp['neto'])
        top_pct = abs(top_value) / abs(total_neto) * 100 if total_neto != 0 else 0

        return ExecutiveInsight(
            title=f"Top MP: {top_name}",
            description=f"{top_name} contributes ${top_value:,.2f} ({top_pct:.1f}% of total P&L).",
            impact_amount=top_value,
            detail=" | ".join(contributions),
            marketplaces=list(df['mp'].str.upper().unique()),
            insight_type="contribution",
        )

    def _coverage_analysis(self, marketplace: str, periodo: str | None) -> ExecutiveInsight | None:
        """Documentary coverage analysis."""
        date_sql, date_params = self._date_clause(periodo)
        mp_sql, mp_params = self._mp_filter(marketplace)

        df = self.db.query(f"""
            SELECT LOWER(l.marketplace) as mp,
                   COUNT(*) as total_rows,
                   SUM(CASE WHEN l.folio_xml IS NOT NULL THEN 1 ELSE 0 END) as with_xml
            FROM marketplace_ledger_v1 l
            WHERE COALESCE(l.include_in_operational_pnl, 1) = 1
              {date_sql}
              {mp_sql}
            GROUP BY mp
            ORDER BY mp
        """, date_params + mp_params)

        if df.empty:
            return None

        total_all = int(df['total_rows'].sum())
        total_xml = int(df['with_xml'].sum())
        cov = total_xml / total_all * 100 if total_all > 0 else 0

        details = []
        for _, r in df.iterrows():
            mp = str(r['mp']).upper()
            t = int(r['total_rows'])
            x = int(r['with_xml'])
            c = x / t * 100 if t > 0 else 0
            details.append(f"{mp}: {c:.1f}% ({x}/{t})")

        return ExecutiveInsight(
            title="Documentary Coverage",
            description=f"Overall DTE coverage: {cov:.1f}% ({total_xml}/{total_all} rows with folio_xml).",
            impact_amount=cov,
            detail=" | ".join(details),
            marketplaces=[marketplace] if marketplace != "ALL" else list(df['mp'].str.upper().unique()),
            insight_type="coverage",
        )

    def _build_summary(self, insights: list[ExecutiveInsight], marketplace: str, period: str) -> str:
        """Build an executive summary narrative from all insights."""
        if not insights:
            return f"No intelligence data for {marketplace} period {period}."

        lines = [f"Executive Summary — {marketplace} | {period}"]
        for ins in insights:
            lines.append(f"  • {ins.title}: {ins.description}")

        return "\n".join(lines)
