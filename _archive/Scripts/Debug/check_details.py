import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
print(db.query("SELECT detalle, tipo_movimiento, include_in_operational_pnl, sum(monto) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace='ML' AND fecha >= '2025-03-01' AND fecha <= '2025-03-31' GROUP BY detalle, tipo_movimiento, include_in_operational_pnl ORDER BY total DESC"))
