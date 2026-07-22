import pandas as pd
import duckdb
from pathlib import Path
import re
import math
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
    SELECT c.id_transaccion, c.monto, c.clasificacion_operativa, c.detalle, v1.archivo_origen 
    FROM marketplace_ledger_clasificado_v1 c 
    JOIN marketplace_ledger_v1 v1 ON c.id_transaccion = v1.id_transaccion 
    WHERE c.marketplace = 'ML'
""").df()

poscobro_dir = Path("01_Raw/ML/Poscobro")
facturacion_dir = Path("01_Raw/ML/Facturacion")

keywords = ['refund', 'reembolso', 'devoluciÃ³n', 'devolucion', 'claim', 'chargeback', 'compensation', 'cashback']
pattern = re.compile('|'.join(keywords), re.IGNORECASE)

source_records = []

# 1. Poscobro
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
            flow = str(row[c_flow]) if c_flow else ''
            reason_id = str(row[c_reason_id]) if c_reason_id else ''
            det = str(row[c_det]) if c_det else ''
            op_type = str(row[c_op_type]) if c_op_type else ''
            stat = str(row[c_stat]) if c_stat else ''
            
            text_to_search = f"{flow} {reason_id} {det} {op_type}".lower()
            if pattern.search(text_to_search):
                monto_raw = float(pd.to_numeric(row[c_amt], errors='coerce') or 0) if c_amt else 0
                monto_dev = float(pd.to_numeric(row[c_dev], errors='coerce') or 0) if c_dev else 0
                val = monto_dev * -1 if monto_dev != 0 else monto_raw
                
                op_id = str(row[c_op]).strip() if c_op and pd.notna(row[c_op]) else ""
                
                final_det = det.strip() if pd.notna(det) and det.strip() != '' and det.strip().lower() != 'nan' else stat.strip() if pd.notna(stat) and stat.strip() != '' and stat.strip().lower() != 'nan' else 'Ajuste Poscobro'

                source_records.append({
                    'Archivo Fuente': f.name,
                    'ID Original': op_id,
                    'Monto Original': val,
                    'Detalle': final_det,
                    '_idx': idx,
                    'Tipo': 'Poscobro',
                    'flow': flow, 'reason_id': reason_id, 'reason_detail': det, 'operation_type': op_type, 'operation_status': stat
                })
    except Exception as e:
        print(f"Error {f.name}: {e}")

# 2. Facturacion
for f in facturacion_dir.glob("*.xlsx"):
    try:
        df = pd.read_excel(f, engine='calamine')
        c_ord = get_col_name(df, ['numerodeventa', 'orderid', 'venta'])
        c_detalle = get_col_name(df, ['detalle', 'description'])
        c_val_cargo = get_col_name(df, ['valordelcargo', 'monto'])
        c_tot_venta = get_col_name(df, ['totaldelaventa', 'valordelacompra'])

        if not c_ord or not c_detalle: continue

        for idx, row in df.iterrows():
            det = str(row[c_detalle])
            text_to_search = det.lower()
            if pattern.search(text_to_search) or 'anulacion' in text_to_search or 'anulaciÃ³n' in text_to_search:
                order_id = str(row[c_ord])
                if normalize(det) == normalize('DevoluciÃ³n de venta'):
                    tot_venta = float(pd.to_numeric(row[c_tot_venta], errors='coerce') or 0.0)
                    val = -tot_venta
                    source_records.append({
                        'Archivo Fuente': f.name, 'ID Original': f"REFUND_{order_id}", 'Monto Original': val,
                        'Detalle': 'DevoluciÃ³n de venta', '_idx': idx, 'Tipo': 'Facturacion',
                        'flow': '', 'reason_id': '', 'reason_detail': det, 'operation_type': '', 'operation_status': ''
                    })
                elif 'anulacion del cargo' in normalize(det) or 'anulaciÃ³n del cargo' in text_to_search:
                    val_cargo = float(pd.to_numeric(row[c_val_cargo], errors='coerce') or 0.0)
                    val = -val_cargo
                    source_records.append({
                        'Archivo Fuente': f.name, 'ID Original': f"REVCOMM_{order_id}", 'Monto Original': val,
                        'Detalle': 'AnulaciÃ³n del cargo por venta', '_idx': idx, 'Tipo': 'Facturacion',
                        'flow': '', 'reason_id': '', 'reason_detail': det, 'operation_type': '', 'operation_status': ''
                    })
                else:
                    val_cargo = float(pd.to_numeric(row[c_val_cargo], errors='coerce') or 0.0)
                    val = -val_cargo
                    source_records.append({
                        'Archivo Fuente': f.name, 'ID Original': f"CHG_{f.name}_{idx}", 'Monto Original': val,
                        'Detalle': det, '_idx': idx, 'Tipo': 'Facturacion',
                        'flow': '', 'reason_id': '', 'reason_detail': det, 'operation_type': '', 'operation_status': ''
                    })
    except Exception as e:
        print(f"Error {f.name}: {e}")

df_source = pd.DataFrame(source_records)

# FASE 1
fase1_grouped = df_source.groupby(['flow', 'reason_id', 'reason_detail', 'operation_type', 'operation_status']).agg(
    count=('Monto Original', 'size'),
    total_amount=('Monto Original', 'sum')
).reset_index()

# Dedup source explicitly as in surgical_loader
df_source_dedup = df_source.copy()
df_source_dedup['_op_id'] = df_source_dedup['ID Original']
df_source_dedup = df_source_dedup.drop_duplicates(subset=['_op_id', 'Detalle', 'Monto Original'])

total_source = df_source_dedup['Monto Original'].sum()
trace_results = []
huerfanos = 0
duplicados = len(df_source) - len(df_source_dedup)
sin_clasificar = 0
total_ledger = 0.0

for _, row in df_source_dedup.iterrows():
    op_id = row['ID Original']
    f_name = row['Archivo Fuente']
    idx = row['_idx']
    
    if row['Tipo'] == 'Poscobro':
        if op_id and op_id not in ['0', '0.0', 'nan', 'none']:
            matches = df_ledger[df_ledger['id_transaccion'].str.contains(f"POS_{op_id}_")]
        else:
            matches = df_ledger[df_ledger['id_transaccion'] == f"POS_{f_name}_{idx}"]
    else:
        # Facturacion ids
        if "REFUND_" in op_id:
            matches = df_ledger[df_ledger['id_transaccion'].str.startswith(op_id)]
        elif "REVCOMM_" in op_id:
            matches = df_ledger[df_ledger['id_transaccion'].str.startswith(op_id)]
        else:
            matches = df_ledger[df_ledger['id_transaccion'] == op_id]

    estado = "MATCH"
    clasif = ""
    lid = ""
    lamt = 0.0

    if matches.empty:
        estado = "HUÃ‰RFANO"
        huerfanos += 1
    else:
        m = matches.iloc[0]
        lid = m['id_transaccion']
        clasif = m['clasificacion_operativa']
        lamt = m['monto']
        if pd.isna(clasif) or clasif == '':
            estado = "SIN CLASIFICAR"
            sin_clasificar += 1
        else:
            estado = "CLASIFICADO"
            total_ledger += lamt

    trace_results.append({
        'Archivo Fuente': f_name,
        'ID Original': op_id,
        'Monto Original': row['Monto Original'],
        'ClasificaciÃ³n Actual': clasif,
        'Ledger ID': lid,
        'Estado': estado
    })

df_trace = pd.DataFrame(trace_results)
df_trace_display = df_trace.head(50)

delta = abs(total_source) - abs(total_ledger)

md = [
    "# DIRECTIVA DE AUDITORÃ A DE TRAZABILIDAD DE DEVOLUCIONES",
    "",
    "## FASE 1: ExtracciÃ³n desde Archivos Fuente",
    "",
    "### AgrupaciÃ³n por Motivo y Flujo",
    "```",
    fase1_grouped.to_string(index=False),
    "```",
    "",
    "## FASE 2: Trazabilidad Archivo Fuente -> Ledger (Muestra)",
    "",
    "```",
    df_trace_display.to_string(index=False),
    "```",
    "",
    "## FASE 3: IdentificaciÃ³n de Registros",
    "",
    f"- **Registros Clasificados**: {len(df_trace[df_trace['Estado'] == 'CLASIFICADO'])}",
    f"- **Registros Excluidos/Duplicados (Deduplicados en carga)**: {duplicados}",
    f"- **Registros HuÃ©rfanos**: {huerfanos}",
    f"- **Registros Sin ClasificaciÃ³n**: {sin_clasificar}",
    "",
    "## FASE 4: Resultados y Delta",
    "",
    f"- **Total Devoluciones Fuente (Suma absoluta)**: ${abs(total_source):,.2f}",
    f"- **Total Devoluciones Ledger (Suma absoluta)**: ${abs(total_ledger):,.2f}",
    f"- **Delta**: ${delta:,.2f}",
    "",
    "## CONCLUSIÃ“N DE AUDITORÃ A",
    "Delta = 0" if math.isclose(delta, 0, abs_tol=1) else f"Discrepancia detectada: ${delta:,.2f}"
]

with open('REFUND_TRACEABILITY_AUDIT.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md))

print("Done. Delta:", delta)
