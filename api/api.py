from __future__ import annotations
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles
import re

def validate_periodo(periodo: str | None) -> None:
    if not periodo:
        return
    if periodo in ("undefined", "null"):
        raise HTTPException(status_code=400, detail="Invalid periodo: " + periodo)
    if periodo != "YTD" and not re.match(r'^\d{4}-\d{2}$', periodo):
        raise HTTPException(status_code=400, detail="Invalid periodo format. Expected YYYY-MM or YTD.")
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.dte_indexer import DTEIndexer

ROOT = Path(__file__).resolve().parent.parent

def clean_records(df: pd.DataFrame) -> list[dict]:
    import math
    records = df.to_dict(orient="records")
    clean_recs = []
    for r in records:
        clean_r = {}
        for k, v in r.items():
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                clean_r[k] = None
            elif pd.isna(v):
                clean_r[k] = None
            elif hasattr(v, 'isoformat'):
                clean_r[k] = v.isoformat()
            else:
                clean_r[k] = v
        clean_recs.append(clean_r)
    return clean_recs

app = FastAPI(title="Marketplace Financial Auditor", version="3.5", description="Surgical Financial Truth Engine")

# CORS and basic config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount shared frontend assets
shared_dir = ROOT / "frontend" / "shared"
shared_dir.mkdir(parents=True, exist_ok=True)
app.mount("/shared", StaticFiles(directory=str(shared_dir)), name="shared")

@app.get("/api/v4/ledger")
def get_marketplace_ledger(
    marketplace: str = "ML",
    periodo: str | None = None,
    financial_group: str | None = None,
    clasificacion_operativa: str | None = None,
    detalle: str | None = None,
    offset: int = 0,
    limit: int = 200,
    filter_zero: bool = True,
    order_id: str | None = None
):
    validate_periodo(periodo)
    db = DatabaseV4.get()

    conditions = ["marketplace = ?"]
    params = [marketplace]

    if order_id:
        conditions.append("(id_transaccion = ? OR id_orden = ?)")
        params.extend([order_id, order_id])
    else:
        if periodo:
            year, month = periodo.split("-")
            import calendar
            last_day = calendar.monthrange(int(year), int(month))[1]
            conditions.append("fecha >= ?")
            params.append(f"{year}-{month}-01")
            conditions.append("fecha <= ?")
            params.append(f"{year}-{month}-{last_day}")

    if financial_group:
        conditions.append("financial_group = ?")
        params.append(financial_group)

    if clasificacion_operativa:
        conditions.append("clasificacion_operativa = ?")
        params.append(clasificacion_operativa)

    if detalle:
        conditions.append("detalle LIKE ?")
        params.append(f"%{detalle}%")


    if filter_zero:
        conditions.append("monto != 0")

    where = " AND ".join(conditions)

    agg = db.query(
        f"SELECT COUNT(*) as cnt, COALESCE(SUM(monto), 0) as sm FROM marketplace_ledger_v1 WHERE {where}",
        params
    )
    total_count = int(agg.iloc[0, 0])
    total_sum = float(agg.iloc[0, 1])

    df = db.query(
        f"SELECT * FROM marketplace_ledger_v1 WHERE {where} ORDER BY fecha DESC LIMIT ? OFFSET ?",
        params + [limit, offset]
    )

    detalles_df = db.query(
        f"SELECT DISTINCT detalle FROM marketplace_ledger_v1 WHERE {where} AND detalle IS NOT NULL ORDER BY detalle",
        params
    )
    detalles = [str(r['detalle']) for _, r in detalles_df.iterrows()]

    return {
        "data": clean_records(df),
        "total_count": total_count,
        "total_sum": total_sum,
        "offset": offset,
        "limit": limit,
        "detalles": detalles
    }

@app.get("/api/v4/cierre")
def get_marketplace_cierre(marketplace: str = "ML", periodo: str | None = None):
    validate_periodo(periodo)
    db = DatabaseV4.get()
    if periodo:
        # periodo = "2024-03"
        year, month = periodo.split("-")
        p_ini = f"{year}-{month}-01"
        df = db.query(
            "SELECT * FROM marketplace_cierre_financiero_v1 WHERE marketplace = ? AND periodo_inicio = ? ORDER BY created_at DESC LIMIT 1",
            [marketplace, p_ini]
        )
    else:
        df = db.query(
            "SELECT * FROM marketplace_cierre_financiero_v1 WHERE marketplace = ? ORDER BY periodo_inicio DESC LIMIT 1",
            [marketplace]
        )
    return clean_records(df)

@app.get("/api/v4/cierre/desglose")
def get_marketplace_cierre_desglose(marketplace: str = "ML", periodo: str | None = None, exclude_non_operational: bool = False):
    validate_periodo(periodo)
    db = DatabaseV4.get()

    if not periodo:
        df_period = db.query("SELECT MAX(fecha) as mx FROM marketplace_ledger_v1 WHERE marketplace = ?", [marketplace])
        if df_period.empty or pd.isna(df_period.iloc[0]['mx']):
            return []
        mx = pd.to_datetime(df_period.iloc[0]['mx'])
        periodo = f"{mx.year}-{mx.month:02d}"

    year, month = periodo.split("-")
    import calendar
    last_day = calendar.monthrange(int(year), int(month))[1]
    p_ini = f"{year}-{month}-01"
    p_fin = f"{year}-{month}-{last_day}"

    sql = """
        SELECT 
            COALESCE(financial_group, 'sin_clasificar') as financial_group,
            detalle,
            tipo_movimiento,
            clasificacion_operativa,
            SUM(COALESCE(monto, 0)) as total,
            COUNT(*) as cantidad
        FROM marketplace_ledger_v1
        WHERE marketplace = ?
          AND fecha BETWEEN ? AND ?
    """
    if exclude_non_operational:
        sql += " AND COALESCE(include_in_operational_pnl, 1) = 1"
    
    sql += """
        GROUP BY financial_group, detalle, tipo_movimiento, clasificacion_operativa
        ORDER BY total ASC
    """
    df = db.query(sql, [marketplace, p_ini, p_fin])

    records = []
    for _, row in df.iterrows():
        detalle_val = str(row['detalle']) if not pd.isna(row['detalle']) else ""
        records.append({
            "detalle": detalle_val,
            "clasificacion_operativa": str(row['clasificacion_operativa']) if not pd.isna(row['clasificacion_operativa']) else detalle_val,
            "tipo_movimiento": row['tipo_movimiento'],
            "total": float(row['total']),
            "cantidad": int(row['cantidad']),
            "categoria": str(row['financial_group']),
            "is_legacy_360": True
        })

    return records

@app.get("/api/v4/dte/count")
def get_dte_count():
    db = DatabaseV4.get()
    return {"count": db.count("dte_truth_v1")}

@app.get("/api/v4/dte/samples")
def get_dte_samples(limit: int = 10):
    db = DatabaseV4.get()
    df = db.query("SELECT * FROM dte_truth_v1 LIMIT ?", [limit])
    return clean_records(df)

@app.get("/api/v4/test_regex")
def diag_regex(val: str = "033-0013380337"):
    db = DatabaseV4.get()
    res = db.query("SELECT regexp_replace(?, '^[0-9]+-0*', '') as norm", [val]).iloc[0]['norm']
    exists = db.query("SELECT count(*) as n FROM dte_truth_v1 WHERE folio = ?", [res]).iloc[0]['n']
    
    # Check join
    sql = """
        SELECT COUNT(*) as n
        FROM marketplace_ledger_v1 l
        JOIN dte_truth_v1 t ON l.folio_xml LIKE '%' || t.folio
        WHERE l.folio_xml = ?
    """
    matches = db.query(sql, [val]).iloc[0]['n']
    
    # Check sum of ledger amounts
    sql_sum = "SELECT SUM(ABS(monto)) as total_ledger FROM marketplace_ledger_v1 WHERE folio_xml = ?"
    total_ledger = db.query(sql_sum, [val]).iloc[0]['total_ledger']
    
    # Get XML total
    sql_xml = "SELECT monto_total FROM dte_truth_v1 WHERE folio = ?"
    monto_xml = db.query(sql_xml, [res]).iloc[0]['monto_total'] if int(exists) > 0 else 0
    
    return {
        "original": val, 
        "normalized": res, 
        "exists_in_truth": int(exists) > 0,
        "ledger_matches_in_truth": int(matches),
        "total_ledger_sum": float(total_ledger or 0),
        "total_xml_amount": float(monto_xml),
        "diff": float(monto_xml) - float(total_ledger or 0)
    }


@app.get("/api/v4/dte/certify")
def get_certification(marketplace: str = "ALL"):
    from engine.v4.certification.document_certification import DocumentCertificationEngine
    engine = DocumentCertificationEngine()
    if marketplace == "ALL":
        return engine.get_all_certifications()
    return engine.get_certification(marketplace)

@app.get("/api/v4/dte/document-gap")
def get_document_gaps(marketplace: str = None, limit: int = 500):
    from engine.v4.certification.document_gap_engine import DocumentGapEngine
    engine = DocumentGapEngine()
    return engine.get_document_gaps(marketplace, limit)

@app.get("/api/v4/dte/document/{transaction_id}")
def get_document_detail(transaction_id: str):
    from engine.v4.certification.document_gap_engine import DocumentGapEngine
    engine = DocumentGapEngine()
    # Mocking single document retrieval for now
    gaps = engine.get_document_gaps(limit=1000)
    for g in gaps:
        if g['transaction_id'] == transaction_id:
            return g
    return {"error": "Document not found"}

@app.get("/api/v4/dte/risk-summary")
def get_risk_summary():
    from engine.v4.certification.document_gap_engine import DocumentGapEngine
    engine = DocumentGapEngine()
    return engine.get_risk_summary()


_DTE_LIMITATIONS = {
    "ml": "Cobertura mixta: exec/summary (51.5pct sin op_pnl) vs financial-structure (94.2pct con op_pnl). Cobertura real depende del filtro operacional aplicado.",
    "ripley": "P19A_003_R1: TRACEABILITY_VERIFIED. Cadena settlement verificada: 48/48 SELLER-CICLOS, 167 settlement_refs en 3 etapas, 52802 ordenes, 219901 filas (97.3pct). DTE SII: 3/407 coinciden con settlement_ref. Los folios DTE son externos al sistema de numeracion Ripley.",
    "paris": "P19A_002: 31/31 DTE folios vinculados (dte_ledger_link). 62 XMLs indexados, 47992/74028 filas con folio_xml.",
    "falabella": "P19A_002: 6/6 DTE folios vinculados (dte_ledger_link). 6 XMLs indexados, 1118/2609 filas con folio_xml."
}


import calendar

def _resolve_period_range(periodo):
    if not periodo or periodo.upper() == "YTD":
        db = DatabaseV4.get()
        latest = db.query("SELECT MAX(periodo_inicio) as mx FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0")
        mx = latest.iloc[0]["mx"]
        if pd.notna(mx):
            mx = pd.to_datetime(mx)
            return (f"{mx.year}-01-01", None, f"{mx.year}-YTD")
        return ("2024-01-01", None, "2024-YTD")
    parts = periodo.split("-")
    if len(parts) == 2:
        year, month = parts
        last_day = calendar.monthrange(int(year), int(month))[1]
        return (f"{year}-{month}-01", f"{year}-{month}-{last_day}", f"{year}-{month}")
    return (periodo, None, periodo)


@app.get("/api/v4/periodos")
def get_periodos():
    db = DatabaseV4.get()
    months = db.query("SELECT periodo_inicio, periodo_fin, marketplace FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0 ORDER BY periodo_inicio DESC")
    periods = []
    seen = set()
    for _, r in months.iterrows():
        key = str(r["periodo_inicio"])[:7]
        if key not in seen:
            seen.add(key)
            periods.append({"periodo": key, "periodo_inicio": str(r["periodo_inicio"])[:10], "label": key})
    return periods


def get_operational_filters(marketplace: str | None = None) -> str:
    """Returns the SQL fragment for enforcing the Single Financial Truth operational perimeter."""
    sql = " AND COALESCE(include_in_operational_pnl, 1) = 1 AND financial_group IS NOT NULL "
    mp_lower = marketplace.lower() if marketplace and marketplace.upper() != "ALL" else "all"
    
    if mp_lower == "ripley":
        sql += " AND detalle != 'order_amount' "
    elif mp_lower == "paris":
        sql += " AND detalle != 'Despacho' "
    elif mp_lower == "all":
        # When querying all marketplaces, we must apply the exclusions conditionnally
        sql += " AND NOT (LOWER(marketplace) = 'ripley' AND detalle = 'order_amount') "
        sql += " AND NOT (LOWER(marketplace) = 'paris' AND detalle = 'Despacho') "
        
    return sql


@app.get("/api/v4/exec/summary")
def get_exec_summary(periodo: str | None = None, marketplace: str | None = None):
    validate_periodo(periodo)
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)
    mp_filter = ""
    mp_params = []
    if marketplace and marketplace.upper() != "ALL":
        mp_filter = "AND marketplace = ?"
        mp_params = [marketplace.upper()]
    if date_end is None:
        ld_where = f"fecha >= ? {mp_filter}"
        ld_params = [date_start] + mp_params
    else:
        ld_where = f"fecha BETWEEN ? AND ? {mp_filter}"
        ld_params = [date_start, date_end] + mp_params
        
    op_filters = get_operational_filters(marketplace)
    
    sql_neto = f"SELECT COALESCE(SUM(monto), 0) as neto FROM marketplace_ledger_v1 WHERE {ld_where} {op_filters}"
    neto = float(db.query(sql_neto, ld_params).iloc[0]["neto"])
    
    r = db.query(f"SELECT COALESCE(SUM(CASE WHEN financial_group='ingresos' THEN monto ELSE 0 END), 0) as gross_sales, COALESCE(SUM(CASE WHEN financial_group='devoluciones' THEN monto ELSE 0 END), 0) as devoluciones, COALESCE(SUM(CASE WHEN financial_group IN ('costos_operacionales','costos_comerciales') THEN monto ELSE 0 END), 0) as costos_op, COALESCE(SUM(CASE WHEN financial_group='comisiones' THEN monto ELSE 0 END), 0) as comisiones, COALESCE(SUM(CASE WHEN financial_group='ajustes' THEN monto ELSE 0 END), 0) as ajustes, COALESCE(SUM(CASE WHEN financial_group='recuperaciones_y_bonificaciones' THEN monto ELSE 0 END), 0) as recuperaciones FROM marketplace_ledger_v1 WHERE {ld_where} {op_filters}", ld_params).iloc[0]
    gross = float(r["gross_sales"])
    returns = float(r["devoluciones"])
    costs_op = float(r["costos_op"])
    comms = float(r["comisiones"])
    adj = float(r["ajustes"])
    recup = float(r["recuperaciones"])
    
    per_mp = {}
    for mp in ["ML", "RIPLEY", "PARIS", "FALABELLA"]:
        mp_op_filters = get_operational_filters(mp)
        sql_mp_neto = f"SELECT COALESCE(SUM(monto), 0) as neto FROM marketplace_ledger_v1 WHERE {ld_where} AND LOWER(marketplace) = ? {mp_op_filters}"
        neto_mp = float(db.query(sql_mp_neto, ld_params + [mp.lower()]).iloc[0]["neto"])
        
        r2 = db.query(f"SELECT COALESCE(SUM(CASE WHEN financial_group='ingresos' THEN monto ELSE 0 END), 0) as gross, COALESCE(SUM(CASE WHEN financial_group='devoluciones' THEN monto ELSE 0 END), 0) as devs, COALESCE(SUM(CASE WHEN financial_group IN ('costos_operacionales','costos_comerciales','comisiones','ajustes','recuperaciones_y_bonificaciones') THEN monto ELSE 0 END), 0) as costs FROM marketplace_ledger_v1 WHERE {ld_where} AND LOWER(marketplace) = ? {mp_op_filters}", ld_params + [mp.lower()]).iloc[0]
        per_mp[mp] = {"ingresos": float(r2["gross"]), "devoluciones": float(r2["devs"]), "costos": float(r2["costs"]), "neto": neto_mp}
        
    return {"period": label, "marketplace": marketplace or "ALL", "gross_sales": gross, "devoluciones": returns, "costos_operacionales": costs_op, "comisiones": comms, "ajustes": adj, "recuperaciones": recup, "neto": neto, "per_marketplace": per_mp}


@app.get("/api/v4/financial-structure")
def get_financial_structure(marketplace: str = "ALL", periodo: str | None = None):
    validate_periodo(periodo)
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)
    mp_filter = ""
    mp_params = []
    if marketplace and marketplace.upper() != "ALL":
        mp_filter = "AND marketplace = ?"
        mp_params = [marketplace.upper()]
    if date_end is None:
        ld_where = f"fecha >= ? {mp_filter}"
        ld_params = [date_start] + mp_params
    else:
        ld_where = f"fecha BETWEEN ? AND ? {mp_filter}"
        ld_params = [date_start, date_end] + mp_params
    op_filters = get_operational_filters(marketplace)
    sql = f"SELECT financial_group, clasificacion_operativa, detalle, SUM(COALESCE(monto, 0)) as total, COUNT(*) as cantidad FROM marketplace_ledger_v1 WHERE {ld_where} {op_filters} GROUP BY financial_group, clasificacion_operativa, detalle ORDER BY financial_group, total ASC"
    df = db.query(sql, ld_params)
    groups = {}
    group_order = {"ingresos": 1, "devoluciones": 2, "comisiones": 3, "costos_operacionales": 4, "costos_comerciales": 5, "ajustes": 6, "recuperaciones_y_bonificaciones": 7, "tesoreria": 8, "flujo_de_caja": 9, "cash_management": 10, "impuestos": 11, "costos_financieros": 12}
    for _, row in df.iterrows():
        fg = str(row["financial_group"])
        if fg not in groups:
            groups[fg] = {"financial_group": fg, "display_name": fg.replace("_", " ").title(), "total": 0.0, "orden": group_order.get(fg, 99), "items": []}
        monto = float(row["total"])
        groups[fg]["total"] += monto
        groups[fg]["items"].append({"detalle": str(row["detalle"]) if not pd.isna(row["detalle"]) else "", "clasificacion_operativa": str(row["clasificacion_operativa"]) if not pd.isna(row["clasificacion_operativa"]) else "", "monto": monto, "cantidad": int(row["cantidad"])})
    categories = sorted(groups.values(), key=lambda x: x["orden"])
    for cat in categories:
        cat["subcategories"] = [{"detalle": item["detalle"], "total": item["monto"]} for item in cat["items"]]
    return {"period": label, "marketplace": marketplace, "categories": categories}


@app.get("/api/v4/exec/waterfall-v3")
def get_exec_waterfall_v3(marketplace: str | None = None, periodo: str | None = None):
    validate_periodo(periodo)
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)
    mp_filter = ""
    mp_params = []
    if marketplace and marketplace.upper() != "ALL":
        mp_filter = "AND marketplace = ?"
        mp_params = [marketplace.upper()]
    if date_end is None:
        ld_where = f"fecha >= ? {mp_filter}"
        ld_params = [date_start] + mp_params
    else:
        ld_where = f"fecha BETWEEN ? AND ? {mp_filter}"
        ld_params = [date_start, date_end] + mp_params
    
    op_filters = get_operational_filters(marketplace)
    
    stages = [("Ingresos Brutos", "ingresos", 1), ("Devoluciones", "devoluciones", -1), ("Comisiones", "comisiones", -1), ("Costos Operacionales", "costos_operacionales", -1), ("Costos Comerciales", "costos_comerciales", -1), ("Ajustes", "ajustes", 1), ("Recuperaciones", "recuperaciones_y_bonificaciones", 1)]
    values = []
    labels_list = []
    
    for display_name, fg, sign in stages:
        r = db.query(f"SELECT COALESCE(SUM(monto), 0) as total FROM marketplace_ledger_v1 WHERE financial_group = ? {op_filters} AND {ld_where}", [fg] + ld_params).iloc[0]
        val = float(r["total"])
        values.append(val)
        labels_list.append(display_name)
        
    sql_neto = f"SELECT COALESCE(SUM(monto), 0) as neto FROM marketplace_ledger_v1 WHERE {ld_where} {op_filters}"
    running = float(db.query(sql_neto, ld_params).iloc[0]["neto"])
    
    return {"period": label, "marketplace": marketplace or "ALL", "labels": labels_list, "values": values, "resultado_neto": running}


@app.get("/api/v4/executive/insights")
def get_executive_insights(marketplace: str | None = None):
    db = DatabaseV4.get()
    df = db.query("SELECT * FROM marketplace_auditoria_v1 ORDER BY detected_at DESC LIMIT 10")
    insights = []
    for _, r in df.iterrows():
        insights.append({"id": str(r.get("order_id", "")), "check_name": str(r.get("check_name", "")), "condition": str(r.get("condition_detected", "")), "action": str(r.get("action_taken", "")), "detected_at": str(r.get("detected_at", ""))})
    return {"insights": insights, "count": len(insights)}


@app.get("/api/v4/intelligence/anomalies")
def get_anomalies(limit: int = 20):
    db = DatabaseV4.get()
    df = db.query("SELECT * FROM marketplace_auditoria_v1 ORDER BY detected_at DESC LIMIT ?", [limit])
    anomalies = []
    for _, r in df.iterrows():
        anomalies.append({"id": str(r.get("order_id", "")), "check_name": str(r.get("check_name", "")), "condition": str(r.get("condition_detected", "")), "action": str(r.get("action_taken", "")), "detected_at": str(r.get("detected_at", ""))})
    return {"anomalies": anomalies, "count": len(anomalies)}

@app.get("/api/v4/intelligence/insights")
def get_intelligence_insights(marketplace: str | None = None):
    db = DatabaseV4.get()
    mp_filter = ""
    mp_params = []
    if marketplace and marketplace.upper() != "ALL":
        mp_filter = "AND LOWER(marketplace) = ?"
        mp_params = [marketplace.lower()]
    df = db.query(f"SELECT * FROM marketplace_auditoria_v1 WHERE 1=1 {mp_filter} ORDER BY detected_at DESC LIMIT 10", mp_params)
    insights = []
    for _, r in df.iterrows():
        insights.append({
            "id": str(r.get("order_id", "")),
            "check_name": str(r.get("check_name", "")),
            "condition": str(r.get("condition_detected", "")),
            "action": str(r.get("action_taken", "")),
            "detected_at": str(r.get("detected_at", ""))
        })
    return {"insights": insights, "count": len(insights)}


@app.get("/api/v4/intelligence/returns")
def get_intelligence_returns(marketplace: str | None = None, periodo: str | None = None):
    validate_periodo(periodo)
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)
    mp_filter = ""
    mp_params = []
    if marketplace and marketplace.upper() != "ALL":
        mp_filter = "AND LOWER(marketplace) = ?"
        mp_params = [marketplace.lower()]
    if date_end is None:
        ld_where = f"fecha >= ? {mp_filter}"
        ld_params = [date_start] + mp_params
    else:
        ld_where = f"fecha BETWEEN ? AND ? {mp_filter}"
        ld_params = [date_start, date_end] + mp_params
    df = db.query(f"SELECT detalle, COUNT(*) as casos, SUM(monto) as total FROM marketplace_ledger_v1 WHERE financial_group = 'devoluciones' AND {ld_where} GROUP BY detalle ORDER BY total ASC LIMIT 10", ld_params)
    returns = []
    for _, r in df.iterrows():
        returns.append({
            "reason": str(r["detalle"]),
            "cases": int(r["casos"]),
            "impact": float(r["total"])
        })
    return {"returns": returns, "count": len(returns)}


@app.get("/api/v4/debug_audit")
def debug_audit(limit: int = 10):
    db = DatabaseV4.get()
    df = db.query("SELECT * FROM marketplace_auditoria_v1 LIMIT ?", [limit])
    return clean_records(df)

@app.get("/api/v4/auditoria")
def get_marketplace_auditoria(marketplace: str = "ML"):
    db = DatabaseV4.get()
    df = db.query("SELECT * FROM marketplace_auditoria_v1 WHERE marketplace = ?", [marketplace])
    return clean_records(df)

@app.post("/api/v4/correcciones")
def post_marketplace_correccion(data: dict):
    engine = MarketplaceAuditorEngine()
    try:
        engine.add_correction(
            id_transaccion=data.get('id_transaccion', 'GLOBAL'),
            detalle_original=data.get('detalle_original', ''),
            detalle_corregido=data['detalle_corregido'],
            motivo=data['motivo'],
            usuario=data.get('usuario', 'manual_api')
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/", response_class=HTMLResponse)
@app.get("/app", response_class=HTMLResponse)
@app.get("/documentary-dashboard", response_class=HTMLResponse)
def index():
    dashboard_path = ROOT / "templates" / "documentary_dashboard.html"
    if dashboard_path.exists():
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    return HTMLResponse("<h1>Dashboard no encontrado</h1>", status_code=404)

@app.get("/executive-dashboard", response_class=HTMLResponse)
def get_executive_dashboard():
    exec_path = ROOT / "templates" / "executive_dashboard.html"
    if exec_path.exists():
        with open(exec_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>Executive Dashboard no encontrado</h1>", status_code=404)

@app.get("/exec", response_class=HTMLResponse)
def exec_dashboard():
    exec_path = ROOT / "templates" / "executive_dashboard.html"
    if exec_path.exists():
        with open(exec_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>Executive Dashboard no encontrado</h1>", status_code=404)

@app.post("/api/v4/run-audit")
def run_full_audit(marketplace: str = "ML"):
    from engine.v4.run_initial_audit import load_marketplace_ledger_standalone
    from engine.v4.surgical_loader import SurgicalLoader
    from engine.v4.dte_indexer import DTEIndexer
    from engine.v4.surgical_xml_justifier import XMLJustifier
    
    try:
        db = DatabaseV4.get()
        # 1. Ingest all raw files for all marketplaces using standalone loader
        # 2. Run Vectorized Classification
        engine = MarketplaceAuditorEngine()
        engine.run_classification()
        
        # 3. Generate monthly financial closures from 2023 to 2026
        for year in [2023, 2024, 2025, 2026]:
            for month in range(1, 13):
                import calendar
                last_day = calendar.monthrange(year, month)[1]
                p_ini = f"{year}-{month:02d}-01"
                p_fin = f"{year}-{month:02d}-{last_day}"
                engine.run_financial_closing(marketplace, p_ini, p_fin)
                
        # 4. Run Audit alerts
        engine.run_audit()
        
        return {"status": "success", "message": f"Ingesta, Cruce DTE y Auditoría completadas para {marketplace}"}
    except Exception as e:
        import logging
        logging.getLogger("api").error(f"Error running audit for {marketplace}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v4/run-indexer")
def run_dte_indexer():
    indexer = DTEIndexer()
    try:
        n = indexer.run()
        return {"status": "success", "new_records": n}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

ALLOWED_SQL_PREFIXES = ("SELECT", "WITH", "DESCRIBE", "EXPLAIN")
BLOCKED_SQL_KEYWORDS = ("INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "ATTACH", "DETACH", "COPY", "EXECUTE", "CALL", "IMPORT", "EXPORT")

def validate_safe_query(sql: str) -> str:
    stripped = sql.strip().upper()
    if not any(stripped.startswith(p) for p in ALLOWED_SQL_PREFIXES):
        raise ValueError("SQL bloqueado: solo se permiten consultas SELECT/WITH")
    for kw in BLOCKED_SQL_KEYWORDS:
        if kw in stripped.split():
            raise ValueError(f"SQL bloqueado: palabra clave '{kw}' no permitida")
    return sql

@app.post("/api/v4/query")
def run_query(data: dict):
    sql = data.get("sql", "")
    if not sql:
        return {"error": "Campo 'sql' requerido"}
    db = DatabaseV4.get()
    try:
        validate_safe_query(sql)
        df = db.query(sql)
        records = df.to_dict(orient="records")
        import math
        clean_records = []
        for r in records:
            clean_r = {}
            for k, v in r.items():
                if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                    clean_r[k] = None
                elif pd.isna(v):
                    clean_r[k] = None
                else:
                    clean_r[k] = v
            clean_records.append(clean_r)
        return clean_records
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/v4/electronic_certification/validate")
async def validate_electronic_certification(request: __import__("fastapi").Request):
    from engine.v4.certification.ecc.ecc_adapter import ECCAdapter
    try:
        content = await request.body()
        xml_content = content.decode("utf-8", errors="ignore")
        marketplace = request.headers.get("X-Marketplace", "ML")
        adapter = ECCAdapter()
        payload = adapter.process(xml_content, marketplace=marketplace)
        return {"status": "success", "data": payload.to_dict()}
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

@app.post("/api/v4/knowledge/export")
def export_to_obsidian(payload_dict: dict):
    from engine.v4.certification.knowledge.obsidian_adapter import ObsidianAdapter
    try:
        adapter = ObsidianAdapter()
        adapter.export_evidence(payload_dict)
        return {"status": "success"}
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

