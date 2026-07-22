import duckdb
import pandas as pd
conn = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
df = conn.execute("SELECT DISTINCT detalle, count(*) as cnt, sum(monto), sum(monto_bruto), sum(comision_marketplace) FROM marketplace_ledger_v1 WHERE marketplace='PARIS' GROUP BY detalle;").df()
print(df)
