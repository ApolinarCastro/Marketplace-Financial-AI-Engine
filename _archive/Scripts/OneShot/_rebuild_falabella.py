"""REPROCESAMIENTO FALABELLA FASE 2-4"""
import sys, json, duckdb, calendar
sys.path.insert(0, '.')
from engine.v4.database import DatabaseV4
DatabaseV4.reset()  # Force fresh connection with fixed temp_directory
from engine.v4.surgical_loader import SurgicalLoader
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.database import DatabaseV4

print("FASE 2 - RESET FALABELLA")
loader = SurgicalLoader()
loader.reset_db('FALABELLA')

db = DatabaseV4.get()
for t in ['marketplace_ledger_v1', 'marketplace_ledger_clasificado_v1', 'ventas_marketplace']:
    cnt = db.query(f"SELECT COUNT(*) as n FROM {t} WHERE marketplace='FALABELLA'").iloc[0,0]
    print(f'  {t}: {cnt} rows (0 esperado)')

db.execute("DELETE FROM marketplace_cierre_financiero_v1 WHERE marketplace='FALABELLA'")
print('  cierres: deleted')

print()
print('FASE 3 - LOAD FALABELLA')
loader.load_falabella()

ledger = db.query("SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'").iloc[0,0]
ventas = db.query("SELECT COUNT(*) as n FROM ventas_marketplace WHERE marketplace='FALABELLA'").iloc[0,0]
print(f'  ledger: {ledger} rows')
print(f'  ventas: {ventas} rows')

concepts = db.query("""
    SELECT detalle, COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'
    GROUP BY detalle ORDER BY SUM(ABS(monto)) DESC
""")
print(f'  Conceptos ({len(concepts)}):')
for _, r in concepts.iterrows():
    print(f'    {str(r["detalle"]):<55s} cnt={int(r["cnt"]):>4d}  ${float(r["total"]):>+10,.0f}')

print()
print('FASE 3b - CLASSIFY + CLOSE')
engine = MarketplaceAuditorEngine()
engine.run_classification()

clasif = db.query("SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE marketplace='FALABELLA'").iloc[0,0]
no_clasif = db.query("SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE marketplace='FALABELLA' AND clasificacion_operativa='NO_CLASIFICADO'").iloc[0,0]
print(f'  Clasificados: {clasif}')
print(f'  NO_CLASIFICADO: {no_clasif}')

null_fg = db.query("SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA' AND financial_group IS NULL").iloc[0,0]
null_co = db.query("SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA' AND clasificacion_operativa IS NULL").iloc[0,0]
print(f'  ledger_v1 financial_group IS NULL: {null_fg}')
print(f'  ledger_v1 clasificacion_operativa IS NULL: {null_co}')

fg = db.query("""
    SELECT COALESCE(financial_group,'sin_clasificar') as fg,
           COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'
    GROUP BY fg ORDER BY total DESC
""")
print()
total_sum = 0
for _, r in fg.iterrows():
    total_sum += float(r['total'])
    print(f'  {str(r["fg"]):<25s} {int(r["cnt"]):>5d} rows  ${float(r["total"]):>+12,.0f}')
print(f'  {"TOTAL":<25s} {int(fg["cnt"].sum()):>5d} rows  ${total_sum:>+12,.0f}')

for year in [2025, 2026]:
    for month in range(1, 13):
        last_day = calendar.monthrange(year, month)[1]
        p_ini = f'{year}-{month:02d}-01'
        p_fin = f'{year}-{month:02d}-{last_day}'
        engine.run_financial_closing('FALABELLA', p_ini, p_fin)

cierres = db.query("""
    SELECT periodo_inicio, total_ingresos, total_costos_operacionales,
           total_costos_comerciales, total_ajustes, resultado_neto
    FROM marketplace_cierre_financiero_v1 WHERE marketplace='FALABELLA'
    ORDER BY periodo_inicio
""")
print()
for _, r in cierres.iterrows():
    ing = float(r['total_ingresos'])
    cop = float(r['total_costos_operacionales'])
    ccm = float(r['total_costos_comerciales'])
    aju = float(r['total_ajustes'])
    net = float(r['resultado_neto'])
    if ing or cop or ccm or aju or net:
        print(f'  {str(r["periodo_inicio"])[:7]:<8s} ingresos=${ing:>+12,.0f}  costos_op=${cop:>+12,.0f}  costos_com=${ccm:>+12,.0f}  ajustes=${aju:>+12,.0f}  neto=${net:>+12,.0f}')

print()
print('FASE 4 - VALIDATION')
tipos = db.query("""
    SELECT detalle, clasificacion_operativa,
           COALESCE(financial_group,'sin_clasificar') as fg,
           COUNT(*) as cnt, SUM(monto) as total
    FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'
    GROUP BY detalle, clasificacion_operativa, fg
    ORDER BY SUM(ABS(monto)) DESC
""")
print(f'  Tipos con clasificacion ({len(tipos)}):')
for _, r in tipos.iterrows():
    print(f'    {str(r["detalle"]):<55s} co={str(r["clasificacion_operativa"]):<40s} fg={str(r["fg"]):<20s} {int(r["cnt"]):>4d}  ${float(r["total"]):>+10,.0f}')

print()
print('FALABELLA REBUILD COMPLETE.')
