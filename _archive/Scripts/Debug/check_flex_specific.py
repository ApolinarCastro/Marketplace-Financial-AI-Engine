import duckdb
con = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
df = con.execute("SELECT id_transaccion, detalle FROM marketplace_ledger_v1 WHERE id_transaccion LIKE '%145404934728%'").df()
print(df)
