import sys, json
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine, NORMALIZED_CLASSIFICATION_MAP, FINANCIAL_STRUCTURE, normalize_detail

with open('master_marketplace_dictionary_v1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('=== DICTIONARY INTEGRATION CHECK ===')
missing = []
for entry in d['dictionary']:
    for alias in entry['aliases']:
        norm = normalize_detail(alias)
        if norm not in NORMALIZED_CLASSIFICATION_MAP:
            missing.append((entry['marketplace'], alias, alias))

if missing:
    print(f'MISSING ({len(missing)}):')
    for mp, a, _ in missing:
        print(f'  [{mp}] {a}')
else:
    print(f'All dictionary entries mapped OK')

# Verify classifications present
for group in ['ingresos', 'devoluciones', 'costos_operacionales', 'costos_comerciales', 'ajustes']:
    print(f'  {group}: {len(FINANCIAL_STRUCTURE[group])} entries')

print('\n=== RUNNING CLASSIFICATION ===')
db = MarketplaceAuditorEngine().db
engine = MarketplaceAuditorEngine()
n = engine.run_classification()
print(f'Classified {n} rows')

clasifs = db.query('SELECT clasificacion_operativa, COUNT(*) as cnt FROM marketplace_ledger_clasificado_v1 GROUP BY clasificacion_operativa ORDER BY cnt DESC')
print(f'\nBreakdown ({len(clasifs)} types):')
for _, r in clasifs.iterrows():
    print(f'  {r["clasificacion_operativa"]}: {r["cnt"]}')

noclas = db.query("SELECT COUNT(*) as c FROM marketplace_ledger_clasificado_v1 WHERE clasificacion_operativa = 'NO_CLASIFICADO'").iloc[0]['c']
print(f'\nNO_CLASIFICADO: {noclas}')
