import duckdb
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

db_path = "data/db/meli_financial_v4.db"
con = duckdb.connect(db_path, read_only=True)

order_ids = ['2000015218717874', '2000015208258540']

query = f"""
SELECT 
    fecha, 
    id_transaccion as operation_id, 
    id_orden as order_id, 
    tipo_movimiento,
    monto as amount, 
    clasificacion_operativa as classification, 
    include_in_operational_pnl
FROM marketplace_ledger_clasificado_v1 
WHERE id_orden IN ('2000015218717874', '2000015208258540', '2000015218717874.0', '2000015208258540.0')
ORDER BY id_orden, fecha
"""

df = con.execute(query).df()
print("LIFECYCLE FOR ORDERS:")
print(df.to_string())

query_v1 = f"""
SELECT 
    fecha, 
    id_transaccion,
    id_orden, 
    tipo_movimiento,
    monto, 
    detalle
FROM marketplace_ledger_v1 
WHERE id_orden IN ('2000015218717874', '2000015208258540', '2000015218717874.0', '2000015208258540.0')
ORDER BY id_orden, fecha
"""
df_v1 = con.execute(query_v1).df()
print("\nRAW V1 DATA:")
print(df_v1.to_string())

