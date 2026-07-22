import sys
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()

df_jan = db.query("""
    SELECT financial_group, SUM(monto) as total
    FROM marketplace_ledger_clasificado_v1
    WHERE marketplace='PARIS' AND fecha LIKE '2026-01-%'
    GROUP BY financial_group
""")
print(df_jan)
