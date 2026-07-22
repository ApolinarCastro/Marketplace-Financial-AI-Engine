import sys
sys.path.insert(0, '.')
from engine.v4.surgical_loader import SurgicalLoader
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.database import DatabaseV4
import pandas as pd

# First load
loader = SurgicalLoader()
loader.load_marketplace('PARIS')

# Then audit
auditor = MarketplaceAuditorEngine()
auditor.run_classification()
res = auditor.run_financial_closing('PARIS', '2026-01-01', '2026-01-31')

print("CIERRE FINANCIERO PARIS ENERO 2026:")
print(f"Ingresos Brutos (Ventas): {res['ingresos']:,.0f}")
print(f"Costos Comerciales (Comisiones): {res['costos_com']:,.0f}")
print(f"Resultado Neto: {res['neto']:,.0f}")

db = DatabaseV4.get()
db.execute("UPDATE pipeline_log SET details = ? WHERE event = 'test'", ['DONE'])
