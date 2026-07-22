import pandas as pd
from pathlib import Path

raw_dir = Path("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/01_Raw/PARIS/Transacciones")

for fpath in raw_dir.glob("**/*.xlsx"):
    try:
        xl = pd.ExcelFile(fpath, engine='calamine')
        for sheet in xl.sheet_names:
            df_raw = xl.parse(sheet, header=None)
            for i in range(len(df_raw)):
                row_vals = [str(x) for x in df_raw.iloc[i].fillna('')]
                if any('15725904' in v or '311081557' in v for v in row_vals):
                    print(f"Found in {fpath.name} sheet {sheet} Row {i}")
                    print(row_vals)
    except Exception as e:
        pass
