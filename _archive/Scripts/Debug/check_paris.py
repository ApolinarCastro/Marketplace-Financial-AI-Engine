import duckdb
import pandas as pd

def run():
    conn = duckdb.connect('database_v4.duckdb')
    df = conn.execute("SELECT detalle, financial_group, sum(monto) as m, sum(monto_bruto) as mb, sum(comision_marketplace) as cm FROM marketplace_ledger_v1 WHERE marketplace='PARIS' AND fecha BETWEEN '2025-01-01' AND '2025-01-31' GROUP BY detalle, financial_group").fetchdf()
    print(df)

if __name__ == "__main__":
    run()
