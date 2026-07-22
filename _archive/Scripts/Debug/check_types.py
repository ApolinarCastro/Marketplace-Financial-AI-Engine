import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()
print(db.query("SELECT detalle, tipo_movimiento, SUM(monto) as total FROM marketplace_ledger_clasificado_v1 WHERE marketplace='ML' AND id_transaccion IN (SELECT id_transaccion FROM marketplace_ledger_v1 WHERE folio_xml='033-0008463012') GROUP BY detalle, tipo_movimiento"))
