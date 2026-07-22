import pandas as pd
from engine.v4.database import DatabaseV4
db = DatabaseV4.get()

sql = "SELECT total_ingresos, total_costos_operacionales, total_costos_comerciales, total_ajustes, resultado_neto FROM marketplace_cierre_financiero_v1 WHERE marketplace='ML' AND periodo_inicio='2025-03-01'"
print(db.query(sql))

sql_tesoreria = """
SELECT tipo_movimiento, sum(monto) as total
FROM marketplace_ledger_clasificado_v1 
WHERE marketplace='ML' 
AND date_trunc('month', fecha) = '2025-03-01'
AND include_in_operational_pnl = False
GROUP BY tipo_movimiento
"""
print(db.query(sql_tesoreria))
