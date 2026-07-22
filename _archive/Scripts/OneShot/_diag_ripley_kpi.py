import duckdb
import pandas as pd

con = duckdb.connect('C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db', read_only=True)

print('=== LIQUIDACION (Ciclos) ===')
q1 = '''
SELECT detalle, SUM(monto) as total 
FROM marketplace_ledger_v1 
WHERE marketplace = 'RIPLEY' 
  AND archivo_origen LIKE '%-%-%-%-%' AND archivo_origen LIKE '%.csv'
  AND fecha >= '2025-01-01' AND fecha < '2025-02-01'
GROUP BY detalle
'''
print(con.execute(q1).df())

print('\n=== SELLER (OPERACIONAL MP) ===')
q2 = '''
SELECT detalle, SUM(monto) as total 
FROM marketplace_ledger_v1 
WHERE marketplace = 'RIPLEY' 
  AND archivo_origen LIKE '%.xlsx' 
  AND fecha >= '2025-01-01' AND fecha < '2025-02-01'
GROUP BY detalle
'''
print(con.execute(q2).df())

print('\n=== FULFILLMENT (OPERACIONAL FF) ===')
q3 = '''
SELECT detalle, SUM(monto) as total 
FROM marketplace_ledger_v1 
WHERE marketplace = 'RIPLEY' 
  AND archivo_origen LIKE '%ff%.csv' 
  AND fecha >= '2025-01-01' AND fecha < '2025-02-01'
GROUP BY detalle
'''
print(con.execute(q3).df())

print('\n=== COMPARATIVE VENTA ===')
q4 = '''
SELECT 
    SUM(CASE WHEN archivo_origen LIKE '%.xlsx' AND detalle IN ('Precio total', 'Importe del pedido', 'order_amount') THEN monto ELSE 0 END) as Venta_Seller,
    SUM(CASE WHEN archivo_origen LIKE '%ff%.csv' AND detalle IN ('transfer_amount') THEN monto ELSE 0 END) as Venta_Fulfillment,
    SUM(CASE WHEN archivo_origen LIKE '%-%-%-%-%' AND archivo_origen LIKE '%.csv' AND detalle='Subtotal' THEN monto ELSE 0 END) as Venta_Liquidacion
FROM marketplace_ledger_v1 
WHERE marketplace = 'RIPLEY' 
  AND fecha >= '2025-01-01' AND fecha < '2025-02-01'
'''
print(con.execute(q4).df())

print('\n=== COMPARATIVE DISPONIBLE (TESORERIA) ===')
q5 = '''
SELECT 
    SUM(CASE WHEN archivo_origen LIKE '%-%-%-%-%' AND archivo_origen LIKE '%.csv' AND detalle='Amount transferred to tienda' THEN monto ELSE 0 END) as Pago_Neto_Liquidacion,
    SUM(CASE WHEN financial_group='tesoreria' THEN monto ELSE 0 END) as Tesoreria_Ledger
FROM marketplace_ledger_v1 
WHERE marketplace = 'RIPLEY' 
  AND fecha >= '2025-01-01' AND fecha < '2025-02-01'
'''
print(con.execute(q5).df())
