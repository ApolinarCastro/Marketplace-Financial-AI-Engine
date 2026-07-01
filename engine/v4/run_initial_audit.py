import re
import sys
from pathlib import Path
import glob
import pandas as pd
import logging

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.utils import load_file, harmonize_series, clean_amount

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("meli.audit_runner")

def _normalize_col_name(s: str) -> str:
    import unicodedata
    t = unicodedata.normalize('NFD', str(s).lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', t)

def _find_col(df, options):
    norm_options = [_normalize_col_name(o) for o in options]
    for col in df.columns:
        col_norm = _normalize_col_name(col)
        for opt_norm in norm_options:
            if opt_norm in col_norm or col_norm in opt_norm:
                return col
    return None

def load_marketplace_ledger_standalone(db):
    from engine.v4.surgical_loader import SurgicalLoader
    loader = SurgicalLoader()
    
    logger.info("Ingesting PARIS through SurgicalLoader...")
    loader.load_marketplace('PARIS')
    
    logger.info("Ingesting RIPLEY through SurgicalLoader...")
    loader.load_marketplace('RIPLEY')
    
    logger.info("Ingesting FALABELLA through SurgicalLoader...")
    loader.load_marketplace('FALABELLA')
    
    # Return count of rows in ledger for these three marketplaces
    cnt = db.query("SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace IN ('PARIS', 'RIPLEY', 'FALABELLA')").iloc[0]['n']
    return int(cnt)

if __name__ == "__main__":
    db = DatabaseV4.get()
    engine = MarketplaceAuditorEngine()
    
    logger.info("--- PASO 1: Ingestión Multi-Marketplace (2023+) ---")
    rows = load_marketplace_ledger_standalone(db)
    logger.info(f"Insertadas {rows} transacciones en marketplace_ledger_v1 para Otros Marketplaces.")

    logger.info("--- PASO 1.5: Ingestión Anatómica Mercado Libre ---")
    from engine.v4.surgical_loader import SurgicalLoader
    loader = SurgicalLoader()
    loader.load_marketplace('ML')
    logger.info("Completada ingesta anatómica de Mercado Libre.")

    logger.info("--- PASO 2: Clasificación ---")
    c = engine.run_classification()
    logger.info(f"Clasificadas {c} transacciones.")

    logger.info("--- PASO 3: Cierres Financieros ---")
    import calendar
    # Generar iterativamente por meses de 2025-2026
    for year in [2025, 2026]:
        for month in range(1, 13):
            last_day = calendar.monthrange(year, month)[1]
            p_ini = f"{year}-{month:02d}-01"
            p_fin = f"{year}-{month:02d}-{last_day}"
            
            engine.run_financial_closing("ML", p_ini, p_fin)
            engine.run_financial_closing("PARIS", p_ini, p_fin)
            engine.run_financial_closing("RIPLEY", p_ini, p_fin)
            engine.run_financial_closing("FALABELLA", p_ini, p_fin)

    logger.info("--- PASO 4: Auditoría ---")
    a = engine.run_audit()
    logger.info(f"Detectadas {a} desviaciones de auditoría en todos los marketplaces.")
