import duckdb

con = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
q = """
SELECT detalle, 
       CASE 
             WHEN archivo_origen LIKE '%.xlsx' THEN 'SELLER'
             WHEN archivo_origen LIKE '%ff%.csv' THEN 'FULFILLMENT'
             WHEN archivo_origen LIKE '%-%-%-%-%' THEN 'CICLOS'
             WHEN archivo_origen LIKE '%.xml' THEN 'XML'
             ELSE 'OTRO'
       END as origen,
       sum(monto) as total
FROM marketplace_ledger_v1 
WHERE marketplace='RIPLEY' 
  AND fecha >= '2025-01-01' AND fecha <= '2025-01-31'
  AND detalle = 'Pedidos reembolsados'
GROUP BY 1, 2
"""
print(con.execute(q).fetchdf())
