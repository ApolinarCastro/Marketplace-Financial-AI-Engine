"""FASE 2+3: Load data for all MPs, run classification, closing, audit"""
import sys, logging
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
logging.basicConfig(level=logging.INFO)

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.surgical_loader import SurgicalLoader

print("=" * 60)
print("FASE 2: CARGANDO DATA FRESHNESS")
print("=" * 60)

# Step 1: Load all marketplaces
loader = SurgicalLoader()

for mp in ['ML', 'PARIS', 'RIPLEY', 'FALABELLA']:
    print(f"\n--- Loading {mp} ---")
    try:
        loader.load_marketplace(mp)
        db = DatabaseV4.get()
        r = db.query(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(monto),0),0) as total, MIN(fecha) as min_f, MAX(fecha) as max_f FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").iloc[0]
        print(f"  {mp}: {int(r['n'])} rows, ${float(r['total']):,.0f}, {r['min_f']} to {r['max_f']}")
    except Exception as e:
        print(f"  ERROR loading {mp}: {e}")

print("\n" + "=" * 60)
print("FASE 3: CLASIFICACIÓN, CIERRE, AUDITORÍA")
print("=" * 60)

# Step 2: Run classification
try:
    engine = MarketplaceAuditorEngine()
    n = engine.run_classification()
    print(f"\nClassification: {n} rows classified")
except Exception as e:
    print(f"ERROR in classification: {e}")

# Step 3: Financial closing for all periods
try:
    db = DatabaseV4.get()
    # Detect all periods for all MPs
    months = db.query("""
        SELECT DISTINCT marketplace, STRFTIME(fecha, '%Y-%m') as periodo
        FROM marketplace_ledger_v1
        WHERE fecha IS NOT NULL
        ORDER BY marketplace, periodo
    """)
    print(f"\nFinancial closing for {len(months)} period-MP combinations...")
    import calendar
    closed = 0
    for _, r in months.iterrows():
        mp = r['marketplace']
        year, month = r['periodo'].split('-')
        last_day = calendar.monthrange(int(year), int(month))[1]
        p_ini = f'{year}-{month}-01'
        p_fin = f'{year}-{month}-{last_day}'
        try:
            engine.run_financial_closing(mp, p_ini, p_fin)
            closed += 1
        except Exception as e:
            print(f"  ERROR closing {mp} {p_ini}: {e}")
    print(f"  Closed: {closed} periods")
except Exception as e:
    print(f"ERROR in closing: {e}")

# Step 4: Run audit
try:
    n = engine.run_audit()
    print(f"\nAudit: {n} alerts generated")
except Exception as e:
    print(f"ERROR in audit: {e}")

print("\n" + "=" * 60)
print("VERIFICATION")
print("=" * 60)

db = DatabaseV4.get()
for mp in ['ML', 'PARIS', 'RIPLEY', 'FALABELLA']:
    lr = db.query(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(monto),0),0) as total, MIN(fecha) as min_f, MAX(fecha) as max_f FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").iloc[0]
    cr = db.query(f"SELECT COUNT(*) as n, COALESCE(ROUND(SUM(resultado_neto),0),0) as total FROM marketplace_cierre_financiero_v1 WHERE marketplace='{mp}'").iloc[0]
    ar = db.query(f"SELECT COUNT(*) as n FROM marketplace_auditoria_v1 WHERE marketplace='{mp}'").iloc[0]
    print(f'{mp}: ledger={int(lr["n"])} rows ${float(lr["total"]):>12,.0f} | cierre={int(cr["n"])} periods ${float(cr["total"]):>12,.0f} | audit={int(ar["n"])} rows')

print("\nDONE.")
