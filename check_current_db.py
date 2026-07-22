import duckdb
conn = duckdb.connect('data/db/meli_financial_v4.db', read_only=True)
r = conn.execute("""
    SELECT marketplace, financial_group, SUM(monto) as total, COUNT(*) as cnt
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY marketplace, financial_group
""").fetchall()
print('=== CURRENT RIPLEY LEDGER ===')
for row in r:
    print(f'{row[0]} | {row[1]} | {row[2]:,.0f} | {row[3]}')

r = conn.execute("""
    SELECT marketplace, periodo_fin, resultado_neto
    FROM marketplace_cierre_financiero_v1
    WHERE marketplace = 'RIPLEY'
    ORDER BY periodo_fin
""").fetchall()
print()
print('=== CURRENT RIPLEY CIERRE ===')
for row in r:
    print(f'{row[0]} | {row[1]} | {row[2]:,.0f}')

r = conn.execute("""
    SELECT marketplace, financial_group, COUNT(*) as cnt
    FROM marketplace_ledger_clasificado_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY marketplace, financial_group
""").fetchall()
print()
print('=== CURRENT RIPLEY CLASIFICADO ===')
for row in r:
    print(f'{row[0]} | {row[1]} | {row[2]}')

conn.close()