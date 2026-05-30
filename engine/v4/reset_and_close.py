"""
Ultra-fast reset: Classification + Closings using the central Engine.
This ensures a single source of truth for the taxonomy.
"""
import sys
from pathlib import Path
import logging
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("meli.fast_reset")

def run():
    logger.info("Paso 1: Iniciando motor de auditoría...")
    db = DatabaseV4.get()
    engine = MarketplaceAuditorEngine()
    
    # 1. Clean previous data
    db.execute("DELETE FROM marketplace_cierre_financiero_v1")
    
    # 2. Run Classification
    logger.info("Paso 2: Clasificando transacciones...")
    n_class = engine.run_classification()
    logger.info(f"Clasificadas {n_class} transacciones.")
    
    # 3. Monthly Closings using the central engine logic
    logger.info("Paso 3: Cierres Mensuales...")
    months_df = db.execute("""
        SELECT DISTINCT strftime('%Y-%m', fecha) as periodo 
        FROM marketplace_ledger_v1 
        WHERE fecha IS NOT NULL 
        ORDER BY 1
    """).df()
    
    n_cierre = 0
    for month in months_df['periodo']:
        if not month: continue
        start_date = f"{month}-01"
        end_date = (pd.to_datetime(start_date) + pd.offsets.MonthEnd(0)).strftime('%Y-%m-%d')
        
        # ML
        engine.run_financial_closing("ML", start_date, end_date)
        # PARIS
        engine.run_financial_closing("PARIS", start_date, end_date)
        # RIPLEY
        engine.run_financial_closing("RIPLEY", start_date, end_date)
        # FALABELLA
        engine.run_financial_closing("FALABELLA", start_date, end_date)
        n_cierre += 4

    logger.info("Cierres generados para los periodos detectados.")
    
    # 4. Audit Alerts
    logger.info("Paso 4: Auditoría...")
    n_audit = engine.run_audit()
    logger.info(f"Alertas de auditoría: {n_audit}")

    # Resumen
    logger.info("=== RESUMEN ===")
    summary = db.query("""
        SELECT marketplace, count(*) as periodos,
               round(sum(total_ingresos),0) as ingresos,
               round(sum(resultado_neto),0) as neto
        FROM marketplace_cierre_financiero_v1
        GROUP BY marketplace ORDER BY marketplace
    """)
    for _, row in summary.iterrows():
        logger.info(f"  {row['marketplace']:10s} | {int(row['periodos']):3d} períodos | "
                    f"Ingresos: ${row['ingresos']:>15,.0f} | Neto: ${row['neto']:>15,.0f}")

if __name__ == "__main__":
    run()
