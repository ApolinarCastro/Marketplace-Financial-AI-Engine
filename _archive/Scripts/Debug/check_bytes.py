import duckdb
conn = duckdb.connect('C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db')
res = conn.execute("SELECT detalle FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' AND detalle = 'Comisiones' LIMIT 1").fetchall()
print("EXACT COMISIONES:", res)
