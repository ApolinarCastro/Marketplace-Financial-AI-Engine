import duckdb
conn = duckdb.connect('data/db/meli_financial_v4.db')
sql = f"""
SELECT clasificacion_operativa, SUM(monto) as monto
FROM marketplace_ledger_clasificado_v1 
WHERE marketplace='RIPLEY' AND fecha >= '2026-01-01'
AND financial_group = 'tesoreria'
GROUP BY clasificacion_operativa
"""
df = conn.execute(sql).df()
print(df)