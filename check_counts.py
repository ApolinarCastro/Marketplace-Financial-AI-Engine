import sys
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()

# Check financial-structure query which might filter
fgroups = ("'ingresos', 'devoluciones', 'costos_operacionales', 'costos_comerciales', 'ajustes', 'recuperaciones_y_bonificaciones'")
count = db.execute(f"SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE financial_group IN ({fgroups})").fetchone()[0]
print(f'financial-structure groups: {count}')

# Check with COALESCE include_in_operational_pnl
count = db.execute(f"SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE financial_group IN ({fgroups}) AND COALESCE(include_in_operational_pnl, 1) = 1").fetchone()[0]
print(f'financial-structure + operational: {count}')

# Check what the financial_structure endpoint actually queries for a specific MP
import pandas as pd
df = db.query('SELECT marketplace, COUNT(*) as cnt FROM marketplace_ledger_v1 GROUP BY marketplace')
print('By marketplace:')
for _, row in df.iterrows():
    print(f'  {row["marketplace"]}: {row["cnt"]}')

df2 = db.query(f'SELECT marketplace, COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE financial_group IN ({fgroups}) GROUP BY marketplace')
print('By marketplace (financial groups only):')
for _, row in df2.iterrows():
    print(f'  {row["marketplace"]}: {row["cnt"]}')

# Check for 207600 specifically - try different marketplace filters
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    count = db.execute(f'SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace = ? AND financial_group IN ({fgroups})', [mp]).fetchone()[0]
    print(f'{mp} (financial groups): {count}')

# Check clasificado by marketplace
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA', 'SHOPIFY']:
    count = db.execute('SELECT COUNT(*) FROM marketplace_ledger_clasificado_v1 WHERE marketplace = ?', [mp]).fetchone()[0]
    print(f'{mp} clasificado: {count}')