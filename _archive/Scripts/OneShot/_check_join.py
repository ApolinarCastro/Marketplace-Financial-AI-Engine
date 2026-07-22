import duckdb
con = duckdb.connect('data/db/meli_financial_v4.db')

# Check ledger fg for non-A-pagar (P&L) rows
r = con.execute("""
    SELECT 
        COUNT(*) as total_rows,
        SUM(monto) as total_amount,
        COUNT(CASE WHEN financial_group IS NOT NULL THEN 1 END) as fg_not_null,
        COUNT(CASE WHEN financial_group IS NULL THEN 1 END) as fg_null,
        SUM(CASE WHEN financial_group IS NOT NULL THEN monto ELSE 0 END) as fg_not_null_amount,
        SUM(CASE WHEN financial_group IS NULL THEN monto ELSE 0 END) as fg_null_amount
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle != 'A pagar'
""").fetchone()
print("=== Non-A-Pagar (P&L) rows ledger-side ===")
print(f"Total: {r[0]:,} rows, ${r[1]:,.2f}")
print(f"financial_group NOT NULL: {r[2]:,} rows, ${r[4]:,.2f}")
print(f"financial_group NULL:     {r[3]:,} rows, ${r[5]:,.2f}")

# Check ledger fg for A pagar rows
r2 = con.execute("""
    SELECT 
        COUNT(*) as total_rows,
        SUM(monto) as total_amount,
        COUNT(CASE WHEN financial_group IS NOT NULL THEN 1 END) as fg_not_null,
        COUNT(CASE WHEN financial_group IS NULL THEN 1 END) as fg_null
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND detalle = 'A pagar'
""").fetchone()
print("\n=== A pagar rows ledger-side ===")
print(f"Total: {r2[0]:,} rows, ${r2[1]:,.2f}")
print(f"financial_group NOT NULL: {r2[2]:,}")
print(f"financial_group NULL:     {r2[3]:,}")

# Check JOIN ON (id_transaccion, detalle) vs just id_transaccion
print("\n=== JOIN COMPARISON ===")
# Using id_transaccion only
r3 = con.execute("""
    SELECT COUNT(*) as matched FROM marketplace_ledger_v1 l
    INNER JOIN marketplace_ledger_clasificado_v1 lc ON l.id_transaccion = lc.id_transaccion
    WHERE l.marketplace = 'RIPLEY' AND l.detalle != 'A pagar'
""").fetchone()[0]
print(f"Join on id_transaccion only: {r3} matched")

# Using id_transaccion AND detalle
r4 = con.execute("""
    SELECT COUNT(*) as matched FROM marketplace_ledger_v1 l
    INNER JOIN marketplace_ledger_clasificado_v1 lc ON l.id_transaccion = lc.id_transaccion AND l.detalle = lc.detalle
    WHERE l.marketplace = 'RIPLEY' AND l.detalle != 'A pagar'
""").fetchone()[0]
print(f"Join on id_transaccion+detalle: {r4} matched")

# Check clasificado financial_group distribution
print("\n=== CLASIFICADO fg distribution (RIPLEY) ===")
fg = con.execute("""
    SELECT clasificacion_operativa, financial_group, COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_clasificado_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY clasificacion_operativa, financial_group
    ORDER BY total DESC
    LIMIT 20
""").fetchdf()
for _, row in fg.iterrows():
    print(f"  {str(row['clasificacion_operativa']):45s} | fg={str(row['financial_group']):25s} | rows={row['cnt']:>5d} | ${row['total']:>12,.2f}")

con.close()
