import duckdb
import pandas as pd
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()
classes = db.execute("SELECT clasificacion_operativa, COUNT(*) FROM marketplace_ledger_v1 GROUP BY clasificacion_operativa").fetchall()
print('Classifications:', classes)
