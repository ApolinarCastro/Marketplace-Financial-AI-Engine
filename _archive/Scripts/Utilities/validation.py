import sys
import pandas as pd
import duckdb

sys.path.append('c:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine')

from engine.v4.database import DatabaseV4
# Provide read_only=True so DuckDB doesn't block
db = DatabaseV4.get(read_only=True)

from api.api import get_exec_summary, get_exec_waterfall, get_exec_cobros_breakdown, _resolve_period_range
date_start, date_end, label = _resolve_period_range('2026-02')

print("=== START ===", date_start, date_end, label)

# 1. Card Marketplace
print("\n=== CARD MARKETPLACE ===")
summary = get_exec_summary('2026-02')
for m in summary['marketplaces']:
    if m['id'] == 'ML':
        print(m)

# 2. Waterfall
print("\n=== WATERFALL ===")
wf = get_exec_waterfall('ML', '2026-02')
print(wf)

# 3. Composición Costos Marketplace
print("\n=== COMPOSICIÓN COSTOS ===")
bk = get_exec_cobros_breakdown('ML', '2026-02')
print(bk)

# SQL Validations
print("\n=== SQL: AJUSTES & RETENCIONES ===")
df_ajustes = db.query("""
    SELECT detalle, financial_group, clasificacion_operativa, SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE financial_group = 'devoluciones' AND clasificacion_operativa = 'OPERATIONAL_REASON'
    GROUP BY detalle, financial_group, clasificacion_operativa
""")
print(df_ajustes.to_string())

print("\n=== SQL: COSTOS MARKETPLACE BREAKDOWN ===")
df_breakdown = db.query(f"""
    SELECT marketplace, detalle, financial_group, clasificacion_operativa, SUM(COALESCE(monto, 0)) as total
    FROM marketplace_ledger_v1
    WHERE financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes')
      AND COALESCE(include_in_operational_pnl, 1) = 1
      AND fecha BETWEEN '{date_start}' AND '{date_end}'
      AND marketplace='ML'
    GROUP BY marketplace, detalle, financial_group, clasificacion_operativa
""")
print(df_breakdown.to_string())

print("\n=== SQL: DISPONIBLE (VENTAS Y DEVOLUCIONES) ===")
df_disp = db.query(f"""
    SELECT
        COALESCE(SUM(CASE WHEN financial_group='ingresos' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as ventas,
        COALESCE(SUM(CASE WHEN financial_group='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as devoluciones,
        COALESCE(SUM(CASE WHEN financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes') AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costos
    FROM marketplace_ledger_v1
    WHERE fecha BETWEEN '{date_start}' AND '{date_end}'
      AND marketplace='ML'
""")
print(df_disp.to_string())
