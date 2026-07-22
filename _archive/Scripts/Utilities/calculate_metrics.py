import duckdb
import json

db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"
conn = duckdb.connect(db_path, read_only=True)

query = """
SELECT 
    SUM(CASE WHEN l.financial_group = 'ingresos' THEN l.monto ELSE 0 END) as ingresos,
    SUM(CASE WHEN l.financial_group = 'devoluciones' THEN l.monto ELSE 0 END) as devoluciones,
    SUM(CASE WHEN l.financial_group = 'costos_operacionales' THEN l.monto ELSE 0 END) as costos_op,
    SUM(CASE WHEN l.financial_group = 'costos_comerciales' THEN l.monto ELSE 0 END) as costos_com,
    SUM(CASE WHEN l.financial_group = 'ajustes' THEN l.monto ELSE 0 END) as ajustes,
    SUM(monto) as neto
FROM marketplace_ledger_v1 l
WHERE l.marketplace = 'ML' AND l.include_in_operational_pnl = true
"""
df = conn.execute(query).df()

with open('metrics_before.json', 'w') as f:
    json.dump(df.to_dict(orient='records')[0], f, indent=2)
print("Metrics before saved.")
