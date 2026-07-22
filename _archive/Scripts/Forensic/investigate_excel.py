import pandas as pd
from pathlib import Path

raw_dir = Path("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/01_Raw/PARIS/Transacciones")

files = ["06-06-2026.xlsx", "1 jun 2026 - 5 jun 2026.xlsx"]

with open("C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/2c921f1a-4258-4b8e-be46-1ad937059ee6/PARIS_V2_ROOT_CAUSE.md", "w", encoding="utf-8") as out:
    out.write("# PARIS V2 ROOT CAUSE\n\n")
    for fname in files:
        fpath = list(raw_dir.glob(f"**/{fname}"))
        if not fpath:
            out.write(f"## Archivo no encontrado: {fname}\n")
            continue
        fpath = fpath[0]
        df_raw = pd.read_excel(fpath, engine='calamine', header=None)
        
        # Display first 5 rows to see where the headers are
        out.write(f"## {fname}\n")
        out.write("### Primeras 10 filas (Raw)\n```\n")
        out.write(df_raw.head(10).to_string(index=False) + "\n```\n")
        out.write("\n")

print("Generated ROOT CAUSE doc.")
