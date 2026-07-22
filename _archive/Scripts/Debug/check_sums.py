import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
print(db.query("SELECT sum(comision_marketplace) FROM marketplace_ledger_clasificado_v1 WHERE marketplace='PARIS' AND fecha >= '2026-01-01' AND fecha <= '2026-01-31' AND clasificacion_operativa IN ('Venta', 'Despacho', 'Cargo por venta')"))
