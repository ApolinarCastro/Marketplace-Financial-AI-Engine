import sys, time, json, os, warnings
warnings.filterwarnings('ignore')
os.chdir(r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
sys.path.insert(0, '.')
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

engine = MarketplaceAuditorEngine()

import tempfile
tmp_dir = tempfile.gettempdir().replace('\\', '/')
engine.db.execute(f"SET temp_directory='{tmp_dir}';")

# Pre-state
pre_ripley = engine.db.query("SELECT COUNT(*) as cnt, COALESCE(SUM(monto),0) as tot FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY'").iloc[0]
pre_null = engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND financial_group IS NULL").iloc[0]['cnt']
print(f'PRE: RIPLEY rows={pre_ripley["cnt"]}, total=${pre_ripley["tot"]:,.2f}, NULL fg={pre_null}')
pre_clasif_total = engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_clasificado_v1").iloc[0]['cnt']
print(f'PRE: clasificado empty after DROP={pre_clasif_total}')

t0 = time.time()
n = engine.run_classification()
t1 = time.time()
print(f'Classified: {n} rows in {t1-t0:.1f}s')

post_null = engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' AND financial_group IS NULL").iloc[0]['cnt']
clasif_rows = engine.db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_clasificado_v1").iloc[0]['cnt']
ripley_clasif = engine.db.query("SELECT COUNT(*) as cnt, COALESCE(SUM(monto),0) as tot FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY'").iloc[0]

print(f'POST: RIPLEY fg NULL={post_null}, total clasificado rows={clasif_rows}')
print(f'RIPLEY clasificado: rows={ripley_clasif["cnt"]}, ${ripley_clasif["tot"]:,.2f}')

rows = engine.db.query("""
    SELECT l.marketplace, COUNT(*) as tot_rows,
        COUNT(CASE WHEN l.financial_group IS NOT NULL THEN 1 END) as fg_rows
    FROM marketplace_ledger_v1 l GROUP BY l.marketplace ORDER BY l.marketplace
""")
for row in rows.to_dict('records'):
    print(f'  {row["marketplace"]:12s}: {row["fg_rows"]}/{row["tot_rows"]} financial_group populated')

print(f'\nFASE 1: {"PASS" if post_null == 0 else "FAIL"}')
