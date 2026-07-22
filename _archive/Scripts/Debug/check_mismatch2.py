import sys
sys.path.append('.')
from engine.v4.database import DatabaseV4
import pandas as pd
import re
from pathlib import Path

db = DatabaseV4(read_only=True)
df_l = db.query("SELECT c.id_transaccion, c.monto, v1.archivo_origen FROM marketplace_ledger_clasificado_v1 c JOIN marketplace_ledger_v1 v1 ON c.id_transaccion = v1.id_transaccion WHERE c.marketplace = 'ML'")

print('Ledger shape:', df_l.shape)

pattern = re.compile(r'refund|reembolso|devoluciÃ³n|devolucion|claim|chargeback|compensation|cashback', re.IGNORECASE)
source_records = []
poscobro_dir = Path('01_Raw/ML/Poscobro')
files = list(poscobro_dir.glob('*.xlsx'))

for f in files:
    df = pd.read_excel(f, engine='calamine')
    cols_map = {c: str(c).lower().replace(' ', '_').replace('.', '') for c in df.columns}
    df = df.rename(columns=cols_map)
    for idx, row in df.iterrows():
        flow = str(row.get('flow', ''))
        reason_id = str(row.get('reason_id', ''))
        reason_detail = str(row.get('reason_detail', ''))
        operation_type = str(row.get('operation_type', ''))
        text_to_search = f'{flow} {reason_id} {reason_detail} {operation_type}'.lower()
        if pattern.search(text_to_search):
            op_id = str(row.get('operation_id', '')).strip()
            if op_id == 'nan' or op_id == 'None': op_id = ''
            amt = float(row['amount']) if 'amount' in row and pd.notna(row['amount']) else float(row.get('operation_amount', 0.0))
            source_records.append({'op_id': op_id, 'file': f.name, 'idx': idx, 'amount': amt})

df_s = pd.DataFrame(source_records)
print('Source shape (Poscobro):', df_s.shape)
print('Source total amount (Poscobro):', df_s['amount'].sum())

# Also load Facturacion
facturacion_dir = Path('01_Raw/ML/Facturacion')
files_fact = list(facturacion_dir.glob('*.xlsx'))
fact_records = []
for f in files_fact:
    df = pd.read_excel(f, engine='calamine')
    cols_map = {}
    for c in df.columns:
        cl = str(c).lower()
        if 'detalle' in cl: cols_map[c] = 'detalle'
        elif 'valor del cargo' in cl: cols_map[c] = 'valor_del_cargo'
        elif 'venta' in cl and 'n' in cl: cols_map[c] = 'order_id'
        elif 'pago' in cl: cols_map[c] = 'op_id'
    df = df.rename(columns=cols_map)
    for idx, row in df.iterrows():
        detalle = str(row.get('detalle', '')).lower()
        if pattern.search(detalle) or 'anulacion' in detalle or 'anulaciÃ³n' in detalle:
            op_id = str(row.get('op_id', '')).strip()
            if op_id == 'nan' or op_id == 'None': op_id = ''
            amt = float(row['valor_del_cargo']) if 'valor_del_cargo' in row and pd.notna(row.get('valor_del_cargo')) else 0.0
            fact_records.append({'op_id': op_id, 'file': f.name, 'idx': idx, 'amount': amt})

df_f = pd.DataFrame(fact_records)
print('Source shape (Facturacion):', df_f.shape)
print('Source total amount (Facturacion):', df_f['amount'].sum())

# Check how many ledger match poscobro
total_ledger_amount = 0
for _, row in df_s.iterrows():
    op_id = row['op_id']
    matches = df_l[df_l['id_transaccion'].str.contains(f'POS_{op_id}_')] if op_id and op_id != '0' else pd.DataFrame()
    if not matches.empty:
        total_ledger_amount += matches.iloc[0]['monto']

print('Total matched ledger amount for Poscobro:', total_ledger_amount)

# Check Facturacion
total_ledger_amount_fact = 0
for _, row in df_f.iterrows():
    op_id = row['op_id']
    matches = df_l[df_l['id_transaccion'].str.contains(f'POS_{op_id}_')] if op_id and op_id != '0' else pd.DataFrame()
    if not matches.empty:
        total_ledger_amount_fact += matches.iloc[0]['monto']

print('Total matched ledger amount for Facturacion:', total_ledger_amount_fact)

