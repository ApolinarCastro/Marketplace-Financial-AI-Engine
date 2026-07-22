import pandas as pd
import duckdb
from pathlib import Path
import re
import unicodedata

def normalize(text):
    if not isinstance(text, str): return ""
    t = unicodedata.normalize('NFD', text.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', t)

def get_col_name(df, possible_names):
    cols_norm = [normalize(str(c)) for c in df.columns]
    for p in possible_names:
        pn = normalize(p)
        for i, cn in enumerate(cols_norm):
            if pn in cn: return df.columns[i]
    return None

db = duckdb.connect("data/db/meli_financial_v4.db")
df_ledger = db.execute("""
    SELECT c.id_transaccion, c.clasificacion_operativa, c.include_in_operational_pnl, c.monto, c.detalle, v1.archivo_origen 
    FROM marketplace_ledger_clasificado_v1 c 
    JOIN marketplace_ledger_v1 v1 ON c.id_transaccion = v1.id_transaccion 
    WHERE c.marketplace = 'ML' AND c.id_transaccion LIKE 'POS_%'
""").df()

poscobro_dir = Path("01_Raw/ML/Poscobro")

source_records = []

for f in poscobro_dir.glob("*.xlsx"):
    try:
        df = pd.read_excel(f, engine='calamine')
        c_ord = get_col_name(df, ['orderid', 'orden', 'transaccion'])
        c_op = get_col_name(df, ['operationid', 'operacionid'])
        c_amt = get_col_name(df, ['operation_amount', 'amount', 'monto'])
        c_dev = get_col_name(df, ['montodevolucion', 'devolucion'])
        c_det = get_col_name(df, ['reasondetail', 'motivo', 'detalle'])
        c_stat = get_col_name(df, ['statusdetail'])
        c_flow = get_col_name(df, ['flow'])
        c_reason_id = get_col_name(df, ['reason_id'])
        c_op_type = get_col_name(df, ['operation_type'])

        if not c_ord: continue

        for idx, row in df.iterrows():
            monto_raw = float(pd.to_numeric(row[c_amt], errors='coerce') or 0) if c_amt else 0
            monto_dev = float(pd.to_numeric(row[c_dev], errors='coerce') or 0) if c_dev else 0
            val = monto_dev * -1 if monto_dev != 0 else monto_raw
            
            op_id = str(row[c_op]).strip() if c_op and pd.notna(row[c_op]) else ""
            
            # id calculation logic
            if op_id and op_id.lower() not in ['', '0', '0.0', 'nan', 'none']:
                trans_id = f"POS_{op_id}_{f.name}_{idx}"
                _op_id = op_id
            else:
                trans_id = f"POS_{f.name}_{idx}"
                _op_id = trans_id
                
            flow = str(row[c_flow]) if c_flow else ''
            reason_id = str(row[c_reason_id]) if c_reason_id else ''
            det = str(row[c_det]) if c_det else ''
            op_type = str(row[c_op_type]) if c_op_type else ''
            
            source_records.append({
                'Archivo': f.name,
                '_op_id': _op_id,
                'ID Transaccion': trans_id,
                'flow': flow,
                'reason_id': reason_id,
                'reason_detail': det,
                'operation_type': op_type,
                'Monto': val
            })
    except Exception as e:
        print(f"Error {f.name}: {e}")

df_source = pd.DataFrame(source_records)

# Dedup similar to surgical loader
df_source = df_source.drop_duplicates(subset=['_op_id', 'reason_detail', 'Monto'])

# Join using partial matching logic if needed, or _op_id
# For speed, let's map df_ledger _op_id
df_ledger['_op_id'] = df_ledger['id_transaccion'].str.extract(r'POS_(\d+)_', expand=False)
df_ledger['_op_id'] = df_ledger['_op_id'].fillna(df_ledger['id_transaccion'])

# Merge source and ledger on _op_id
df_merged = pd.merge(df_source, df_ledger, on='_op_id', how='left', suffixes=('_src', '_ldg'))

# Group for analysis
grouped = df_merged.groupby(['flow', 'reason_id', 'reason_detail', 'operation_type', 'clasificacion_operativa', 'include_in_operational_pnl']).agg(
        Qtd=('Monto', 'count'),
        Total_Amount=('Monto', 'sum')
).reset_index()

grouped = grouped.sort_values(by='Total_Amount', ascending=True)

md = [
    "# AUDITORÃ A COMPLETA DE POSCOBROS (CLAIM / CHARGEBACK)",
    "",
    "Esta auditorÃ­a cruza los campos crudos del archivo de Poscobros (`flow`, `reason_id`, `reason_detail`, `operation_type`) contra la clasificaciÃ³n final en la base de datos `marketplace_ledger_clasificado_v1`.",
    "",
    "## 1. Mapeo General de Eventos Operativos vs ClasificaciÃ³n",
    "",
    "```",
    grouped.to_string(index=False),
    "```",
    "",
    "## 2. Foco EspecÃ­fico: Claims y Chargebacks",
    ""
]

claims_chargebacks = grouped[grouped['flow'].str.lower().str.contains('claim|chargeback', na=False) | 
                             grouped['reason_detail'].str.lower().str.contains('claim|chargeback', na=False) |
                             grouped['operation_type'].str.lower().str.contains('claim|chargeback', na=False) |
                             grouped['reason_id'].str.lower().str.contains('claim|chargeback', na=False)]

md.append("```")
if claims_chargebacks.empty:
    md.append("No se encontraron registros de claims o chargebacks.")
else:
    md.append(claims_chargebacks.to_string(index=False))
md.append("```")

with open('POSCOBRO_CLASSIFICATION_AUDIT.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))

print("Audit complete.")
