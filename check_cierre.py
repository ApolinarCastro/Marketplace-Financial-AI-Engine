import duckdb

snap = duckdb.connect('data/db/snapshot_pre_poscobro_fix_20260605_155052/meli_financial_v4.db', read_only=True)

# Check cierre rows for RIPLEY
r = snap.execute("""
    SELECT marketplace, COUNT(*) as cnt
    FROM marketplace_cierre_financiero_v1
    GROUP BY marketplace
""").fetchall()
print('CIERRE ROWS BY MARKETPLACE (snapshot):')
for row in r:
    print(f'  {row[0]}: {row[1]}')

# Check RIPLEY periods with non-zero neto
r = snap.execute("""
    SELECT periodo_fin, resultado_neto
    FROM marketplace_cierre_financiero_v1
    WHERE marketplace = 'RIPLEY' AND resultado_neto != 0
    ORDER BY periodo_fin
""").fetchall()
print()
print('RIPLEY CIERRE PERIODS WITH NON-ZERO NETO:')
for row in r:
    print(f'  {row[0]}: {row[1]:,.0f}')

snap.close()