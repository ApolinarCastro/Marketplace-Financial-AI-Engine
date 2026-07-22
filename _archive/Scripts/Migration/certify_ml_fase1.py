import pandas as pd
from engine.v4.database import DatabaseV4
import warnings
warnings.filterwarnings('ignore')

db = DatabaseV4.get()

# Fetch all ML data
df = db.query("""
    SELECT id_orden, tipo_movimiento, fecha, clasificacion_operativa, monto, financial_group
    FROM marketplace_ledger_clasificado_v1 
    WHERE marketplace='ML'
""")

df['fecha'] = pd.to_datetime(df['fecha'])

# Identificar ordenes cuya venta ocurrio en 2025-03
ventas_marzo = df[(df['clasificacion_operativa'] == 'Ingresos de venta') & 
                  (df['fecha'].dt.year == 2025) & 
                  (df['fecha'].dt.month == 3)]
ordenes_marzo = ventas_marzo['id_orden'].unique()

print(f"Total de ordenes con venta en Marzo 2025: {len(ordenes_marzo)}")

# Filtrar todos los movimientos ligados a esas ordenes (Ventas, Comisiones, Envios, Liberaciones)
df_marzo = df[df['id_orden'].isin(ordenes_marzo)]

# Calcular metricas
v_bruta = df_marzo[df_marzo['clasificacion_operativa'] == 'Ingresos de venta']['monto'].sum()
comision = df_marzo[df_marzo['clasificacion_operativa'] == 'Costos Comerciales']['monto'].sum()
envios = df_marzo[df_marzo['clasificacion_operativa'] == 'Costos Operacionales']['monto'].sum()
ajustes = df_marzo[df_marzo['clasificacion_operativa'].isin(['Ajustes', 'Devoluciones y Cancelaciones'])]['monto'].sum()

pago_neto = v_bruta + comision + envios + ajustes

payout = df_marzo[df_marzo['clasificacion_operativa'] == 'Retiro de dinero']['monto'].sum()

# Some Payouts might not be linked to id_orden, let's verify if 'Retiro de dinero' has id_orden
payout_total_marzo = df[(df['clasificacion_operativa'] == 'Retiro de dinero') & 
                        (df['fecha'].dt.year == 2025) & 
                        (df['fecha'].dt.month == 3)]['monto'].sum()

print("\n--- FASE 1 & FASE 3: FLUJO 2025-03 ---")
print(f"Venta Bruta: {v_bruta:,.2f}")
print(f"Comision: {comision:,.2f}")
print(f"Envios: {envios:,.2f}")
print(f"Ajustes/Devoluciones: {ajustes:,.2f}")
print(f"--> Pago Neto Operacional: {pago_neto:,.2f}")

print(f"\nPayout (Liberaciones ligadas a las ordenes): {payout:,.2f}")

# Payout diferido / Saldo retenido (Pendiente de liberar)
# Si el Pago Neto es lo que deberia liberar, y Payout es lo que se liberó, la diferencia es la Reserva / Pendiente
pendiente = pago_neto + payout # Assuming payout is negative? Let's check sign.
if payout > 0:
    pendiente = pago_neto - payout

print(f"--> Saldo Pendiente Liberar (Dinero en Transito/Reserva/Contracargo): {pendiente:,.2f}")
print(f"Comprobacion Delta = Pago Neto ({pago_neto:,.2f}) - [Payout ({payout:,.2f}) + Pendiente ({pendiente:,.2f})] = {pago_neto - (payout + pendiente):,.2f}")

# Let's check how many payouts have NO id_orden
payouts_no_orden = df[df['clasificacion_operativa'] == 'Retiro de dinero']['id_orden'].isnull().sum()
print(f"\nRetiros sin id_orden asociado: {payouts_no_orden}")
