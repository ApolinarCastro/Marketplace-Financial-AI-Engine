import duckdb
import pandas as pd
from pathlib import Path
import os

db_path = "data/db/meli_financial_v4_copy.db"
conn = duckdb.connect(db_path, read_only=True)
artifacts_dir = Path("C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/2c921f1a-4258-4b8e-be46-1ad937059ee6")

# FASE 1: MISSING ROWS
df_missing = conn.execute("""
    SELECT id_transaccion, id_orden, fecha, marketplace, archivo_origen, 
           monto, monto_bruto, comision_marketplace
    FROM marketplace_ledger_v1
    WHERE marketplace = 'PARIS' 
      AND detalle = 'Venta'
      AND (monto_bruto IS NULL OR comision_marketplace IS NULL)
""").df()

missing_md = f"""# PARIS V2 MISSING ROWS

## Total Faltantes: {len(df_missing)}

```
{df_missing.to_string(index=False)}
```
"""
with open(artifacts_dir / "PARIS_V2_MISSING_ROWS.md", "w", encoding="utf-8") as f:
    f.write(missing_md)

# Summarize by file
df_files = df_missing['archivo_origen'].value_counts().reset_index()
df_files.columns = ['archivo_origen', 'count']
print("Archivos con filas faltantes:")
print(df_files)

