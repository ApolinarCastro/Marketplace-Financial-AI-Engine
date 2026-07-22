"""Explore snapshot meli_financial_v4.db"""
import duckdb, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

db = r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\data\db\snapshot_baseline_v6_20260529_105928\meli_financial_v4.db"
conn = duckdb.connect(db)

tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog')").fetchall()
print("Tables:", [t[0] for t in tables])

for t in tables:
    name = t[0]
    cnt = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(f"\n{name}: {cnt} rows")
    cols = conn.execute(f"DESCRIBE {name}").fetchall()
    for c in cols:
        print(f"  {c[0]} ({c[1]})")
