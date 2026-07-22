import pandas as pd
from engine.v4.database import DatabaseV4
import warnings
warnings.filterwarnings('ignore')

db = DatabaseV4.get()

df = db.query("""
    SELECT 
        periodo_inicio as Periodo, 
        total_ingresos as Venta_Bruta, 
        total_costos_comerciales as Comision_Marketplace, 
        total_costos_operacionales as Envios, 
        total_ajustes as Ajustes_y_Devoluciones, 
        resultado_neto as Pago_Neto
    FROM marketplace_cierre_financiero_v1 
    WHERE marketplace='ML' 
    ORDER BY periodo_inicio
""")

tesoreria = db.query("""
    SELECT 
        date_trunc('month', fecha) as Periodo,
        SUM(monto) as Payout_Liberaciones
    FROM marketplace_ledger_clasificado_v1
    WHERE marketplace='ML' AND clasificacion_operativa='Retiro de dinero'
    GROUP BY 1 ORDER BY 1
""")

print("=== CERTIFICACION ML ===")
print("Ecuacion: Venta_Bruta + Comision_Marketplace + Envios + Ajustes_y_Devoluciones = Pago_Neto")
print(df.to_string(index=False))

print("\n=== PAGO NETO (TESORERIA) ===")
# Format tesoreria period to match
tesoreria['Periodo'] = pd.to_datetime(tesoreria['Periodo']).dt.strftime('%Y-%m-%d')
print(tesoreria.to_string(index=False))

# Calculate Delta
merged = pd.merge(df, tesoreria, on='Periodo', how='outer').fillna(0)
merged['Delta'] = merged['Pago_Neto'] - merged['Payout_Liberaciones']
print("\n=== DELTA (Pago Neto vs Liberaciones) ===")
print(merged[['Periodo', 'Pago_Neto', 'Payout_Liberaciones', 'Delta']].to_string(index=False))
