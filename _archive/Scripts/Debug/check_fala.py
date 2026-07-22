from engine.v4.database import DatabaseV4
import pandas as pd

db = DatabaseV4.get()
df = db.query("SELECT * FROM dte_truth_v1 WHERE marketplace='FALABELLA'")
print(df)
