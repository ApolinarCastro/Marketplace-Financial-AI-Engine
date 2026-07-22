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
    # Padding: Si tiene 9 dígitos, rellenar a 10 con un 0 (estándar Chile Business One)
    if s.isdigit() and len(s) == 9:
        s = s.zfill(10)
    return s

def get_col(df, possible_names):
    for name in possible_names:
        if name.upper() in df.columns: return df[name.upper()]
    return pd.Series([None] * len(df))

def main():
    print(f"[{datetime.now()}] >>> REINTENTANDO CARGA PRODUCTIVA V3 <<<")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Reset de Tablas
    cursor.executescript("""
        DELETE FROM ml_billing_raw;
        DELETE FROM sap_raw;
        DELETE FROM retailer_raw WHERE marketplace = 'PARIS';
    """)

    # 2. CARGA SAP
    print("Cargando maestros SAP...")
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

    # 3. CARGA BILLING
    print("Cargando Billing MELI...")
    if os.path.exists(DIR_BILLING):
        for arc in [f for f in os.listdir(DIR_BILLING) if f.endswith('.xlsx')]:
            df = pd.read_excel(os.path.join(DIR_BILLING, arc), dtype=str)
            df.columns = [str(c).upper().strip() for c in df.columns]
            
            df_b = pd.DataFrame({
                'n_factura': get_col(df, ['N° DE FACTURA FISCAL', 'N DE FACTURA FISCAL', 'FOLIO']),
                'fecha_cargo': get_col(df, ['FECHA DEL CARGO', 'FECHA']),
                'id_cargo': get_col(df, ['NÚMERO DEL CARGO', 'ID DEL CARGO', 'NUMERO DEL CARGO']),
                'detalle': get_col(df, ['DETALLE', 'DESCRIPTION']),
                'monto': pd.to_numeric(get_col(df, ['MONTO TOTAL', 'MONTO', 'TOTAL']), errors='coerce').fillna(0),
                'source_file': [arc] * len(df)
            })
            df_b.to_sql('ml_billing_raw', conn, if_exists='append', index=False)

    # 4. CARGA PARIS
    print("Cargando París con ID Armonizado...")
    if os.path.exists(DIR_PARIS):
        for arc in [f for f in os.listdir(DIR_PARIS) if f.endswith('.xlsx')]:
            df = pd.read_excel(os.path.join(DIR_PARIS, arc), dtype=str)
            df.columns = [str(c).lower().strip() for c in df.columns]
            df_p = pd.DataFrame({
                'marketplace': ['PARIS'] * len(df),
                'orden_compra': df['número orden'].apply(harmonizar_id),
                'monto_venta': pd.to_numeric(df['monto'], errors='coerce').fillna(0),
                'source_file': [arc] * len(df)
            }).dropna(subset=['orden_compra'])
            df_p.to_sql('retailer_raw', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] >>> PROCESO COMPLETADO <<<")

if __name__ == "__main__":
    main()
