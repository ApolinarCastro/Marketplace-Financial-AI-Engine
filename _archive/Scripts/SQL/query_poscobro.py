import duckdb
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

db_path = "data/db/meli_financial_v4.db"
con = duckdb.connect(db_path, read_only=True)

query = """
SELECT 
    fecha, 
    id_transaccion as operation_id, 
    id_transaccion as transaction_id, 
    id_orden as order_id, 
    clasificacion_operativa as reason_id, 
    detalle as reason_detail, 
    detalle as detail_original, 
    monto as amount, 
    marketplace, 
    clasificacion_operativa as classification, 
    include_in_operational_pnl,
    archivo_origen as source_file
FROM marketplace_ledger_clasificado_v1 
LEFT JOIN marketplace_ledger_v1 USING(marketplace, id_transaccion, id_orden, fecha, monto, tipo_movimiento)
WHERE clasificacion_operativa IN ('Ajuste Poscobro Conciliado', 'Ajuste Poscobro General')
ORDER BY monto DESC
"""

try:
    df = con.execute(query).df()
    print(df.to_string())
except Exception as e:
    print("Error:", e)
    # let's try just getting it from clasificado_v1 if join fails
    query2 = """
    SELECT * FROM marketplace_ledger_clasificado_v1 
    WHERE clasificacion_operativa IN ('Ajuste Poscobro Conciliado', 'Ajuste Poscobro General')
    """
    df2 = con.execute(query2).df()
    print("Fallback Query:")
    print(df2.to_string())

