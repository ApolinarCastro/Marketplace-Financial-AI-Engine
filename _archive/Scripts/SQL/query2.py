import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
df = db.query("SELECT DISTINCT detalle, count(*) as cnt, sum(monto), sum(monto_bruto), sum(comision_marketplace) FROM marketplace_ledger_v1 WHERE marketplace='PARIS' GROUP BY detalle;")
print(df)
