import sys
sys.path.append('.')
from engine.v4.database import DatabaseV4
import pandas as pd

db = DatabaseV4('database.duckdb')
res = db.query("SELECT c.id_transaccion, c.monto, v1.archivo_origen FROM marketplace_ledger_clasificado_v1 c JOIN marketplace_ledger_v1 v1 ON c.id_transaccion = v1.id_transaccion WHERE c.marketplace = 'ML'")
print(res.shape)
