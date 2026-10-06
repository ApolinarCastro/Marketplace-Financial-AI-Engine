"""
reconciliation_engine.py — Universal Reconciliation Authority.

Single source of truth for certification status across all marketplaces.
5 levels of reconciliation, all consuming marketplace_ledger_clasificado_v1
as the sole financial source (Single Financial Truth).

Statuses:
  CERTIFICADO               delta=0, taxonomy=100%, document>=95%
  PARCIAL                   delta<=10, taxonomy>=50%, document>=50%
  PENDIENTE                 delta<=100, taxonomy>=10%, document>=10%
  ERROR                     any threshold exceeded
  FINANCIAL_INTEGRITY_BROKEN delta > 1000

Usage:
    engine = ReconciliationEngine()
    result = engine.validate_marketplace_consistency("ML", "2026-01")
"""
from __future__ import annotations
from pathlib import Path
from typing import Any
import logging
import math
import yaml
import pandas as pd

from engine.v4.database import DatabaseV4
from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.reconciliation.reconciliation_contracts import (
    ReconciliationResult,
    ReconciliationAlert,
    LevelResult,
    ReconciliationMetrics,
    CertificationStatus,
)

logger = logging.getLogger("meli.reconciliation")

ROOT = Path(__file__).resolve().parent
RULES_PATH = ROOT / "reconciliation_rules.yaml"

_MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
           "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
_MARKETPLACES = ["ML", "PARIS", "RIPLEY", "FALABELLA"]

# Groups considered treasury (cash/settlement side)
_TREASURY_GROUPS = {"tesoreria"}

# Groups considered operational P&L
_OPERATIONAL_GROUPS = {
    "ingresos", "devoluciones", "costos_operacionales",
    "costos_comerciales", "ajustes", "recuperaciones_y_bonificaciones", "riesgos_y_compensaciones", "impuestos",
}


def _safe_float(v: Any) -> float:
    """Convert to float, replacing NaN/None with 0.0."""
    if v is None:
        return 0.0
    try:
        f = float(v)
        return 0.0 if math.isnan(f) or math.isinf(f) else f
    except (ValueError, TypeError):
        return 0.0


def _safe_delta(a: float, b: float) -> float:
    """Absolute difference, NaN-safe."""
    return abs(_safe_float(a) - _safe_float(b))


def _load_rules() -> dict[str, Any]:
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _build_alert(
    marketplace: str, period: str, level: str,
    rule: str, impact_amount: float, record_count: int,
    sql_query: str, evidence: str,
) -> ReconciliationAlert:
    return ReconciliationAlert(
        marketplace=marketplace,
        period=period,
        level=level,
        rule=rule,
        impact_amount=round(impact_amount, 2),
        record_count=record_count,
        sql_query=sql_query,
        evidence=evidence,
    )


def _determine_status(
    delta: float,
    taxonomy_coverage: float,
    document_coverage: float,
    rules: dict[str, Any],
) -> CertificationStatus:
    delta = _safe_float(delta)
    taxonomy_coverage = _safe_float(taxonomy_coverage)
    document_coverage = _safe_float(document_coverage)
    critical_delta = rules.get("critical_delta", 1)
    allowed_delta = rules.get("allowed_delta", 0)

    if delta > 1000:
        return "FINANCIAL_INTEGRITY_BROKEN"
    if delta > critical_delta:
        return "ERROR"
    if taxonomy_coverage < 50 or document_coverage < 10:
        return "PENDIENTE"
    if taxonomy_coverage < 100 or document_coverage < 95:
        return "PARCIAL"
    if delta > allowed_delta:
        return "PARCIAL"
    return "CERTIFICADO"


class ReconciliationEngine:
    """Universal reconciliation authority. Single entry point for all certification statuses."""

    def __init__(self, db: DatabaseV4 | None = None):
        self.db = db or DatabaseV4.get()
        self.fe = FinancialEngine(self.db)
        self.rules = _load_rules()

    # ──────────────────────────────────────────────────────────────
    # PUBLIC API
    # ──────────────────────────────────────────────────────────────

    def validate_marketplace_consistency(
        self,
        marketplace: str,
        periodo: str | None = None,
    ) -> ReconciliationResult:
        """Main entry point: run all 5 levels and return unified result."""
        marketplace = marketplace.upper()
        start, end, label = self.fe.resolve_period_range(periodo)
        period_label = label if periodo else f"YTD ({start})"

        levels: dict[str, LevelResult] = {}
        all_alerts: list[ReconciliationAlert] = []

        # Level 1: Internal — clasificado vs cierre
        l1 = self._level_1_internal(marketplace, start, end, period_label)
        levels["INTERNA"] = l1
        all_alerts.extend(l1.alerts)

        # Level 2: Operational — op_pnl vs resultado_neto
        l2 = self._level_2_operational(marketplace, start, end, period_label)
        levels["OPERACIONAL"] = l2
        all_alerts.extend(l2.alerts)

        # Level 3: Treasury — tesoreria vs P&L mirror
        l3 = self._level_3_treasury(marketplace, start, end, period_label, l2.source_total)
        levels["TESORERÍA"] = l3
        all_alerts.extend(l3.alerts)

        # Level 4: Documentary — ledger vs document_match_v1
        l4 = self._level_4_documentary(marketplace, start, end, period_label)
        levels["DOCUMENTAL"] = l4
        all_alerts.extend(l4.alerts)

        # Aggregated metrics
        total_records = self._count_records(marketplace, start, end)
        taxonomy_coverage = self._taxonomy_coverage(marketplace, start, end)
        document_coverage = self._document_coverage(marketplace, start, end)
        orphan_records = self._orphan_records(marketplace, start, end)

        operational_total = _safe_float(l2.source_total)
        settlement_total = _safe_float(l1.source_total)
        treasury_total = _safe_float(l3.source_total)

        total_delta = _safe_delta(0, _safe_float(l1.delta)) + _safe_delta(0, _safe_float(l2.delta)) + _safe_delta(0, _safe_float(l3.delta))

        status = _determine_status(total_delta, taxonomy_coverage, document_coverage, self.rules)

        metrics = ReconciliationMetrics(
            reconciliation_delta=round(total_delta, 2),
            taxonomy_coverage=round(taxonomy_coverage, 2),
            document_coverage=round(document_coverage, 2),
            orphan_records=orphan_records,
            certification_status=status,
        )

        return ReconciliationResult(
            marketplace=marketplace,
            period=period_label,
            certification_status=status,
            delta=round(total_delta, 2),
            operational_total=round(operational_total, 2),
            settlement_total=round(settlement_total, 2),
            treasury_total=round(treasury_total, 2),
            taxonomy_coverage=round(taxonomy_coverage, 2),
            document_coverage=round(document_coverage, 2),
            orphan_records=orphan_records,
            total_records=total_records,
            alerts=all_alerts,
            levels=levels,
            metrics=metrics,
        )

    def validate_all_marketplaces(
        self,
        periodo: str | None = None,
    ) -> dict[str, ReconciliationResult]:
        """Run validation for all 4 marketplaces (Level 5 wrapper)."""
        results = {}
        for mp in _MARKETPLACES:
            results[mp] = self.validate_marketplace_consistency(mp, periodo)
        return results

    # ──────────────────────────────────────────────────────────────
    # LEVEL 1 — INTERNAL: Ledger Clasificado vs Cierre
    # ──────────────────────────────────────────────────────────────

    def _level_1_internal(
        self, marketplace: str, start: str, end: str | None, period_label: str,
    ) -> LevelResult:
        """Compare SUM per financial_group against cierre_financiero_v1 totals."""
        alerts: list[ReconciliationAlert] = []

        # Source A: clasificado_v1 totals per group
        sql_clasif = """
            SELECT COALESCE(financial_group, 'sin_clasificar') as financial_group,
                   SUM(COALESCE(monto, 0)) as total
            FROM marketplace_ledger_clasificado_v1
            WHERE marketplace = ?
              AND fecha >= ?
              {date_end}
              {op_filter}
            GROUP BY financial_group
            ORDER BY financial_group
        """
        params_clasif = [marketplace, start]
        date_clause = ""
        if end:
            date_clause = "AND fecha <= ?"
            params_clasif.append(end)
            
        # Source A is scoped to the same operational universe as the cierre
        # target (run_financial_closing aggregates include_in_operational_pnl
        # = TRUE only). Non-operational groups (e.g. tesoreria, op_pnl = FALSE)
        # must not raise UNEXPECTED_GROUP: Level 3 requires them while Level 1
        # must not flag them.
        op_filter = "AND include_in_operational_pnl = TRUE"
            
        sql_clasif_full = sql_clasif.format(date_end=date_clause, op_filter=op_filter)

        df_clasif = self.db.query(sql_clasif_full, params_clasif)
        clasif_totals = {}
        for _, row in df_clasif.iterrows():
            clasif_totals[str(row["financial_group"])] = _safe_float(row["total"])
        source_total = sum(clasif_totals.values())

        # Source B: cierre_financiero_v1
        sql_cierre = """
            SELECT SUM(COALESCE(total_ingresos, 0)) as total_ingresos, 
                   SUM(COALESCE(total_costos_operacionales, 0)) as total_costos_operacionales,
                   SUM(COALESCE(total_costos_comerciales, 0)) as total_costos_comerciales, 
                   SUM(COALESCE(total_ajustes, 0)) as total_ajustes, 
                   SUM(COALESCE(resultado_neto, 0)) as resultado_neto
            FROM marketplace_cierre_financiero_v1
            WHERE marketplace = ?
              AND periodo_inicio >= ?
        """
        if end:
            sql_cierre += " AND periodo_fin <= ?"
            params_cierre = [marketplace, start, end]
        else:
            params_cierre = [marketplace, start]

        df_cierre = self.db.query(sql_cierre, params_cierre)
        target_total = 0.0
        cierre_groups: dict[str, float] = {}
        if not df_cierre.empty:
            row = df_cierre.iloc[0]
            cierre_groups = {
                "ingresos": float(row["total_ingresos"] or 0),
                "costos_operacionales": float(row["total_costos_operacionales"] or 0),
                "costos_comerciales": float(row["total_costos_comerciales"] or 0),
                "ajustes": float(row["total_ajustes"] or 0),
            }
            target_total = float(row["resultado_neto"] or 0)

        # Compare per group
        group_deltas: dict[str, float] = {}
        for group, cierre_total in cierre_groups.items():
            clasif_val = clasif_totals.get(group, 0.0)
            if group == "ajustes":
                clasif_val += clasif_totals.get("devoluciones", 0.0)
                clasif_val += clasif_totals.get("riesgos_y_compensaciones", 0.0)
                clasif_val += clasif_totals.get("recuperaciones_y_bonificaciones", 0.0)
                clasif_val += clasif_totals.get("impuestos", 0.0)
            group_delta = _safe_delta(clasif_val, cierre_total)
            group_deltas[group] = group_delta

            if group_delta > self.rules.get("allowed_delta", 0):
                alerts.append(_build_alert(
                    marketplace=marketplace,
                    period=period_label,
                    level="INTERNA",
                    rule=f"GROUP_MISMATCH:{group}",
                    impact_amount=group_delta,
                    record_count=int(df_clasif[df_clasif["financial_group"] == group].shape[0]) if group in df_clasif["financial_group"].values else 0,
                    sql_query=sql_clasif_full,
                    evidence=f"clasificado={clasif_val:.2f} vs cierre={cierre_total:.2f}, delta={group_delta:.2f}",
                ))

        # Check for groups in clasificado but not in cierre
        extra_groups = set(clasif_totals.keys()) - set(cierre_groups.keys()) - {"sin_clasificar", "devoluciones", "riesgos_y_compensaciones", "recuperaciones_y_bonificaciones", "impuestos"}
        for eg in extra_groups:
            alerts.append(_build_alert(
                marketplace=marketplace,
                period=period_label,
                level="INTERNA",
                rule=f"UNEXPECTED_GROUP:{eg}",
                impact_amount=clasif_totals[eg],
                record_count=1,
                sql_query=sql_clasif_full,
                evidence=f"Group '{eg}' (total={clasif_totals[eg]:.2f}) not found in cierre",
            ))

        # Check for sin_clasificar records
        sin_clasif = clasif_totals.get("sin_clasificar", 0.0)
        if sin_clasif != 0:
            alerts.append(_build_alert(
                marketplace=marketplace,
                period=period_label,
                level="INTERNA",
                rule="UNCLASSIFIED_RECORDS",
                impact_amount=sin_clasif,
                record_count=int(df_clasif[df_clasif["financial_group"] == "sin_clasificar"].shape[0]) if "sin_clasificar" in df_clasif["financial_group"].values else 0,
                sql_query=sql_clasif_full,
                evidence=f"{sin_clasif:.2f} in records without financial_group",
            ))

        total_delta = max(_safe_float(v) for v in group_deltas.values()) if group_deltas else 0.0
        level_status = "PASS" if total_delta <= self.rules.get("allowed_delta", 0) and not alerts else "ALERTA"

        return LevelResult(
            level="INTERNA",
            status=level_status,
            delta=round(total_delta, 2),
            source_total=round(source_total, 2),
            target_total=round(target_total, 2),
            alerts=alerts,
        )

    # ──────────────────────────────────────────────────────────────
    # LEVEL 2 — OPERACIONAL: Operational P&L vs Resultado Neto
    # ──────────────────────────────────────────────────────────────

    def _level_2_operational(
        self, marketplace: str, start: str, end: str | None, period_label: str,
    ) -> LevelResult:
        """Compare operational P&L (include_in_operational_pnl=1) against cierre resultado_neto."""
        alerts: list[ReconciliationAlert] = []

        # Source A: operational P&L from clasificado
        sql_op = """
            SELECT SUM(COALESCE(monto, 0)) as total
            FROM marketplace_ledger_clasificado_v1
            WHERE marketplace = ?
              AND fecha >= ?
              {date_end}
              AND COALESCE(include_in_operational_pnl, 1) = 1
        """
        params_op = [marketplace, start]
        date_clause = ""
        if end:
            date_clause = "AND fecha <= ?"
            params_op.append(end)
        sql_op_full = sql_op.format(date_end=date_clause)

        df_op = self.db.query(sql_op_full, params_op)
        operational_total = _safe_float(df_op.iloc[0]["total"]) if not df_op.empty else 0.0

        # Source B: cierre resultado_neto
        sql_rn = """
            SELECT SUM(COALESCE(resultado_neto, 0)) as resultado_neto
            FROM marketplace_cierre_financiero_v1
            WHERE marketplace = ?
              AND periodo_inicio >= ?
        """
        params_rn = [marketplace, start]
        if end:
            sql_rn += " AND periodo_fin <= ?"
            params_rn.append(end)

        df_rn = self.db.query(sql_rn, params_rn)
        resultado_neto = _safe_float(df_rn.iloc[0]["resultado_neto"]) if not df_rn.empty else 0.0

        delta = _safe_delta(operational_total, resultado_neto)
        if delta > self.rules.get("allowed_delta", 0):
            alerts.append(_build_alert(
                marketplace=marketplace,
                period=period_label,
                level="OPERACIONAL",
                rule="OP_PNL_VS_RESULTADO_NETO",
                impact_amount=delta,
                record_count=int(df_op.shape[0]),
                sql_query=sql_op_full,
                evidence=f"operational_total={operational_total:.2f} vs resultado_neto={resultado_neto:.2f}, delta={delta:.2f}",
            ))

        level_status = "PASS" if delta <= self.rules.get("allowed_delta", 0) else "ALERTA"
        return LevelResult(
            level="OPERACIONAL",
            status=level_status,
            delta=round(delta, 2),
            source_total=round(operational_total, 2),
            target_total=round(resultado_neto, 2),
            alerts=alerts,
        )

    # ──────────────────────────────────────────────────────────────
    # LEVEL 3 — TESORERÍA: Treasury vs Settlement mirror
    # ──────────────────────────────────────────────────────────────

    def _level_3_treasury(
        self, marketplace: str, start: str, end: str | None,
        period_label: str, operational_total: float,
    ) -> LevelResult:
        """Compare treasury total against the P&L mirror (net settlement).

        The financial equation: SUM(P&L) + SUM(treasury) ≈ 0
        P&L generates cash; treasury records the cash movement.
        """
        alerts: list[ReconciliationAlert] = []

        # Source A: treasury totals
        sql_tes = """
            SELECT SUM(COALESCE(monto, 0)) as total
            FROM marketplace_ledger_clasificado_v1
            WHERE marketplace = ?
              AND fecha >= ?
              {date_end}
              AND financial_group IN ('tesoreria')
        """
        params_tes = [marketplace, start]
        date_clause = ""
        if end:
            date_clause = "AND fecha <= ?"
            params_tes.append(end)
        sql_tes_full = sql_tes.format(date_end=date_clause)

        df_tes = self.db.query(sql_tes_full, params_tes)
        treasury_total = _safe_float(df_tes.iloc[0]["total"]) if not df_tes.empty else 0.0

        # The P&L side (operational) and treasury should be mirrored
        # i.e., operational_total + treasury_total ≈ 0
        op = _safe_float(operational_total)
        tr = _safe_float(treasury_total)
        mirror_delta = abs(op + tr)

        if mirror_delta > self.rules.get("allowed_delta", 0):
            alerts.append(_build_alert(
                marketplace=marketplace,
                period=period_label,
                level="TESORERÍA",
                rule="PNL_TREASURY_MISMATCH",
                impact_amount=mirror_delta,
                record_count=int(df_tes.shape[0]),
                sql_query=sql_tes_full,
                evidence=f"operational_total={operational_total:.2f} + treasury_total={treasury_total:.2f} = {operational_total + treasury_total:.2f} (expected ~0)",
            ))

        level_status = "PASS" if mirror_delta <= self.rules.get("allowed_delta", 0) else "ALERTA"
        return LevelResult(
            level="TESORERÍA",
            status=level_status,
            delta=round(mirror_delta, 2),
            source_total=round(treasury_total, 2),
            target_total=round(-operational_total, 2),
            alerts=alerts,
        )

    # ──────────────────────────────────────────────────────────────
    # LEVEL 4 — DOCUMENTAL: Ledger vs Document Match
    # ──────────────────────────────────────────────────────────────

    def _level_4_documentary(
        self, marketplace: str, start: str, end: str | None, period_label: str,
    ) -> LevelResult:
        """Check document coverage via document_match_v1 + dte_truth_v1.

        Uses ONLY marketplace_ledger_clasificado_v1 + document_match_v1 + dte_truth_v1.
        No folio_xml access needed (not in clasificado_v1 schema).
        """
        alerts: list[ReconciliationAlert] = []

        date_clause = ""
        params_total = [marketplace, start]
        if end:
            date_clause = "AND fecha <= ?"
            params_total.append(end)

        # Total records in clasificado_v1
        sql_total = f"""
            SELECT COUNT(*) as total
            FROM marketplace_ledger_clasificado_v1
            WHERE marketplace = ?
              AND fecha >= ?
              {date_clause}
        """
        df_total = self.db.query(sql_total, params_total)
        total = int(df_total.iloc[0]["total"]) if not df_total.empty else 0

        # Matched records via document_match_v1 (JOIN on id_transaccion = ledger_id)
        sql_matched = f"""
            SELECT COUNT(DISTINCT c.id_transaccion) as matched
            FROM marketplace_ledger_clasificado_v1 c
            INNER JOIN document_match_v1 d
                ON c.marketplace = d.marketplace
                AND c.id_transaccion = d.ledger_id
            WHERE c.marketplace = ?
              AND c.fecha >= ?
              {date_clause}
              AND d.match_status = 'CONCILIATED'
        """
        params_matched = [marketplace, start]
        if end:
            params_matched.append(end)

        df_matched = self.db.query(sql_matched, params_matched)
        matched = int(df_matched.iloc[0]["matched"]) if not df_matched.empty else 0
        unmatched = total - matched

        coverage = (matched / total * 100) if total > 0 else 0.0

        min_doc_cov = self.rules.get("minimum_document_coverage", 95)
        if coverage < min_doc_cov:
            alerts.append(_build_alert(
                marketplace=marketplace,
                period=period_label,
                level="DOCUMENTAL",
                rule="INSUFFICIENT_DOCUMENT_COVERAGE",
                impact_amount=float(unmatched),
                record_count=unmatched,
                sql_query=sql_matched,
                evidence=f"coverage={coverage:.1f}% (min={min_doc_cov}%). {unmatched}/{total} records without document match",
            ))

        # Orphan records: records in document_match_v1 that don't exist in clasificado_v1
        sql_orphans = f"""
            SELECT COUNT(*) as orphans
            FROM document_match_v1 d
            WHERE d.marketplace = ?
              AND d.document_date >= ?
              {date_clause.replace('fecha', 'd.document_date') if date_clause else ''}
              AND NOT EXISTS (
                  SELECT 1 FROM marketplace_ledger_clasificado_v1 c
                  WHERE c.marketplace = d.marketplace
                    AND c.id_transaccion = d.ledger_id
              )
        """
        params_orphans = [marketplace, start]
        if end:
            params_orphans.append(end)

        df_orphans = self.db.query(sql_orphans, params_orphans)
        orphan_records = int(df_orphans.iloc[0]["orphans"]) if not df_orphans.empty else 0

        if orphan_records > 0:
            alerts.append(_build_alert(
                marketplace=marketplace,
                period=period_label,
                level="DOCUMENTAL",
                rule="ORPHAN_RECORDS",
                impact_amount=float(orphan_records),
                record_count=orphan_records,
                sql_query=sql_orphans,
                evidence=f"{orphan_records} orphan records in document_match_v1 without ledger match",
            ))

        level_status = "PASS" if coverage >= min_doc_cov and orphan_records == 0 else "ALERTA"
        return LevelResult(
            level="DOCUMENTAL",
            status=level_status,
            delta=round(100.0 - coverage, 2),
            source_total=float(matched),
            target_total=float(total),
            alerts=alerts,
        )

    # ──────────────────────────────────────────────────────────────
    # HELPER: Taxonomy coverage
    # ──────────────────────────────────────────────────────────────

    def _taxonomy_coverage(self, marketplace: str, start: str, end: str | None) -> float:
        """Percentage of records with a non-null financial_group."""
        sql = """
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN financial_group IS NOT NULL AND financial_group != '' THEN 1 ELSE 0 END) as classified
            FROM marketplace_ledger_clasificado_v1
            WHERE marketplace = ?
              AND fecha >= ?
              {date_end}
        """
        params = [marketplace, start]
        date_clause = ""
        if end:
            date_clause = "AND fecha <= ?"
            params.append(end)

        df = self.db.query(sql.format(date_end=date_clause), params)
        if df.empty:
            return 0.0
        total = float(df.iloc[0]["total"])
        classified = float(df.iloc[0]["classified"])
        return (classified / total * 100) if total > 0 else 100.0

    # ──────────────────────────────────────────────────────────────
    # HELPER: Document coverage
    # ──────────────────────────────────────────────────────────────

    def _document_coverage(self, marketplace: str, start: str, end: str | None) -> float:
        """Percentage of records with a document match via document_match_v1."""
        date_clause = ""
        params = [marketplace, start]
        if end:
            date_clause = "AND c.fecha <= ?"
            params.append(end)

        sql = f"""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN d.match_id IS NOT NULL THEN 1 ELSE 0 END) as matched
            FROM marketplace_ledger_clasificado_v1 c
            LEFT JOIN document_match_v1 d
                ON c.marketplace = d.marketplace
                AND c.id_transaccion = d.ledger_id
            WHERE c.marketplace = ?
              AND c.fecha >= ?
              {date_clause}
        """
        df = self.db.query(sql, params)
        if df.empty:
            return 0.0
        total = float(df.iloc[0]["total"])
        matched = float(df.iloc[0]["matched"])
        return (matched / total * 100) if total > 0 else 0.0

    # ──────────────────────────────────────────────────────────────
    # HELPER: Orphan records
    # ──────────────────────────────────────────────────────────────

    def _orphan_records(self, marketplace: str, start: str, end: str | None) -> int:
        """Count ledger records without a corresponding document_match_v1 entry."""
        date_clause = ""
        params = [marketplace, start]
        if end:
            date_clause = "AND c.fecha <= ?"
            params.append(end)

        sql = f"""
            SELECT COUNT(*) as orphans
            FROM marketplace_ledger_clasificado_v1 c
            WHERE c.marketplace = ?
              AND c.fecha >= ?
              {date_clause}
              AND NOT EXISTS (
                  SELECT 1 FROM document_match_v1 d
                  WHERE d.marketplace = c.marketplace
                    AND d.ledger_id = c.id_transaccion
              )
        """
        df = self.db.query(sql, params)
        return int(df.iloc[0]["orphans"]) if not df.empty else 0

    # ──────────────────────────────────────────────────────────────
    # HELPER: Total record count
    # ──────────────────────────────────────────────────────────────

    def _count_records(self, marketplace: str, start: str, end: str | None) -> int:
        sql = """
            SELECT COUNT(*) as total
            FROM marketplace_ledger_clasificado_v1
            WHERE marketplace = ?
              AND fecha >= ?
              {date_end}
        """
        params = [marketplace, start]
        date_clause = ""
        if end:
            date_clause = "AND fecha <= ?"
            params.append(end)

        df = self.db.query(sql.format(date_end=date_clause), params)
        return int(df.iloc[0]["total"]) if not df.empty else 0
