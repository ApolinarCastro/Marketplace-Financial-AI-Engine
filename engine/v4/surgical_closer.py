import logging
import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("surgical.closing")

class SurgicalCloser:
    def __init__(self):
        self.db = DatabaseV4.get()

    def run(self):
        logger.info("Starting Surgical Financial Consolidation for Mercado Libre...")
        
        # 1. Clear previous closing
        self.db.execute("DELETE FROM marketplace_cierre_financiero_v1 WHERE marketplace = 'ML'")
        
        # 2. Get all months present in ledger
        months_df = self.db.query("""
            SELECT DISTINCT strftime('%Y-%m', fecha) as periodo 
            FROM marketplace_ledger_v1 
            WHERE marketplace = 'ML' AND fecha IS NOT NULL 
            ORDER BY 1
        """)
        
        engine = MarketplaceAuditorEngine()
        
        # 3. Run Financial Closing for each period
        count = 0
        for month in months_df['periodo']:
            if not month: continue
            start_date = f"{month}-01"
            # Get last day of the month safely
            end_date = (pd.to_datetime(start_date) + pd.offsets.MonthEnd(0)).strftime('%Y-%m-%d')
            
            res = engine.run_financial_closing("ML", start_date, end_date)
            logger.info(f"Result for {month}: Neto = ${res['neto']:,.0f} (Ingresos = ${res['ingresos']:,.0f})")
            count += 1
            
        logger.info(f"Consolidated {count} periods.")
        logger.info("Consolidation COMPLETED.")

if __name__ == "__main__":
    closer = SurgicalCloser()
    closer.run()

