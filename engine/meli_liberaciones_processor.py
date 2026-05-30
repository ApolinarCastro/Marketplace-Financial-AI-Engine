import sqlite3
import pandas as pd
import os
import glob
import warnings
from datetime import datetime

# Configuración de Rutas
DB_PATH = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/database/conciliador.db'
SAP_ML = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/SAP/ML/SapQuery/SapQuery Ene23-Dic25.xlsx'
LIBERACIONES_PATH = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/ML/Liberaciones'
OUTPUT_DIR = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/02_Curated/Reporte_Gerencial'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'Conciliacion_ML_Liberaciones_V6.xlsx')

warnings.filterwarnings('ignore')

def harmonizar_id_meli(val):
    if pd.isna(val) or str(val).lower() == 'nan' or str(val).strip() == '':
        return None
    
    # Manejo robusto de floats y strings
    try:
        # Convertir a float y luego a int para quitar .0, luego a string
        s = str(int(float(val)))
    except:
        s = str(val).strip().split('.')[0]
    
    if len(s) == 16:
        return s
        
    if 0 < len(s) < 16 and s.startswith('2'):
        gap = 16 - len(s)
        return s[0] + ('0' * gap) + s[1:]
    
    return s

def load_all_liberaciones():
    print(f"Buscando archivos en {LIBERACIONES_PATH}...")
    files = glob.glob(os.path.join(LIBERACIONES_PATH, "**/*.xlsx"), recursive=True)
    all_data = []
    
    for f in files:
        try:
            df_tmp = pd.read_excel(f)
            df_tmp.columns = [str(c).upper().strip() for c in df_tmp.columns]
            # Seleccionamos solo lo vital para el cruce inicial
            cols = ['ID DE LA ORDEN', 'ID DEL PAQUETE', 'FECHA DE LIBERACIÓN', 
                    'MONTO BRUTO DE LA OPERACIÓN', 'MONTO NETO ACREDITADO', 
                    'COMISIÓN DE MERCADO PAGO O MERCADO LIBRE (INCLUYE IVA)', 'COSTO DE ENVÍO']
            df_tmp = df_tmp[[c for c in cols if c in df_tmp.columns]]
            df_tmp['SOURCE_FILE'] = os.path.relpath(f, LIBERACIONES_PATH)
            all_data.append(df_tmp)
            print(f"  Cargado: {os.path.basename(f)} ({len(df_tmp)} filas)")
        except Exception as e:
            print(f"  Error cargando {f}: {e}")
            
    if not all_data: return pd.DataFrame()
    return pd.concat(all_data, ignore_index=True)

def generate_report():
    print("--- INICIANDO PROCESADOR MASTER V7: SAP vs LIBERACIONES ---")
    
    # 1. Liberaciones
    df_lib_raw = load_all_liberaciones()
    if df_lib_raw.empty: return

    print("Limpiando IDs en Liberaciones...")
    df_lib_raw['ID_ORDER'] = df_lib_raw['ID DE LA ORDEN'].apply(harmonizar_id_meli)
    df_lib_raw['ID_PACK'] = df_lib_raw['ID DEL PAQUETE'].apply(harmonizar_id_meli)
    
    def to_short_date(val):
        if pd.isna(val): return None
        return str(val).split(' ')[0].split('T')[0]

    # Agrupar ML (Suminamos todo por ID de Orden)
    # Nota: No agrupamos por fecha aquí para evitar duplicar el ID si el pago se liberó en días distintos
    print("Agrupando ML por ID de Orden...")
    df_ml_grouped = df_lib_raw.groupby('ID_ORDER').agg({
        'ID_PACK': 'first',
        'FECHA DE LIBERACIÓN': 'max',
        'MONTO BRUTO DE LA OPERACIÓN': 'sum',
        'MONTO NETO ACREDITADO': 'sum',
        'COMISIÓN DE MERCADO PAGO O MERCADO LIBRE (INCLUYE IVA)': 'sum',
        'COSTO DE ENVÍO': 'sum'
    }).reset_index()
    df_ml_grouped['FECHA_MP'] = df_ml_grouped['FECHA DE LIBERACIÓN'].apply(to_short_date)

    # 2. SAP
    print("Cargando SAP ML...")
    df_sap_raw = pd.read_excel(SAP_ML, dtype=str)
    df_sap_raw['ID_SAP'] = df_sap_raw['Orden de Venta'].apply(harmonizar_id_meli)
    
    # Consolidar SAP (1 linea por orden)
    df_sap_grouped = df_sap_raw.groupby('ID_SAP').agg({
        'Número SAP': 'first',
        'Tipo': 'first',
        'Fecha': 'first',
        'Total Documento': lambda x: pd.to_numeric(x, errors='coerce').sum(),
        'Total Sin Despacho': lambda x: pd.to_numeric(x, errors='coerce').sum(),
        'Despacho': lambda x: pd.to_numeric(x, errors='coerce').sum()
    }).reset_index()
    df_sap_grouped['FECHA_SAP'] = df_sap_grouped['Fecha'].apply(to_short_date)

    # DEBUG INTERSECCIÓN
    set_sap = set(df_sap_grouped['ID_SAP'].dropna())
    set_ml = set(df_ml_grouped['ID_ORDER'].dropna())
    inter = set_sap & set_ml
    print(f"DEBUG: IDs Únicos SAP: {len(set_sap)}")
    print(f"DEBUG: IDs Únicos ML (Liberaciones): {len(set_ml)}")
    print(f"DEBUG: PRODUCTO DE INTERSECCIÓN: {len(inter)} órdenes coincidentes")

    # 3. CRUCE
    print("Cruzando Bases...")
    df_final = pd.merge(df_sap_grouped, df_ml_grouped, left_on='ID_SAP', right_on='ID_ORDER', how='outer')

    # Renombrar columnas ANTES de los cálculos
    df_final = df_final.rename(columns={
        'FECHA_SAP': 'Fecha',
        'ID_SAP': 'Orden de Venta',
        'Número SAP': 'Numerador',
        'Tipo': 'Tipo Sap',
        'Total Documento': 'Valor Sap',
        'FECHA_MP': 'Fecha MeliMP',
        'MONTO BRUTO DE LA OPERACIÓN': 'Valor MeliMP',
        'ID_ORDER': 'ID_DeLaOrdenMeliMP',
        'ID_PACK': 'ID_PaqueteMeliMP',
        'MONTO NETO ACREDITADO': 'Neto_Meli_Audit',
        'COMISIÓN DE MERCADO PAGO O MERCADO LIBRE (INCLUYE IVA)': 'Comision_Meli_Audit',
        'COSTO DE ENVÍO': 'Envio_Meli_Audit'
    })

    # 4. Cálculos y Estatus (Espejo de Conciliación_MP)
    df_final['Saldo Pendiente'] = df_final['Valor Sap'].fillna(0) - df_final['Valor MeliMP'].fillna(0)
    
    def get_status(row):
        if pd.isna(row['Valor Sap']) or row['Valor Sap'] == 0:
            return 'Solo en Mercado Pago (Liberaciones)'
        if pd.isna(row['Valor MeliMP']) or row['Valor MeliMP'] == 0:
            return 'Pendiente de Cobro (SAP sin Liberación)'
        if abs(row['Saldo Pendiente']) < 10:
            return 'Conciliado_Liberaciones'
        return 'Discrepancia'

    df_final['Conciliado'] = df_final.apply(get_status, axis=1)
    
    # OrigenClave Única
    df_final['OrigenClave'] = df_final['Orden de Venta'].fillna('NO_SAP') + "_" + df_final['ID_DeLaOrdenMeliMP'].fillna('NO_ML')
    
    df_final['Tipo Pago MeliMP'] = 'Liberación Real'
    df_final['Detalle Conciliación'] = ''


    # Reordenar al formato exacto solicitado por el usuario (según screenshot)
    cols_final = [
        'Fecha', 'Orden de Venta', 'Numerador', 'Tipo Sap', 'Valor Sap', 
        'Total Sin Despacho', 'Despacho', 'Saldo Pendiente', 'Fecha MeliMP', 
        'Valor MeliMP', 'OrigenClave', 'Detalle Conciliación',
        'Tipo Pago MeliMP', 'ID_DeLaOrdenMeliMP', 'ID_PaqueteMeliMP', 
        'Conciliado', 'Neto_Meli_Audit', 'Comision_Meli_Audit', 'Envio_Meli_Audit'
    ]

    
    for c in cols_final:
        if c not in df_final.columns: df_final[c] = ''
        
    df_final = df_final[cols_final]

    # 6. Exportar
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    df_final.to_excel(OUTPUT_FILE, index=False)
    
    print(f"\n[OK] Reporte Generado exitosamente: {OUTPUT_FILE}")
    print(f"Registros Conciliados: {len(df_final[df_final['Conciliado']=='Conciliado_Liberaciones']):,}")
    print(f"Total Registros: {len(df_final):,}")

if __name__ == "__main__":
    generate_report()
