import duckdb, pandas as pd, pathlib
snap = pathlib.Path(r'data/db/snapshot_pre_dec019_20260607_161324/meli_financial_v4.db')
conn = duckdb.connect(str(snap), read_only=True)

print('=== LEDGER financial_group per MP (op_pnl=1) ===')
df = conn.execute("""
SELECT marketplace, COALESCE(financial_group,'NULL') as fg, 
  ROUND(SUM(monto),2) as total, COUNT(*) as cnt
FROM marketplace_ledger_v1
WHERE COALESCE(include_in_operational_pnl,1)=1
GROUP BY marketplace, financial_group
ORDER BY marketplace, fg
""").fetchdf()
for _, r in df.iterrows():
    mp = r['marketplace']
    fg = str(r['fg'])
    cnt = int(r['cnt'])
    total = float(r['total'])
    print(f"  {mp:12s} | {fg:30s} | {cnt:8d} | ${total:>14.2f}")

print()
print('=== PARIS details in costos_operacionales ===')
df2 = conn.execute("""
SELECT detalle, ROUND(SUM(monto),2) as total, COUNT(*) as cnt
FROM marketplace_ledger_v1
WHERE marketplace='PARIS' AND financial_group='costos_operacionales'
  AND COALESCE(include_in_operational_pnl,1)=1
GROUP BY detalle
ORDER BY ABS(SUM(monto)) DESC
""").fetchdf()
for _, r in df2.iterrows():
    det = str(r['detalle'])
    cnt = int(r['cnt'])
    total = float(r['total'])
    print(f"  {det:40s} | {cnt:6d} | ${total:>14.2f}")

print()
print('=== PARIS details in ajustes ===')
df3 = conn.execute("""
SELECT detalle, ROUND(SUM(monto),2) as total, COUNT(*) as cnt
FROM marketplace_ledger_v1
WHERE marketplace='PARIS' AND financial_group='ajustes'
  AND COALESCE(include_in_operational_pnl,1)=1
GROUP BY detalle
ORDER BY ABS(SUM(monto)) DESC
""").fetchdf()
for _, r in df3.iterrows():
    det = str(r['detalle'])
    cnt = int(r['cnt'])
    total = float(r['total'])
    print(f"  {det:40s} | {cnt:6d} | ${total:>14.2f}")

print()
print('=== PARIS: ledger vs clasificado mismatch ===')
df4 = conn.execute("""
SELECT l.financial_group as led_fg, c.financial_group as cla_fg,
  COUNT(*) as cnt, ROUND(SUM(l.monto),2) as total
FROM marketplace_ledger_v1 l
JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
WHERE l.marketplace='PARIS' AND COALESCE(l.include_in_operational_pnl,1)=1
  AND LOWER(l.financial_group) != LOWER(c.financial_group)
GROUP BY l.financial_group, c.financial_group
ORDER BY cnt DESC
""").fetchdf()
if len(df4) > 0:
    for _, r in df4.iterrows():
        lfg = str(r['led_fg'])
        cfg = str(r['cla_fg'])
        cnt = int(r['cnt'])
        total = float(r['total'])
        print(f"  led={lfg:30s} cla={cfg:30s} | {cnt:6d} | ${total:>14.2f}")
else:
    print("  ALL rows match")

print()
print('=== Has financial_subgroup column? ===')
try:
    cols = conn.execute('DESCRIBE marketplace_ledger_v1').fetchdf()
    has_subgroup = 'financial_subgroup' in cols['column_name'].tolist()
    print(f"  Has financial_subgroup: {has_subgroup}")
    if has_subgroup:
        print("  All column names:", cols['column_name'].tolist())
except Exception as e:
    print(f"  Error: {e}")

print()
print('=== RIPLEY details per group (top 5 per group) ===')
for g in ['ingresos','devoluciones','costos_operacionales','costos_comerciales','ajustes']:
    df5 = conn.execute(f"""
    SELECT detalle, ROUND(SUM(monto),2) as total, COUNT(*) as cnt
    FROM marketplace_ledger_v1
    WHERE marketplace='RIPLEY' AND financial_group='{g}'
      AND COALESCE(include_in_operational_pnl,1)=1
    GROUP BY detalle
    ORDER BY ABS(SUM(monto)) DESC
    LIMIT 5
    """).fetchdf()
    total_g = float(df5['total'].sum()) if len(df5) > 0 else 0
    print(f"  {g} (total ${total_g:>.2f}):")
    for _, r in df5.iterrows():
        det = str(r['detalle'])
        cnt = int(r['cnt'])
        total = float(r['total'])
        print(f"    {det:40s} | {cnt:5d} | ${total:>14.2f}")

conn.close()
