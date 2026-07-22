import pandas as pd, glob, os, sys, logging
from datetime import datetime
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

logging.basicConfig(level=logging.INFO)

SYNC_COLUMNS_TO_LEDGER = [
    ('Numero de documento', 'folio_xml'),
    ('Tipo de documento', None),  # used for tipo_mov detection
    ('Fecha de Transaccion', 'fecha'),
    ('Descripcion Factura', None),  # DTE description
    ('Tipo de Transaccion', 'detalle'),
    ('Nombre del producto', None),
    ('SKU vendedor', 'sku'),
    ('SKU Falabella', None),
    ('Monto (Sin IVA)', None),
    ('IVA', None),
    ('Monto con IVA', 'monto'),
    ('Divisa', None),
    ('N estado de cuenta', None),
    ('N de orden', 'id_orden'),
    ('Referencia de pago Fpay', None),
    ('Falabella-Id', 'id_transaccion'),
    ('Estado de la orden', None),
    ('Modalidad logistica', None),
    ('Tipo de envio', None),
    ('Detalles de transaccion', None),
    ('Seller ID', None),
    ('Tipo de Seller', None),
]

LEDGER_COLS = ['marketplace', 'id_transaccion', 'id_orden', 'fecha', 'detalle', 'monto', 'tipo_movimiento', 'archivo_origen', 'folio_xml']
VENTAS_COLS = ['order_id', 'sku', 'quantity', 'unit_price', 'gross_amount', 'sale_date', 'marketplace', 'source_file']

def normalize(text):
    if not isinstance(text, str): return ""
    import unicodedata, re
    t = unicodedata.normalize('NFD', text.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', t)

def get_col_name(df, possible_names):
    cols_norm = [normalize(str(c)) for c in df.columns]
    for p in possible_names:
        pn = normalize(p)
        for i, cn in enumerate(cols_norm):
            if pn in cn:
                return df.columns[i]
    return None

base = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\FALABELLA\Transacciones'
files = sorted(glob.glob(os.path.join(base, '*.xlsx')))

db = DatabaseV4.get()
db.execute("DELETE FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'")
db.execute("DELETE FROM ventas_marketplace WHERE marketplace = 'FALABELLA'")

total_ledger = 0

for f in files:
    print(f"\n{'='*80}")
    print(f"Processing: {os.path.basename(f)}")
    
    df = pd.read_excel(f, engine='calamine', header=0)
    print(f"  Shape: {df.shape}")
    
    # Column detection
    c_id = get_col_name(df, ['Falabella-Id', 'Falabella Id', 'FalabellaId'])
    c_ord = get_col_name(df, ['N de orden', 'N de orden', 'Nro de orden', '# de orden', 'orden'])
    c_fecha = get_col_name(df, ['Fecha de Transaccion', 'Fecha de transacción', 'Fecha Transaccion'])
    c_tipo = get_col_name(df, ['Tipo de Transaccion', 'Tipo de transaccion', 'Tipotransaccion', 'Transaccion'])
    c_monto = get_col_name(df, ['Monto con IVA', 'Monto Con IVA', 'montoconiva'])
    c_sku = get_col_name(df, ['SKU vendedor', 'sku vendedor', 'skuvendedor', 'sku'])
    c_folio = get_col_name(df, ['Numero de documento', 'numero de documento', 'n document', 'ndocumento'])
    
    print(f"  Detected columns:")
    print(f"    id: {c_id}")
    print(f"    order: {c_ord}")
    print(f"    fecha: {c_fecha}")
    print(f"    tipo: {c_tipo}")
    print(f"    monto: {c_monto}")
    print(f"    sku: {c_sku}")
    print(f"    folio: {c_folio}")
    
    if not c_ord or not c_monto or not c_tipo:
        print(f"  SKIP: missing critical columns")
        continue
    
    # Try to find sales (but these XLSX likely don't have them - just fees)
    if c_tipo:
        sales_mask = df[c_tipo].astype(str).str.lower().str.contains('precio del producto', na=False)
        print(f"  Sales rows (precio del producto): {sales_mask.sum()}")
    
    # Build ledger rows
    ledger_rows = []
    for idx, row in df.iterrows():
        try:
            trans_id = str(row[c_id]) if c_id and pd.notna(row[c_id]) and str(row[c_id]).lower() != 'nan' else f"FAL_{os.path.basename(f)}_{idx}"
            order_id = str(int(row[c_ord])) if c_ord and pd.notna(row[c_ord]) and str(row[c_ord]).lower() != 'nan' else None
            if not order_id or order_id == 'nan':
                continue
            
            try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha and pd.notna(row[c_fecha]) else None
            except: fecha = None
            
            detail = str(row[c_tipo]).strip() if c_tipo and pd.notna(row[c_tipo]) else "UNKNOWN"
            monto_val = float(pd.to_numeric(row[c_monto], errors='coerce') or 0.0)
            
            # Determine tipo_mov: PAGO if monto > 0 and doc type is NC, else CARGO for Factura
            doc_type = str(row['Tipo de documento']).lower() if 'Tipo de documento' in df.columns and pd.notna(row.get('Tipo de documento')) else ''
            if 'nota de credito' in doc_type and monto_val > 0:
                tipo_mov = 'PAGO'
            elif monto_val > 0:
                tipo_mov = 'PAGO'
            else:
                tipo_mov = 'CARGO'
            
            folio = str(int(row[c_folio])) if c_folio and pd.notna(row[c_folio]) and str(row[c_folio]).lower() != 'nan' and float(row[c_folio]) > 0 else None
            
            if abs(monto_val) > 0 or 'precio' in detail.lower():
                ledger_rows.append({
                    'marketplace': 'FALABELLA', 'id_transaccion': trans_id,
                    'id_orden': order_id, 'fecha': fecha,
                    'detalle': detail, 'monto': monto_val,
                    'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
                    'folio_xml': folio
                })
        except Exception as e:
            print(f"  Error row {idx}: {e}")
    
    if ledger_rows:
        df_ledger = pd.DataFrame(ledger_rows)[LEDGER_COLS]
        n = db.insert_df(df_ledger, "marketplace_ledger_v1", dedup_cols=['id_transaccion'])
        total_ledger += n
        print(f"  Loaded {n} ledger rows")
    else:
        print(f"  No ledger rows loaded")

# Validation
print(f"\n{'='*80}")
print(f"VALIDATION")
print(f"{'='*80}")

ventas = db.query("SELECT COUNT(*) as cnt FROM ventas_marketplace WHERE marketplace = 'FALABELLA'").iloc[0]['cnt']
ledger = db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'").iloc[0]['cnt']
print(f"ventas_marketplace: {ventas} rows")
print(f"marketplace_ledger_v1: {ledger} rows")

# Concepts loaded
if ledger > 0:
    concepts = db.query("""
        SELECT detalle, COUNT(*) as cnt, SUM(monto) as total
        FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'
        GROUP BY detalle ORDER BY SUM(ABS(monto)) DESC
    """)
    print(f"\nConcepts in ledger ({len(concepts)}):")
    for _, r in concepts.iterrows():
        print(f"  {str(r['detalle'])[:65]:<65s} | cnt={r['cnt']:>4d} | ${r['total']:>10,.0f}")
    
    # Unique orders
    orders = db.query("SELECT COUNT(DISTINCT id_orden) FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'").iloc[0, 0]
    print(f"\nUnique orders in ledger: {orders}")
    
    # Cross-domain match
    venta_orders = db.query("SELECT COUNT(DISTINCT order_id) FROM ventas_marketplace WHERE marketplace = 'FALABELLA'").iloc[0, 0]
    print(f"Unique orders in ventas: {venta_orders}")
    print(f"\nNOTE: The XLSX files are InvoiceReports (fees only).")
    print(f"No sales data loaded because 'Precio del producto' is not in these files.")
    print(f"The 75 ventas from earlier loader were cleared by reset_db.")
