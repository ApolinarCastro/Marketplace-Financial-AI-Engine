import sqlite3
import pandas as pd
import os
import warnings
from datetime import datetime

# Configuración de Rutas
DB_PATH = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/database/conciliador.db'
SAP_ML = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/SAP/ML/SapQuery/SapQuery Ene23-Dic25.xlsx'
OUTPUT_DIR = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/02_Curated/Reporte_Gerencial'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'Conciliacion_ML_Completa_MP.xlsx')

warnings.filterwarnings('ignore')

def harmonizar_id(val):
    if pd.isna(val) or str(val).lower() == 'nan': return None
    s = str(val).strip().split('.')[0]
    if s == '': return None
    
    # REGLA MELI: Si empieza con 2 y es corto, rellenar a 16 ceros post-primer dígito
    if 0 < len(s) < 16 and s.startswith('2'):
        gap = 16 - len(s)
        return s[0] + ('0' * gap) + s[1:]
        
    return s

def formatear_fecha_corta(val):
    if pd.isna(val): return None
    try:
        dt = pd.to_datetime(val)
        return dt.strftime('%Y-%m-%d')
    except:
        return str(val).split(' ')[0].split('T')[0]

def generate_full_meli_mp():
    print('--- INICIANDO GENERACIÓN DE ESPEJO CONCILIACIÓN_MP (SIN DUPLICADOS) ---')
    
    # 1. Cargar SAP ML y AGRUPAR por Orden de Venta
    print('Cargando y Agrupando Detalle SAP ML...')
    df_sap_raw = pd.read_excel(SAP_ML, dtype=str)
    
    df_sap = pd.DataFrame({
        'Fecha': df_sap_raw.get('Fecha'),
        'Orden de Venta': df_sap_raw['Orden de Venta'].apply(harmonizar_id),
        'Numerador': df_sap_raw.get('Número SAP'),
        'Tipo Sap': df_sap_raw.get('Tipo', 'Venta'),
        'Valor Sap': pd.to_numeric(df_sap_raw.get('Total Documento', 0), errors='coerce').fillna(0),
        'Total Sin Despacho': pd.to_numeric(df_sap_raw.get('Total Sin Despacho', 0), errors='coerce').fillna(0),
        'Despacho': pd.to_numeric(df_sap_raw.get('Despacho', 0), errors='coerce').fillna(0)
    }).dropna(subset=['Orden de Venta'])

    # Agrupar SAP para evitar duplicados si hay múltiples líneas para la misma Orden de Venta
    df_sap_grouped = df_sap.groupby(['Orden de Venta', 'Numerador', 'Tipo Sap', 'Fecha']).agg({
        'Valor Sap': 'sum',
        'Total Sin Despacho': 'sum',
        'Despacho': 'sum'
    }).reset_index()
    df_sap_grouped['Fecha'] = df_sap_grouped['Fecha'].apply(formatear_fecha_corta)

    # 2. Cargar Liquidaciones MP y AGRUPAR
    print('Recuperando y Agrupando Liquidaciones MP...')
    conn = sqlite3.connect(DB_PATH)
    df_mp_raw = pd.read_sql("SELECT * FROM meli_settlement_raw", conn)
    conn.close()

    # Agrupamos por ID de Orden
    df_mp_by_order = df_mp_raw.groupby(['order_id_meli', 'pack_id', 'settlement_date']).agg({
        'bruto_compra': 'sum',
        'id': 'first' 
    }).reset_index().rename(columns={
        'order_id_meli': 'ID_DeLaOrdenMeliMP',
        'pack_id': 'ID_PaqueteMeliMP',
        'settlement_date': 'Fecha MeliMP',
        'bruto_compra': 'Valor MeliMP'
    })
    
    df_mp_by_order['Fecha MeliMP'] = df_mp_by_order['Fecha MeliMP'].apply(formatear_fecha_corta)

    # 3. CRUCE INTELIGENTE
    print('Ejecutando Cruce Agrupado (SAP vs MP)...')
    
    # Intentamos primero por Order ID
    df_final = pd.merge(df_sap_grouped, df_mp_by_order, left_on='Orden de Venta', right_on='ID_DeLaOrdenMeliMP', how='outer')
    
    # 4. Enriquecimiento Final
    df_final['Saldo Pendiente'] = df_final['Valor Sap'].fillna(0) - df_final['Valor MeliMP'].fillna(0)
    df_final['Tipo Pago MeliMP'] = 'Liquidación Marketplace'
    
    def generar_clave(row):
        sap_id = str(row['Orden de Venta']) if pd.notna(row['Orden de Venta']) else 'S' + str(row['Numerador'])
        mp_id = str(row['ID_DeLaOrdenMeliMP']) if pd.notna(row['ID_DeLaOrdenMeliMP']) else str(row['ID_PaqueteMeliMP']) if pd.notna(row['ID_PaqueteMeliMP']) else 'N/A'
        return f"{sap_id}_{mp_id}"

    df_final['OrigenClave'] = df_final.apply(generar_clave, axis=1)
    
    def status_conciliador(row):
        if pd.isna(row['Valor Sap']) or row['Valor Sap'] == 0:
            return 'Solo en Mercado Pago'
        if pd.isna(row['Valor MeliMP']) or row['Valor MeliMP'] == 0:
            return 'Pendiente de Cobro'
        if abs(row['Saldo Pendiente']) < 10:
            return 'Conciliado_MP'
        return 'Discrepancia'

    df_final['Conciliado'] = df_final.apply(status_conciliador, axis=1)
    df_final['Detalle Conciliación'] = ''
    
    # 5. Orden de Columnas (Screenshot style)
    cols_user = [
        'Fecha', 'Orden de Venta', 'Numerador', 'Tipo Sap', 'Valor Sap', 
        'Total Sin Despacho', 'Despacho', 'Saldo Pendiente', 'Fecha MeliMP', 
        'Valor MeliMP', 'OrigenClave', 'Detalle Conciliación',
        'Tipo Pago MeliMP', 'ID_DeLaOrdenMeliMP', 'ID_PaqueteMeliMP', 'Conciliado'
    ]
    
    for c in cols_user:
        if c not in df_final.columns: df_final[c] = ''
        
    df_final = df_final[cols_user]

    # 6. Exportar
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    df_final.to_excel(OUTPUT_FILE, index=False)
    
    print(f'[OK] Reporte Espejo Formateado y Agrupado: {OUTPUT_FILE}')
    print(f'Total Líneas Consolidadas: {len(df_final):,}')

if __name__ == "__main__":
    generate_full_meli_mp()

