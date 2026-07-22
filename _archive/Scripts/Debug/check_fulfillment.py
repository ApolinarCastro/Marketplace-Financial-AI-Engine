import pandas as pd
from pathlib import Path

fpath = Path("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/01_Raw/PARIS/Transacciones/Fulfillment/1 jun 2026 - 5 jun 2026.xlsx")

df_raw = pd.read_excel(fpath, engine='calamine', header=None)
print("File:", fpath.name)
print(df_raw.head(10).to_string(index=False))

