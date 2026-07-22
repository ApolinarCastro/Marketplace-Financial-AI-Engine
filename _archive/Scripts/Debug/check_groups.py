import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
print(db.query("SELECT DISTINCT financial_group FROM marketplace_ledger_clasificado_v1"))
