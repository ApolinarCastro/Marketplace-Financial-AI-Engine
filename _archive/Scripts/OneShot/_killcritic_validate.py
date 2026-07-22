from __future__ import annotations
import sys, json
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get()

# === 1. Schema check ===
print("=== marketplace_ledger_v1 columns ===")
cols = db.query("PRAGMA table_info(marketplace_ledger_v1)")
for c in cols.to_dict('records'):
    print(f"  {c['name']:30s} {c['type']}")
print()

print("=== marketplace_ledger_clasificado_v1 columns ===")
cols2 = db.query("PRAGMA table_info(marketplace_ledger_clasificado_v1)")
for c in cols2.to_dict('records'):
    print(f"  {c['name']:30s} {c['type']}")
print()

# === 2. financial_group stats ===
print("=== financial_group in ledger_v1 ===")
r = db.query("SELECT financial_group, COUNT(*) as cnt, SUM(COALESCE(monto,0)) as total FROM marketplace_ledger_v1 WHERE financial_group IS NOT NULL GROUP BY financial_group ORDER BY total DESC")
for row in r.to_dict('records'):
    print(f"  {str(row['financial_group']):35s} cnt={row['cnt']:>6d}  total=${row['total']:>12,.0f}")
nulls = db.query("SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE financial_group IS NULL")
print(f"  NULL financial_group: {nulls.iloc[0,0]}")
print()

# === 3. Row counts per marketplace ===
print("=== Rows per marketplace ===")
r2 = db.query("SELECT marketplace, COUNT(*) as cnt, SUM(COALESCE(monto,0)) as total FROM marketplace_ledger_v1 GROUP BY marketplace ORDER BY total DESC")
for row in r2.to_dict('records'):
    print(f"  {str(row['marketplace']):12s} cnt={row['cnt']:>7d}  total=${row['total']:>14,.0f}")
print()

# === 4. Test each marketplace: desglose sum vs ledger sum filtered ===
marketplaces = ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']
for mp in marketplaces:
    # Most recent period
    df_period = db.query("SELECT MAX(fecha) as mx FROM marketplace_ledger_v1 WHERE marketplace = ?", [mp])
    mx = df_period.iloc[0]['mx']
    if mx is None:
        print(f"{mp}: NO DATA")
        continue
    mx = str(mx)[:7]  # YYYY-MM
    year, month = mx.split('-')
    import calendar
    last_day = calendar.monthrange(int(year), int(month))[1]
    p_ini = f"{year}-{month}-01"
    p_fin = f"{year}-{month}-{last_day}"

    # Desglose sum
    desg = db.query("""
        SELECT SUM(total) as subtotal FROM (
            SELECT SUM(monto) as total
            FROM marketplace_ledger_v1
            WHERE marketplace = ? AND fecha BETWEEN ? AND ?
            GROUP BY detalle, tipo_movimiento, COALESCE(financial_group,'?')
        )
    """, [mp, p_ini, p_fin])
    desg_total = float(desg.iloc[0]['subtotal'] or 0)

    # Ledger total sum (same filter, no group by)
    ledg = db.query("SELECT SUM(COALESCE(monto,0)) as total FROM marketplace_ledger_v1 WHERE marketplace = ? AND fecha BETWEEN ? AND ?", [mp, p_ini, p_fin])
    ledg_total = float(ledg.iloc[0]['total'] or 0)

    # Financial groups in desglose
    fg = db.query("""
        SELECT COALESCE(financial_group,'?') as fg, COUNT(*) as cnt, SUM(COALESCE(monto,0)) as total
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND fecha BETWEEN ? AND ?
        GROUP BY fg ORDER BY total DESC
    """, [mp, p_ini, p_fin])

    match = "OK" if abs(desg_total - ledg_total) < 0.01 else "MISMATCH"
    print(f"{mp} [periodo={mx}] desglose=${desg_total:>10,.0f} ledger=${ledg_total:>10,.0f} diff=${abs(desg_total - ledg_total):>8,.0f}  {match}")
    for f in fg.to_dict('records'):
        print(f"    {str(f['fg']):35s} cnt={f['cnt']:>6d}  ${f['total']:>12,.0f}")
    print()

# === 5. Test financial_group filter on ledger endpoint ===
print("=== financial_group filter test (RIPLEY, 'ingresos_brutos') ===")
for mp in marketplaces:
    fg_test = db.query("""
        SELECT COALESCE(financial_group,'?') as fg, SUM(COALESCE(monto,0)) as total
        FROM marketplace_ledger_v1
        WHERE marketplace = ? AND financial_group = 'ingresos_brutos'
        GROUP BY fg
    """, [mp])
    if not fg_test.empty:
        row = fg_test.iloc[0]
        print(f"  {mp}: ingresos_brutos = ${row['total']:>12,.0f}")
    else:
        print(f"  {mp}: ingresos_brutos = NO DATA")

print()
print("=== VALIDATION COMPLETE ===")
