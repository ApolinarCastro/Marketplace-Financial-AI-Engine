import sys
sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)

# Test desglose for RIPLEY 2026-12
resp = client.get("/api/v4/cierre/desglose?marketplace=RIPLEY&periodo=2026-12")
data = resp.json()

print(f"Total rows: {len(data)}")
total = sum(r['total'] for r in data)
print(f"Total sum: ${total:,.0f}")

# Group by financial_group/categoria
from collections import defaultdict
by_cat = defaultdict(float)
for r in data:
    by_cat[r['categoria']] += r['total']

print("\n=== By financial_group ===")
for cat, tot in sorted(by_cat.items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {cat:25s} ${tot:>12,.0f}")

# Check if "A pagar" or ajustes with include_in_operational_pnl=False appears
print("\n=== Detail rows ===")
for r in data:
    if r['detalle'] == 'A pagar' or abs(r['total']) > 10000:
        print(f"  cat={r['categoria']:25s} detalle={str(r['detalle']):50s} total=${r['total']:>12,.0f}")

# Now query the DB directly with the same conditions
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
df = db.query("""
    SELECT COALESCE(financial_group, '?') as fg, detalle, SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND fecha BETWEEN '2026-12-01' AND '2026-12-31'
      AND COALESCE(include_in_operational_pnl, 1) = 1
    GROUP BY fg, detalle
    ORDER BY total ASC
""")
print("\n=== DB direct (with include_in_operational_pnl filter) ===")
for _, r in df.iterrows():
    print(f"  fg={str(r['fg']):25s} detalle={str(r['detalle']):50s} total=${float(r['total']):>12,.0f}")
db_total = float(df['total'].sum())
print(f"  {'TOTAL':25s} {'':50s} ${db_total:>12,.0f}")
