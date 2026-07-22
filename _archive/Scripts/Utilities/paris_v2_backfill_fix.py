import duckdb
import json

db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db"

with open("recovered_data.json", "r") as f:
    recovered = json.load(f)

print(f"Loaded {len(recovered)} records for backfill.")

conn = duckdb.connect(db_path, read_only=False)

try:
    conn.execute("BEGIN TRANSACTION")
    updated = 0
    for tid, data in recovered.items():
        gross = data['monto_bruto']
        net = data['monto_a_pagar']
        comision = gross - net
        
        conn.execute(f"""
            UPDATE marketplace_ledger_v1
            SET monto_bruto = {gross},
                comision_marketplace = {comision}
            WHERE id_transaccion = '{tid}' AND marketplace = 'PARIS' AND detalle = 'Venta'
        """)
        updated += 1

    conn.execute("COMMIT")
    print(f"Successfully updated {updated} records in marketplace_ledger_v1.")
except Exception as e:
    conn.execute("ROLLBACK")
    print(f"Error during backfill: {e}")
finally:
    conn.close()
