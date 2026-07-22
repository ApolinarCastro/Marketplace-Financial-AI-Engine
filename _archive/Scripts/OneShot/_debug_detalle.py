import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

# Show ALL Ripley distinct detalles
print("=== ALL RIPLEY DISTINCT DETALLES ===")
rows = db.query("SELECT DISTINCT detalle FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' ORDER BY detalle")
for r in rows:
    val = r[0]
    print("  [%s] type=%s len=%d" % (repr(val), type(val).__name__, len(str(val)) if val else 0))

# Show a few 'A pagar' transactions
print("\n=== SAMPLE 'A pagar' TRANSACTIONS ===")
rows2 = db.query("""
    SELECT id_transaccion, detalle, monto, fecha
    FROM marketplace_ledger_v1 
    WHERE marketplace='RIPLEY' AND detalle LIKE '%pagar%'
    LIMIT 5
""")
for r in rows2:
    print("  id=%s detalle=%s monto=%s fecha=%s" % (r[0], repr(r[1]), r[2], r[3]))

# Check total
total = db.query("SELECT COUNT(*) as c, SUM(monto) as t FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND detalle LIKE '%pagar%'")
print("\nTotal: cnt=%s sum=%s" % (total.iloc[0]['c'], total.iloc[0]['t']))
