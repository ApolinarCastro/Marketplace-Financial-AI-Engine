import sys, os, time, json
os.chdir(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
sys.path.insert(0, '.')
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

engine = MarketplaceAuditorEngine()

# Determine RIPLEY periods from ledger data
periods = engine.db.query("""
    SELECT DISTINCT strftime(fecha, '%Y-%m') as month
    FROM marketplace_ledger_v1
    WHERE marketplace = 'RIPLEY'
    ORDER BY month
""")
all_periods = periods['month'].tolist()
print(f"RIPLEY periods to close: {len(all_periods)}")
print(f"  {all_periods}")

import calendar
results = {}
t0 = time.time()
for month_str in all_periods:
    year, month = int(month_str[:4]), int(month_str[5:])
    periodo_inicio = f"{year}-{month:02d}-01"
    last_day = calendar.monthrange(year, month)[1]
    periodo_fin = f"{year}-{month:02d}-{last_day}"
    
    t_start = time.time()
    res = engine.run_financial_closing('RIPLEY', periodo_inicio, periodo_fin)
    t_elapsed = time.time() - t_start
    results[month_str] = res
    print(f"  {month_str}: neto=${res['neto']:>10,.2f} ({t_elapsed:.1f}s)")

t1 = time.time()
print(f"\nTotal duration: {t1-t0:.1f}s")

# Verify: count cierre rows for RIPLEY
post_count = engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_cierre_financiero_v1 WHERE marketplace='RIPLEY'").iloc[0]['cnt']
print(f"RIPLEY cierre rows: {post_count}")

# Verify neto matches expected
total_neto = sum(r['neto'] for r in results.values())
print(f"Total neto across periods: ${total_neto:,.2f}")
print(f"Expected (Rest = half of total): $206,946,843.00")

with open('_fase2_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str, ensure_ascii=False)
print("\nResults saved to _fase2_results.json")
