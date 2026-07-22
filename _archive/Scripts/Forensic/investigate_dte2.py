import duckdb
db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"
conn = duckdb.connect(db_path, read_only=True)

df = conn.execute("SELECT emisor_rut, emisor_nombre, count(*) FROM dte_truth_v1 WHERE marketplace IS NULL GROUP BY emisor_rut, emisor_nombre").df()
print(df)
