import sys
sys.path.append('.')
from engine.v4.database import DatabaseV4
import pandas as pd

db = DatabaseV4(read_only=True)

def run_q(query, title):
    print(f'\n=== {title} ===')
    try:
        df = db.query(query)
        print(df.to_markdown())
    except Exception as e:
        print(f'Error: {e}')

run_q("SELECT COUNT(*) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY'", 'Total Ripley Clasificado')
run_q("SELECT COUNT(*) as has_fin FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' AND financial_group IS NOT NULL", 'Ripley Financial Group IS NOT NULL')
run_q("SELECT COUNT(*) as no_fin FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' AND financial_group IS NULL", 'Ripley Financial Group IS NULL')
run_q("SELECT financial_group, SUM(monto) as total_monto FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' GROUP BY financial_group", 'Ripley SUM amount by financial_group')

# For Falabella
run_q("SELECT COUNT(*) as total FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA'", 'Total Falabella Ledger V1')
run_q("SELECT COUNT(*) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace='FALABELLA'", 'Total Falabella Clasificado')
