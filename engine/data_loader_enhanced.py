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
DIR_PARIS = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/PARIS/Transacciones'
DIR_RIPLEY = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw/RIPLEY/Ripley/'

warnings.filterwarnings('ignore')

def limpiar_id(val):
    if pd.isna(val): return None
    s = str(val).strip().replace('.0', '')
    return s if s != 'nan' else None

def main():
    print(f"[{datetime.now()}] >>> INICIANDO CARGA MEJORADA (ORDEN + PAQUETE) <<<")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Reset de Tablas para asegurar consistencia
    cursor.execute("DROP TABLE IF EXISTS meli_settlement_raw")
    cursor.execute("""
        CREATE TABLE meli_settlement_raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            external_reference TEXT,
            order_id_meli TEXT,
            pack_id TEXT,
            bruto_compra REAL,
            fee_meli REAL,
            shipping_meli REAL,
            settlement_date TEXT
        )
    """)
    
    cursor.execute("DROP TABLE IF EXISTS sap_raw")
    cursor.execute("""
        CREATE TABLE sap_raw (
            order_id TEXT,
            doc_num TEXT,
            total_product REAL,
            shipping_sap REAL,
            canal TEXT
        )
    """)

    # 2. CARGA SAP
    print("Cargando maestros SAP...")
    maestros = [(SAP_ML, 'ML'), (SAP_PARIS, 'PARIS'), (SAP_RIPLEY, 'RIPLEY')]
    for path, canal in maestros:
        if os.path.exists(path):
            df = pd.read_excel(path)
            df_sap = pd.DataFrame({
                'order_id': df['Orden de Venta'].apply(limpiar_id),
                'doc_num': df.get('Número SAP'),
                'total_product': df.get('Total Sin Despacho', 0),
                'shipping_sap': df.get('Despacho', 0),
                'canal': [canal] * len(df)
            }).dropna(subset=['order_id'])
            df_sap.to_sql('sap_raw', conn, if_exists='append', index=False)
            print(f"  - SAP {canal}: {len(df_sap)} registros.")

    # 3. CARGA SETTLEMENTS MELI
    print("Cargando Liquidaciones MELI...")
    for arc in os.listdir(DIR_SETTLEMENT):
        if not arc.endswith('.csv'): continue
        path = os.path.join(DIR_SETTLEMENT, arc)
        try:
            df = None
            for sep in [';', ',']:
                try:
                    temp = pd.read_csv(path, sep=sep, on_bad_lines='skip', quotechar='"')
                    if len(temp.columns) > 10: 
                        df = temp
                        break
                except: continue
            
            if df is not None:
                df.columns = [str(c).upper().strip() for c in df.columns]
                df_meli = pd.DataFrame({
                    'external_reference': df.get('EXTERNAL_REFERENCE', '').astype(str).apply(limpiar_id),
                    'order_id_meli': df.get('ORDER_ID', '').astype(str).apply(limpiar_id),
                    'pack_id': df.get('PACK_ID', '').astype(str).apply(limpiar_id),
                    'bruto_compra': pd.to_numeric(df.get('TRANSACTION_AMOUNT', 0), errors='coerce').fillna(0),
                    'fee_meli': pd.to_numeric(df.get('MKP_FEE_AMOUNT', 0), errors='coerce').fillna(0),
                    'shipping_meli': pd.to_numeric(df.get('SHIPPING_FEE_AMOUNT', 0), errors='coerce').fillna(0),
                    'settlement_date': df.get('SETTLEMENT_DATE', '')
                })
                df_meli.to_sql('meli_settlement_raw', conn, if_exists='append', index=False)
                print(f"  - {arc}: {len(df_meli)} registros.")
        except Exception as e:
            print(f"  - Error en {arc}: {e}")

    # 4. CARGA RETAILERS (Paris/Ripley)
    # Ya lo hicimos antes pero lo incluimos para flujo completo
    print("Cargando Ripley...")
    if os.path.exists(DIR_RIPLEY):
        for arc in [f for f in os.listdir(DIR_RIPLEY) if f.endswith('.xlsx')]:
            df = pd.read_excel(os.path.join(DIR_RIPLEY, arc))
            if 'Orden de compra' in df.columns:
                df_c = pd.DataFrame({
                    'marketplace': ['RIPLEY'] * len(df),
                    'orden_compra': df['Orden de compra'].apply(limpiar_id),
                    'monto_venta': df.get('A pagar', 0),
                    'source_file': [arc] * len(df)
                }).dropna(subset=['orden_compra'])
                df_c.to_sql('retailer_raw', conn, if_exists='append', index=False)
    
    print("Cargando París...")
    if os.path.exists(DIR_PARIS):
        for arc in [f for f in os.listdir(DIR_PARIS) if f.endswith('.xlsx')]:
            df = pd.read_excel(os.path.join(DIR_PARIS, arc))
            df_p = pd.DataFrame({
                'marketplace': ['PARIS'] * len(df),
                'orden_compra': df['número orden'].apply(limpiar_id),
                'monto_venta': df.get('monto', 0),
                'source_file': [arc] * len(df)
            }).dropna(subset=['orden_compra'])
            df_p.to_sql('retailer_raw', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] >>> PROCESO FINALIZADO EXITOSAMENTE <<<")

if __name__ == "__main__":
    main()
