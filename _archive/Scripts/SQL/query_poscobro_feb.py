import duckdb
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

db_path = "data/db/meli_financial_v4.db"
con = duckdb.connect(db_path, read_only=True)

query = """
SELECT 
    c.fecha, 
    c.id_transaccion as operation_id, 
    c.id_orden as order_id, 
    v.detalle as detail_original, 
    c.monto as amount, 
    c.marketplace, 
    c.clasificacion_operativa as classification, 
    c.include_in_operational_pnl,
    v.archivo_origen as source_file
FROM marketplace_ledger_clasificado_v1 c
LEFT JOIN marketplace_ledger_v1 v 
  ON c.marketplace = v.marketplace 
  AND c.id_transaccion = v.id_transaccion 
  AND c.id_orden = v.id_orden 
  AND c.fecha = v.fecha 
  AND c.monto = v.monto 
  AND c.tipo_movimiento = v.tipo_movimiento
WHERE c.clasificacion_operativa IN ('Ajuste Poscobro Conciliado', 'Ajuste Poscobro General')
  AND c.fecha >= '2026-02-01' AND c.fecha <= '2026-02-28'
ORDER BY c.monto DESC
"""

df = con.execute(query).df()
print(f"Total Amount Conciliado: {df[df['classification'] == 'Ajuste Poscobro Conciliado']['amount'].sum()}")
print(f"Total Amount General: {df[df['classification'] == 'Ajuste Poscobro General']['amount'].sum()}")
print("----------------")
print(df.to_string())
