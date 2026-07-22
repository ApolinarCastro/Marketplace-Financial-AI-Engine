import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

# Simple queries
print("Total ML rows:", db.query("SELECT COUNT(*) as c FROM marketplace_ledger_v1 WHERE marketplace='ML'").iloc[0]['c'])
print("Total RIPLEY rows:", db.query("SELECT COUNT(*) as c FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY'").iloc[0]['c'])
print("Total PARIS rows:", db.query("SELECT COUNT(*) as c FROM marketplace_ledger_v1 WHERE marketplace='PARIS'").iloc[0]['c'])

# Check distinct detalles for each
for mp in ['ML', 'RIPLEY', 'PARIS']:
    q = db.query("SELECT detalle, COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace=? GROUP BY detalle ORDER BY cnt DESC LIMIT 5", [mp])
    print(f"\n{mp} top 5 detalles:")
    for _, r in q.iterrows():
        print(f"  '{r['detalle']}' cnt={r['cnt']}")

# Check a single row
print("\nFirst 3 ML rows:")
q = db.query("SELECT marketplace, id_transaccion, detalle, monto, fecha FROM marketplace_ledger_v1 WHERE marketplace='ML' LIMIT 3")
for _, r in q.iterrows():
    print(f"  mp={r['marketplace']} id={r['id_transaccion']} det={r['detalle']} monto={r['monto']} fecha={r['fecha']}")
