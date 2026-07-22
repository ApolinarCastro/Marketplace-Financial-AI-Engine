import duckdb
conn = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
res = conn.execute("SELECT DISTINCT clasificacion_operativa, financial_group FROM marketplace_ledger_v1 WHERE marketplace='PARIS'").fetchall()
print("PARIS CLASIFICACION:", res)
