import pandas as pd
import os
import sys

# Try to find the database file in different locations
possible_paths = [
    'data/db/meli_financial_v4.db',
    'data/db/meli_financial_v4.db',
    'data/db/marketplace.db',
]

for db_path in possible_paths:
    if os.path.exists(db_path):
        print(f"Found database at: {db_path}")
        print(f"File size: {os.path.getsize(db_path)}")
        
        # Try to read with pandas
        try:
            conn_str = f"duckdb://{db_path}"
            query = "SELECT detalle, COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace='ML' AND (LOWER(detalle) LIKE '%bigger%' OR LOWER(detalle) LIKE '%not_match%' OR LOWER(detalle) LIKE '%different%' OR LOWER(detalle) LIKE '%repentant%' OR LOWER(detalle) LIKE '%undelivered%') GROUP BY detalle ORDER BY cnt DESC LIMIT 20"
            print(f"\nQuerying: {query}")
            df = pd.read_sql(query, conn_str)
            print(df.to_string())
        except Exception as e:
            print(f"Error with {db_path}: {e}")
        break
else:
    print("No database found in expected locations")