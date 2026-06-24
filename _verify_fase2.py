import duckdb, json
con = duckdb.connect('data/db/meli_financial_v4.db')

# Verify cierre
count = con.execute("SELECT COUNT(*) FROM marketplace_cierre_financiero_v1 WHERE marketplace='RIPLEY'").fetchone()[0]
print(f"RIPLEY cierre rows: {count} (expected 17)")

# Show all cierre
rows = con.execute("""
    SELECT periodo_inicio, periodo_fin, total_ingresos, total_costos_operacionales, 
           total_costos_comerciales, total_ajustes, resultado_neto
    FROM marketplace_cierre_financiero_v1
    WHERE marketplace = 'RIPLEY'
    ORDER BY periodo_inicio
""").fetchdf()
print(f"\n{'Periodo':10s} {'Ingresos':>14s} {'CostOp':>12s} {'CostCom':>12s} {'Ajustes':>12s} {'Neto':>14s}")
for _, r in rows.iterrows():
    print(f"{str(r['periodo_inicio'])[:7]:10s} {r['total_ingresos']:>14,.2f} {r['total_costos_operacionales']:>12,.2f} {r['total_costos_comerciales']:>12,.2f} {r['total_ajustes']:>12,.2f} {r['resultado_neto']:>14,.2f}")
print(f"{'TOTAL':10s} {rows['total_ingresos'].sum():>14,.2f} {rows['total_costos_operacionales'].sum():>12,.2f} {rows['total_costos_comerciales'].sum():>12,.2f} {rows['total_ajustes'].sum():>12,.2f} {rows['resultado_neto'].sum():>14,.2f}")

# Compare to previous stale state
print("\n=== COMPARISON: OLD (pre-RFC-001 stale) vs NEW (post-RFC-001 correct) ===")
# Old stale neto total was $284,897,360 (included A pagar)
# New correct neto total should be $206,946,843 (excluding A pagar)
# Delta = $206,946,843 - $284,897,360 = -$77,950,517
old_neto = 284897360.00
new_neto = rows['resultado_neto'].sum()
print(f"Old stale neto (included A pagar): ${old_neto:>14,.2f}")
print(f"New correct neto (excluded A pagar): ${new_neto:>14,.2f}")
print(f"Delta: ${new_neto - old_neto:>14,.2f}")

# Verify ML/PARIS/FALABELLA unchanged
print("\n=== ML/PARIS/FALABELLA CIERRE (should be unchanged) ===")
for m in ['ML', 'PARIS', 'FALABELLA']:
    r = con.execute(f"SELECT COUNT(*) as cnt, SUM(resultado_neto) as neto FROM marketplace_cierre_financiero_v1 WHERE marketplace='{m}'").fetchone()
    print(f"  {m:12s}: periods={r[0]:>2d} neto=${r[1]:>16,.2f}")

con.close()
