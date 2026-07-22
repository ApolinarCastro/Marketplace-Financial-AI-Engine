import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import FINANCIAL_STRUCTURE
db = DatabaseV4.get()

def fmt(items): return "'" + "','".join(items) + "'"

sql = f"""
SELECT 
    SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ingresos"])}) THEN COALESCE(monto_bruto, monto) ELSE 0 END) as total_ingresos,
    SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["devoluciones"])}) THEN monto ELSE 0 END) as total_devoluciones,
    SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_operacionales"])}) THEN monto ELSE 0 END) as total_costos_op,
    SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ingresos"])}) THEN -COALESCE(comision_marketplace, 0) ELSE 0 END) +
    SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["costos_comerciales"])}) THEN monto ELSE 0 END) as total_costos_com,
    SUM(CASE WHEN clasificacion_operativa IN ({fmt(FINANCIAL_STRUCTURE["ajustes"])}) THEN monto ELSE 0 END) as total_ajustes
FROM marketplace_ledger_clasificado_v1
WHERE marketplace = 'PARIS' AND fecha >= '2026-01-01' AND fecha <= '2026-01-31'
"""

print(db.query(sql))
