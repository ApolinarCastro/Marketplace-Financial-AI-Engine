import duckdb
con = duckdb.connect('data/db/meli_financial_v4.db')

# Show all RIPLEY cierre rows
rows = con.execute("""
    SELECT periodo_inicio, periodo_fin, total_ingresos, total_costos_operacionales, 
           total_costos_comerciales, total_ajustes, resultado_neto
    FROM marketplace_cierre_financiero_v1
    WHERE marketplace = 'RIPLEY'
    ORDER BY periodo_inicio
""").fetchdf()
print("=== RIPLEY CIERRE ROWS ===")
valid = ['2025-01','2025-02','2025-03','2025-04','2025-05','2025-06','2025-07','2025-08','2025-09','2025-10','2025-11','2025-12',
         '2026-01','2026-02','2026-03','2026-04','2026-05']
for _, r in rows.iterrows():
    pi = str(r['periodo_inicio'])[:7]
    is_valid = pi in valid
    print(f"  {str(r['periodo_inicio'])[:10]:10s} | ing={r['total_ingresos']:>12,.2f} | neto={r['resultado_neto']:>12,.2f} | {'VALID' if is_valid else 'STALE'}")

# Delete stale rows
print()
deleted = con.execute("""
    DELETE FROM marketplace_cierre_financiero_v1 
    WHERE marketplace = 'RIPLEY' 
      AND CAST(strftime(periodo_inicio, '%Y-%m') AS VARCHAR) NOT IN ('2025-01','2025-02','2025-03','2025-04','2025-05','2025-06','2025-07','2025-08','2025-09','2025-10','2025-11','2025-12','2026-01','2026-02','2026-03','2026-04','2026-05')
""")
print(f"Deleted stale rows: {deleted}")

# Verify only 17 remain
count = con.execute("SELECT COUNT(*) FROM marketplace_cierre_financiero_v1 WHERE marketplace='RIPLEY'").fetchone()[0]
print(f"RIPLEY cierre rows after cleanup: {count} (expected 17)")
con.close()
