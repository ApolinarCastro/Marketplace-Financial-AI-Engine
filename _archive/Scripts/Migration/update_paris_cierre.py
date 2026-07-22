from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.database import DatabaseV4
import pandas as pd

db = DatabaseV4.get()
periods = db.query("SELECT DISTINCT strftime('%Y-%m', fecha) as per FROM marketplace_ledger_clasificado_v1 WHERE marketplace='PARIS'")

auditor = MarketplaceAuditorEngine()

for _, row in periods.iterrows():
    per = row['per']
    if pd.notna(per):
        year, month = per.split('-')
        import calendar
        last_day = calendar.monthrange(int(year), int(month))[1]
        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month}-{last_day}"
        print(f"Running financial closing for PARIS {start_date} to {end_date}...")
        auditor.run_financial_closing("PARIS", start_date, end_date)
