import duckdb

db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4_copy.db"
conn = duckdb.connect(db_path, read_only=True)

tables = conn.execute("SHOW TABLES").df()
print("Tables:", tables)
