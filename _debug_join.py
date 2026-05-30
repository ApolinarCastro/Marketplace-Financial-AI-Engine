import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

# Correct JOIN with marketplace
q = db.query("""
    SELECT c.clasificacion_operativa, COUNT(*) as cnt
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion AND l.marketplace = c.marketplace
    WHERE l.marketplace='RIPLEY' AND l.detalle = 'A pagar'
    GROUP BY c.clasificacion_operativa
""")
print("'A pagar' classification (correct JOIN):")
for _, r in q.iterrows():
    print("  %s: %s" % (r['clasificacion_operativa'], r['cnt']))

# Also check all Ripley classifications with correct JOIN
q2 = db.query("""
    SELECT c.clasificacion_operativa, COUNT(*) as cnt, SUM(l.monto) as total
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion AND l.marketplace = c.marketplace
    WHERE l.marketplace='RIPLEY'
    GROUP BY c.clasificacion_operativa
    ORDER BY cnt DESC
""")
print("\nRipley classifications (correct JOIN):")
for _, r in q2.iterrows():
    print("  %-40s cnt=%s total=$%.0f" % (r['clasificacion_operativa'], r['cnt'], r['total']))

# Check classification of 'A pagar' specifically
q3 = db.query("""
    SELECT c.clasificacion_operativa, c.origen_clasificacion, c.detalle as clas_detalle
    FROM marketplace_ledger_v1 l
    JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion AND l.marketplace = c.marketplace
    WHERE l.marketplace='RIPLEY' AND l.detalle = 'A pagar'
    LIMIT 3
""")
print("\n'A pagar' classification samples:")
for _, r in q3.iterrows():
    print("  clasif=%s origen=%s det=%s" % (r['clasificacion_operativa'], r['origen_clasificacion'], r['clas_detalle']))
