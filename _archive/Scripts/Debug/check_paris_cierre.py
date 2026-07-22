import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
df = db.query("SELECT * FROM marketplace_cierre_financiero_v1 WHERE marketplace='PARIS' AND periodo_inicio='2026-01-01'")
pd.set_option('display.max_columns', None)
print(df)
