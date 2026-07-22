import calendar
import logging
import time
from functools import wraps

# Setup audit logger
audit_logger = logging.getLogger("sql_audit")
audit_logger.setLevel(logging.INFO)
fh = logging.FileHandler("marketplace_audit_sql.log")
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
if not audit_logger.handlers:
    audit_logger.addHandler(fh)

def _resolve_period_range(periodo: str):
    """
    Directiva 1 & 2: Extraer a modulo compartido y NUNCA inferir fechas ni usar el ultimo periodo.
    """
    if not periodo:
        raise ValueError("El parametro 'periodo' es obligatorio y no puede ser inferido.")
    
    if periodo.upper() == "ALL":
        raise ValueError("El parametro 'periodo' no puede ser ALL.")

    parts = periodo.split("-")
    if len(parts) == 2:
        year, month = parts
        try:
            last_day = calendar.monthrange(int(year), int(month))[1]
            return (f"{year}-{month}-01", f"{year}-{month}-{last_day}", f"{year}-{month}")
        except ValueError:
            pass # fallback to exact string if not a valid YYYY-MM
    
    # If YTD e.g., 2025-YTD
    if "YTD" in periodo.upper():
        year = parts[0]
        return (f"{year}-01-01", f"{year}-12-31", periodo)
        
    # Return strict strings, date_end = None means exact match if not a range
    return (periodo, None, periodo)

def log_sql_audit(endpoint, marketplace, periodo, sql, params, rows, execution_time_ms):
    """
    Directiva 4: Auditoria SQL mediante logging, sin devolver info al frontend.
    """
    msg = (f"[ENDPOINT: {endpoint}] [MARKETPLACE: {marketplace}] [PERIODO: {periodo}] "
           f"[TIEMPO_MS: {execution_time_ms:.2f}] [FILAS: {rows}] "
           f"[SQL: {sql}] [PARAMS: {params}]")
    audit_logger.info(msg)
