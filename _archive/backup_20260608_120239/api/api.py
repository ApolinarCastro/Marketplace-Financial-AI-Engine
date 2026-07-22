from __future__ import annotations
import os
import json
import base64
import hmac
import hashlib
import time
import math
import calendar
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.dte_indexer import DTEIndexer

ROOT = Path(__file__).resolve().parent.parent

# ── Auth Configuration ──
AUTH_ENABLED = os.environ.get("MFE_AUTH_ENABLED", "").lower() == "true"
API_KEY = os.environ.get("MFE_API_KEY", "")
JWT_SECRET = os.environ.get("MFE_JWT_SECRET", "change-me-in-production")

PUBLIC_PATHS = {"/", "/app", "/health", "/docs", "/openapi.json", "/redoc"}


def _b64_decode(data: str) -> bytes:
    padding = 4 - len(data) % 4
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data)


def verify_jwt(token: str) -> bool:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return False
        header_b64, payload_b64, sig_b64 = parts
        sig_bytes = _b64_decode(sig_b64)
        expected = hmac.new(
            JWT_SECRET.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256,
        ).digest()
        if not hmac.compare_digest(sig_bytes, expected):
            return False
        claims = json.loads(_b64_decode(payload_b64))
        exp = claims.get("exp", 0)
        if exp < time.time():
            return False
        return True
    except Exception:
        return False


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not AUTH_ENABLED:
            return await call_next(request)

        path = request.url.path.rstrip("/")
        if path in PUBLIC_PATHS or path.startswith("/app"):
            return await call_next(request)

        api_key = request.headers.get("X-API-Key", "")
        if api_key and api_key == API_KEY:
            return await call_next(request)

        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer ") and verify_jwt(auth[7:]):
            return await call_next(request)

        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized. Provide X-API-Key or Authorization: Bearer <jwt>"},
        )


def clean_records(df: pd.DataFrame) -> list[dict]:
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

RATE_LIMIT_REQUESTS = int(os.environ.get("MFE_RATE_LIMIT", "100"))
RATE_LIMIT_WINDOW = 60  # seconds
CORS_ORIGINS = os.environ.get("MFE_CORS_ORIGINS", "http://localhost:8003,http://127.0.0.1:8003").split(",")


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = RATE_LIMIT_REQUESTS, window: int = RATE_LIMIT_WINDOW):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self._clients: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        forwarded = request.headers.get("x-forwarded-for", "")
        client_ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "127.0.0.1")
        now = time.time()
        window_start = now - self.window
        if client_ip in self._clients:
            timestamps = [t for t in self._clients[client_ip] if t > window_start]
            self._clients[client_ip] = timestamps
            if len(timestamps) >= self.max_requests:
                return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Try again later."})
            self._clients[client_ip].append(now)
        else:
            self._clients[client_ip] = [now]
        return await call_next(request)


app = FastAPI(title="Marketplace Financial Auditor", version="3.5", description="Surgical Financial Truth Engine")

# Middleware stack (outermost first):
#   1. CORS — intercept OPTIONS preflight before any other middleware
#   2. Rate limit — prevent abuse before auth check
#   3. Auth — default deny for all non-public paths
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)

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
        year, month = periodo.split("-")
        y, m = int(year), int(month)
        last_day = calendar.monthrange(y, m)[1]
        p_fin = f"{y}-{m:02d}-{last_day}"
        df = db.query(
            "SELECT * FROM marketplace_cierre_financiero_v1 WHERE marketplace = ? AND periodo_fin = ? ORDER BY created_at DESC LIMIT 1",
            [marketplace, p_fin]
        )
    else:
        df = db.query(
            "SELECT * FROM marketplace_cierre_financiero_v1 WHERE marketplace = ? ORDER BY periodo_inicio DESC LIMIT 1",
            [marketplace]
        )
    return clean_records(df)

@app.get("/api/v4/cierre/desglose")
def get_marketplace_cierre_desglose(
    marketplace: str = "ML",
    periodo: str | None = None,
    exclude_non_operational: bool = False
):
    db = DatabaseV4.get()

    if not periodo:
        df_period = db.query("SELECT MAX(fecha) as mx FROM marketplace_ledger_v1 WHERE marketplace = ?", [marketplace])
        if df_period.empty or pd.isna(df_period.iloc[0]['mx']):
            return []
        mx = pd.to_datetime(df_period.iloc[0]['mx'])
        periodo = f"{mx.year}-{mx.month:02d}"

    year, month = periodo.split("-")
    last_day = calendar.monthrange(int(year), int(month))[1]
    p_ini = f"{year}-{month}-01"
    p_fin = f"{year}-{month}-{last_day}"

    exclude_clause = "AND financial_group IS NOT NULL" if exclude_non_operational else ""
    if marketplace == "ML":
        exclude_clause += " AND COALESCE(include_in_operational_pnl, 1) = 1"

    sql = f"""
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
          {exclude_clause}
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

@app.get("/health")
def health():
    db_ok = False
    try:
        db = DatabaseV4.get()
        db.execute("SELECT 1")
        db_ok = True
    except Exception:
        pass
    return {"status": "ok" if db_ok else "degraded", "database": "connected" if db_ok else "unreachable"}

@app.get("/exec", response_class=HTMLResponse)
def executive_dashboard():
    exec_path = ROOT / "templates" / "executive_dashboard.html"
    if exec_path.exists():
        with open(exec_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>Executive Dashboard no encontrado</h1>", status_code=404)


def _resolve_period_range(periodo: str | None) -> tuple:
    """Resolve period string to (date_start, date_end, label).
    
    - None or 'YTD': (year_start, None, 'YYYY-YTD') — open-ended from year start
    - 'YYYY-MM': (month_start, month_end, 'YYYY-MM') — exact month range
    """
    if not periodo or periodo.upper() == 'YTD':
        db = DatabaseV4.get()
        latest = db.query("SELECT MAX(periodo_inicio) as mx FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0")
        mx = latest.iloc[0]['mx']
        if pd.notna(mx):
            mx = pd.to_datetime(mx)
            return (f"{mx.year}-01-01", None, f"{mx.year}-YTD")
        return ("2026-01-01", None, "2026-YTD")
    year, month = periodo.split('-')
    y, m = int(year), int(month)
    last_day = calendar.monthrange(y, m)[1]
    return (f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last_day}", periodo)


_DETALLE_TO_CONCEPT = {
    'Cargo por venta (Comisión)': 'Comisiones',
    'Comisiones sobre pedidos': 'Comisiones',
    'Comisión por venta': 'Comisiones',
    'Comisiones': 'Comisiones',
    'Comisión de reembolso': 'Comisiones',
    'Cargo por envíos de Mercado Libre': 'Logística',
    'Cargo por Mercado Envíos': 'Logística',
    'Envío': 'Logística',
    'Gastos de envío (RIPLEY) pagados por el operador': 'Logística',
    'Gastos de envío (RIPLEY)': 'Logística',
    'Importe del envío del pedido': 'Logística',
    'Despacho': 'Logística',
    'Cobro por despacho': 'Logística',
    'Logística inversa': 'Logística',
    'Compensación logística': 'Logística',
    'Cofinanciamiento logístico': 'Logística',
    'Recargo por precio mínimo': 'Logística',
    'Descuento por costo logístico': 'Logística',
    'Descuento por logística inversa': 'Logística',
    'Mercado Envíos': 'Logística',
    'Descuento logistico': 'Logística',
    'Cobro por cofinanciamiento logistico': 'Logística',
    'Product Ads': 'Publicidad',
    'Cargo por publicidad': 'Publicidad',
    'Cargo por publicación': 'Publicidad',
    'Publicidad': 'Publicidad',
    'Costo de Marketing': 'Publicidad',
    'Cargo por Asesoría Comercial': 'Servicios',
    'Asesoría Comercial': 'Servicios',
    'Cargo por Mi Página': 'Servicios',
    'Mi Página': 'Servicios',
    'Full': 'Fulfillment',
    'Costo Full': 'Fulfillment',
    'Almacenamiento': 'Fulfillment',
    'Retiro stock': 'Fulfillment',
    'Stock antiguo': 'Fulfillment',
    'Cobro por almacenamiento': 'Fulfillment',
}


def _map_detalle_to_concept(detalle: str) -> str:
    if not detalle:
        return 'Otros'
    direct = _DETALLE_TO_CONCEPT.get(detalle)
    if direct:
        return direct
    lower = detalle.lower()
    for key, val in _DETALLE_TO_CONCEPT.items():
        if lower in key.lower() or key.lower() in lower:
            return val
    if 'bonificación' in lower or 'incentivo' in lower:
        return 'Bonificaciones'
    if 'comisión' in lower or 'comision' in lower:
        return 'Comisiones'
    if any(x in lower for x in ('envío', 'envio', 'logísti', 'logisti', 'despacho')):
        return 'Logística'
    if 'publicidad' in lower or 'ads' in lower:
        return 'Publicidad'
    if 'full' in lower or 'almacen' in lower:
        return 'Fulfillment'
    if 'asesoría' in lower or 'asesoria' in lower:
        return 'Servicios'
    return 'Otros'


_MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


@app.get("/api/v4/periodos")
def get_periodos():
    """Unified period list — single source of temporal truth for all dashboards."""
    db = DatabaseV4.get()
    df = db.query("""
        SELECT DISTINCT periodo_inicio
        FROM marketplace_cierre_financiero_v1
        WHERE resultado_neto != 0
        ORDER BY periodo_inicio DESC
    """)
    periodos = [{"value": "YTD", "label": "Year to Date"}]
    for _, r in df.iterrows():
        p = pd.to_datetime(r['periodo_inicio'])
        label = f"{_MONTHS[p.month - 1]} {p.year}"
        periodos.append({"value": f"{p.year}-{p.month:02d}", "label": label})
    return periodos


@app.get("/api/v4/exec/summary")
def get_exec_summary(periodo: str | None = None):
    """Consolidated executive summary — one period, one truth."""
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)

    if date_end is None:
        mx = db.query("SELECT MAX(periodo_inicio) as mx FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0")
        mx_val = mx.iloc[0]['mx']
        if pd.notna(mx_val):
            mx_dt = pd.to_datetime(mx_val)
            last_day = calendar.monthrange(mx_dt.year, mx_dt.month)[1]
            ytd_end = f"{mx_dt.year}-{mx_dt.month:02d}-{last_day}"
        else:
            ytd_end = date_start
        dt_where = "periodo_inicio >= ? AND periodo_fin <= ?"
        dt_params = [date_start, ytd_end]
        ld_where = "fecha >= ?"
        ld_params = [date_start]
    else:
        dt_where = "periodo_inicio >= ? AND periodo_fin <= ?"
        dt_params = [date_start, date_end]
        ld_where = "fecha BETWEEN ? AND ?"
        ld_params = [date_start, date_end]

    cierre = db.query(f"""
        SELECT marketplace,
               SUM(total_ingresos) as gross_revenue,
               SUM(resultado_neto) as net_revenue
        FROM marketplace_cierre_financiero_v1
        WHERE {dt_where}
        GROUP BY marketplace ORDER BY marketplace
    """, dt_params)

    dev = db.query(f"""
        SELECT marketplace, COALESCE(SUM(monto), 0) as devoluciones
        FROM marketplace_ledger_v1
        WHERE financial_group = 'devoluciones'
          AND COALESCE(include_in_operational_pnl, 1) = 1
          AND {ld_where}
        GROUP BY marketplace
    """, ld_params)

    dev_map = {str(r['marketplace']): float(r['devoluciones']) for _, r in dev.iterrows()}

    audit = db.query("SELECT marketplace, COUNT(*) as alert_count FROM marketplace_auditoria_v1 GROUP BY marketplace")
    alert_map = {str(r['marketplace']): int(r['alert_count']) for _, r in audit.iterrows()}

    marketplaces = []
    total_gross = total_net = total_alerts = 0.0
    for _, r in cierre.iterrows():
        mp = str(r['marketplace'])
        gross = float(r['gross_revenue']) if r['gross_revenue'] else 0.0
        net = float(r['net_revenue']) if r['net_revenue'] else 0.0
        dev_mp = dev_map.get(mp, 0)
        alerts = alert_map.get(mp, 0)
        marketplaces.append({
            "id": mp,
            "gross_revenue": gross,
            "devoluciones": dev_mp,
            "cobros": net - gross - dev_mp,
            "net_revenue": net,
            "alert_count": alerts,
        })
        total_gross += gross
        total_net += net
        total_alerts += alerts

    return {
        "period": label,
        "marketplaces": marketplaces,
        "total_gross_revenue": total_gross,
        "total_devoluciones": sum(m["devoluciones"] for m in marketplaces),
        "total_cobros": sum(m["cobros"] for m in marketplaces),
        "total_net_revenue": total_net,
        "total_alert_count": int(total_alerts),
    }


@app.get("/api/v4/exec/waterfall")
def get_exec_waterfall(marketplace: str | None = None, periodo: str | None = None):
    """Waterfall data — source of truth operacional certificado.
    
    RN = Ingresos + Devoluciones + Costos_Op + Costos_Com + Ajustes
    Filtrado por include_in_operational_pnl = 1.
    """
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)

    mp_filter = ""
    mp_params: list = []
    if marketplace:
        mp_filter = "AND marketplace = ?"
        mp_params = [marketplace]

    if date_end is None:
        mx = db.query("SELECT MAX(periodo_inicio) as mx FROM marketplace_cierre_financiero_v1 WHERE resultado_neto != 0")
        mx_val = mx.iloc[0]['mx']
        if pd.notna(mx_val):
            mx_dt = pd.to_datetime(mx_val)
            last_day = calendar.monthrange(mx_dt.year, mx_dt.month)[1]
            ytd_end = f"{mx_dt.year}-{mx_dt.month:02d}-{last_day}"
        else:
            ytd_end = date_start
        ledger_where = f"fecha >= ? {mp_filter.replace('marketplace', 'marketplace')}"
        ledger_params = [date_start] + mp_params
    else:
        ledger_where = f"fecha BETWEEN ? AND ? {mp_filter.replace('marketplace', 'marketplace')}"
        ledger_params = [date_start, date_end] + mp_params

    ledger = db.query(f"""
        SELECT
            COALESCE(SUM(CASE WHEN financial_group='ingresos' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as ingresos,
            COALESCE(SUM(CASE WHEN financial_group='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as devoluciones,
            COALESCE(SUM(CASE WHEN financial_group='costos_operacionales' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costos_op,
            COALESCE(SUM(CASE WHEN financial_group='costos_comerciales' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costos_com,
            COALESCE(SUM(CASE WHEN financial_group='ajustes' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as ajustes
        FROM marketplace_ledger_v1
        WHERE {ledger_where}
    """, ledger_params)

    r = ledger.iloc[0]
    ingresos = float(r['ingresos'])
    devoluciones = float(r['devoluciones'])
    costos_op = float(r['costos_op'])
    costos_com = float(r['costos_com'])
    ajustes = float(r['ajustes'])
    neto = ingresos + devoluciones + costos_op + costos_com + ajustes

    cobros = -(costos_op + costos_com + ajustes)

    return {
        "labels": ["Ingresos Brutos", "Devoluciones", "Costos Operacionales", "Costos Comerciales", "Ajustes", "Resultado Neto"],
        "values": [ingresos, devoluciones, costos_op, costos_com, ajustes, neto],
        "cobros": cobros,
        "marketplace": marketplace or "CONSOLIDADO",
        "neto_full": float(db.query("SELECT COALESCE(SUM(resultado_neto), 0) FROM marketplace_cierre_financiero_v1").iloc[0,0]),
    }


@app.get("/api/v4/exec/cobros-breakdown")
def get_exec_cobros_breakdown(marketplace: str | None = None, periodo: str | None = None):
    db = DatabaseV4.get()
    date_start, date_end, label = _resolve_period_range(periodo)

    mp_filter = ""
    mp_params: list = []
    if marketplace and marketplace not in ("ALL", "", None):
        mp_filter = "AND marketplace = ?"
        mp_params = [marketplace]

    if date_end is None:
        ledger_where = f"fecha >= ? {mp_filter}"
        ledger_params = [date_start] + mp_params
    else:
        ledger_where = f"fecha BETWEEN ? AND ? {mp_filter}"
        ledger_params = [date_start, date_end] + mp_params

    df = db.query(f"""
        SELECT marketplace, detalle, financial_group, SUM(COALESCE(monto, 0)) as total
        FROM marketplace_ledger_v1
        WHERE financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes')
          AND COALESCE(include_in_operational_pnl, 1) = 1
          AND financial_group IS NOT NULL
          AND {ledger_where}
        GROUP BY marketplace, detalle, financial_group
        ORDER BY marketplace, total ASC
    """, ledger_params)

    concept_data = {}
    mp_set = set()

    for _, row in df.iterrows():
        detalle = str(row['detalle']) if not pd.isna(row['detalle']) else ""
        mp = str(row['marketplace'])
        total = float(row['total'])
        concept = _map_detalle_to_concept(detalle)

        mp_set.add(mp)
        key = (concept, mp)
        concept_data[key] = concept_data.get(key, 0) + total

    mps = sorted(mp_set)
    concept_keys = set(k[0] for k in concept_data)

    concept_totals = {}
    for concept in concept_keys:
        total = sum(concept_data.get((concept, mp), 0) for mp in mps)
        concept_totals[concept] = total

    sorted_concepts = sorted(concept_totals.keys(), key=lambda c: abs(concept_totals[c]), reverse=True)

    matrix = []
    for concept in sorted_concepts:
        row = {"concept": concept}
        for mp in mps:
            row[mp] = concept_data.get((concept, mp), 0)
        row["total"] = concept_totals[concept]
        matrix.append(row)

    total_cobros = sum(concept_totals.values())

    return {
        "matrix": matrix,
        "total_cobros": total_cobros,
        "mps": mps,
        "concept_totals": concept_totals,
    }


@app.get("/api/v4/exec/audit-drilldown")
def get_exec_audit_drilldown(
    marketplace: str | None = None,
    check_name: str | None = None,
    offset: int = 0,
    limit: int = 50,
):
    """Audit drill-down — paginated, filterable."""
    db = DatabaseV4.get()

    conditions = []
    params = []

    if marketplace:
        conditions.append("marketplace = ?")
        params.append(marketplace)
    if check_name:
        conditions.append("check_name = ?")
        params.append(check_name)

    where = " AND ".join(conditions) if conditions else "1=1"

    count_df = db.query(f"SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE {where}", params)
    total = int(count_df.iloc[0]['n'])

    df = db.query(f"""
        SELECT marketplace, check_name, condition_detected, action_taken, order_id, detected_at
        FROM marketplace_auditoria_v1
        WHERE {where}
        ORDER BY detected_at DESC
        LIMIT ? OFFSET ?
    """, params + [limit, offset])

    return {
        "data": clean_records(df),
        "total": total,
        "offset": offset,
        "limit": limit,
    }


@app.get("/api/v4/exec/audit-types")
def get_exec_audit_types():
    """Distinct check_name values for filter dropdown."""
    db = DatabaseV4.get()
    df = db.query("SELECT DISTINCT check_name FROM marketplace_auditoria_v1 ORDER BY check_name")
    return [str(r['check_name']) for _, r in df.iterrows()]


@app.get("/", response_class=HTMLResponse)
@app.get("/app", response_class=HTMLResponse)
def index():
    dashboard_path = ROOT / "templates" / "dashboard.html"
    if dashboard_path.exists():
        with open(dashboard_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>Dashboard no encontrado</h1>", status_code=404)

@app.post("/api/v4/run-audit")
def run_audit_only(marketplace: str = "ML"):
    """Safe audit — only regenerates auditoria_v1 alerts.
    NO run_classification (preserva DEC-019).
    NO run_financial_closing (preserva cierres certificados).
    DEC-019 preserved. op_pnl preserved. Single Financial Truth preserved.
    """
    try:
        engine = MarketplaceAuditorEngine()
        engine.run_audit()
        return {"status": "success", "message": f"Auditoría completada para {marketplace}. DEC-019 preservado."}
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


