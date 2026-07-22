import duckdb
con = duckdb.connect('database.duckdb', read_only=True)
df = con.execute("DESCRIBE marketplace_ledger_clasificado_v1").df()
print(df.to_string())
