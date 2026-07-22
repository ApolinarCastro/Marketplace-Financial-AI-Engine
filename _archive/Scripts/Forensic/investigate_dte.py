import duckdb
db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"
conn = duckdb.connect(db_path, read_only=True)

df = conn.execute("SELECT * FROM dte_truth_v1 WHERE marketplace IS NULL LIMIT 10").df()
print(df)
print("\nUnique rut_receptor with null marketplace:")
print(conn.execute("SELECT rut_receptor, count(*) FROM dte_truth_v1 WHERE marketplace IS NULL GROUP BY rut_receptor").df())
