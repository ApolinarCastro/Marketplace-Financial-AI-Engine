"""
return_reasons.py — Decomposition of devoluciones by detalle/reason.

SQL-only analysis. Every metric is traceable to ledger rows.
No LLM. No placeholders.
"""
from __future__ import annotations
from dataclasses import dataclass, field

from engine.v4.database import DatabaseV4


@dataclass
class ReturnReason:
    reason: str
    total_amount: float
    case_count: int
    participation_pct: float
    transaction_count: int


@dataclass
class ReturnAnalysisReport:
    marketplace: str
    period: str
    total_returns: float
    total_cases: int
    reasons: list[ReturnReason] = field(default_factory=list)
    top_reason: str = ""
    sql_query: str = ""


class ReturnReasonAnalyzer:
    """Analyze return reasons from ledger data."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()

    def analyze(
        self,
        marketplace: str | None = None,
        periodo: str | None = None,
    ) -> ReturnAnalysisReport:
        mp = marketplace.upper() if marketplace else "ALL"
        period_label = periodo or "YTD"

        mp_filter = "AND marketplace = ?" if mp != "ALL" else ""
        mp_params = [mp] if mp != "ALL" else []

        date_sql, date_params = self._date_clause(periodo)

        sql = f"""
            SELECT detalle, COUNT(*) as casos, SUM(COALESCE(monto, 0)) as total_monto,
                   SUM(COUNT(*)) OVER () as total_casos,
                   SUM(SUM(COALESCE(monto, 0))) OVER () as gran_total
            FROM marketplace_ledger_clasificado_v1
            WHERE financial_group = 'devoluciones'
              {mp_filter}
              {date_sql}
            GROUP BY detalle
            ORDER BY total_monto ASC
        """
        params = mp_params + date_params
        df = self.db.query(sql, params)

        reasons = []
        gran_total = float(df.iloc[0]["gran_total"]) if not df.empty else 0
        total_casos = int(df.iloc[0]["total_casos"]) if not df.empty else 0

        for _, r in df.iterrows():
            amount = float(r["total_monto"])
            cases = int(r["casos"])
            pct = (abs(amount) / abs(gran_total) * 100) if gran_total != 0 else 0
            reasons.append(ReturnReason(
                reason=str(r["detalle"]),
                total_amount=amount,
                case_count=cases,
                participation_pct=round(pct, 1),
                transaction_count=cases,
            ))

        top = reasons[0].reason if reasons else ""

        return ReturnAnalysisReport(
            marketplace=mp,
            period=period_label,
            total_returns=gran_total,
            total_cases=total_casos,
            reasons=reasons,
            top_reason=top,
            sql_query=sql,
        )

    def _date_clause(self, periodo: str | None) -> tuple[str, list]:
        if not periodo or periodo.upper() == "YTD":
            return "", []
        y, m = map(int, periodo.split("-"))
        import calendar
        last = calendar.monthrange(y, m)[1]
        return "AND fecha BETWEEN ? AND ?", [f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last}"]
