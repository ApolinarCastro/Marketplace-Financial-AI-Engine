import pandas as pd, glob, os

base = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine\01_Raw\FALABELLA\Transacciones'
files = sorted(glob.glob(os.path.join(base, '*.xlsx')))

for f in files:
    print(f"\n{'='*100}")
    print(f"FILE: {os.path.basename(f)}")
    print(f"{'='*100}")
    
    # Read raw (no header)
    df_raw = pd.read_excel(f, engine='calamine', header=None)
    print(f"\nFirst 10 rows (raw, no header):")
    for i in range(10):
        vals = [str(v)[:40] for v in df_raw.iloc[i].values]
        print(f"  Row {i}: {vals[:10]}")
    
    # Try with skiprows=5 like the loader does
    df = pd.read_excel(f, skiprows=5)
    print(f"\nWith skiprows=5, shape={df.shape}")
    print(f"Columns: {list(df.columns)[:15]}")
    print(f"\nFirst 3 rows (first few cols):")
    for i in range(3):
        vals = [str(v)[:35] for v in df.iloc[i].values[:7]]
        print(f"  Row {i}: {vals}")
    
    # Check if 'Precio del producto' appears
    tipo_cols = [c for c in df.columns if 'ipo' in str(c).lower() or 'trans' in str(c).lower()]
    print(f"\nTipo columns found: {tipo_cols}")
    if tipo_cols:
        tc = tipo_cols[0]
        unique_tipos = df[tc].dropna().unique()
        print(f"  Unique tipos ({len(unique_tipos)}):")
        for t in unique_tipos[:20]:
            cnt = (df[tc] == t).sum()
            print(f"    [{cnt:>4d}x] {str(t)[:70]}")
        # Check for 'precio del producto'
        mask = df[tc].astype(str).str.lower().str.contains('precio del producto', na=False)
        print(f"\n  'precio del producto' rows: {mask.sum()}")
    
    # Check column detection
    from engine.v4.surgical_loader import get_col_name
    print(f"\nColumn detection:")
    for alias in ['Falabella-Id', 'Falabella Id', 'N de orden', 'Nº de orden', 'Fecha de Transaccion', 'Tipo de Transaccion', 'Monto con IVA', 'SKU vendedor']:
        found = get_col_name(df, [alias])
        print(f"  {alias:40s} -> {found}")
