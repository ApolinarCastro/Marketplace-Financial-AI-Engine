import duckdb
from pathlib import Path
import logging
import pandas as pd
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("surgical.recovery")

ROOT = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine")
DB_PATH = ROOT / "data" / "db" / "meli_financial_v4.db"

def run():
    logger.info("Starting Surgical Recovery Flow...")
    
    conn = duckdb.connect(str(DB_PATH))
    logger.info("Resetting classifications...")
    conn.execute("DELETE FROM marketplace_ledger_clasificado_v1")
    conn.close()

    engine = MarketplaceAuditorEngine()
    logger.info("Executing Re-Classification with new rules...")
    n = engine.run_classification()
    logger.info(f"Classified {n} records.")

    # Get all months present in ledger
    conn = duckdb.connect(str(DB_PATH))
    months_df = conn.execute("""
        SELECT DISTINCT strftime('%Y-%m', fecha) as periodo 
        FROM marketplace_ledger_v1 
        WHERE fecha IS NOT NULL 
        ORDER BY 1
    """).df()
    conn.close()
    
    logger.info("Running Financial Closing for each period...")
    for month in months_df['periodo']:
        if not month: continue
        start_date = f"{month}-01"
        end_date = (pd.to_datetime(start_date) + pd.offsets.MonthEnd(0)).strftime('%Y-%m-%d')
        res = engine.run_financial_closing("ML", start_date, end_date)
        logger.info(f"Result for {month}: ${res['neto'] or 0:,.2f} (Ingresos: ${res['ingresos'] or 0:,.2f})")

    logger.info("Surgical Recovery Flow COMPLETED.")

if __name__ == "__main__":
    run()
