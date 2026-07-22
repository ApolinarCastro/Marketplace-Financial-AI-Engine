import duckdb
con = duckdb.connect('data/db/meli_financial_v4.db')

# Which RIPLEY rows have NULL financial_group?
df = con.execute("""
    SELECT id_transaccion, detalle, monto, fecha
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY' AND financial_group IS NULL
    ORDER BY monto DESC
    LIMIT 50
""").fetchdf()
print("=== NULL financial_group RIPLEY rows (top 50 by monto) ===")
for _, r in df.iterrows():
    print(f'  {r["id_transaccion"]:20s} | detalle="{r["detalle"]}" | ${r["monto"]:>10,.2f} | {r["fecha"]}')

print()
# Check if these id_transaccion exist in clasificado table
missing = con.execute("""
    SELECT COUNT(*) as cnt
    FROM marketplace_ledger_v1 l
    LEFT JOIN marketplace_ledger_clasificado_v1 lc ON l.id_transaccion = lc.id_transaccion
    WHERE l.marketplace = 'RIPLEY' AND l.financial_group IS NULL AND lc.id_transaccion IS NULL
""").fetchone()[0]
print(f"Rows missing from clasificado entirely: {missing}")

# Check if they have clasificado rows but NULL financial_group was from propagation mismatch
mismatch = con.execute("""
    SELECT COUNT(*) as cnt
    FROM marketplace_ledger_v1 l
    INNER JOIN marketplace_ledger_clasificado_v1 lc ON l.id_transaccion = lc.id_transaccion
    WHERE l.marketplace = 'RIPLEY' AND l.financial_group IS NULL AND lc.financial_group IS NOT NULL
""").fetchone()[0]
print(f"Rows with clasificado data but ledger fg NULL (propagation mismatch): {mismatch}")

# Distribution of detalle for unmatched
detalles = con.execute("""
    SELECT l.detalle, COUNT(*) as cnt, SUM(l.monto) as total
    FROM marketplace_ledger_v1 l
    LEFT JOIN marketplace_ledger_clasificado_v1 lc ON l.id_transaccion = lc.id_transaccion
    WHERE l.marketplace = 'RIPLEY' AND l.financial_group IS NULL
    GROUP BY l.detalle
    ORDER BY total DESC
""").fetchdf()
print()
print("=== NULL fg by detalle ===")
for _, r in detalles.iterrows():
    print(f'  "{r["detalle"]:45s}" | cnt={r["cnt"]:>5d} | total=${r["total"]:>12,.2f}')

# Check: does the clasificado table have financial_group populated for RIPLEY?
fg_check = con.execute("""
    SELECT financial_group, COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_clasificado_v1
    WHERE marketplace = 'RIPLEY'
    GROUP BY financial_group
    ORDER BY financial_group
""").fetchdf()
print()
print("=== RIPLEY clasificado financial_group check ===")
for _, r in fg_check.iterrows():
    print(f'  {str(r["financial_group"]):25s} | cnt={r["cnt"]:>5d} | total=${r["total"]:>12,.2f}')

con.close()
