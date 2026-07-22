import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()

print("Schema marketplace_ledger_v1:")
schema = db.query("PRAGMA table_info(marketplace_ledger_v1)")
print(schema[['name', 'type']])

print("\nSample Data Paris Jan 2026:")
data = db.query("SELECT * FROM marketplace_ledger_v1 WHERE marketplace='PARIS' AND fecha >= '2026-01-01' LIMIT 5")
print(data)
