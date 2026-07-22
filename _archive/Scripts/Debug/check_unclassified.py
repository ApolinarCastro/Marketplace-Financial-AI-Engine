import duckdb
import pandas as pd

conn = duckdb.connect('C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db')
try:
    df = conn.execute("SELECT marketplace, detalle, COUNT(1) as cnt FROM marketplace_ledger_clasificado_v1 WHERE (financial_group IS NULL OR financial_group = '') GROUP BY marketplace, detalle ORDER BY cnt DESC LIMIT 20").df()
    print(df)
except Exception as e:
    print("Error:", e)
finally:
    conn.close()
