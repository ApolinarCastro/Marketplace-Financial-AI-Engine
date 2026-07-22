import duckdb

db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4_copy.db"
conn = duckdb.connect(db_path, read_only=True)

import json
with open("recovered_data.json", "r") as f:
    recovered = json.load(f)

recovered_ids = list(recovered.keys())

df = conn.execute(f"""
    SELECT id_transaccion, id_orden, fecha, archivo_origen, monto
    FROM marketplace_ledger_v1
    WHERE marketplace = 'PARIS' AND detalle = 'Venta' AND monto_bruto IS NULL
      AND id_transaccion NOT IN ({','.join(["'"+str(x)+"'" for x in recovered_ids])})
""").df()

print(df)
