import sys, os, time, json
os.chdir(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
sys.path.insert(0, '.')

from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

start = time.time()

engine = MarketplaceAuditorEngine()

# Set temp directory for DuckDB before classification
import tempfile
tmp_dir = tempfile.gettempdir().replace("\\", "/")
engine.db.execute(f"SET temp_directory='{tmp_dir}';")

# Pre-state ledger row counts
pre_counts = {}
for m in ['RIPLEY', 'ML', 'PARIS', 'FALABELLA']:
    r = engine.db.query(f"SELECT COUNT(*) as cnt, SUM(monto) as total FROM marketplace_ledger_v1 WHERE marketplace = '{m}'").iloc[0]
    pre_counts[m] = {'rows': int(r['cnt']), 'total': float(r['total'])}
    
pre_clasif_rows = int(engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_clasificado_v1 WHERE marketplace = 'RIPLEY'").iloc[0]['cnt'])
pre_clasif_amount = float(engine.db.query("SELECT COALESCE(SUM(monto),0) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace = 'RIPLEY'").iloc[0]['total'])
pre_null_fg = int(engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY' AND financial_group IS NULL").iloc[0]['cnt'])

print(f"=== PRE-STATE ===")
print(f"Ledger: RIPLEY={pre_counts['RIPLEY']['rows']:,} rows, ${pre_counts['RIPLEY']['total']:,.2f}")
print(f"Clasificado: RIPLEY={pre_clasif_rows:,} rows, ${pre_clasif_amount:,.2f}")
print(f"RIPLEY financial_group NULL: {pre_null_fg:,} rows")
print()

# Execute classification
t0 = time.time()
n = engine.run_classification()
t1 = time.time()
duration = t1 - t0

print(f"=== CLASSIFICATION RESULT ===")
print(f"Rows classified: {n:,}")
print(f"Duration: {duration:.2f}s")

# Post-state
post_counts = {}
for m in ['RIPLEY', 'ML', 'PARIS', 'FALABELLA']:
    r = engine.db.query(f"SELECT COUNT(*) as cnt, SUM(monto) as total FROM marketplace_ledger_v1 WHERE marketplace = '{m}'").iloc[0]
    post_counts[m] = {'rows': int(r['cnt']), 'total': float(r['total'])}
    
post_clasif_rows = int(engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_clasificado_v1").iloc[0]['cnt'])
ripley_clasif_rows = int(engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_clasificado_v1 WHERE marketplace = 'RIPLEY'").iloc[0]['cnt'])
ripley_clasif_amount = float(engine.db.query("SELECT COALESCE(SUM(monto),0) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace = 'RIPLEY'").iloc[0]['total'])
post_null_fg = int(engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace = 'RIPLEY' AND financial_group IS NULL").iloc[0]['cnt'])
post_null_fg_total_all = int(engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE financial_group IS NULL").iloc[0]['cnt'])

# Coverage by marketplace
coverage = engine.db.query("""
    SELECT l.marketplace,
        COUNT(*) as total_rows,
        COUNT(CASE WHEN lc.financial_group IS NOT NULL THEN 1 END) as clasif_rows,
        COALESCE(SUM(CASE WHEN lc.financial_group IS NOT NULL THEN l.monto ELSE 0 END),0) as clasif_amount,
        COALESCE(SUM(l.monto),0) as total_amount
    FROM marketplace_ledger_v1 l
    LEFT JOIN marketplace_ledger_clasificado_v1 lc ON l.id_transaccion = lc.id_transaccion AND l.detalle = lc.detalle
    GROUP BY l.marketplace
    ORDER BY l.marketplace
""")

results = {
    'pre_state': pre_counts,
    'post_state': post_counts,
    'pre_clasif_rows': pre_clasif_rows,
    'pre_clasif_amount': pre_clasif_amount,
    'post_clasif_total_rows': post_clasif_rows,
    'post_ripley_clasif_rows': ripley_clasif_rows,
    'post_ripley_clasif_amount': ripley_clasif_amount,
    'pre_null_fg': pre_null_fg,
    'post_null_fg_ripley': post_null_fg,
    'post_null_fg_all_marketplaces': post_null_fg_total_all,
    'duration_seconds': round(duration, 2),
    'coverage': coverage.to_dict('records'),
    'pass': post_null_fg == 0 and post_null_fg_total_all == 0
}

print()
print(f"=== POST-STATE ===")
print(f"Total clasificado rows: {post_clasif_rows:,}")
print(f"RIPLEY clasificado rows: {ripley_clasif_rows:,}")
print(f"RIPLEY clasificado amount: ${ripley_clasif_amount:,.2f}")
print(f"RIPLEY financial_group NULL: {post_null_fg:,}")
print(f"ALL marketplaces financial_group NULL: {post_null_fg_total_all:,}")
print(f"Coverage per marketplace:")
for r in coverage.to_dict('records'):
    cov_pct = (r['clasif_rows'] / r['total_rows'] * 100) if r['total_rows'] else 0
    amt_cov = (r['clasif_amount'] / r['total_amount'] * 100) if r['total_amount'] else 0
    print(f"  {r['marketplace']:12s}: rows={r['clasif_rows']:>6d}/{r['total_rows']:>6d} ({cov_pct:.2f}%) amt=${r['clasif_amount']:>14,.2f}/{r['total_amount']:>14,.2f} ({amt_cov:.2f}%)")

print(f"\nFASE 1 {'PASS' if results['pass'] else 'FAIL'}")

with open('_fase1_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str, ensure_ascii=False)
print("Results saved to _fase1_results.json")
