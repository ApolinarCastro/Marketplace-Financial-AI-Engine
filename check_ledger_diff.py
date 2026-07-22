import duckdb

cur = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
snap = duckdb.connect('data/db/snapshot_pre_poscobro_fix_20260605_155052/meli_financial_v4.db', read_only=True)

# Check what's new in ledger - by marketplace
print('=== LEDGER NEW ROWS BY MARKETPLACE ===')
r = cur.execute("""
    SELECT marketplace, COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_v1
    GROUP BY marketplace
""").fetchall()
print('CURRENT:')
for row in r:
    print(f'  {row[0]}: {row[1]:,} rows, {row[2]:,.0f}')

r = snap.execute("""
    SELECT marketplace, COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_v1
    GROUP BY marketplace
""").fetchall()
print('SNAPSHOT:')
for row in r:
    print(f'  {row[0]}: {row[1]:,} rows, {row[2]:,.0f}')

# Check classified
print()
print('=== CLASIFICADO NEW ROWS BY MARKETPLACE ===')
r = cur.execute("""
    SELECT marketplace, financial_group, COUNT(*) as cnt
    FROM marketplace_ledger_clasificado_v1
    GROUP BY marketplace, financial_group
    ORDER BY marketplace, cnt DESC
""").fetchall()
print('CURRENT:')
for row in r:
    print(f'  {row[0]} | {row[1]} | {row[2]:,}')

r = snap.execute("""
    SELECT marketplace, financial_group, COUNT(*) as cnt
    FROM marketplace_ledger_clasificado_v1
    GROUP BY marketplace, financial_group
    ORDER BY marketplace, cnt DESC
""").fetchall()
print('SNAPSHOT:')
for row in r:
    print(f'  {row[0]} | {row[1]} | {row[2]:,}')

cur.close()
snap.close()