import pandas as pd
from engine.v4.database import DatabaseV4
print(DatabaseV4.get().query("SELECT DISTINCT id_transaccion FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' LIMIT 10"))
