import pandas as pd, glob, os, sys
sys.path.insert(0, r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

LEDGER_COLS = ['marketplace', 'id_transaccion', 'id_orden', 'fecha', 'detalle', 'monto', 'tipo_movimiento', 'archivo_origen', 'folio_xml']

db = DatabaseV4.get()
db.execute("DELETE FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'")
db.execute("DELETE FROM ventas_marketplace WHERE marketplace = 'FALABELLA'")

base = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\FALABELLA\Transacciones'
files = sorted(glob.glob(os.path.join(base, '*.xlsx')))

total = 0
for f in files:
    print(f"\n=== {os.path.basename(f)} ===")
    df = pd.read_excel(f, engine='calamine', header=0)
    print(f"  Shape: {df.shape}")

    df.columns = [str(c).strip().replace('\xa0', ' ').replace('\u00a0', ' ') for c in df.columns]
    cols = list(df.columns)
    print(f"  Columns: {cols}")

    # Manual column mapping by exact match
    col_map = {}
    for c in cols:
        cl = c.lower().strip()
        if cl == 'n de orden':
            col_map['order'] = c
        elif cl == 'falabella-id':
            col_map['id'] = c
        elif cl == 'tipo de transaccion':
            col_map['tipo'] = c
        elif cl == 'monto con iva':
            col_map['monto'] = c
        elif cl == 'fecha de transaccion':
            col_map['fecha'] = c
        elif cl == 'numero de documento':
            col_map['folio'] = c
        elif cl == 'tipo de documento':
            col_map['doc_type'] = c

    print(f"  Mapped: {col_map}")

    if 'order' not in col_map or 'monto' not in col_map or 'tipo' not in col_map:
        print(f"  SKIP: missing critical columns")
        continue

    ledger_rows = []
    for idx, row in df.iterrows():
        try:
            raw_order = row[col_map['order']]
            if pd.isna(raw_order) or str(raw_order).strip() == '':
                continue
            order_id = str(raw_order).strip()
            if order_id.lower() in ('nan', 'none', ''):
                continue

            fecha = pd.to_datetime(row[col_map['fecha']], errors='coerce') if 'fecha' in col_map and pd.notna(row[col_map['fecha']]) else None
            detail = str(row[col_map['tipo']]).strip()

            raw_monto = row[col_map['monto']]
            try:
                monto_val = float(pd.to_numeric(raw_monto, errors='coerce') or 0.0)
            except:
                monto_val = 0.0

            if monto_val == 0.0:
                continue

            tipo_mov = 'PAGO' if monto_val > 0 else 'CARGO'

            folio = None
            if 'folio' in col_map and pd.notna(row[col_map['folio']]):
                try:
                    fv = row[col_map['folio']]
                    if str(fv).strip().lower() not in ('nan', 'none', ''):
                        folio = str(int(float(fv)))
                except:
                    pass

            trans_id = str(row[col_map['id']]) if 'id' in col_map and pd.notna(row[col_map['id']]) and str(row[col_map['id']]).strip().lower() not in ('nan', 'none', '') else f"FAL_{os.path.basename(f)}_{idx}"

            ledger_rows.append({
                'marketplace': 'FALABELLA', 'id_transaccion': trans_id,
                'id_orden': order_id, 'fecha': fecha.date() if pd.notna(fecha) else None,
                'detalle': detail, 'monto': monto_val,
                'tipo_movimiento': tipo_mov, 'archivo_origen': os.path.basename(f),
                'folio_xml': folio
            })
        except Exception as e:
            print(f"  Error row {idx}: {e}")

    if ledger_rows:
        df_ledger = pd.DataFrame(ledger_rows)[LEDGER_COLS]
        n = db.insert_df(df_ledger, "marketplace_ledger_v1", dedup_cols=['id_transaccion'])
        total += n
        print(f"  Loaded {n} ledger rows")
    else:
        print(f"  No rows loaded")

print(f"\n{'='*60}")
ventas = db.query("SELECT COUNT(*) as cnt FROM ventas_marketplace WHERE marketplace = 'FALABELLA'").iloc[0]['cnt']
ledger = db.query("SELECT COUNT(*) as cnt FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'").iloc[0]['cnt']
print(f"ventas_marketplace: {ventas} rows")
print(f"marketplace_ledger_v1: {ledger} rows")

if ledger > 0:
    concepts = db.query("""
        SELECT detalle, COUNT(*) as cnt, SUM(monto) as total,
               SUM(CASE WHEN monto > 0 THEN monto ELSE 0 END) as total_pago,
               SUM(CASE WHEN monto < 0 THEN monto ELSE 0 END) as total_cargo
        FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'
        GROUP BY detalle ORDER BY SUM(ABS(monto)) DESC
    """)
    print(f"\nConcepts ({len(concepts)}):")
    for _, r in concepts.iterrows():
        print(f"  {str(r['detalle'])[:60]:<60s} | cnt={r['cnt']:>4d} | ${r['total']:>10,.0f} | PAGO=${r['total_pago']:>10,.0f} | CARGO=${r['total_cargo']:>10,.0f}")

    orders_count = db.query("SELECT COUNT(DISTINCT id_orden) as n FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'")
    print(f"\nUnique orders in ledger: {orders_count['n'].iloc[0]}")
    
    # Summary stats
    summary = db.query("""
        SELECT COUNT(*) as total_rows,
               SUM(monto) as net_total,
               SUM(CASE WHEN monto > 0 THEN monto ELSE 0 END) as total_pago,
               SUM(CASE WHEN monto < 0 THEN ABS(monto) ELSE 0 END) as total_cargo_abs
        FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA'
    """)
    s = summary.iloc[0]
    print(f"\nSummary: {s['total_rows']} rows | Net: ${s['net_total']:,.0f} | PAGO total: ${s['total_pago']:,.0f} | CARGO total: ${s['total_cargo_abs']:,.0f}")
    
    # Net by month
    months = db.query("""
        SELECT strftime('%Y-%m', fecha) as mes,
               COUNT(*) as cnt, SUM(monto) as net
        FROM marketplace_ledger_v1 WHERE marketplace = 'FALABELLA' AND fecha IS NOT NULL
        GROUP BY mes ORDER BY mes
    """)
    print(f"\nNet by month:")
    for _, r in months.iterrows():
        print(f"  {r['mes']}: {r['cnt']:>4d} rows | ${r['net']:>10,.0f}")
