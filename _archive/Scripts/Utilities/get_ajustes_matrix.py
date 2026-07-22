import pandas as pd
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

# We want everything in 'ajustes' financial group, or clasificacion_operativa LIKE '%Ajuste%'
query = """
    SELECT 
        clasificacion_operativa as clasificacion,
        marketplace,
        COUNT(*) as cantidad_registros,
        SUM(COALESCE(monto, 0)) as monto_total,
        include_in_operational_pnl
    FROM marketplace_ledger_clasificado_v1
    WHERE financial_group = 'ajustes' OR clasificacion_operativa LIKE '%Ajuste%'
    GROUP BY clasificacion_operativa, marketplace, include_in_operational_pnl
    ORDER BY clasificacion_operativa, marketplace
"""

df = db.query(query)

for _, row in df.iterrows():
    print(f"| {row['clasificacion']} | {row['cantidad_registros']} | ${row['monto_total']:,.2f} | {row['marketplace']} | {row['include_in_operational_pnl']} |")
