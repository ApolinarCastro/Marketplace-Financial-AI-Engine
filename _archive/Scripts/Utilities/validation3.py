import duckdb
import pandas as pd

conn = duckdb.connect("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine/data/db/meli_financial_v4.db", read_only=True)

date_start, date_end = '2026-02-01', '2026-02-28'

print("=== VALIDACION 1: COSTOS MARKETPLACE ===")
print("Querying Cierre para Card Marketplace (Antiguo calculo: net - gross - dev):")
df_cierre = conn.execute(f"""
    SELECT marketplace, SUM(total_ingresos) as gross, SUM(resultado_neto) as net 
    FROM marketplace_cierre_financiero_v1 
    WHERE periodo_inicio >= '{date_start}' AND periodo_fin <= '{date_end}' AND marketplace='ML'
    GROUP BY marketplace
""").df()
print(df_cierre.to_string())

df_dev = conn.execute(f"""
    SELECT marketplace, COALESCE(SUM(monto), 0) as dev 
    FROM marketplace_ledger_v1 
    WHERE financial_group = 'devoluciones' AND COALESCE(include_in_operational_pnl, 1) = 1
      AND fecha BETWEEN '{date_start}' AND '{date_end}' AND marketplace='ML'
    GROUP BY marketplace
""").df()
print(df_dev.to_string())

if not df_cierre.empty and not df_dev.empty:
    net = df_cierre['net'].iloc[0]
    gross = df_cierre['gross'].iloc[0]
    dev = df_dev['dev'].iloc[0]
    print(f"--> Card Marketplace (API Antigua): {net} - {gross} - ({dev}) = {net - gross - dev}")

print("\nQuerying Waterfall / Composicion (Costos Reales del Ledger):")
df_wf = conn.execute(f"""
    SELECT 
        COALESCE(SUM(CASE WHEN financial_group='costos_operacionales' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costos_op,
        COALESCE(SUM(CASE WHEN financial_group='costos_comerciales' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as costos_com,
        COALESCE(SUM(CASE WHEN financial_group='ajustes' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as ajustes
    FROM marketplace_ledger_v1
    WHERE fecha BETWEEN '{date_start}' AND '{date_end}' AND marketplace='ML'
""").df()
print(df_wf.to_string())
if not df_wf.empty:
    total_costos = df_wf['costos_op'].iloc[0] + df_wf['costos_com'].iloc[0] + df_wf['ajustes'].iloc[0]
    print(f"--> Waterfall / Composicion (API Correcta): {total_costos}")


print("\n=== VALIDACION 2: AJUSTES & RETENCIONES ===")
print("Buscando en Ledger todos los retornos operativos...")
df_op_dev = conn.execute(f"""
    SELECT detalle, COUNT(*) as qty, SUM(monto) as total
    FROM marketplace_ledger_v1
    WHERE clasificacion_operativa = 'OPERATIONAL_REASON'
      AND fecha BETWEEN '{date_start}' AND '{date_end}'
    GROUP BY detalle
""").df()
print(df_op_dev.to_string())


print("\n=== VALIDACION 3: TRAZABILIDAD COMPLETA ===")
df_traz = conn.execute(f"""
    SELECT
        COALESCE(SUM(CASE WHEN financial_group='ingresos' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as Ventas,
        COALESCE(SUM(CASE WHEN financial_group='devoluciones' AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as Devoluciones,
        COALESCE(SUM(CASE WHEN financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes') AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as Costos_Marketplace
    FROM marketplace_ledger_v1
    WHERE fecha BETWEEN '{date_start}' AND '{date_end}'
      AND marketplace='ML'
""").df()
print(df_traz.to_string())
if not df_traz.empty:
    disp = df_traz['Ventas'].iloc[0] + df_traz['Devoluciones'].iloc[0] + df_traz['Costos_Marketplace'].iloc[0]
    print(f"--> Disponible = {disp}")
