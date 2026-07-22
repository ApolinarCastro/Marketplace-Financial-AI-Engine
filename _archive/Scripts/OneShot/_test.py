import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine

db = DatabaseV4.get()

# 1. Rebuild classification
print("Rebuilding classification...")
auditor = MarketplaceAuditorEngine()
auditor.run_classification()

# 2. Find unclassified
print("\n=== UNCLASSIFIED RIPLEY DETALLES ===")
res_clas = db.query("SELECT detalle, COUNT(*) as cnt FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' AND (financial_group IS NULL OR financial_group='NO_CLASIFICADO' OR financial_group='') GROUP BY detalle")
for _, row in res_clas.iterrows():
    print(f"UNCLASSIFIED: '{row['detalle']}' ({row['cnt']} rows)")
if len(res_clas) == 0:
    print("ALL CONCEPTS SUCCESSFULLY CLASSIFIED! (0 unclassified)")

# 3. Clasificación por concepto
print("\n=== CLASIFICACIÓN POR CONCEPTO ===")
clas_por_concepto = db.query("SELECT detalle, financial_group, COUNT(*) as cantidad_filas, SUM(monto) as monto FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' GROUP BY detalle, financial_group ORDER BY financial_group")
print(clas_por_concepto.to_string(index=False))

# 4. Include in operational pnl
print("\n=== INCLUDE IN OPERATIONAL PNL ===")
pnl_table = db.query("SELECT detalle, financial_group, include_in_operational_pnl FROM marketplace_ledger_clasificado_v1 WHERE marketplace='RIPLEY' GROUP BY detalle, financial_group, include_in_operational_pnl ORDER BY financial_group")
print(pnl_table.to_string(index=False))

# 5. Duplicidad check
print("\n=== DUPLICIDAD VALIDATION (Precio total vs order_amount) ===")
# Lets check for orders that have both
dupes = db.query("""
SELECT r1.id_orden, r1.detalle as det1, r1.monto as monto1, r2.detalle as det2, r2.monto as monto2
FROM marketplace_ledger_v1 r1
JOIN marketplace_ledger_v1 r2 ON r1.id_orden = r2.id_orden
WHERE r1.marketplace='RIPLEY' AND r2.marketplace='RIPLEY'
AND r1.detalle = 'Precio total' AND r2.detalle = 'order_amount'
LIMIT 10
""")
print(dupes.to_string(index=False))
