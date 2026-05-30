import sys
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()

# Check include_in_operational_pnl for "A pagar" in both tables
for tbl in ['marketplace_ledger_v1', 'marketplace_ledger_clasificado_v1']:
    r = db.query(f"""
        SELECT include_in_operational_pnl, COUNT(*) as cnt, SUM(COALESCE(monto,0)) as total
        FROM {tbl}
        WHERE marketplace = 'RIPLEY' AND (detalle = 'A pagar' OR financial_group = 'ajustes')
        GROUP BY include_in_operational_pnl
    """)
    print(f"=== {tbl} (A pagar / ajustes) ===")
    for _, row in r.iterrows():
        val = row['include_in_operational_pnl']
        print(f"  include_in_operational_pnl={repr(val)}  cnt={row['cnt']}  total=${row['total']:>,.0f}")
    print()

# Check: what does COALESCE produce for these values?
r2 = db.query("""
    SELECT DISTINCT include_in_operational_pnl, 
           COALESCE(include_in_operational_pnl, 1) as coalesced,
           TYPEOF(include_in_operational_pnl) as typ
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'A pagar'
""")
print("=== Type info for A pagar ===")
for _, row in r2.iterrows():
    print(f"  raw={repr(row['include_in_operational_pnl'])}  type={row['typ']}  coalesced={row['coalesced']}")

# Full table stats: what values exist?
r3 = db.query("""
    SELECT DISTINCT include_in_operational_pnl, TYPEOF(include_in_operational_pnl) as typ,
           COUNT(*) as cnt
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY include_in_operational_pnl
""")
print("\n=== All distinct include_in_operational_pnl values in ledger_v1 (RIPLEY) ===")
for _, row in r3.iterrows():
    print(f"  value={repr(row['include_in_operational_pnl'])}  type={row['typ']}  cnt={row['cnt']}")
