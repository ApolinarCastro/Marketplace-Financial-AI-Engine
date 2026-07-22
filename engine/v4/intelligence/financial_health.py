from typing import Any
from engine.v4.database import DatabaseV4


class FinancialHealth:
    """Integrated Financial Intelligence: answers 'Are we making or losing money?' with full evidence chain."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()

    def get_health(self, marketplace: str | None = None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace)
        latest = self._latest_period()
        if not latest:
            return {"status": "no_data", "answer": "No hay datos financieros disponibles"}

        period_end = latest["periodo_fin"]
        prev_end = self._previous_period_end(period_end)

        current = self._rn_by_period(period_end, mp_filter, mp_params)
        previous = self._rn_by_period(prev_end, mp_filter, mp_params) if prev_end else {}

        total_current = sum(m["rn"] for m in current.values()) if current else 0
        total_previous = sum(m["rn"] for m in previous.values()) if previous else 0
        delta = total_current - total_previous
        delta_pct = (delta / abs(total_previous) * 100) if total_previous != 0 else 0

        evidence = self._build_evidence(period_end, mp_filter, mp_params) if current else []
        explanation = self._explain(total_current, delta, delta_pct, current, previous, str(period_end), str(prev_end) if prev_end else None)
        per_mp = self._per_mp_detail(current, previous)

        return {
            "question": "¿Estoy ganando o perdiendo dinero hoy?",
            "period": str(period_end),
            "previous_period": str(prev_end) if prev_end else None,
            "answer": {
                "status": "profit" if total_current >= 0 else "loss",
                "rn_operacional": round(total_current, 2),
                "previous_rn": round(total_previous, 2),
                "delta": round(delta, 2),
                "delta_pct": round(delta_pct, 2),
                "is_profit": total_current >= 0,
                "summary": f"{'Estás GANANDO' if total_current >= 0 else 'Estás PERDIENDO'} dinero: ${total_current:,.0f}",
            },
            "explanation": explanation,
            "breakdown": per_mp,
            "evidence": evidence,
        }

    def _mp_filter(self, marketplace: str | None) -> tuple[str, list]:
        if marketplace and marketplace.upper() != "ALL":
            return "AND LOWER(c.marketplace) = ?", [marketplace.lower()]
        return "", []

    def _latest_period(self) -> dict | None:
        df = self.db.query("""
            SELECT DISTINCT periodo_fin
            FROM marketplace_cierre_financiero_v1
            WHERE resultado_neto != 0 AND periodo_inicio != '2023-01-01'
              AND LOWER(marketplace) NOT IN ('all')
              AND periodo_inicio <= CURRENT_DATE
            ORDER BY periodo_fin DESC
            LIMIT 1
        """)
        if df.empty:
            return None
        return {"periodo_fin": df.iloc[0]["periodo_fin"]}

    def _previous_period_end(self, current_end) -> Any:
        import datetime
        if isinstance(current_end, str):
            current_end = datetime.date.fromisoformat(current_end)
        df = self.db.query("""
            SELECT DISTINCT periodo_fin
            FROM marketplace_cierre_financiero_v1
            WHERE resultado_neto != 0 AND periodo_inicio != '2023-01-01'
              AND LOWER(marketplace) NOT IN ('all')
              AND periodo_fin < ?
            ORDER BY periodo_fin DESC
            LIMIT 1
        """, [str(current_end)])
        return df.iloc[0]["periodo_fin"] if not df.empty else None

    def _rn_by_period(self, period_end, mp_filter: str, mp_params: list) -> dict[str, dict]:
        import datetime
        if isinstance(period_end, str):
            period_end = datetime.date.fromisoformat(period_end)
        params = [str(period_end)] + mp_params
        sql = f"""
            SELECT LOWER(c.marketplace) as mp, c.resultado_neto as rn
            FROM marketplace_cierre_financiero_v1 c
            WHERE c.periodo_fin = ?
              AND c.resultado_neto != 0
              AND LOWER(c.marketplace) NOT IN ('all')
            {mp_filter}
            ORDER BY c.marketplace
        """
        df = self.db.query(sql, params)
        result = {}
        for _, r in df.iterrows():
            result[r["mp"]] = {"rn": float(r["rn"]), "marketplace": r["mp"]}
        return result

    def _build_evidence(self, period_end, mp_filter: str, mp_params: list) -> list[dict]:
        import datetime
        import math
        if isinstance(period_end, str):
            period_end = datetime.date.fromisoformat(period_end)
        params = [str(period_end)] + mp_params
        df = self.db.query(f"""
            SELECT LOWER(c.marketplace) as mp, c.resultado_neto,
                   c.total_ingresos, c.total_costos_operacionales,
                   c.total_costos_comerciales, c.total_ajustes,
                   c.periodo_inicio
            FROM marketplace_cierre_financiero_v1 c
            WHERE c.periodo_fin = ? AND c.resultado_neto != 0
              AND LOWER(c.marketplace) NOT IN ('all')
            {mp_filter}
            ORDER BY c.marketplace
        """, params)
        evidence = []
        for _, r in df.iterrows():
            mp = r["mp"]
            p_start = r["periodo_inicio"]
            ledger_sample = self._ledger_sample(mp, p_start, period_end)
            raw_files = self._raw_files(ledger_sample) if ledger_sample else []
            etl_info = self._etl_info(mp, p_start, period_end)
            xml_info = self._xml_info(ledger_sample) if ledger_sample else []
            evidence.append({
                "marketplace": mp,
                "kpi": "resultado_neto",
                "value": float(r["resultado_neto"]),
                "source": "marketplace_cierre_financiero_v1",
                "sql": f"SELECT resultado_neto FROM marketplace_cierre_financiero_v1 WHERE LOWER(marketplace)='{mp}' AND periodo_fin='{period_end}'",
                "components": {
                    "ingresos": float(r["total_ingresos"]),
                    "costos_operacionales": float(r["total_costos_operacionales"]),
                    "costos_comerciales": float(r["total_costos_comerciales"]),
                    "ajustes": float(r["total_ajustes"]),
                },
                "ledger_samples": ledger_sample[:3] if ledger_sample else [],
                "raw_sources": raw_files[:3] if raw_files else [],
                "etl": etl_info,
                "xml": xml_info[:3] if xml_info else [],
            })
        return evidence

    def _etl_info(self, mp: str, start, end) -> dict:
        df = self.db.query("""
            SELECT MIN(load_ts) as first_load, MAX(load_ts) as last_load,
                   COUNT(*) as total_rows,
                   COUNT(DISTINCT archivo_origen) as source_files
            FROM marketplace_ledger_v1
            WHERE LOWER(marketplace) = ? AND fecha BETWEEN ? AND ?
              AND COALESCE(include_in_operational_pnl, 1) = 1
        """, [mp, str(start), str(end)])
        if df.empty:
            return {"pipeline": "unknown", "rows": 0, "source_files": 0}
        r = df.iloc[0]
        import math
        fl = r["first_load"]
        return {
            "pipeline": "surgical_loader_v4",
            "rows": int(r["total_rows"]),
            "source_files": int(r["source_files"]),
            "first_load": str(fl) if not isinstance(fl, float) or not math.isnan(fl) else None,
            "last_load": str(r["last_load"]) if not isinstance(r["last_load"], float) or not math.isnan(r["last_load"]) else None,
        }

    def _xml_info(self, samples: list[dict]) -> list[dict]:
        folios = [s.get("folio_xml") for s in samples if s.get("folio_xml")]
        if not folios:
            return []
        import math
        folios = [f for f in folios if not (isinstance(f, float) and math.isnan(f))]
        if not folios:
            return []
        placeholders = ",".join(["?"] * len(folios))
        df = self.db.query(f"""
            SELECT folio, tipo_dte, monto_total, fecha_emision, emisor_nombre
            FROM dte_truth_v1
            WHERE folio IN ({placeholders})
        """, folios)
        return df.to_dict("records") if not df.empty else []

    def _ledger_sample(self, mp: str, start, end) -> list[dict]:
        import math
        df = self.db.query("""
            SELECT id_transaccion, id_orden, detalle, monto, financial_group,
                   archivo_origen, folio_xml
            FROM marketplace_ledger_v1
            WHERE LOWER(marketplace) = ? AND fecha BETWEEN ? AND ?
              AND COALESCE(include_in_operational_pnl, 1) = 1
            ORDER BY ABS(monto) DESC
            LIMIT 5
        """, [mp, str(start), str(end)])
        if df.empty:
            return []
        records = df.to_dict("records")
        for r in records:
            for k, v in list(r.items()):
                if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                    r[k] = None
        return records

    def _raw_files(self, samples: list[dict]) -> list[str]:
        seen = set()
        files = []
        for s in samples:
            f = s.get("archivo_origen")
            if f and f not in seen:
                seen.add(f)
                files.append(f)
        return files

    def _explain(self, total: float, delta: float, delta_pct: float,
                 current_mp: dict, previous_mp: dict, label: str, prev_label: str | None) -> dict:
        parts = []
        if delta > 0:
            parts.append(f"Estas ganando ${total:,.0f}, que es ${delta:,.0f} MAS que el periodo anterior ({prev_label or 'N/A'}).")
        elif delta < 0:
            parts.append(f"Estas ganando ${total:,.0f}, pero es ${abs(delta):,.0f} MENOS que el periodo anterior ({prev_label or 'N/A'}).")
        else:
            parts.append(f"Estas ganando ${total:,.0f}, sin cambios vs el periodo anterior.")

        if delta_pct != 0:
            parts.append(f"Variacion: {delta_pct:+.1f}%.")

        mp_changes = []
        for mp, cur in sorted(current_mp.items()):
            prev_rn = previous_mp.get(mp, {}).get("rn", 0) if previous_mp else 0
            mp_delta = cur["rn"] - prev_rn
            mp_change = f"{mp.upper()}: ${cur['rn']:,.0f} ({mp_delta:+,.0f} vs anterior)"
            mp_changes.append(mp_change)
        if mp_changes:
            parts.append("Por Marketplace: " + "; ".join(mp_changes) + ".")

        return {"text": " ".join(parts), "bullet_points": mp_changes}

    def _per_mp_detail(self, current_mp: dict, previous_mp: dict) -> list[dict]:
        detail = []
        for mp, cur in sorted(current_mp.items()):
            prev_rn = previous_mp.get(mp, {}).get("rn", 0) if previous_mp else 0
            mp_delta = cur["rn"] - prev_rn
            detail.append({
                "marketplace": mp,
                "rn": round(cur["rn"], 2),
                "previous_rn": round(prev_rn, 2),
                "delta": round(mp_delta, 2),
                "delta_pct": round((mp_delta / abs(prev_rn) * 100) if prev_rn != 0 else 0, 2),
                "is_profit": cur["rn"] >= 0,
            })
        return detail
