import sys
sys.path.insert(0, "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine")

from engine.v4.database import DatabaseV4

v8 = "data/db/baseline_estable_v8_candidate_20260717/meli_financial_v4.db"
db = DatabaseV4(db_path=v8, read_only=True)

for mp in ['ML', 'PARIS', 'RIPLEY', 'FALABELLA']:
    df = db.query(
        "SELECT LOWER(financial_group) as fg, COUNT(*) as cnt, SUM(monto) as sum_monto "
        "FROM marketplace_ledger_v1 WHERE marketplace = ? GROUP BY LOWER(financial_group)",
        [mp]
    )
    print(f'=== {mp} ===')
    print(df.to_string())
    print()

db.close()