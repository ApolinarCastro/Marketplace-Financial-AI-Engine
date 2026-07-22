import pandas as pd
import sqlite3
import os
import warnings
from datetime import datetime

# Configuración de Rutas
DB_PATH = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/database/conciliador.db'
SAP_ML = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/SAP/ML/SapQuery/SapQuery Ene23-Dic25.xlsx'
SAP_PARIS = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/SAP/PARIS/SapQuery/SapQuery Oct23-Dic25.xlsx'
SAP_RIPLEY = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/SAP/RIPLEY/SapQuery/SapQuery Ene23-Nov25.xlsx'

DIR_SETTLEMENT = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/ML/Settlement'
DIR_BILLING = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/ML/Facturacion'
DIR_PARIS = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/PARIS/Transacciones'
DIR_RIPLEY = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/RIPLEY/Ripley/'

warnings.filterwarnings('ignore')

def harmonizar_id(val):
    if pd.isna(val) or str(val).lower() == 'nan': return None
    s = str(val).strip().split('.')[0]
    if s == '': return None
    # Padding: Si tiene 9 dígitos, rellenar a 10 con un 0
    if s.isdigit() and len(s) == 9:
        s = s.zfill(10)
    return s

def get_col(df, possible_names):
    for name in possible_names:
        if name.upper() in df.columns: return df[name.upper()]
    return pd.Series([None] * len(df))

def main():
    print(f"[{datetime.now()}] >>> INICIANDO CARGA PRODUCTIVA V4 (NUEVOS FORMATOS) <<<")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Reset de Tablas para asegurar limpieza de datos viejos
    cursor.executescript("""
        DELETE FROM sap_raw;
        DELETE FROM meli_settlement_raw;
        DELETE FROM retailer_raw;
        DELETE FROM ml_billing_raw;
    """)

    # 2. CARGA SAP
    print("Exportando Maestros SAP...")
    maestros = [(SAP_ML, 'ML'), (SAP_PARIS, 'PARIS'), (SAP_RIPLEY, 'RIPLEY')]
    for path, canal in maestros:
        if os.path.exists(path):
            df = pd.read_excel(path, dtype=str)
            df_sap = pd.DataFrame({
                'order_id': df['Orden de Venta'].apply(harmonizar_id),
                'doc_num': df.get('Número SAP'),
                'total_product': pd.to_numeric(df['Total Sin Despacho'], errors='coerce').fillna(0),
                'shipping_sap': pd.to_numeric(df.get('Despacho', 0), errors='coerce').fillna(0),
                'canal': [canal] * len(df)
            }).dropna(subset=['order_id'])
            df_sap.to_sql('sap_raw', conn, if_exists='append', index=False)
            print(f"  - SAP {canal}: {len(df_sap)} registros.")

    # 3. CARGA SETTLEMENTS MELI (NUEVOS XLSX)
    print("Procesando Nuevas Liquidaciones MELI (XLSX)...")
    for arc in [f for f in os.listdir(DIR_SETTLEMENT) if f.endswith('.xlsx')]:
        path = os.path.join(DIR_SETTLEMENT, arc)
        try:
            df = pd.read_excel(path, dtype=str)
            df.columns = [str(c).upper().strip() for c in df.columns]
            
            df_meli = pd.DataFrame({
                'external_reference': get_col(df, ['NÚMERO DE IDENTIFICACIÓN', 'ID DE OPERACIÓN EN MERCADO PAGO']).apply(harmonizar_id),
                'order_id_meli': get_col(df, ['ID DE LA ORDEN']).apply(harmonizar_id),
                'pack_id': get_col(df, ['ID DEL PAQUETE']).apply(harmonizar_id),
                'bruto_compra': pd.to_numeric(get_col(df, ['VALOR DE LA COMPRA']), errors='coerce').fillna(0),
                'fee_meli': pd.to_numeric(get_col(df, ['COMISIÓN DE MERCADO LIBRE + IVA', 'COMISIONES + IVA']), errors='coerce').fillna(0),
                'shipping_meli': pd.to_numeric(get_col(df, ['COSTO DE ENVÍO']), errors='coerce').fillna(0),
                'settlement_date': get_col(df, ['FECHA DE LIBERACIÓN DEL DINERO'])
            })
            df_meli.to_sql('meli_settlement_raw', conn, if_exists='append', index=False)
            print(f"  - {arc}: {len(df_meli)} registros.")
        except Exception as e:
            print(f"  - Error en {arc}: {e}")

    # 4. CARGA RETAILERS
    print("Normalizando Ripley...")
    if os.path.exists(DIR_RIPLEY):
        for arc in [f for f in os.listdir(DIR_RIPLEY) if f.endswith('.xlsx')]:
            df = pd.read_excel(os.path.join(DIR_RIPLEY, arc), dtype=str)
            df.columns = [str(c).strip() for c in df.columns]
            if 'Orden de compra' in df.columns:
                df_c = pd.DataFrame({
                    'marketplace': ['RIPLEY'] * len(df),
                    'orden_compra': df['Orden de compra'].apply(harmonizar_id),
                    'monto_venta': pd.to_numeric(df.get('A pagar', 0), errors='coerce').fillna(0),
                    'source_file': [arc] * len(df)
                }).dropna(subset=['orden_compra'])
                df_c.to_sql('retailer_raw', conn, if_exists='append', index=False)

    print("Normalizando París...")
    if os.path.exists(DIR_PARIS):
        for arc in [f for f in os.listdir(DIR_PARIS) if f.endswith('.xlsx')]:
            df = pd.read_excel(os.path.join(DIR_PARIS, arc), dtype=str)
            df.columns = [str(c).lower().strip() for c in df.columns]
            if 'número orden' in df.columns:
                df_p = pd.DataFrame({
                    'marketplace': ['PARIS'] * len(df),
                    'orden_compra': df['número orden'].apply(harmonizar_id),
                    'monto_venta': pd.to_numeric(df['monto'], errors='coerce').fillna(0),
                    'source_file': [arc] * len(df)
                }).dropna(subset=['orden_compra'])
                df_p.to_sql('retailer_raw', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] >>> PROCESO COMPLETADO EXITO <<<")

if __name__ == "__main__":
    main()
