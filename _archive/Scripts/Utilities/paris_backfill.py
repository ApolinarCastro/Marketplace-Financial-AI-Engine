import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.run_initial_audit import load_marketplace_ledger_standalone
db = DatabaseV4.get()
print('Deleting Paris records...')
db.execute("DELETE FROM marketplace_ledger_v1 WHERE marketplace='PARIS'")
print('Running load...')
load_marketplace_ledger_standalone(db)
print('Done!')
