import pandas as pd, os, traceback, sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

base = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\FALABELLA\Transacciones'
f = os.path.join(base, 'InvoiceReport_FACL-778981009-2026-03-21-2026-04-20_2026-05-11T21_38_35.158622344.xlsx')

df = pd.read_excel(f, engine='calamine', header=0)
df.columns = [str(c).strip().replace('\xa0', ' ').replace('\u00a0', ' ') for c in df.columns]

col_map = {}
for c in df.columns:
    cl = c.lower().strip()
    if cl == 'n de orden': col_map['order'] = c
    elif cl == 'falabella-id': col_map['id'] = c
    elif cl == 'tipo de transaccion': col_map['tipo'] = c
    elif cl == 'monto con iva': col_map['monto'] = c
    elif cl == 'fecha de transaccion': col_map['fecha'] = c
    elif cl == 'numero de documento': col_map['folio'] = c
    elif cl == 'tipo de documento': col_map['doc_type'] = c

print(f"col_map: {col_map}")
print(f"Test row[col_map['order']] = {df.iloc[0][col_map['order']]}")
print(f"Test row[col_map['fecha']] = {df.iloc[0][col_map['fecha']]}")
print(f"Test row[col_map['tipo']] = {df.iloc[0][col_map['tipo']]}")
print(f"Test row[col_map['monto']] = {df.iloc[0][col_map['monto']]}")
print(f"Test row[col_map['id']] = {df.iloc[0][col_map['id']]}")

# Now test with iterrows
for idx, row in df.head(3).iterrows():
    print(f"\n--- Row {idx} ---")
    try:
        raw_order = row[col_map['order']]
        print(f"1. raw_order: {raw_order} (type={type(raw_order).__name__})")
        
        if pd.isna(raw_order) or str(raw_order).strip() == '':
            print("   SKIP: empty order")
            continue
        
        order_id = str(raw_order).strip()
        print(f"2. order_id: {order_id}")
        
        fecha = pd.to_datetime(row[col_map['fecha']], errors='coerce') if 'fecha' in col_map and pd.notna(row[col_map['fecha']]) else None
        print(f"3. fecha: {fecha}")
        
        detail = str(row[col_map['tipo']]).strip()
        print(f"4. detail: {detail}")
        
        raw_monto = row[col_map['monto']]
        print(f"5. raw_monto: {raw_monto} (type={type(raw_monto).__name__})")
        
        monto_val = float(pd.to_numeric(raw_monto, errors='coerce') or 0.0)
        print(f"6. monto_val: {monto_val}")
        
        if monto_val == 0.0:
            print("   SKIP: zero monto")
            continue
            
        tipo_mov = 'PAGO' if monto_val > 0 else 'CARGO'
        
        folio = None
        if 'folio' in col_map and pd.notna(row[col_map['folio']]):
            fv = row[col_map['folio']]
            print(f"7. folio raw: {fv} (type={type(fv).__name__})")
            if str(fv).strip().lower() not in ('nan', 'none', ''):
                folio = str(int(float(fv)))
        
        trans_id = str(row[col_map['id']]) if 'id' in col_map and pd.notna(row[col_map['id']]) and str(row[col_map['id']]).strip().lower() not in ('nan', 'none', '') else f"FAL_{os.path.basename(f)}_{idx}"
        print(f"8. trans_id: {trans_id}")
        
        # Build dict
        ledger_row = {
            'marketplace': 'FALABELLA', 'id_transaccion': trans_id,
            'id_orden': order_id, 'fecha': fecha.date() if pd.notna(fecha) else None,
            'detalle': detail, 'monto': monto_val,
            'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
            'folio_xml': folio
        }
        print(f"9. SUCCESS: {ledger_row}")
    except Exception as e:
        print(f"  ERROR at step?: {e}")
        traceback.print_exc()
