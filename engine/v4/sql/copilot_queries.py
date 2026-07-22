"""All SQL queries consumed by CopilotEngine — Single repository, zero embedded SQL in handlers.

Every function returns a SQL string (possibly with {mp_filter} placeholder).
The caller replaces {mp_filter} and appends mp_params at the end.

Evidence SQLs return parameterized strings for display — NOT for execution.
"""

from __future__ import annotations

MP_FILTER_PLACEHOLDER = "{mp_filter}"


# ── Cierre queries ──────────────────────────────────────────────

def latest_period_sql() -> str:
    return """
        SELECT DISTINCT periodo_fin
        FROM marketplace_cierre_financiero_v1
        WHERE resultado_neto != 0 AND periodo_inicio != '2023-01-01'
          AND LOWER(marketplace) NOT IN ('all')
          AND periodo_inicio <= CURRENT_DATE
        ORDER BY periodo_fin DESC
        LIMIT 1
    """


def previous_period_sql() -> str:
    return """
        SELECT DISTINCT periodo_fin
        FROM marketplace_cierre_financiero_v1
        WHERE resultado_neto != 0 AND periodo_inicio != '2023-01-01'
          AND LOWER(marketplace) NOT IN ('all')
          AND periodo_fin < ?
        ORDER BY periodo_fin DESC
        LIMIT 1
    """


def rn_by_period_sql(mp_filter: str = "") -> str:
    return f"""
        SELECT LOWER(c.marketplace) as mp, c.resultado_neto as rn
        FROM marketplace_cierre_financiero_v1 c
        WHERE c.periodo_fin = ?
          AND c.resultado_neto != 0
          AND LOWER(c.marketplace) NOT IN ('all')
        {mp_filter}
        ORDER BY c.marketplace
    """


def cierre_evidence_sql(mp_filter: str = "") -> str:
    return f"""
        SELECT LOWER(c.marketplace) as mp, c.resultado_neto,
               c.total_ingresos, c.total_costos_operacionales,
               c.total_costos_comerciales, c.total_ajustes,
               c.periodo_inicio
        FROM marketplace_cierre_financiero_v1 c
        WHERE c.periodo_fin = ? AND c.resultado_neto != 0
          AND LOWER(c.marketplace) NOT IN ('all')
        {mp_filter}
        ORDER BY c.marketplace
    """


def cash_flow_sql(mp_filter: str = "") -> str:
    return f"""
        SELECT LOWER(c.marketplace) as mp, c.resultado_neto, c.total_ajustes
        FROM marketplace_cierre_financiero_v1 c
        WHERE c.periodo_fin = ? AND c.resultado_neto != 0
          AND LOWER(c.marketplace) NOT IN ('all')
        {mp_filter}
    """


def cost_change_sql(mp_filter: str = "") -> str:
    return f"""
        SELECT LOWER(c.marketplace) as mp,
               c.total_costos_operacionales, c.total_costos_comerciales, c.total_ajustes
        FROM marketplace_cierre_financiero_v1 c
        WHERE c.resultado_neto != 0 AND LOWER(c.marketplace) NOT IN ('all')
          AND c.periodo_fin = ?
        {mp_filter}
    """


# ── Ledger queries ──────────────────────────────────────────────

def top_detalle_sql(mp_filter: str = "") -> str:
    return f"""
        SELECT LOWER(marketplace) as mp, detalle, SUM(COALESCE(monto, 0)) as total, COUNT(*) as cnt
        FROM marketplace_ledger_v1
        WHERE fecha BETWEEN ? AND ?
          AND COALESCE(include_in_operational_pnl, 1) = 1
          AND financial_group IS NOT NULL
        {mp_filter}
        GROUP BY LOWER(marketplace), detalle
        ORDER BY ABS(total) DESC, detalle
        LIMIT 10
    """


def commission_impact_sql(mp_filter: str = "") -> str:
    return f"""
        SELECT LOWER(marketplace) as mp, financial_group, detalle, SUM(COALESCE(monto, 0)) as total
        FROM marketplace_ledger_v1
        WHERE fecha BETWEEN ? AND ?
          AND COALESCE(include_in_operational_pnl, 1) = 1
          AND LOWER(financial_group) IN ('comisiones', 'costos_comerciales')
        {mp_filter}
        GROUP BY LOWER(marketplace), financial_group, detalle
        ORDER BY ABS(total) DESC, detalle
        LIMIT 20
    """


def top_transactions_sql(mp_filter: str = "") -> str:
    return f"""
        SELECT LOWER(marketplace) as mp, id_transaccion, id_orden, detalle, monto, financial_group, archivo_origen, folio_xml
        FROM marketplace_ledger_v1
        WHERE fecha BETWEEN ? AND ?
          AND COALESCE(include_in_operational_pnl, 1) = 1
          AND financial_group IS NOT NULL
        {mp_filter}
        ORDER BY ABS(monto) DESC, id_transaccion
        LIMIT 20
    """


def evidence_chain_sql(mp_filter: str = "") -> str:
    return f"""
        SELECT LOWER(marketplace) as mp, id_transaccion, id_orden, detalle, monto, financial_group, archivo_origen, folio_xml
        FROM marketplace_ledger_v1
        WHERE fecha BETWEEN ? AND ?
          AND COALESCE(include_in_operational_pnl, 1) = 1
          AND financial_group IS NOT NULL
        {mp_filter}
        ORDER BY ABS(monto) DESC, id_transaccion
        LIMIT 3
    """


def ledger_sample_sql() -> str:
    return """
        SELECT id_transaccion, id_orden, detalle, monto, financial_group,
               archivo_origen, folio_xml
        FROM marketplace_ledger_v1
        WHERE LOWER(marketplace) = ? AND fecha BETWEEN ? AND ?
          AND COALESCE(include_in_operational_pnl, 1) = 1
        ORDER BY ABS(monto) DESC, id_transaccion
        LIMIT 5
    """


def etl_info_sql() -> str:
    return """
        SELECT MIN(load_ts) as first_load, MAX(load_ts) as last_load,
               COUNT(*) as total_rows,
               COUNT(DISTINCT archivo_origen) as source_files
        FROM marketplace_ledger_v1
        WHERE LOWER(marketplace) = ? AND fecha BETWEEN ? AND ?
          AND COALESCE(include_in_operational_pnl, 1) = 1
    """


def validate_ledger_sql() -> str:
    return """
        SELECT COUNT(*) as row_count,
               COUNT(DISTINCT archivo_origen) as raw_count,
               COUNT(folio_xml) as xml_count
        FROM marketplace_ledger_v1
        WHERE LOWER(marketplace) = ? AND fecha BETWEEN ? AND ?
          AND COALESCE(include_in_operational_pnl, 1) = 1
    """


# ── DTE / XML queries ───────────────────────────────────────────

def xml_info_sql(folio_count: int) -> str:
    placeholders = ",".join(["?"] * folio_count)
    return f"""
        SELECT folio, tipo_dte, monto_total, fecha_emision, emisor_nombre
        FROM dte_truth_v1
        WHERE folio IN ({placeholders})
    """


# ── Evidence display SQLs (informational, not executed) ──────────

def evidence_rn_sql(mp: str, period_end: str) -> str:
    return f"SELECT resultado_neto FROM marketplace_cierre_financiero_v1 WHERE LOWER(marketplace)='{mp}' AND periodo_fin='{period_end}'"


def evidence_cash_flow_sql(mp: str, period_end: str) -> str:
    return f"SELECT resultado_neto FROM marketplace_cierre_financiero_v1 WHERE LOWER(marketplace)='{mp}' AND periodo_fin='{str(period_end)}'"


def evidence_commission_sql(detalle: str) -> str:
    return f"SELECT SUM(monto) FROM marketplace_ledger_v1 WHERE LOWER(financial_group) IN ('comisiones','costos_comerciales') AND detalle='{detalle}'"


def evidence_cost_sql(component: str, mp: str, period_end: str) -> str:
    return f"SELECT {component} FROM marketplace_cierre_financiero_v1 WHERE LOWER(marketplace)='{mp}' AND periodo_fin='{str(period_end)}'"


def evidence_transaction_sql(tx_id: str) -> str:
    return f"SELECT monto FROM marketplace_ledger_v1 WHERE id_transaccion='{tx_id}'"


def evidence_full_row_sql(tx_id: str) -> str:
    return f"SELECT * FROM marketplace_ledger_v1 WHERE id_transaccion='{tx_id}'"


def evidence_detalle_sql(detalle: str, p_start: str, p_end: str) -> str:
    return f"SELECT monto FROM marketplace_ledger_v1 WHERE detalle='{detalle}' AND fecha BETWEEN '{p_start}' AND '{p_end}'"
