import sys, os, time, json, calendar
os.chdir(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
sys.path.insert(0, '.')
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

engine = MarketplaceAuditorEngine()

# Delete ALL stale RIPLEY cierre rows first
engine.db.execute("DELETE FROM marketplace_cierre_financiero_v1 WHERE marketplace = 'RIPLEY'")
print("Deleted all stale RIPLEY cierre rows")

# Get periods from ledger
periods = engine.db.query("""
    SELECT DISTINCT strftime(fecha, '%Y-%m') as month
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    ORDER BY month
""")
all_periods = periods['month'].tolist()
print(f"RIPLEY periods: {len(all_periods)}")

results = {}
t0 = time.time()
for month_str in all_periods:
    year, month = int(month_str[:4]), int(month_str[5:])
    periodo_inicio = f"{year}-{month:02d}-01"
    last_day = calendar.monthrange(year, month)[1]
    periodo_fin = f"{year}-{month:02d}-{last_day}"
    res = engine.run_financial_closing('RIPLEY', periodo_inicio, periodo_fin)
    results[month_str] = res

t1 = time.time()
print(f"\nTotal: {t1-t0:.1f}s")
total_neto = sum(r['neto'] for r in results.values())
print(f"Total neto: ${total_neto:,.2f}")

count = engine.db.query("SELECT COUNT(*) FROM marketplace_cierre_financiero_v1 WHERE marketplace='RIPLEY'").iloc[0]['cnt']
print(f"RIPLEY cierre rows: {count}/{len(all_periods)}")

# Show all
for month_str, r in sorted(results.items()):
    print(f"  {month_str}: ing={r['ingresos']:>12,.2f} dev={r['devoluciones']:>11,.2f} cop={r['costos_op']:>11,.2f} ccm={r['costos_com']:>11,.2f} aju={r['ajustes']:>11,.2f} neto={r['neto']:>12,.2f}")

with open('_fase2_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)
print("\nFASE 2 COMPLETE")
