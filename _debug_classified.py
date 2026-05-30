import sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

# Count table sizes
print("Ledger total:", db.query("SELECT COUNT(*) as c FROM marketplace_ledger_v1").iloc[0]['c'])
print("Classified total:", db.query("SELECT COUNT(*) as c FROM marketplace_ledger_clasificado_v1").iloc[0]['c'])

# Check how many unique (marketplace, id_transaccion) pairs
print("\nUnique ledger pairs:", db.query("SELECT COUNT(*) as c FROM (SELECT DISTINCT marketplace, id_transaccion FROM marketplace_ledger_v1)").iloc[0]['c'])
print("Unique classified pairs:", db.query("SELECT COUNT(*) as c FROM (SELECT DISTINCT marketplace, id_transaccion FROM marketplace_ledger_clasificado_v1)").iloc[0]['c'])

# Check if there are duplicates in classified
print("\nDuplicates in classified:")
dups = db.query("""
    SELECT marketplace, id_transaccion, COUNT(*) as cnt
    FROM marketplace_ledger_clasificado_v1
    GROUP BY marketplace, id_transaccion
    HAVING COUNT(*) > 1
    LIMIT 10
""")
for _, r in dups.iterrows():
    print(f"  {r['marketplace']} {r['id_transaccion']}: {r['cnt']}")

# Sample classified rows
print("\nSample classified (5 rows):")
samp = db.query("SELECT * FROM marketplace_ledger_clasificado_v1 LIMIT 5")
for _, r in samp.iterrows():
    print(f"  mp={r['marketplace']} id={r['id_transaccion']} det={r['detalle']} clasif={r['clasificacion_operativa']}")
