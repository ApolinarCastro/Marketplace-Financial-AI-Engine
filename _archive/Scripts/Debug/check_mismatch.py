import pandas as pd
import duckdb
import re
from pathlib import Path

pattern = re.compile(r'refund|reembolso|devolución|devolucion|claim|chargeback|compensation|cashback', re.IGNORECASE)
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

db = duckdb.connect('database.duckdb')
df_l = db.execute('''
    SELECT c.id_transaccion, c.monto, v1.archivo_origen 
    FROM marketplace_ledger_clasificado_v1 c 
    JOIN marketplace_ledger_v1 v1 ON c.id_transaccion = v1.id_transaccion
''').df()

for _, row in df_s.head(200).iterrows():
    op_id = row['op_id']
    matches = df_l[df_l['id_transaccion'].str.contains(f'POS_{op_id}_')] if op_id and op_id != '0' else pd.DataFrame()
    if not matches.empty:
        l_amt = matches.iloc[0]['monto']
        if abs(abs(row['amount']) - abs(l_amt)) > 0.01:
            print(f"Mismatch: op_id={op_id}, src={row['amount']}, ledger={l_amt}")
