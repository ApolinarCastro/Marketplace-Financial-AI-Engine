import pandas as pd, os, traceback

base = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\FALABELLA\Transacciones'
f = os.path.join(base, 'InvoiceReport_FACL-778981009-2026-03-21-2026-04-20_2026-05-11T21_38_35.158622344.xlsx')

df = pd.read_excel(f, engine='calamine', header=0)
df.columns = [str(c).strip().replace('\xa0', ' ') for c in df.columns]

print(f"Shape: {df.shape}")
print(f"Dtypes:")
for c in df.columns:
    print(f"  {c}: {df[c].dtype}")

print(f"\nRow 0 values:")
for c in df.columns:
    print(f"  {c}: {repr(df.iloc[0][c])} (type: {type(df.iloc[0][c]).__name__})")

# Now try row iteration
print(f"\nTrying iterrows on first 3 rows:")
for idx, row in df.head(3).iterrows():
    print(f"\n  Row {idx}: type(row)={type(row).__name__}")
    try:
        order_val = row['N de orden']
        print(f"    N de orden: {repr(order_val)} (type={type(order_val).__name__})")
        order_id = str(order_val).strip()
        print(f"    order_id: {order_id}")
        
        tipo_val = row['Tipo de Transaccion']
        print(f"    Tipo de Transaccion: {repr(tipo_val)}")
        
        monto_val = row['Monto con IVA']
        print(f"    Monto con IVA: {repr(monto_val)} (type={type(monto_val).__name__})")
        
        fecha_val = row['Fecha de Transaccion']
        print(f"    Fecha de Transaccion: {repr(fecha_val)} (type={type(fecha_val).__name__})")
        
        fal_id = row['Falabella-Id']
        print(f"    Falabella-Id: {repr(fal_id)} (type={type(fal_id).__name__})")
        
        folio = row['Numero de documento']
        print(f"    Numero de documento: {repr(folio)} (type={type(folio).__name__})")
    except Exception as e:
        print(f"    ERROR: {e}")
        traceback.print_exc()
