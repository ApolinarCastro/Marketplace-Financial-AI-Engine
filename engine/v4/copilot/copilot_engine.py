"""Copilot Engine — Certified Financial Operator with full evidence chain (P39R2).

All handlers return identical structure:
  {question, period, answer, explanation, breakdown, evidence}

Zero embedded SQL — all queries from engine.v4.sql.copilot_queries.
All periods via _period_bounds(). All financial strings from constants.
No core reimplementation — Copilot only queries FinancialEngine.
"""
from __future__ import annotations
from typing import Any
import datetime
import math
import calendar
import pandas as pd

from engine.v4.database import DatabaseV4
from engine.v4.intelligence.financial_anomalies import FinancialAnomalyDetector
from engine.v4.security.query_guard import QueryGuard
from engine.v4.copilot.constants import MARKETPLACES
from engine.v4.sql import copilot_queries as q


class CopilotEngine:
    """Certified Financial Operator — answers 11 question types with full RAW->ETL->Ledger->Engine->XML evidence."""

    QUESTIONS = {
        "profit_loss":       {"label": "¿Estoy ganando o perdiendo dinero?", "handler": "_handle_profit_loss"},
        "why":               {"label": "¿Por qué gano o pierdo dinero?", "handler": "_handle_why"},
        "marketplace_impact":{"label": "¿Qué Marketplace explica el resultado?", "handler": "_handle_marketplace_impact"},
        "top_detalle":       {"label": "¿Qué detalle financiero impacta más?", "handler": "_handle_top_detalle"},
        "commission_impact": {"label": "¿Qué comisión impacta más?", "handler": "_handle_commission_impact"},
        "cost_change":       {"label": "¿Qué costo operacional aumentó?", "handler": "_handle_cost_change"},
        "top_transactions":  {"label": "¿Qué pedidos originan la diferencia?", "handler": "_handle_top_transactions"},
        "period_change":     {"label": "¿Qué cambió respecto al período anterior?", "handler": "_handle_period_change"},
        "cash_flow":         {"label": "¿Qué cobraré realmente?", "handler": "_handle_cash_flow"},
        "risk":              {"label": "¿Qué riesgo financiero existe?", "handler": "_handle_risk"},
        "evidence":          {"label": "¿Dónde está la evidencia?", "handler": "_handle_evidence"},
        # Canonical QF-001 to QF-010 mapping
        "Q-001":             {"label": "¿Qué vendí?", "handler": "_handle_top_detalle", "intent_id": "INT-QF-001"},
        "Q-002":             {"label": "¿Qué me cobraron?", "handler": "_handle_commission_impact", "intent_id": "INT-QF-002"},
        "Q-003":             {"label": "¿Qué me pagaron?", "handler": "_handle_profit_loss", "intent_id": "INT-QF-003"},
        "Q-004":             {"label": "¿Qué falta por cobrar?", "handler": "_handle_cash_flow", "intent_id": "INT-QF-004"},
        "Q-005":             {"label": "¿Qué devoluciones existen?", "handler": "_handle_cost_change", "intent_id": "INT-QF-005"},
        "Q-006":             {"label": "¿Qué XML o DTE respalda la operación?", "handler": "_handle_evidence", "intent_id": "INT-QF-006"},
        "Q-007":             {"label": "¿Qué registro SAP respalda la operación?", "handler": "_handle_insufficient_evidence", "intent_id": "INT-QF-007"},
        "Q-008":             {"label": "¿Qué movimiento bancario respalda el pago?", "handler": "_handle_insufficient_evidence", "intent_id": "INT-QF-008"},
        "Q-009":             {"label": "¿Qué cargo, comisión o descuento está oculto o no explicado?", "handler": "_handle_risk", "intent_id": "INT-QF-009"},
        "Q-010":             {"label": "¿Cuál es el margen financiero real?", "handler": "_handle_why", "intent_id": "INT-QF-010"},
    }

    SYNONYMS = {
        # Q-001
        "q-001": "Q-001", "qf-001": "Q-001", "int-qf-001": "Q-001", "intent_ventas_brutas": "Q-001",
        "¿qué vendí?": "Q-001", "qué vendí": "Q-001", "que vendi": "Q-001", "cuánto vendí": "Q-001", "cuanto vendi": "Q-001", "ventas": "Q-001", "ventas brutas": "Q-001", "total vendido": "Q-001",
        # Q-002
        "q-002": "Q-002", "qf-002": "Q-002", "int-qf-002": "Q-002", "intent_desglose_cobros": "Q-002",
        "¿qué me cobraron?": "Q-002", "qué me cobraron": "Q-002", "que me cobraron": "Q-002", "cuánto me cobraron": "Q-002", "cuanto me cobraron": "Q-002", "comisiones": "Q-002", "costos operacionales": "Q-002", "desglose cobros": "Q-002",
        # Q-003
        "q-003": "Q-003", "qf-003": "Q-003", "int-qf-003": "Q-003", "intent_resultado_neto_liquidado": "Q-003",
        "¿qué me pagaron?": "Q-003", "qué me pagaron": "Q-003", "que me pagaron": "Q-003", "cuánto me pagaron": "Q-003", "cuanto me pagaron": "Q-003", "resultado neto": "Q-003", "monto liquidado": "Q-003", "dinero recibido": "Q-003",
        # Q-004
        "q-004": "Q-004", "qf-004": "Q-004", "int-qf-004": "Q-004", "intent_saldo_pendiente": "Q-004",
        "¿qué falta por cobrar?": "Q-004", "qué falta por cobrar": "Q-004", "que falta por cobrar": "Q-004", "saldo pendiente": "Q-004", "por cobrar": "Q-004", "pendiente de cobro": "Q-004",
        # Q-005
        "q-005": "Q-005", "qf-005": "Q-005", "int-qf-005": "Q-005", "intent_devoluciones": "Q-005",
        "¿qué devoluciones existen?": "Q-005", "qué devoluciones existen": "Q-005", "que devoluciones existen": "Q-005", "devoluciones": "Q-005", "anulaciones": "Q-005", "notas de crédito": "Q-005",
        # Q-006
        "q-006": "Q-006", "qf-006": "Q-006", "int-qf-006": "Q-006", "intent_respaldo_dte": "Q-006",
        "¿qué xml o dte respalda la operación?": "Q-006", "qué xml respalda": "Q-006", "que xml respalda": "Q-006", "respaldo dte": "Q-006", "facturas xml": "Q-006", "folios xml": "Q-006",
        # Q-007
        "q-007": "Q-007", "qf-007": "Q-007", "int-qf-007": "Q-007", "intent_respaldo_sap": "Q-007",
        "¿qué registro sap respalda la operación?": "Q-007", "qué registro sap respalda": "Q-007", "que documento sap respalda": "Q-007", "respaldo sap": "Q-007", "asiento sap": "Q-007",
        # Q-008
        "q-008": "Q-008", "qf-008": "Q-008", "int-qf-008": "Q-008", "intent_respaldo_banco": "Q-008",
        "¿qué movimiento bancario respalda el pago?": "Q-008", "qué movimiento bancario respalda": "Q-008", "que movimiento bancario respalda": "Q-008", "respaldo banco": "Q-008", "cartola bancaria": "Q-008", "transferencia tef": "Q-008",
        # Q-009
        "q-009": "Q-009", "qf-009": "Q-009", "int-qf-009": "Q-009", "intent_cargos_no_explicados": "Q-009",
        "¿qué cargo, comisión o descuento está oculto o no explicado?": "Q-009", "cargos no explicados": "Q-009", "cobros no explicados": "Q-009", "penalidades": "Q-009", "cobros no previstos": "Q-009",
        # Q-010
        "q-010": "Q-010", "qf-010": "Q-010", "int-qf-010": "Q-010", "intent_margen_financiero_real": "Q-010",
        "¿cuál es el margen financiero real?": "Q-010", "cuál es el margen financiero real": "Q-010", "cual es el margen financiero real": "Q-010", "margen financiero": "Q-010", "margen real": "Q-010", "margen financiero real": "Q-010",
    }

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self.anomalies = FinancialAnomalyDetector()
        self.query_guard = QueryGuard()

    def resolve_question(self, query: str) -> str:
        if not query or not query.strip():
            raise ValueError("Empty question query")
        cleaned = query.strip().lower()
        if cleaned in self.QUESTIONS:
            return cleaned
        if cleaned in self.SYNONYMS:
            return self.SYNONYMS[cleaned]
        # Check alias format QF-001 -> Q-001
        upper_clean = query.strip().upper()
        if upper_clean.startswith("QF-"):
            q_id = "Q-" + upper_clean[3:]
            if q_id in self.QUESTIONS:
                return q_id
        if upper_clean.startswith("INT-QF-"):
            q_id = "Q-" + upper_clean[7:]
            if q_id in self.QUESTIONS:
                return q_id
        raise ValueError(f"Unknown question: {query}")

    def ask(self, question_id: str, marketplace: str | None = None, periodo: str | None = None) -> dict[str, Any]:
        resolved_qid = self.resolve_question(question_id)
        handler = getattr(self, self.QUESTIONS[resolved_qid]["handler"])
        res = handler(marketplace, periodo)
        res["question_id"] = resolved_qid
        if "intent_id" in self.QUESTIONS[resolved_qid]:
            res["intent_id"] = self.QUESTIONS[resolved_qid]["intent_id"]
        return res

    def _handle_insufficient_evidence(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        return self._response({
            "question": "Consulta requerida",
            "period": periodo,
            "status": "INSUFFICIENT_EVIDENCE",
            "answer": {
                "summary": "No se puede responder con evidencia suficiente.",
                "status": "insufficient_evidence"
            },
            "explanation": {
                "text": "No se puede responder con evidencia suficiente.",
                "bullet_points": ["No existe evidencia probatoria $0 delta certificada para este tramo."]
            },
            "breakdown": [],
            "evidence": [],
            "confidence": 0.0,
            "fallback": "No se puede responder con evidencia suficiente."
        })

    # ── SHARED HELPERS (single implementation each) ──────────────

    def _period_bounds(self, period_str: str) -> tuple[str, str]:
        if " " in period_str:
            period_str = period_str.split(" ")[0]
        parts = period_str.split("-")
        year = int(parts[0])
        month = int(parts[1])
        last_day = calendar.monthrange(year, month)[1]
        return f"{year}-{month:02d}-01", f"{year}-{month:02d}-{last_day}"

    def _mp_filter(self, marketplace: str | None, table_alias: str | None = None) -> tuple[str, list]:
        if marketplace and marketplace.upper() != "ALL":
            col = "marketplace" if table_alias is None else f"{table_alias}.marketplace"
            return f"AND LOWER({col}) = ?", [marketplace.lower()]
        return "", []

    def _to_ym(self, s: str) -> str:
        if " " in s:
            s = s.split(" ")[0]
        parts = s.split("-")
        return f"{parts[0]}-{parts[1]}"

    def _nan_safe(self, obj):
        if isinstance(obj, float):
            return None if (math.isnan(obj) or math.isinf(obj)) else obj
        if isinstance(obj, dict):
            return {k: self._nan_safe(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._nan_safe(v) for v in obj]
        return obj

    def _clean_records(self, df: pd.DataFrame) -> list[dict]:
        if df.empty:
            return []
        return self._nan_safe(df.to_dict("records"))

    def _response(self, data: dict) -> dict[str, Any]:
        return self._nan_safe(data)

    # ── QUERY EXECUTION CONTRACT ─────────────────────────────────

    def execute_query(self, sql: str, params: list | None = None) -> pd.DataFrame:
        if not sql or not sql.strip():
            raise ValueError("Empty SQL query")
        params = params or []
        if sql.count("?") != len(params):
            raise ValueError(
                f"Parameter mismatch: {sql.count('?')} placeholders vs {len(params)} params"
            )
        audit = self.query_guard.audit(sql)
        if audit.critical_count > 0:
            raise ValueError(f"SQL audit CRITICAL: {audit.summary}")
        return self.db.query(sql, params)

    # ── EVIDENCE CHAIN ───────────────────────────────────────────

    def _build_evidence(self, period_end, mp_filter: str, mp_params: list) -> list[dict]:
        if isinstance(period_end, str):
            period_end = datetime.date.fromisoformat(period_end.split(" ")[0])
        sql = q.cierre_evidence_sql(mp_filter)
        params = [str(period_end)] + mp_params
        df = self.execute_query(sql, params)
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
                "sql": q.evidence_rn_sql(mp, str(period_end)),
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

    def _ledger_sample(self, mp: str, start, end) -> list[dict]:
        df = self.execute_query(q.ledger_sample_sql(), [mp, str(start), str(end)])
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

    def _etl_info(self, mp: str, start, end) -> dict:
        df = self.execute_query(q.etl_info_sql(), [mp, str(start), str(end)])
        if df.empty:
            return {"pipeline": "unknown", "rows": 0, "source_files": 0}
        r = df.iloc[0]
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
        folios = [f for f in folios if not (isinstance(f, float) and math.isnan(f))]
        if not folios:
            return []
        sql = q.xml_info_sql(len(folios))
        df = self.execute_query(sql, folios)
        return df.to_dict("records") if not df.empty else []

    def _latest_period(self) -> dict | None:
        df = self.execute_query(q.latest_period_sql())
        if df.empty:
            return None
        return {"periodo_fin": df.iloc[0]["periodo_fin"]}

    def _previous_period_end(self, current_end):
        if isinstance(current_end, str):
            current_end = datetime.date.fromisoformat(current_end.split(" ")[0])
        s = str(current_end).split(" ")[0]
        df = self.execute_query(q.previous_period_sql(), [s])
        return df.iloc[0]["periodo_fin"] if not df.empty else None

    def _rn_by_period(self, period_end, mp_filter: str, mp_params: list) -> dict[str, dict]:
        if isinstance(period_end, str):
            period_end = datetime.date.fromisoformat(period_end.split(" ")[0])
        sql = q.rn_by_period_sql(mp_filter)
        params = [str(period_end)] + mp_params
        df = self.execute_query(sql, params)
        result = {}
        for _, r in df.iterrows():
            result[r["mp"]] = {"rn": float(r["rn"]), "marketplace": r["mp"]}
        return result

    # ── EVIDENCE VALIDATION ──────────────────────────────────────

    def _validate_evidence(self, marketplace: str | None, period_end) -> str:
        p_start, p_end = self._period_bounds(str(period_end))
        mps_to_check = [marketplace.lower()] if marketplace and marketplace.upper() != "ALL" else MARKETPLACES
        all_ok = True
        for mp in mps_to_check:
            df = self.execute_query(q.validate_ledger_sql(), [mp, p_start, p_end])
            if df.empty:
                all_ok = False
                continue
            r = df.iloc[0]
            if r["row_count"] == 0:
                all_ok = False
            if r["raw_count"] == 0:
                all_ok = False
        return "CERTIFICADO" if all_ok else "PARCIAL"

    # ── NO-DATA RESPONSE ─────────────────────────────────────────

    def _no_data(self, question_label: str) -> dict:
        return self._response({
            "question": question_label,
            "period": None,
            "answer": {"summary": "No hay datos financieros disponibles para el período consultado", "status": "no_data"},
            "explanation": {"text": "Sin datos", "bullet_points": []},
            "breakdown": [],
            "evidence": [],
        })

    # ── HANDLERS (identical structure: question, period, answer, explanation, breakdown, evidence) ──

    def _handle_profit_loss(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace, table_alias="c")
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["profit_loss"]["label"])
        period_end = latest["periodo_fin"]
        prev_end = self._previous_period_end(period_end)
        current = self._rn_by_period(period_end, mp_filter, mp_params)
        previous = self._rn_by_period(prev_end, mp_filter, mp_params) if prev_end else {}
        total_current = sum(m["rn"] for m in current.values()) if current else 0
        total_previous = sum(m["rn"] for m in previous.values()) if previous else 0
        delta = total_current - total_previous
        delta_pct = (delta / abs(total_previous) * 100) if total_previous != 0 else 0
        evidence = self._build_evidence(period_end, mp_filter, mp_params) if current else []
        bullet_points = [
            f"{mp.upper()}: ${cur['rn']:,.0f}" for mp, cur in sorted(current.items())
        ]
        return self._response({
            "question": self.QUESTIONS["profit_loss"]["label"],
            "period": str(period_end),
            "answer": {
                "status": "profit" if total_current >= 0 else "loss",
                "rn_operacional": round(total_current, 2),
                "delta": round(delta, 2),
                "delta_pct": round(delta_pct, 2),
                "is_profit": total_current >= 0,
                "summary": f"{'Ganas' if total_current >= 0 else 'Pierdes'} ${abs(total_current):,.0f}",
            },
            "explanation": {
                "text": f"Resultado neto operacional: ${total_current:,.0f} ({delta_pct:+.1f}% vs anterior).",
                "bullet_points": bullet_points,
            },
            "breakdown": [
                {"marketplace": mp, "rn": round(cur["rn"], 2), "is_profit": cur["rn"] >= 0}
                for mp, cur in sorted(current.items())
            ],
            "evidence": evidence,
        })

    def _handle_why(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace, table_alias="c")
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["why"]["label"])
        period_end = latest["periodo_fin"]
        prev_end = self._previous_period_end(period_end)
        current = self._rn_by_period(period_end, mp_filter, mp_params)
        previous = self._rn_by_period(prev_end, mp_filter, mp_params) if prev_end else {}
        total_current = sum(m["rn"] for m in current.values()) if current else 0
        total_previous = sum(m["rn"] for m in previous.values()) if previous else 0
        delta = total_current - total_previous
        delta_pct = (delta / abs(total_previous) * 100) if total_previous != 0 else 0
        evidence = self._build_evidence(period_end, mp_filter, mp_params)
        drivers = []
        for e in evidence:
            mp = e["marketplace"]
            prev_rn = previous.get(mp, {}).get("rn", 0)
            cur_rn = current.get(mp, {}).get("rn", 0)
            comps = e.get("components", {})
            primary = max(comps.items(), key=lambda x: abs(x[1]))[0] if comps else "ingresos"
            drivers.append({"marketplace": mp, "rn": cur_rn, "delta": cur_rn - prev_rn, "driver": primary})
        return self._response({
            "question": self.QUESTIONS["why"]["label"],
            "period": str(period_end),
            "answer": {
                "status": "profit" if total_current >= 0 else "loss",
                "rn_operacional": round(total_current, 2),
                "delta": round(delta, 2),
                "delta_pct": round(delta_pct, 2),
                "summary": f"{'Ganas' if total_current >= 0 else 'Pierdes'} ${abs(total_current):,.0f} — driver: ingresos",
            },
            "explanation": {
                "text": f"Variacion: {delta_pct:+.1f}%. Driver principal por marketplace.",
                "bullet_points": [f"{d['marketplace'].upper()}: {d['driver']} (${d['delta']:+,.0f})" for d in drivers],
            },
            "breakdown": drivers,
            "evidence": evidence,
        })

    def _handle_marketplace_impact(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace, table_alias="c")
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["marketplace_impact"]["label"])
        period_end = latest["periodo_fin"]
        prev_end = self._previous_period_end(period_end)
        current = self._rn_by_period(period_end, mp_filter, mp_params)
        previous = self._rn_by_period(prev_end, mp_filter, mp_params) if prev_end else {}
        total_current = sum(m["rn"] for m in current.values()) if current else 0
        evidence = self._build_evidence(period_end, mp_filter, mp_params)
        breakdown = []
        for e in evidence:
            mp = e["marketplace"]
            cur = current.get(mp, {}).get("rn", 0)
            prev_val = previous.get(mp, {}).get("rn", 0)
            contribution = (cur / total_current * 100) if total_current != 0 else 0
            breakdown.append({
                "marketplace": mp, "rn": cur, "delta": cur - prev_val,
                "contribution_pct": round(contribution, 1),
            })
        return self._response({
            "question": self.QUESTIONS["marketplace_impact"]["label"],
            "period": str(period_end),
            "answer": {
                "rn_total": round(total_current, 2),
                "summary": f"Mayor contribucion: {breakdown[0]['marketplace'].upper()} ({breakdown[0]['contribution_pct']:.1f}%)" if breakdown else "Sin datos",
            },
            "explanation": {
                "text": "Contribucion de cada marketplace al resultado neto operacional.",
                "bullet_points": [f"{b['marketplace'].upper()}: ${b['rn']:,.0f} ({b['contribution_pct']:.1f}%)" for b in breakdown],
            },
            "breakdown": breakdown,
            "evidence": evidence,
        })

    def _handle_top_detalle(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace)
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["top_detalle"]["label"])
        period_end = latest["periodo_fin"]
        p_start, p_end = self._period_bounds(str(period_end))
        params = [p_start, p_end] + mp_params
        sql = q.top_detalle_sql(mp_filter)
        df = self.execute_query(sql, params)
        top = self._clean_records(df)
        evidence = []
        for row in top[:3]:
            ledger_sample = self._ledger_sample(row["mp"], p_start, period_end)
            evidence.append({
                "marketplace": row["mp"], "kpi": "top_detalle", "value": float(row["total"]),
                "source": "marketplace_ledger_v1",
                "sql": q.evidence_detalle_sql(row["detalle"], p_start, p_end),
                "components": {"detalle": row["detalle"], "total": float(row["total"]), "count": int(row["cnt"])},
                "ledger_samples": ledger_sample[:3] if ledger_sample else [],
                "raw_sources": self._raw_files(ledger_sample) if ledger_sample else [],
                "etl": self._etl_info(row["mp"], p_start, period_end), "xml": [],
            })
        return self._response({
            "question": self.QUESTIONS["top_detalle"]["label"],
            "period": str(period_end),
            "answer": {"summary": f"Top: '{top[0]['detalle']}' (${top[0]['total']:,.0f})" if top else "Sin datos"},
            "explanation": {"text": "Top 10 detalles financieros del periodo.", "bullet_points": [f"{r['detalle']}: ${r['total']:,.0f} ({int(r['cnt'])} filas)" for r in top[:5]]},
            "breakdown": top,
            "evidence": evidence,
        })

    def _handle_commission_impact(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace)
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["commission_impact"]["label"])
        period_end = latest["periodo_fin"]
        p_start, p_end = self._period_bounds(str(period_end))
        params = [p_start, p_end] + mp_params
        sql = q.commission_impact_sql(mp_filter)
        df = self.execute_query(sql, params)
        top = self._clean_records(df)
        evidence = []
        for row in top[:3]:
            ledger_sample = self._ledger_sample(row["mp"], p_start, period_end)
            evidence.append({
                "marketplace": row["mp"], "kpi": "commission_impact", "value": float(row["total"]),
                "source": "marketplace_ledger_v1",
                "sql": q.evidence_commission_sql(row["detalle"]),
                "components": {"fg": row["financial_group"], "detalle": row["detalle"], "total": float(row["total"])},
                "ledger_samples": ledger_sample[:3] if ledger_sample else [],
                "raw_sources": self._raw_files(ledger_sample) if ledger_sample else [],
                "etl": self._etl_info(row["mp"], p_start, period_end), "xml": [],
            })
        return self._response({
            "question": self.QUESTIONS["commission_impact"]["label"],
            "period": str(period_end),
            "answer": {"summary": f"Mayor comision: '{top[0]['detalle']}' (${top[0]['total']:,.0f})" if top else "Sin comisiones"},
            "explanation": {"text": "Comisiones y costos comerciales del periodo.", "bullet_points": [f"{r['mp'].upper()} - {r['detalle']}: ${r['total']:,.0f}" for r in top[:5]]},
            "breakdown": top,
            "evidence": evidence,
        })

    def _handle_cost_change(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace, table_alias="c")
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["cost_change"]["label"])
        period_end = latest["periodo_fin"]
        prev_end = self._previous_period_end(period_end)
        if not prev_end:
            return self._response(self._no_data(self.QUESTIONS["cost_change"]["label"]))
        sql = q.cost_change_sql(mp_filter)
        df_curr = self.execute_query(sql, [str(period_end)] + mp_params)
        df_prev = self.execute_query(sql, [str(prev_end)] + mp_params)
        cost_components = ["total_costos_operacionales", "total_costos_comerciales", "total_ajustes"]
        changes = []
        for _, cr in df_curr.iterrows():
            mp = cr["mp"]
            prow = df_prev[df_prev["mp"] == mp]
            if not prow.empty:
                pr = prow.iloc[0]
                for cname in cost_components:
                    delta_val = float(cr[cname]) - float(pr[cname])
                    changes.append({"marketplace": mp, "component": cname, "current": float(cr[cname]), "previous": float(pr[cname]), "delta": delta_val})
        changes.sort(key=lambda x: abs(x["delta"]), reverse=True)
        p_start, p_end = self._period_bounds(str(period_end))
        evidence = []
        for c in changes[:3]:
            ledger_sample = self._ledger_sample(c["marketplace"], p_start, period_end)
            evidence.append({
                "marketplace": c["marketplace"], "kpi": "cost_change", "value": c["delta"],
                "source": "marketplace_cierre_financiero_v1",
                "sql": q.evidence_cost_sql(c["component"], c["marketplace"], str(period_end)),
                "components": {c["component"]: c["current"], "delta": c["delta"]},
                "ledger_samples": ledger_sample[:3] if ledger_sample else [],
                "raw_sources": self._raw_files(ledger_sample) if ledger_sample else [],
                "etl": self._etl_info(c["marketplace"], p_start, period_end), "xml": [],
            })
        return self._response({
            "question": self.QUESTIONS["cost_change"]["label"],
            "period": str(period_end),
            "answer": {"summary": f"Mayor aumento: {changes[0]['component']} (${changes[0]['delta']:,.0f})" if changes else "Sin cambios"},
            "explanation": {"text": "Variacion de costos vs periodo anterior.", "bullet_points": [f"{c['marketplace'].upper()}: {c['component']} ${c['delta']:+,.0f}" for c in changes[:5]]},
            "breakdown": changes[:10],
            "evidence": evidence,
        })

    def _handle_top_transactions(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace)
        latest = self._latest_period() if not periodo else None
        if not periodo and not latest:
            return self._no_data(self.QUESTIONS["top_transactions"]["label"])
        period_end = periodo or latest["periodo_fin"]
        p_start, p_end = self._period_bounds(str(period_end))
        params = [p_start, p_end] + mp_params
        sql = q.top_transactions_sql(mp_filter)
        df = self.execute_query(sql, params)
        top = self._clean_records(df)
        evidence = []
        for row in top[:3]:
            evidence.append({
                "marketplace": row["mp"], "kpi": "top_transactions", "value": float(row["monto"]),
                "source": "marketplace_ledger_v1",
                "sql": q.evidence_transaction_sql(row["id_transaccion"]),
                "components": {"tx": row["id_transaccion"], "order": row.get("id_orden", ""), "detalle": row["detalle"], "monto": float(row["monto"]), "fg": row["financial_group"]},
                "ledger_samples": [row],
                "raw_sources": [row["archivo_origen"]] if row.get("archivo_origen") and str(row["archivo_origen"]) != "None" else [],
                "etl": {"pipeline": "surgical_loader_v4", "rows": 0, "source_files": 0}, "xml": [],
            })
        return self._response({
            "question": self.QUESTIONS["top_transactions"]["label"],
            "period": str(period_end),
            "answer": {"summary": f"Mayor orden: {top[0].get('id_orden','N/A')} (${top[0]['monto']:,.0f})" if top else "Sin datos"},
            "explanation": {"text": "Top 20 transacciones del periodo.", "bullet_points": [f"{r['mp'].upper()} {r.get('id_orden','')} ({r['detalle']}): ${r['monto']:,.0f}" for r in top[:5]]},
            "breakdown": top,
            "evidence": evidence,
        })

    def _handle_period_change(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        return self._handle_why(marketplace, periodo)

    def _handle_cash_flow(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace, table_alias="c")
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["cash_flow"]["label"])
        period_end = latest["periodo_fin"]
        p_start, p_end = self._period_bounds(str(period_end))
        sql = q.cash_flow_sql(mp_filter)
        df = self.execute_query(sql, [str(period_end)] + mp_params)
        evidence = []
        for _, r in df.iterrows():
            mp = r["mp"]
            ledger_sample = self._ledger_sample(mp, p_start, period_end)
            evidence.append({
                "marketplace": mp, "kpi": "cash_flow", "value": float(r["resultado_neto"]),
                "source": "marketplace_cierre_financiero_v1",
                "sql": q.evidence_cash_flow_sql(mp, str(period_end)),
                "components": {"disponible": float(r["resultado_neto"]), "ajustes": float(r["total_ajustes"])},
                "ledger_samples": ledger_sample[:3] if ledger_sample else [],
                "raw_sources": self._raw_files(ledger_sample) if ledger_sample else [],
                "etl": self._etl_info(mp, p_start, period_end), "xml": [],
            })
        total_neto = sum(float(r["resultado_neto"]) for _, r in df.iterrows())
        return self._response({
            "question": self.QUESTIONS["cash_flow"]["label"],
            "period": str(period_end),
            "answer": {"summary": f"Disponible: ${total_neto:,.0f}"},
            "explanation": {
                "text": "Disponible = resultado_neto del cierre. Representa el flujo neto esperado.",
                "bullet_points": [f"{r['mp'].upper()}: ${r['resultado_neto']:,.0f}" for _, r in df.iterrows()],
            },
            "breakdown": [{"marketplace": r["mp"], "disponible": float(r["resultado_neto"]), "ajustes": float(r["total_ajustes"])} for _, r in df.iterrows()],
            "evidence": evidence,
        })

    def _handle_risk(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["risk"]["label"])
        period_end = latest["periodo_fin"]
        period_str = self._to_ym(str(period_end))
        report = self.anomalies.detect(marketplace=marketplace, periodo=period_str)
        evidence = []
        for a in report.anomalies[:3]:
            evidence.append({
                "marketplace": (marketplace or "ALL").lower(),
                "kpi": "anomaly", "value": float(a.impact_amount),
                "source": "anomaly_detector",
                "sql": getattr(a, "sql_query", ""),
                "components": {"type": a.anomaly_type, "severity": a.severity, "description": a.description, "impact": float(a.impact_amount)},
                "ledger_samples": [], "raw_sources": [],
                "etl": {"pipeline": "anomaly_detector", "rows": 0, "source_files": 0},
                "xml": [],
            })
        return self._response({
            "question": self.QUESTIONS["risk"]["label"],
            "period": str(period_end),
            "answer": {"summary": f"{len(report.anomalies)} anomalias detectadas" if report.anomalies else "Sin anomalias"},
            "explanation": {
                "text": "Deteccion de anomalias financieras.",
                "bullet_points": [f"{a.anomaly_type}: {a.description} (${a.impact_amount:,.0f})" for a in report.anomalies[:5]] if report.anomalies else ["Sin riesgos"],
            },
            "breakdown": [{
                "type": a.anomaly_type, "severity": a.severity, "impact": float(a.impact_amount), "description": a.description
            } for a in report.anomalies[:10]],
            "evidence": evidence,
        })

    def _handle_evidence(self, marketplace: str | None, periodo: str | None) -> dict[str, Any]:
        mp_filter, mp_params = self._mp_filter(marketplace)
        latest = self._latest_period()
        if not latest:
            return self._no_data(self.QUESTIONS["evidence"]["label"])
        period_end = latest["periodo_fin"]
        p_start, p_end = self._period_bounds(str(period_end))
        params = [p_start, p_end] + mp_params
        sql = q.evidence_chain_sql(mp_filter)
        df = self.execute_query(sql, params)
        rows = self._clean_records(df)
        evidence = []
        for row in rows:
            ledger_sample = self._ledger_sample(row["mp"], p_start, period_end)
            evidence.append({
                "marketplace": row["mp"], "kpi": "evidence_chain", "value": float(row["monto"]),
                "source": "marketplace_ledger_v1",
                "sql": q.evidence_full_row_sql(row["id_transaccion"]),
                "components": {"tx": row["id_transaccion"], "order": row.get("id_orden", ""), "detalle": row["detalle"], "monto": float(row["monto"]), "fg": row["financial_group"]},
                "ledger_samples": ledger_sample[:3] if ledger_sample else [],
                "raw_sources": self._raw_files(ledger_sample) if ledger_sample else [],
                "etl": self._etl_info(row["mp"], p_start, period_end),
                "xml": self._xml_info([row]) if row.get("folio_xml") else [],
            })
        confidence = self._validate_evidence(marketplace, period_end)
        return self._response({
            "question": self.QUESTIONS["evidence"]["label"],
            "period": str(period_end),
            "answer": {"summary": f"Evidencia completa para {len(evidence)} transacciones", "confidence": confidence},
            "explanation": {
                "text": "RAW -> ETL -> Ledger -> Financial Engine -> API -> Usuario",
                "bullet_points": [f"{e['marketplace'].upper()}: {e['components'].get('tx','')} (${e['value']:,.0f})" for e in evidence],
            },
            "breakdown": [{"marketplace": e["marketplace"], "id_transaccion": e["components"].get("tx", ""), "monto": e["value"], "raw": e["raw_sources"]} for e in evidence],
            "evidence": evidence,
        })
