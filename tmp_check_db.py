import sys, warnings
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
warnings.filterwarnings('ignore')

import duckdb

db_path = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db'
con = duckdb.connect(db_path, read_only=True)

tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchdf()
print('=== LIVE DB TABLES ===')
for _, r in tables.iterrows():
    print(f'  {r["table_name"]}')

for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    r = con.execute(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(monto),0),0) as total, MIN(fecha) as min_f, MAX(fecha) as max_f FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").fetchdf().iloc[0]
    print(f'{mp}: {int(r["n"]):>6d} rows, ${float(r["total"]):>12,.0f}, {r["min_f"]} to {r["max_f"]}')

# Check cierre
print()
print('=== CIERRES POR MP ===')
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    r = con.execute(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(resultado_neto),0),0) as total FROM marketplace_cierre_financiero_v1 WHERE marketplace='{mp}'").fetchdf().iloc[0]
    print(f'{mp}: {int(r["n"]):>3d} cierres, neto=${float(r["total"]):>12,.0f}')

# Check auditoria
print()
print('=== AUDITORIA POR MP ===')
for mp in ['ML','PARIS','RIPLEY','FALABELLA']:
    r = con.execute(f"SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE marketplace='{mp}'").fetchdf().iloc[0]
    print(f'{mp}: {int(r["n"])} rows')

con.close()
