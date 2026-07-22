import pandas as pd
from pathlib import Path
import duckdb

raw_dir = Path("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/01_Raw/PARIS")
db_path = "C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4_copy.db"

conn = duckdb.connect(db_path, read_only=True)

df_missing = conn.execute("""
    SELECT id_transaccion, id_orden, fecha, archivo_origen 
    FROM marketplace_ledger_v1
    WHERE marketplace = 'PARIS' AND detalle = 'Venta' AND monto_bruto IS NULL
""").df()

files_to_check = list(raw_dir.glob("**/*.xlsx"))

missing_tx_ids = set(df_missing['id_transaccion'].astype(str))
print(f"Looking for {len(missing_tx_ids)} unique transaction IDs.")

found_txs = {}
tx_to_gross_net = {}

for fpath in files_to_check:
    try:
        xl = pd.ExcelFile(fpath, engine='calamine')
        for sheet in xl.sheet_names:
            df_raw = xl.parse(sheet, header=None)
            
            header_idx = None
            for i in range(min(15, len(df_raw))):
                row_vals = [str(x).lower() for x in df_raw.iloc[i].fillna('')]
                if any('id' in v or 'orden' in v or 'trans' in v for v in row_vals):
                    header_idx = i
                    break
            
            if header_idx is not None:
                df = df_raw.iloc[header_idx+1:].copy()
                df.columns = [str(x).strip() for x in df_raw.iloc[header_idx]]
                
                # find ID column
                id_col = None
                for col in df.columns:
                    if col.lower() == 'id':
                        id_col = col
                        break
                
                if not id_col:
                    continue
                
                df[id_col] = df[id_col].astype(str)
                
                # find MONTO and MONTO A PAGAR
                gross_col = None
                net_col = None
                for col in df.columns:
                    cn = col.lower()
                    if 'monto' in cn and 'pagar' in cn:
                        net_col = col
                    elif cn == 'monto' or (cn.startswith('monto') and 'pagar' not in cn and 'comision' not in cn and 'total' not in cn):
                        if gross_col is None:
                            gross_col = col
                
                if not gross_col:
                    gross_col = net_col
                
                intersection = missing_tx_ids.intersection(set(df[id_col]))
                if intersection:
                    found_txs[fpath.name] = found_txs.get(fpath.name, 0) + len(intersection)
                    
                    # Store values
                    for idx, row in df[df[id_col].isin(intersection)].iterrows():
                        tx_id = str(row[id_col])
                        gross = pd.to_numeric(row[gross_col], errors='coerce') if gross_col else 0
                        net = pd.to_numeric(row[net_col], errors='coerce') if net_col else 0
                        tx_to_gross_net[tx_id] = {'monto_bruto': float(gross), 'monto_a_pagar': float(net)}
                        missing_tx_ids.remove(tx_id)
                        
    except Exception as e:
        print(f"Error reading {fpath.name}: {e}")

print("Missing transactions found in files:")
for fname, count in found_txs.items():
    print(f"{fname}: {count}")

print(f"Remaining missing: {len(missing_tx_ids)}")

import json
with open("recovered_data.json", "w") as f:
    json.dump(tx_to_gross_net, f)

