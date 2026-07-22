import pandas as pd
from pathlib import Path

fpath = Path("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/01_Raw/PARIS/Transacciones/Fulfillment/1 jun 2026 - 8 jun 2026.xlsx")

df_raw = pd.read_excel(fpath, engine='calamine', header=None)

# Find row containing 15725904
for i in range(len(df_raw)):
    row_vals = [str(x) for x in df_raw.iloc[i].fillna('')]
    if any('15725904' in v or '311081557' in v for v in row_vals):
        print(f"Row {i}:", row_vals)
