import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
sql = '''
    SELECT 
        SUM(CASE WHEN financial_group='ingresos' THEN monto ELSE 0 END) as ingresos,
        SUM(CASE WHEN financial_group='devoluciones' THEN monto ELSE 0 END) as devoluciones,
        SUM(CASE WHEN financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes') THEN monto ELSE 0 END) as costos
    FROM marketplace_ledger_v1 
    WHERE marketplace='ML' AND fecha BETWEEN '2026-02-01' AND '2026-02-28'
      AND COALESCE(include_in_operational_pnl, 1) = 1
'''
df = db.query(sql)
row = df.iloc[0]
ingresos = float(row['ingresos']) if pd.notna(row['ingresos']) else 0.0
devoluciones = float(row['devoluciones']) if pd.notna(row['devoluciones']) else 0.0
costos = float(row['costos']) if pd.notna(row['costos']) else 0.0
neto = ingresos + devoluciones + costos

print('MERCADO LIBRE')
print('FEBRERO 2026')
print('')
print('TABLA 1')
print(f'Ventas: ${ingresos:,.2f}')
print(f'Devoluciones: ${devoluciones:,.2f}')
print(f'Costos Marketplace: ${costos:,.2f}')
print(f'Resultado Neto: ${neto:,.2f}')
print('')
print('TABLA 2')
print(f'Ventas: ${ingresos:,.2f}')
print('+')
print(f'Devoluciones: ${devoluciones:,.2f}')
print('+')
print(f'Costos Marketplace: ${costos:,.2f}')
print('==================')
print(f'Resultado Neto: ${neto:,.2f}')
print(f'Delta: ${(ingresos + devoluciones + costos) - neto:,.2f}')
