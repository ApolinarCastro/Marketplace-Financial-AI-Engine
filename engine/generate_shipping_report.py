import sqlite3
import pandas as pd
import os

# Configuración de Rutas
DB_PATH = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/database/conciliador.db'
OUTPUT_DIR = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/02_Curated/Auditoria_Excepciones'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def generate_shipping_report():
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Obtener Balances Netos SAP por Orden
    query_sap = """
    SELECT order_id, canal, SUM(total_product) as sap_product_net, SUM(shipping_sap) as sap_shipping_net
    FROM sap_raw
    WHERE canal IN ('PARIS', 'RIPLEY')
    GROUP BY order_id, canal
    """
    df_sap = pd.read_sql(query_sap, conn)
    
    # 2. Obtener Balances Netos Marketplace por Orden
    query_mp = """
    SELECT orden_compra as order_id, marketplace as canal, SUM(monto_venta) as mp_paid_net
    FROM retailer_raw
    WHERE marketplace IN ('PARIS', 'RIPLEY')
    GROUP BY orden_compra, marketplace
    """
    df_mp = pd.read_sql(query_mp, conn)
    
    # 3. Unificar y Detectar Discrepancias de Flete
    df_comp = pd.merge(df_sap, df_mp, on=['order_id', 'canal'], how='inner')
    df_comp['diff'] = (df_comp['sap_product_net'] - df_comp['mp_paid_net']).round(0)
    df_comp['abs_diff'] = df_comp['diff'].abs()
    
    # Definir valores típicos de flete para reclamo
    typical_shipping = [3990, 4990, 5990, 2990, 1990]
    
    # Filtrar solo discrepancias de flete
    df_report = df_comp[df_comp['abs_diff'].isin(typical_shipping)].copy()
    
    # Etiquetar según el monto del flete
    df_report['tipo_flete'] = df_report['abs_diff'].apply(lambda x: f"Flete ${x:,.0f}")
    
    # Resumen para el usuario
    resumen = df_report.groupby(['canal', 'tipo_flete']).agg({
        'order_id': 'count',
        'abs_diff': 'sum'
    }).reset_index().rename(columns={'order_id': 'cantidad_ordenes', 'abs_diff': 'monto_total_reclamable'})
    
    print("\n--- RESUMEN DE RECUPERACIÓN DE FLETES (V4 NETEADO) ---")
    print(resumen.to_string(index=False))
    
    # Exportar listado detallado para el reclamo
    output_path = os.path.join(OUTPUT_DIR, 'Auditoria_Recupero_Fletes_TOTAL_V4.xlsx')
    df_report.to_excel(output_path, index=False)
    
    print(f"\n[ÉXITO] Reporte listo para reclamo en: {output_path}")
    conn.close()

if __name__ == "__main__":
    generate_shipping_report()
