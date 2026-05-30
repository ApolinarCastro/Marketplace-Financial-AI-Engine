import duckdb, sys, json
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.surgical_loader import SurgicalLoader

conn = duckdb.connect(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\meli_financial_v4.db')

# Step 1: Backup existing Falabella ventas
ventas_backup = conn.execute("SELECT * FROM ventas_marketplace WHERE marketplace = 'FALABELLA'").fetchall()
cols = [c[0] for c in conn.execute("PRAGMA table_info('ventas_marketplace')").fetchall()]
print(f"=== VENTAS BACKUP ===")
print(f"Backed up {len(ventas_backup)} ventas records")
if ventas_backup:
    print(f"  First: order_id={ventas_backup[0][0]}, sku={ventas_backup[0][1]}, gross=${ventas_backup[0][4]:.0f}")
    print(f"  Last:  order_id={ventas_backup[-1][0]}, sku={ventas_backup[-1][1]}, gross=${ventas_backup[-1][4]:.0f}")
    print(f"  Period: {ventas_backup[0][5]} to {ventas_backup[-1][5]}")
    venta_oids = set(r[0] for r in ventas_backup)
    print(f"  Unique order_ids: {len(venta_oids)}")

# Step 2: Run the loader
print(f"\n=== RUNNING FALABELLA LOADER ===")
loader = SurgicalLoader()
try:
    loader.load_marketplace('FALABELLA')
    print("Loader completed successfully")
except Exception as e:
    print(f"Loader error: {e}")

# Step 3: Check what was loaded
print(f"\n=== POST-LOAD VALIDATION ===")

# ventas
ventas = conn.execute("SELECT COUNT(*) FROM ventas_marketplace WHERE marketplace = 'FALABELLA'").fetchone()[0]
print(f"ventas_marketplace: {ventas} rows")

# ledger
ledger = conn.execute("SELECT COUNT(*) FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'").fetchone()[0]
print(f"marketplace_ledger_v1: {ledger} rows")

if ledger > 0:
    # Unique concepts loaded
    concepts = conn.execute("SELECT detalle, COUNT(*) as cnt, SUM(monto) as total FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA' GROUP BY detalle ORDER BY SUM(ABS(monto)) DESC").fetchall()
    print(f"\nConcepts loaded to ledger ({len(concepts)}):")
    for r in concepts:
        print(f"  {str(r[0])[:65]:<65s} | cnt={r[1]:>4d} | ${r[2]:>10,.0f}")
    
    # Unique order_ids in ledger
    ledger_oids = conn.execute("SELECT DISTINCT id_orden FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA' AND id_orden IS NOT NULL AND id_orden != 'nan'").fetchall()
    ledger_oid_set = set(str(r[0]) for r in ledger_oids)
    print(f"\nUnique order_ids in ledger: {len(ledger_oid_set)}")

# Step 4: Restore ventas backup
if ventas_backup:
    print(f"\n=== RESTORING VENTAS BACKUP ===")
    # Need to re-insert since reset_db cleared them
    import pandas as pd
    df_backup = pd.DataFrame(ventas_backup, columns=cols)
    if 'load_ts' in cols:
        from datetime import datetime
        df_backup['load_ts'] = datetime.now()
    conn.execute("INSERT INTO ventas_marketplace SELECT * FROM df_backup")
    
    ventas_after = conn.execute("SELECT COUNT(*) FROM ventas_marketplace WHERE marketplace = 'FALABELLA'").fetchone()[0]
    print(f"ventas_marketplace after restore: {ventas_after} rows")

# Step 5: Cross-domain match validation
print(f"\n=== CROSS-DOMAIN MATCH VALIDATION ===")
if ventas_after > 0 and ledger > 0:
    matched = conn.execute("""
        SELECT COUNT(DISTINCT v.order_id) as venta_orders,
               COUNT(DISTINCT l.id_orden) as ledger_orders,
               COUNT(DISTINCT CASE WHEN v.order_id = l.id_orden THEN v.order_id END) as matched_orders
        FROM ventas_marketplace v
        JOIN marketplace_ledger_v1 l ON v.marketplace = l.marketplace AND v.order_id = l.id_orden
        WHERE v.marketplace = 'FALABELLA'
    """).fetchone()
    print(f"Venta orders: {matched[0]}")
    print(f"Ledger orders: {matched[1]}")
    print(f"Matched: {matched[2]}")
    if matched[0] > 0:
        print(f"Match rate: {matched[2]/matched[0]*100:.1f}%")

    # Waterfall sample
    print(f"\n=== WATERFALL SAMPLE ===")
    waterfall = conn.execute("""
        SELECT l.id_orden as order_id,
               SUM(CASE WHEN l.tipo_movimiento = 'PAGO' THEN l.monto ELSE 0 END) as total_payments,
               SUM(CASE WHEN l.tipo_movimiento = 'CARGO' THEN l.monto ELSE 0 END) as total_charges,
               SUM(l.monto) as net_total
        FROM marketplace_ledger_v1 l
        WHERE l.marketplace = 'FALABELLA' AND l.id_orden IN (
            SELECT v.order_id FROM ventas_marketplace v 
            WHERE v.marketplace = 'FALABELLA' 
            LIMIT 3
        )
        GROUP BY l.id_orden
    """).fetchall()
    for r in waterfall:
        print(f"  Order {r[0]:15s} | Payments=${r[1]:>10,.0f} | Charges=${r[2]:>10,.0f} | Net=${r[3]:>10,.0f}")
else:
    if ventas_after == 0:
        print("VENTAS: 0 rows — the XLSX files lack 'Precio del producto' concept")
    if ledger == 0:
        print("LEDGER: 0 rows — loader didn't find XLSX or parsing failed")
