import pandas as pd
from pathlib import Path
import duckdb

raw_dir = Path("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/01_Raw/PARIS/Transacciones")
db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4_copy.db"

conn = duckdb.connect(db_path, read_only=True)

df_missing = conn.execute("""
    SELECT id_transaccion, id_orden, fecha, archivo_origen 
    FROM marketplace_ledger_v1
    WHERE marketplace = 'PARIS' AND detalle = 'Venta' AND monto_bruto IS NULL
""").df()

files_to_check = list(raw_dir.glob("**/*.xlsx"))

missing_tx_ids = set(df_missing['id_transaccion'].astype(str))

found_in_files = {}

for fpath in files_to_check:
    try:
        df_raw = pd.read_excel(fpath, engine='calamine', header=None)
        # find header row
        header_idx = None
        for i in range(min(15, len(df_raw))):
            row_vals = [str(x).lower() for x in df_raw.iloc[i].fillna('')]
            if any('id' in v or 'orden' in v or 'trans' in v for v in row_vals):
                header_idx = i
                break
        
        if header_idx is not None:
            df = df_raw.iloc[header_idx+1:].copy()
            df.columns = df_raw.iloc[header_idx]
            
            # find ID column
            id_col = None
            for col in df.columns:
                if str(col).strip().lower() == 'id':
                    id_col = col
                    break
            
            if id_col:
                file_ids = set(df[id_col].astype(str))
                intersection = missing_tx_ids.intersection(file_ids)
                if intersection:
                    found_in_files[fpath.name] = len(intersection)
    except Exception as e:
        print(f"Error reading {fpath.name}: {e}")

print("Missing transactions found in files:")
for fname, count in found_in_files.items():
    print(f"{fname}: {count}")

