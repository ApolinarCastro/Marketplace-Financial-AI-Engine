"""
FASE 2 — EXECUTE run_classification()
FASE 3 — EXECUTE run_financial_closing() for all RIPLEY periods
"""
import sys, time, math, json
from datetime import datetime
sys.path.insert(0, '.')

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine, FINANCIAL_STRUCTURE, CLASIFICACION_TO_FINANCIAL_GROUP

db = DatabaseV4.get()
auditor = MarketplaceAuditorEngine()

# ============================================================
# FASE 2 — CLASSIFICATION
# ============================================================
print("=" * 70)
print("FASE 2 — CLASSIFICATION EXECUTION")
print("=" * 70)

# Pre-counts
pre = {
    'clasif_rows': db.count("marketplace_ledger_clasificado_v1"),
    'ripley_ledger_fg_null': float(db.execute("SELECT COALESCE(SUM(monto),0) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND financial_group IS NULL").fetchone()[0]),
}

print(f"Pre-classification:")
print(f"  Clasificado rows: {pre['clasif_rows']:,}")
print(f"  RIPLEY financial_group=NULL: ${pre['ripley_ledger_fg_null']:,.2f}")

# Execute
start = time.time()
n = auditor.run_classification()
elapsed = time.time() - start

print(f"\nClassification executed in {elapsed:.1f}s")
print(f"Rows inserted into clasificado: {n:,}")

# Post-counts
post_clasif = db.count("marketplace_ledger_clasificado_v1")
ripley_fg_null = float(db.execute("SELECT COALESCE(SUM(monto),0) FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND financial_group IS NULL").fetchone()[0])

print(f"\nPost-classification:")
print(f"  Clasificado rows: {post_clasif:,}")
print(f"  RIPLEY financial_group=NULL: ${ripley_fg_null:,.2f} (should be $0)")
print(f"  RIPLEY financial_group NULL eliminated: ${pre['ripley_ledger_fg_null'] - ripley_fg_null:,.2f}")

# RIPLEY financial_group distribution
print(f"\nRIPLEY financial_group after classification:")
r = db.execute("SELECT COALESCE(financial_group, 'NULL') as fg, COUNT(*) as cnt, COALESCE(SUM(monto),0) as tot FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' GROUP BY fg ORDER BY tot DESC").fetchdf()
for _, row in r.iterrows():
    pct = float(row['tot']) / 413893686 * 100
    print(f"  {row['fg']:<30} {row['cnt']:>6,} rows = ${float(row['tot']):>12,.2f} ({pct:.1f}%)")

# RIPLEY clasificacion_operativa distribution
print(f"\nRIPLEY clasificacion_operativa after classification:")
r = db.execute("SELECT clasificacion_operativa, COUNT(*) as cnt, COALESCE(SUM(monto),0) as tot FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' GROUP BY clasificacion_operativa ORDER BY tot DESC").fetchdf()
for _, row in r.iterrows():
    print(f"  {str(row['clasificacion_operativa']):<45} {row['cnt']:>6,} rows = ${float(row['tot']):>12,.2f}")

# RIPLEY include_in_operational_pnl
print(f"\nRIPLEY include_in_operational_pnl after classification:")
r = db.execute("SELECT COALESCE(include_in_operational_pnl::VARCHAR, 'NULL') as pnl, COUNT(*) as cnt, COALESCE(SUM(monto),0) as tot FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' GROUP BY pnl").fetchdf()
for _, row in r.iterrows():
    print(f"  pnl={str(row['pnl']):<10} {row['cnt']:>6,} rows = ${float(row['tot']):>12,.2f}")

# ============================================================
# FASE 3 — FINANCIAL CLOSING
# ============================================================
print("\n" + "=" * 70)
print("FASE 3 — FINANCIAL CLOSING")
print("=" * 70)

# Get all distinct year-month periods for RIPLEY
r = db.execute("SELECT DISTINCT strftime(fecha, '%Y-%m') as month FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' ORDER BY month").fetchdf()
periods = list(r['month'])
print(f"RIPLEY periods to close: {len(periods)}")
for p in periods:
    print(f"  {p}")

# Execute closing for each period
closing_results = {}
for p in periods:
    year, month = p.split('-')
    # Last day of month
    import calendar
    last_day = calendar.monthrange(int(year), int(month))[1]
    periodo_inicio = f"{p}-01"
    periodo_fin = f"{p}-{last_day:02d}"
    
    result = auditor.run_financial_closing('RIPLEY', periodo_inicio, periodo_fin)
    closing_results[p] = result
    print(f"  {p}: neto=${result['neto']:>10,.2f} (ing=${result['ingresos']:>10,.2f} dev=${result['devoluciones']:>10,.2f} cop=${result['costos_op']:>10,.2f} ccm=${result['costos_com']:>10,.2f} aju=${result['ajustes']:>10,.2f})")

# Cross-check: verify closing matches desglose query
print(f"\n--- Cross-check: Cierre vs Desglose sum ---")
total_neto_cierre = sum(r['neto'] for r in closing_results.values())
print(f"Total neto (cierre): ${total_neto_cierre:,.2f}")

# Verificar via desglose query
print(f"\n--- Desglose sum check ---")
for p in periods:
    year, month = p.split('-')
    last_day = calendar.monthrange(int(year), int(month))[1]
    periodo_inicio = f"{p}-01"
    periodo_fin = f"{p}-{last_day:02d}"
    
    r2 = db.execute(f"""
        SELECT COALESCE(financial_group, 'sin_clasificar') as fg, SUM(COALESCE(monto, 0)) as total
        FROM marketplace_ledger_v1
        WHERE marketplace='RIPLEY' AND fecha BETWEEN '{periodo_inicio}' AND '{periodo_fin}'
          AND COALESCE(include_in_operational_pnl, 1) = 1
        GROUP BY fg
    """).fetchdf()
    amounts = {row['fg']: float(row['total']) for _, row in r2.iterrows()}
    ing = amounts.get('ingresos', 0)
    dev = amounts.get('devoluciones', 0)
    cop = amounts.get('costos_operacionales', 0)
    ccm = amounts.get('costos_comerciales', 0)
    aju = amounts.get('ajustes', 0)
    sin = amounts.get('sin_clasificar', 0)
    neto = ing + dev + cop + ccm + aju
    cierre_neto = closing_results[p]['neto']
    delta = abs(neto - cierre_neto)
    match = "MATCH" if delta < 0.01 else f"MISMATCH (delta=${delta:,.2f})"
    print(f"  {p}: neto=${neto:>10,.2f} (cierre=${cierre_neto:>10,.2f}) sin_clasif=${sin:>10,.2f}  {match}")

# Totals by month
print(f"\n--- Monthly Resultado Neto RIPLEY ---")
print(f"{'Month':<10} {'Neto':>12} {'Ingresos':>12} {'Devoluciones':>12} {'CostOp':>12} {'CostCom':>12} {'Ajustes':>12}")
print("-" * 70)
total_neto = 0
total_ing = 0
total_dev = 0
total_cop = 0
total_ccm = 0
total_aju = 0
for p in periods:
    r3 = closing_results[p]
    print(f"{p:<10} ${r3['neto']:>10,.0f} ${r3['ingresos']:>10,.0f} ${r3['devoluciones']:>10,.0f} ${r3['costos_op']:>10,.0f} ${r3['costos_com']:>10,.0f} ${r3['ajustes']:>10,.0f}")
    total_neto += r3['neto']
    total_ing += r3['ingresos']
    total_dev += r3['devoluciones']
    total_cop += r3['costos_op']
    total_ccm += r3['costos_com']
    total_aju += r3['ajustes']
print("-" * 70)
print(f"{'TOTAL':<10} ${total_neto:>10,.0f} ${total_ing:>10,.0f} ${total_dev:>10,.0f} ${total_cop:>10,.0f} ${total_ccm:>10,.0f} ${total_aju:>10,.0f}")

# Save results
results = {
    'classification': {
        'elapsed_sec': elapsed,
        'rows_inserted': n,
        'post_clasif_rows': post_clasif,
    },
    'closing': closing_results
}
with open('_classification_results.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\nResults saved to _classification_results.json")
db.close()
