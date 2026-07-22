"""
explainability_engine.py — Explain any KPI with components, formula, movements, origin, reconciliation, certification.

Each explanation includes: what it is, how it's calculated, what it includes/excludes,
period movement, source of truth, certification status, and drill-down query.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from engine.v4.database import DatabaseV4
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.certification import CertificationEngine
from engine.v4.lineage import LineageEngine


KPI_CATALOG = {
    "ventas_brutas": {
        "name": "Ventas Brutas",
        "formula": "SUM(monto) WHERE financial_group='ingresos'",
        "definition": "Ventas brutas del período a precio de venta final, antes de devoluciones y costos.",
        "includes": "Todas las transacciones clasificadas como ingresos en el período.",
        "excludes": "Devoluciones, costos operacionales, costos comerciales, ajustes.",
        "source": "marketplace_ledger_clasificado_v1.financial_group='ingresos' — certified Single Financial Truth",
        "sql": "SELECT marketplace, periodo, SUM(monto) as ventas FROM marketplace_ledger_clasificado_v1 WHERE financial_group='ingresos' GROUP BY marketplace, periodo",
    },
    "devoluciones": {
        "name": "Devoluciones",
        "formula": "SUM(monto) WHERE financial_group='devoluciones' (monto is negative)",
        "definition": "Devoluciones de productos, notas de crédito y ajustes de devolución del período.",
        "includes": "Devoluciones de clientes, notas de crédito emitidas, ajustes por devolución.",
        "excludes": "Ingresos, costos operacionales, costos comerciales, ajustes no relacionados.",
        "source": "marketplace_ledger_clasificado_v1.financial_group='devoluciones' — certified Single Financial Truth",
        "sql": "SELECT marketplace, periodo, SUM(monto) as devoluciones FROM marketplace_ledger_clasificado_v1 WHERE financial_group='devoluciones' GROUP BY marketplace, periodo",
    },
    "margen_bruto": {
        "name": "Margen Bruto",
        "formula": "Ventas Brutas + Devoluciones + Costos Logísticos + Costos Marketplace",
        "definition": "Resultado neto después de deducir devoluciones y costos de las ventas brutas.",
        "includes": "Ventas brutas, devoluciones (negativas), costos logísticos y costos marketplace.",
        "excludes": "Ajustes no operacionales, treasury items.",
        "source": "Derivado de marketplace_ledger_clasificado_v1 — certified via ReconciliationEngine",
        "sql": "",
    },
    "resultado_neto": {
        "name": "Resultado Neto (Disponible)",
        "formula": "SUM(resultado_neto) FROM marketplace_cierre_financiero_v1",
        "definition": "Resultado financiero final después de todos los conceptos. Es el 'cash final' del período.",
        "includes": "Todos los conceptos financieros netos: ingresos - devoluciones - costos + ajustes.",
        "excludes": "N/A — es el resultado integral del período.",
        "source": "marketplace_cierre_financiero_v1.resultado_neto — certified Single Financial Truth",
        "sql": "SELECT marketplace, periodo_inicio, SUM(resultado_neto) as neto FROM marketplace_cierre_financiero_v1 GROUP BY marketplace, periodo_inicio ORDER BY periodo_inicio",
    },
    "costo_logistico": {
        "name": "Costo Logístico",
        "formula": "SUM(monto) WHERE financial_group='costos_operacionales'",
        "definition": "Costos de logística y operación: despacho, almacenaje, fulfillment, others.",
        "includes": "Costos de despacho, costo de almacenaje, fulfillment, costos operacionales directos.",
        "excludes": "Costos comerciales, publicidad, comisiones, ajustes.",
        "source": "marketplace_ledger_clasificado_v1.financial_group='costos_operacionales'",
        "sql": "SELECT marketplace, periodo, SUM(monto) as costo_logistico FROM marketplace_ledger_clasificado_v1 WHERE financial_group='costos_operacionales' GROUP BY marketplace, periodo",
    },
    "ajustes": {
        "name": "Ajustes & Conciliaciones",
        "formula": "SUM(monto) WHERE financial_group='ajustes'",
        "definition": "Ajustes contables, conciliaciones, reclamos, chargebacks, y otros movimientos no operacionales.",
        "includes": "Ajustes, reclamos (claims), chargebacks, conciliaciones, bonificaciones, penalidades.",
        "excludes": "Ingresos operacionales, devoluciones, costos operacionales/comerciales.",
        "source": "marketplace_ledger_clasificado_v1.financial_group='ajustes'",
        "sql": "SELECT marketplace, periodo, SUM(monto) as ajustes FROM marketplace_ledger_clasificado_v1 WHERE financial_group='ajustes' GROUP BY marketplace, periodo",
    },
}


class ExplainabilityEngine:
    """Explain any financial KPI with full traceability."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self.fe = FinancialEngine(self.db)
        self.cert = CertificationEngine(self.db)
        self.lineage = LineageEngine(self.db)

    def explain(self, kpi: str, marketplace: str, periodo: str | None = None) -> dict[str, Any] | None:
        kpi = kpi.lower().replace(" ", "_")
        if kpi not in KPI_CATALOG:
            return None

        meta = KPI_CATALOG[kpi]
        mp = marketplace.upper()
        period_label = periodo or "YTD"

        # Compute the current value
        current_value = self._compute_kpi(kpi, mp, periodo)

        # Get previous period value
        prev_value = self._compute_kpi(kpi, mp, self._prev_period(periodo))

        # Get certification for this KPI
        try:
            cert = self.cert.certify(mp, periodo)
            cert_status = next(
                (c.status for c in cert.claims if c.kpi and kpi in c.kpi.lower().replace(" ", "_")),
                "PENDIENTE"
            )
            cert_detail = cert.status
        except Exception:
            cert_status = "PENDIENTE"
            cert_detail = "Certification engine unavailable"

        # Get reconciliation status
        try:
            from engine.v4.reconciliation import ReconciliationEngine
            recon = ReconciliationEngine(self.db)
            r = recon.validate_marketplace_consistency(mp, periodo)
            recon_status = f"Delta=${r.delta:,.2f} ({r.certification_status})"
        except Exception:
            recon_status = "PENDIENTE"

        # Sample transactions for drill-down
        drill_sql = self._drill_sql(kpi, mp, periodo)
        drill_samples = []
        if drill_sql:
            drill_df = self.db.query(drill_sql)
            if drill_df is not None and not drill_df.empty:
                for _, row in drill_df.iterrows():
                    drill_samples.append({k: str(v) for k, v in row.to_dict().items()})

        return {
            "kpi": kpi,
            "name": meta["name"],
            "marketplace": mp,
            "period": period_label,
            "current_value": round(current_value, 2),
            "previous_value": round(prev_value, 2),
            "variation": round(current_value - prev_value, 2),
            "variation_pct": f"{((current_value - prev_value) / max(abs(prev_value), 1)) * 100:.1f}%" if prev_value != 0 else "N/A",
            "definition": meta["definition"],
            "formula": meta["formula"],
            "includes": meta["includes"],
            "excludes": meta["excludes"],
            "source_of_truth": meta["source"],
            "reconciliation": recon_status,
            "certification": cert_status,
            "certification_detail": cert_detail,
            "sql_query": meta["sql"],
            "drill_samples": drill_samples[:10],
        }

    def _compute_kpi(self, kpi: str, mp: str, periodo: str | None) -> float:
        if kpi == "ventas_brutas":
            return self._sum_ledger("ingresos", mp, periodo)
        elif kpi == "devoluciones":
            return self._sum_ledger("devoluciones", mp, periodo)
        elif kpi == "margen_bruto":
            v = self._sum_ledger("ingresos", mp, periodo)
            d = self._sum_ledger("devoluciones", mp, periodo)
            cl = self._sum_ledger("costos_operacionales", mp, periodo)
            cm = self._sum_ledger("costos_comerciales", mp, periodo)
            a = self._sum_ledger("ajustes", mp, periodo)
            return v + d + cl + cm + a
        elif kpi == "resultado_neto":
            sql = "SELECT COALESCE(SUM(COALESCE(resultado_neto, 0)), 0) as t FROM marketplace_cierre_financiero_v1 WHERE marketplace=?"
            if periodo:
                y, m = map(int, periodo.split("-"))
                sql += " AND periodo_inicio >= ?"
                df = self.db.query(sql, [mp, f"{y}-{m:02d}-01"])
            else:
                df = self.db.query(sql, [mp])
            return float(df.iloc[0]["t"]) if not df.empty else 0
        elif kpi == "costo_logistico":
            return self._sum_ledger("costos_operacionales", mp, periodo)
        elif kpi == "ajustes":
            return self._sum_ledger("ajustes", mp, periodo)
        return 0

    def _sum_ledger(self, group: str, mp: str, periodo: str | None) -> float:
        sql = "SELECT COALESCE(SUM(COALESCE(monto, 0)), 0) as t FROM marketplace_ledger_clasificado_v1 WHERE financial_group=? AND COALESCE(include_in_operational_pnl,1)=1 AND marketplace=?"
        if periodo:
            y, m = map(int, periodo.split("-"))
            import calendar
            last = calendar.monthrange(y, m)[1]
            sql += " AND fecha BETWEEN ? AND ?"
            df = self.db.query(sql, [group, mp, f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last}"])
        else:
            df = self.db.query(sql, [group, mp])
        return float(df.iloc[0]["t"]) if not df.empty else 0

    def _prev_period(self, periodo: str | None) -> str | None:
        if not periodo or periodo.upper() == "YTD":
            return None
        y, m = map(int, periodo.split("-"))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
        return f"{y}-{m:02d}"

    def _drill_sql(self, kpi: str, mp: str, periodo: str | None) -> str:
        group_map = {
            "ventas_brutas": "ingresos",
            "devoluciones": "devoluciones",
            "costo_logistico": "costos_operacionales",
            "ajustes": "ajustes",
        }
        g = group_map.get(kpi)
        if not g:
            return ""
        sql = f"""SELECT l.id_transaccion, l.detalle, l.monto, l.fecha, l.archivo_origen, l.folio_xml FROM marketplace_ledger_v1 l WHERE l.financial_group='{g}' AND l.marketplace='{mp}' AND COALESCE(l.include_in_operational_pnl,1)=1"""
        if periodo:
            y, m = map(int, periodo.split("-"))
            import calendar
            last = calendar.monthrange(y, m)[1]
            sql += f" AND fecha BETWEEN '{y}-{m:02d}-01' AND '{y}-{m:02d}-{last}'"
        sql += " LIMIT 20"
        return sql
