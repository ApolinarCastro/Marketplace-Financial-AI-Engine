"""Traceability Engine — Transaction traceability via inline SQL.

Provides:
- trace_transaction(): full evidence chain for a single transaction
- search_transactions(): filtered search with pagination
- trace_by_order(): all transactions for an order
- evidence_chain(): structured evidence steps (RAW→ETL→Ledger→Classif→Cierre→XML→Settlement)
- sap_reconciliation(): cross-reference marketplace transactions vs SAP data

Uses inline SQL (not a persisted VIEW) to avoid DB state issues.
"""

from __future__ import annotations
import math
import calendar
from typing import Any
import pandas as pd
from engine.v4.database import DatabaseV4


TX_VIEW_SQL = """
SELECT
    l.marketplace,
    l.id_transaccion,
    l.id_orden,
    l.fecha,
    l.detalle,
    l.monto,
    l.tipo_movimiento,
    l.financial_group,
    COALESCE(l.include_in_operational_pnl, TRUE) AS in_operational_pnl,
    l.archivo_origen,
    l.folio_xml,
    l.clasificacion_operativa,
    l.monto_bruto,
    l.comision_marketplace,
    c.confianza_clasificacion,
    c.origen_clasificacion,
    c.financial_subgroup,
    ci.total_ingresos AS cierre_ingresos,
    ci.total_costos_operacionales AS cierre_costos_operacionales,
    ci.total_costos_comerciales AS cierre_costos_comerciales,
    ci.total_ajustes AS cierre_ajustes,
    ci.resultado_neto AS cierre_resultado_neto,
    dtl.dte_folio,
    dtl.dte_monto,
    dtl.dte_fecha,
    dtl.emisor_nombre,
    dtl.emisor_rut,
    dtl.tipo_dte,
    COALESCE(dtl.dte_linked, 0) AS has_dte_link,
    lib.release_date,
    lib.released_amount,
    aud.check_name AS audit_check,
    aud.condition_detected AS audit_condition,
    aud.action_taken AS audit_action,
    CASE
        WHEN l.archivo_origen IS NOT NULL AND l.archivo_origen != '' THEN 'TRACED'
        ELSE 'UNTRACED'
    END AS trace_status,
    CASE
        WHEN dtl.dte_linked = 1 THEN 'DTE_CERTIFIED'
        WHEN l.folio_xml IS NOT NULL AND l.folio_xml != '' THEN 'HAS_FOLIO'
        ELSE 'NO_DOCUMENT'
    END AS document_status
FROM marketplace_ledger_v1 l
LEFT JOIN marketplace_ledger_clasificado_v1 c
    ON l.marketplace = c.marketplace AND l.id_transaccion = c.id_transaccion
LEFT JOIN dte_ledger_link dtl
    ON l.marketplace = dtl.marketplace AND l.id_transaccion = dtl.id_transaccion
LEFT JOIN liberaciones lib
    ON l.id_orden = lib.order_id AND l.marketplace = lib.marketplace
LEFT JOIN marketplace_auditoria_v1 aud
    ON l.marketplace = aud.marketplace AND l.id_orden = aud.order_id
LEFT JOIN marketplace_cierre_financiero_v1 ci
    ON l.marketplace = ci.marketplace
    AND l.fecha >= ci.periodo_inicio
    AND l.fecha <= ci.periodo_fin
"""


def _clean(r: dict) -> dict:
    """Sanitize NaN/NaT/inf for JSON serialization."""
    out = {}
    for k, v in r.items():
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            out[k] = None
        elif pd.isna(v):
            out[k] = None
        elif hasattr(v, 'isoformat'):
            out[k] = v.isoformat()
        else:
            out[k] = v
    return out


def _response(data: list[dict] | dict, meta: dict | None = None) -> dict:
    resp = {"data": data, "total": len(data) if isinstance(data, list) else 1}
    if meta:
        resp["meta"] = meta
    return resp


def trace_transaction(marketplace: str, tx_id: str) -> dict:
    """Full evidence chain for a single transaction."""
    db = DatabaseV4.get()
    df = db.query(
        f"SELECT * FROM ({TX_VIEW_SQL}) sub "
        "WHERE LOWER(marketplace) = LOWER(?) AND id_transaccion = ?",
        [marketplace, tx_id]
    )
    if df.empty:
        return _response([], {"error": f"Transaction {tx_id} not found for {marketplace}"})

    rows = [_clean(r) for r in df.to_dict("records")]
    return _response(rows)


def search_transactions(
    marketplace: str | None = None,
    query: str | None = None,
    fecha_desde: str | None = None,
    fecha_hasta: str | None = None,
    financial_group: str | None = None,
    trace_status: str | None = None,
    document_status: str | None = None,
    has_dte: bool | None = None,
    offset: int = 0,
    limit: int = 100
) -> dict:
    """Search with filters and pagination."""
    db = DatabaseV4.get()
    conditions = []
    params = []

    if marketplace:
        conditions.append("LOWER(marketplace) = LOWER(?)")
        params.append(marketplace)
    if query:
        conditions.append("(id_transaccion LIKE ? OR id_orden LIKE ? OR detalle LIKE ? OR archivo_origen LIKE ?)")
        q = f"%{query}%"
        params.extend([q, q, q, q])
    if fecha_desde:
        conditions.append("fecha >= ?")
        params.append(fecha_desde)
    if fecha_hasta:
        conditions.append("fecha <= ?")
        params.append(fecha_hasta)
    if financial_group:
        conditions.append("LOWER(financial_group) = LOWER(?)")
        params.append(financial_group)
    if trace_status:
        conditions.append("trace_status = ?")
        params.append(trace_status.upper())
    if document_status:
        conditions.append("document_status = ?")
        params.append(document_status.upper())
    if has_dte is True:
        conditions.append("has_dte_link = 1")
    elif has_dte is False:
        conditions.append("has_dte_link = 0 AND folio_xml IS NOT NULL AND folio_xml != ''")

    where = " AND ".join(conditions) if conditions else "1=1"

    count_df = db.query(
        f"SELECT COUNT(*) AS cnt FROM ({TX_VIEW_SQL}) sub WHERE {where}", params
    )
    total = int(count_df["cnt"].iloc[0])

    df = db.query(
        f"SELECT * FROM ({TX_VIEW_SQL}) sub WHERE {where} ORDER BY fecha DESC LIMIT ? OFFSET ?",
        params + [limit, offset]
    )
    rows = [_clean(r) for r in df.to_dict("records")]
    return _response(rows, {"offset": offset, "limit": limit, "total": total})


def trace_by_order(marketplace: str, order_id: str) -> dict:
    """All transactions for a given order."""
    return search_transactions(marketplace=marketplace, query=order_id)


def evidence_chain(marketplace: str, tx_id: str) -> dict:
    """Structured evidence steps for a transaction."""
    tx = trace_transaction(marketplace, tx_id)
    if not tx["data"]:
        return tx

    record = tx["data"][0]

    steps = [
        {
            "step": 1, "layer": "RAW", "label": "Archivo Original",
            "source": record.get("archivo_origen"),
            "status": "TRACED" if record.get("archivo_origen") else "UNTRACED",
        },
        {
            "step": 2, "layer": "ETL", "label": "Carga a Ledger",
            "transaction_id": record.get("id_transaccion"),
            "detail": record.get("detalle"), "amount": record.get("monto"),
            "status": "TRACED" if record.get("monto") is not None else "UNTRACED",
        },
        {
            "step": 3, "layer": "LEDGER", "label": "Registro en Ledger",
            "marketplace": record.get("marketplace"),
            "financial_group": record.get("financial_group"),
            "movement_type": record.get("tipo_movimiento"),
            "status": "VERIFIED" if record.get("financial_group") else "UNTRACED",
        },
        {
            "step": 4, "layer": "CLASSIFICATION", "label": "Clasificación Financiera",
            "confidence": record.get("confianza_clasificacion"),
            "classification_source": record.get("origen_clasificacion"),
            "operational_classification": record.get("clasificacion_operativa"),
            "in_operational_pnl": record.get("in_operational_pnl"),
            "financial_subgroup": record.get("financial_subgroup"),
            "status": "CERTIFIED" if record.get("confianza_clasificacion") is not None else "UNTRACED",
        },
        {
            "step": 5, "layer": "CIERRE", "label": "Cierre Financiero",
            "total_ingresos": record.get("cierre_ingresos"),
            "total_costos_operacionales": record.get("cierre_costos_operacionales"),
            "total_ajustes": record.get("cierre_ajustes"),
            "resultado_neto": record.get("cierre_resultado_neto"),
            "status": "CERTIFIED" if record.get("cierre_resultado_neto") is not None else "UNTRACED",
        },
        {
            "step": 6, "layer": "XML", "label": "Respaldo DTE",
            "folio": record.get("dte_folio") or record.get("folio_xml"),
            "tipo_dte": record.get("tipo_dte"),
            "emisor": record.get("emisor_nombre"),
            "emisor_rut": record.get("emisor_rut"),
            "dte_monto": record.get("dte_monto"),
            "dte_fecha": record.get("dte_fecha"),
            "status": record.get("document_status", "NO_DOCUMENT"),
        },
        {
            "step": 7, "layer": "SETTLEMENT", "label": "Liquidación",
            "release_date": record.get("release_date"),
            "released_amount": record.get("released_amount"),
            "status": "TRACED" if record.get("release_date") else "NOT_AVAILABLE",
        },
        {
            "step": 8, "layer": "AUDIT", "label": "Auditoría",
            "check": record.get("audit_check"),
            "condition": record.get("audit_condition"),
            "action": record.get("audit_action"),
            "status": "AUDITED" if record.get("audit_check") else "NOT_AUDITED",
        },
    ]

    trace_status = record.get("trace_status", "UNTRACED")
    overall = "COMPLETE" if all(
        s["status"] not in ("UNTRACED", "NOT_AVAILABLE", "NO_DOCUMENT", "NOT_AUDITED")
        for s in steps
    ) else "PARTIAL"

    return _response({
        "transaction": record,
        "evidence_chain": steps,
        "trace_status": trace_status,
        "overall_status": overall,
    })


def traceability_summary() -> dict:
    """Aggregate statistics from all traceability layers."""
    db = DatabaseV4.get()
    df = db.query(f"""
        SELECT
            marketplace,
            trace_status,
            document_status,
            COUNT(*) AS count,
            SUM(CASE WHEN has_dte_link = 1 THEN 1 ELSE 0 END) AS with_dte,
            COUNT(DISTINCT archivo_origen) AS source_files
        FROM ({TX_VIEW_SQL}) sub
        GROUP BY marketplace, trace_status, document_status
        ORDER BY marketplace, trace_status, document_status
    """)
    rows = [_clean(r) for r in df.to_dict("records")]
    return _response(rows, {"description": "Traceability summary per marketplace"})


def sap_reconciliation(period: str | None = None) -> dict:
    """Cross-reference marketplace vs SAP data.
    Note: SAP data is not yet loaded into the DB.
    Returns current traceability coverage as baseline."""
    db = DatabaseV4.get()
    conditions = []
    params = []
    if period:
        year, month = period.split("-")
        last_day = calendar.monthrange(int(year), int(month))[1]
        conditions.append("fecha >= ?")
        params.append(f"{year}-{month}-01")
        conditions.append("fecha <= ?")
        params.append(f"{year}-{month}-{last_day}")

    where = " AND ".join(conditions) if conditions else "1=1"

    df = db.query(f"""
        SELECT
            marketplace,
            COUNT(*) AS total_transactions,
            SUM(ABS(monto)) AS total_volume,
            SUM(CASE WHEN trace_status = 'TRACED' THEN 1 ELSE 0 END) AS traced,
            SUM(CASE WHEN document_status = 'DTE_CERTIFIED' THEN 1 ELSE 0 END) AS dte_certified,
            SUM(CASE WHEN document_status = 'HAS_FOLIO' THEN 1 ELSE 0 END) AS has_folio,
            SUM(CASE WHEN release_date IS NOT NULL THEN 1 ELSE 0 END) AS has_settlement,
            COUNT(DISTINCT archivo_origen) AS source_files
        FROM ({TX_VIEW_SQL}) sub
        WHERE {where}
        GROUP BY marketplace
        ORDER BY marketplace
    """, params)
    rows = [_clean(r) for r in df.to_dict("records")]
    return _response(rows, {
        "period": period or "ALL",
        "note": "SAP data not yet loaded. These are marketplace-side traceability metrics.",
    })
