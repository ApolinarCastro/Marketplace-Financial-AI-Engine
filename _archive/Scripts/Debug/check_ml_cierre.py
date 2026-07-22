import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
print(db.query("SELECT * FROM marketplace_cierre_financiero_v1 WHERE marketplace='ML'"))
