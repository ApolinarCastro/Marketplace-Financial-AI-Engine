"""Final comprehensive validation"""
from engine.v4.database import DatabaseV4
import json
info = {}

db = DatabaseV4.get()

for mp in ['ML', 'RIPLEY', 'PARIS', 'FALABELLA']:
    total = int(db.query(f"SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").iloc[0]['n'])
    sum_monto = float(db.query(f"SELECT COALESCE(SUM(monto),0) as t FROM marketplace_ledger_v1 WHERE marketplace='{mp}'").iloc[0]['t'])
    null_fg = int(db.query(f"SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='{mp}' AND financial_group IS NULL").iloc[0]['n'])
    null_co = int(db.query(f"SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE marketplace='{mp}' AND clasificacion_operativa IS NULL").iloc[0]['n'])
    no_clas = int(db.query(f"SELECT COUNT(*) as n FROM marketplace_ledger_clasificado_v1 WHERE marketplace='{mp}' AND clasificacion_operativa='NO_CLASIFICADO'").iloc[0]['n'])
    fg_dist = db.query(f"SELECT COALESCE(financial_group,'NULL') as fg, COUNT(*) as cnt, SUM(monto) as t FROM marketplace_ledger_v1 WHERE marketplace='{mp}' GROUP BY fg ORDER BY t DESC")
    
    info[mp] = {
        'total_rows': total,
        'sum_monto': sum_monto,
        'null_financial_group': null_fg,
        'null_clasificacion_operativa': null_co,
        'no_clasificado': no_clas,
        'financial_groups': {str(r['fg']): {'rows': int(r['cnt']), 'total': float(r['t'])} for _, r in fg_dist.iterrows()}
    }

total_all = sum(v['total_rows'] for v in info.values())
sum_all = sum(v['sum_monto'] for v in info.values())
print(json.dumps({'total_rows_all': total_all, 'sum_monto_all': sum_all, 'marketplaces': info}, indent=2, ensure_ascii=False))
