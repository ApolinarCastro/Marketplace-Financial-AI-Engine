import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()

q = """
WITH seller_orders AS (
    SELECT DISTINCT id_orden FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' AND detalle='Importe del pedido'
),
ciclos_orders AS (
    SELECT id_orden, MIN(fecha) as fecha, SUM(monto) as monto 
    FROM marketplace_ledger_clasificado_v1 
    WHERE marketplace='RIPLEY' AND detalle='Precio total'
    GROUP BY id_orden
)
SELECT 
    YEAR(fecha) as anio, MONTH(fecha) as mes, COUNT(id_orden) as ordenes_faltantes, SUM(monto) as monto_faltante
FROM ciclos_orders 
WHERE id_orden NOT IN (SELECT id_orden FROM seller_orders)
GROUP BY YEAR(fecha), MONTH(fecha)
ORDER BY anio, mes
"""
print("Órdenes en Ciclos pero no en Seller por Mes:")
print(db.query(q).to_string())
