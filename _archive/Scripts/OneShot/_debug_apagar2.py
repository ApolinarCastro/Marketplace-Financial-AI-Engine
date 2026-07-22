import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

# Find 'A pagar' specifically
q = db.query("""
    SELECT detalle, COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_v1 
    WHERE marketplace='RIPLEY' AND detalle LIKE '%pagar%'
    GROUP BY detalle
""")
print("Ripley 'A pagar' matches:")
for _, r in q.iterrows():
    print("  detalle='%s' cnt=%s total=$%.0f" % (r['detalle'], r['cnt'], r['total']))

# Check its classification
q2 = db.query("""
    SELECT c.clasificacion_operativa, COUNT(*) as cnt
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
    WHERE l.marketplace='RIPLEY' AND l.detalle LIKE '%pagar%'
    GROUP BY c.clasificacion_operativa
""")
print("\nClassification:")
for _, r in q2.iterrows():
    print("  %s: %s" % (r['clasificacion_operativa'], r['cnt']))
