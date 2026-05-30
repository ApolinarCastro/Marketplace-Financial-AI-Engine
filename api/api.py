from __future__ import annotations
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

    conditions.append("COALESCE(include_in_operational_pnl, 1) = 1")

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
def get_marketplace_cierre_desglose(marketplace: str = "ML", periodo: str | None = None):
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
          AND COALESCE(include_in_operational_pnl, 1) = 1
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
def index():
    dashboard_path = ROOT / "templates" / "dashboard.html"
    if dashboard_path.exists():
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>Dashboard no encontrado</h1>", status_code=404)

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


