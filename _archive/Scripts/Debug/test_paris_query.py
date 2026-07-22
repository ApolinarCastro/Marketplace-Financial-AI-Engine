import sys
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4
import pandas as pd

db = DatabaseV4.get()
df = db.query("SELECT * FROM marketplace_ledger_v1 WHERE marketplace='PARIS' AND detalle='Venta' LIMIT 1")
print(df.to_dict('records'))
