import pandas as pd
import duckdb
from pathlib import Path

db = duckdb.connect("data/db/meli_financial_v4.db")

df_clasif = db.execute("""
    SELECT c.id_transaccion, c.clasificacion_operativa, c.include_in_operational_pnl, c.monto, c.detalle, v1.archivo_origen
    FROM marketplace_ledger_clasificado_v1 c
    JOIN marketplace_ledger_v1 v1 ON c.id_transaccion = v1.id_transaccion
    WHERE c.marketplace = 'ML' AND c.id_transaccion LIKE 'POS_%'
""").df()

print("== Resumen ClasificaciÃ³n Poscobro en BD ==")
print(df_clasif.groupby(['clasificacion_operativa', 'include_in_operational_pnl'])['monto'].agg(['sum', 'count']).reset_index().to_string())

# Buscar detalles especÃ­ficos de Claim / Chargeback
print("\n== Resumen Detalles ==")
claim_mask = df_clasif['detalle'].str.lower().str.contains('claim|chargeback|reclamo|contracargo|compensation', na=False)
print(df_clasif[claim_mask].groupby(['detalle', 'clasificacion_operativa', 'include_in_operational_pnl'])['monto'].agg(['sum', 'count']).reset_index().to_string())
