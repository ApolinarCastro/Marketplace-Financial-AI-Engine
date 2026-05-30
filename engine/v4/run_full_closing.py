import duckdb
from pathlib import Path
import logging
import pandas as pd
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("surgical.closing")

ROOT = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine")
DB_PATH = ROOT / "data" / "db" / "meli_financial_v4.db"

def run():
    logger.info("Initializing Full Financial Closing for Mercado Libre...")
    engine = MarketplaceAuditorEngine()
    conn = duckdb.connect(str(DB_PATH))
    
    # Get all months present in ledger
    months_df = conn.execute("""
        SELECT DISTINCT strftime('%Y-%m', fecha) as periodo 
        FROM marketplace_ledger_v1 
        WHERE fecha IS NOT NULL 
        ORDER BY 1
    """).df()
    
    conn.close()
    
    if months_df.empty:
        logger.warning("No data found in ledger to close.")
        return

    for month in months_df['periodo']:
        if not month: continue
        
        # Calculate start and end dates
        start_date = f"{month}-01"
        # Use pandas to find end of month
        end_date = (pd.to_datetime(start_date) + pd.offsets.MonthEnd(0)).strftime('%Y-%m-%d')
        
        logger.info(f"Closing Period: {start_date} to {end_date}")
        res = engine.run_financial_closing("ML", start_date, end_date)
        logger.info(f"Result for {month}: ${res['neto'] or 0:,.2f}")

    logger.info("Full Financial Closing COMPLETED.")

if __name__ == "__main__":
    run()
