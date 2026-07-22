import duckdb
conn = duckdb.connect('data/db/snapshot_pre_poscobro_fix_20260605_155052/meli_financial_v4.db', read_only=True)
# Check RIPLEY ledger
r = conn.execute("""
    SELECT financial_group, COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY financial_group
""").fetchall()
print('=== RIPLEY LEDGER (pre_poscobro_fix) ===')
for row in r:
    print(f'{row[0]} | {row[1]} | {row[2]:,.0f}')

# Check RIPLEY cierre
r = conn.execute("""
    SELECT marketplace, periodo_fin, resultado_neto
    FROM marketplace_cierre_financiero_v1
    WHERE marketplace = 'RIPLEY'
    ORDER BY periodo_fin
""").fetchall()
print()
print('=== RIPLEY CIERRE (pre_poscobro_fix) ===')
for row in r:
    print(f'{row[0]} | {row[1]} | {row[2]:,.0f}')

# Check classified
r = conn.execute("""
    SELECT financial_group, COUNT(*) as cnt
    FROM marketplace_ledger_clasificado_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY financial_group
""").fetchall()
print()
print('=== RIPLEY CLASIFICADO (pre_poscobro_fix) ===')
for row in r:
    print(f'{row[0]} | {row[1]}')

conn.close()