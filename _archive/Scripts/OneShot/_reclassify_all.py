"""REPROCESAMIENTO COMPLETO: rerun classification for ALL marketplaces with fixed op_flag"""
import sys, calendar
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4
DatabaseV4.reset()  # Force fresh connection
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

print("=== RUNNING CLASSIFICATION FOR ALL MARKETPLACES ===")
engine = MarketplaceAuditorEngine()
n = engine.run_classification()
print(f'  Clasificados total: {n}')

db = DatabaseV4.get()

# Verify by marketplace
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    total = db.query(f"SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE marketplace='{mp}'").iloc[0,0]
    no_clas = db.query(f"SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE marketplace='{mp}' AND clasificacion_operativa='NO_CLASIFICADO'").iloc[0,0]
    null_fg = db.query(f"SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='{mp}' AND financial_group IS NULL").iloc[0,0]
    null_co = db.query(f"SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='{mp}' AND clasificacion_operativa IS NULL").iloc[0,0]
    print(f'  {mp}: total={total} no_clas={no_clas} null_fg={null_fg} null_co={null_co}')

# Run financial closing for all marketplaces and periods
periods = db.query("""
    SELECT DISTINCT marketplace, STRFTIME(fecha, '%Y-%m') as mes
    FROM marketplace_ledger_v1
    ORDER BY marketplace, mes
""")
print()
print('=== RUNNING FINANCIAL CLOSING ===')
for _, r in periods.iterrows():
    mp = r['marketplace']
    year, month = r['mes'].split('-')
    last_day = calendar.monthrange(int(year), int(month))[1]
    p_ini = f'{year}-{month}-01'
    p_fin = f'{year}-{month}-{last_day}'
    engine.run_financial_closing(mp, p_ini, p_fin)

print()
for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    cierres = db.query(f"""
        SELECT periodo_inicio, resultado_neto
        FROM marketplace_cierre_financiero_v1 WHERE marketplace='{mp}'
        ORDER BY periodo_inicio
    """)
    total = sum(float(r['resultado_neto']) for _, r in cierres.iterrows())
    print(f'  {mp}: {len(cierres)} cierres, total_neto=${total:>+12,.0f}')

print()
print('FULL RECLASSIFICATION COMPLETE.')
