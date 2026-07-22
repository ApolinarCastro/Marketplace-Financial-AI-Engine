import duckdb
import pandas as pd

conn = duckdb.connect('C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db')
try:
    df = conn.execute("SELECT financial_group, SUM(monto) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace='PARIS' GROUP BY financial_group").df()
    print("PARIS GROUPS:")
    print(df)
    
    df2 = conn.execute("SELECT detalle, SUM(monto) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace='PARIS' AND financial_group='ingresos' GROUP BY detalle").df()
    print("\nPARIS INGRESOS:")
    print(df2)
except Exception as e:
    print("Error:", e)
finally:
    conn.close()
