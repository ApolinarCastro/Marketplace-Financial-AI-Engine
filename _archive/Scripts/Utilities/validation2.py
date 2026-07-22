import sys
import pandas as pd
sys.path.append('c:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine')
from engine.v4.database import DatabaseV4

db = DatabaseV4.get(read_only=True)
date_start, date_end = '2026-02-01', '2026-02-28'

print("=== CIERRE (OLD CARD MARKETPLACE) ===")
df_cierre = db.query(f"""
    SELECT marketplace, SUM(total_ingresos) as gross, SUM(resultado_neto) as net 
    FROM marketplace_cierre_financiero_v1 
    WHERE periodo_inicio >= '{date_start}' AND periodo_fin <= '{date_end}' AND marketplace='ML'
    GROUP BY marketplace
""")
print(df_cierre.to_string())

print("\n=== LEDGER DEVOLUCIONES (OLD CARD MARKETPLACE) ===")
df_dev = db.query(f"""
    SELECT marketplace, COALESCE(SUM(monto), 0) as dev 
    FROM marketplace_ledger_v1 
    WHERE financial_group = 'devoluciones' AND COALESCE(include_in_operational_pnl, 1) = 1
      AND fecha BETWEEN '{date_start}' AND '{date_end}' AND marketplace='ML'
    GROUP BY marketplace
""")
print(df_dev.to_string())

print("\n=== LEDGER COSTOS (WATERFALL) ===")
df_wf = db.query(f"""
    SELECT 
        COALESCE(SUM(CASE WHEN financial_group='costos_operacionales' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costos_op,
        COALESCE(SUM(CASE WHEN financial_group='costos_comerciales' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costos_com,
        COALESCE(SUM(CASE WHEN financial_group='ajustes' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as ajustes
    FROM marketplace_ledger_v1
    WHERE fecha BETWEEN '{date_start}' AND '{date_end}' AND marketplace='ML'
""")
print(df_wf.to_string())

print("\n=== LEDGER DEVOLUCIONES OPERATIVAS (DEFECT 2) ===")
df_op_dev = db.query(f"""
    SELECT detalle, COUNT(*) as qty, SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE financial_group = 'devoluciones' AND clasificacion_operativa = 'OPERATIONAL_REASON'
      AND fecha BETWEEN '{date_start}' AND '{date_end}'
    GROUP BY detalle
""")
print(df_op_dev.to_string())
