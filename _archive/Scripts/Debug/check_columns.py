import duckdb
db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"
conn = duckdb.connect(db_path, read_only=True)
print("Columns in marketplace_ledger_v1:")
print(conn.execute("DESCRIBE marketplace_ledger_v1;").df())
print("\nColumns in document_match_v1:")
print(conn.execute("DESCRIBE document_match_v1;").df())
print("\nColumns in dte_truth_v1:")
print(conn.execute("DESCRIBE dte_truth_v1;").df())
