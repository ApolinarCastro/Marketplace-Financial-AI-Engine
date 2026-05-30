import pandas as pd
import os
import glob
import warnings
import numpy as np
from datetime import datetime

# Configuración de Rutas
RAW_BASE = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/01_Raw'
LIBERACIONES_PATH = os.path.join(RAW_BASE, 'ML/Liberaciones')
LIQUIDACION_FF_PATH = os.path.join(RAW_BASE, 'ML/Liquidacion_FF')
ML_FACTURACION_PATH = os.path.join(RAW_BASE, 'ML/ML_Facturacion')
SAP_ML_PATH = os.path.join(RAW_BASE, 'Sap/ML') # Ruta específica para Mercado Libre
OUTPUT_DIR = 'C:/Users/ASUS Zenbook/Documents/Marketplace_Conciliacion/02_Curated/ML_Master'

warnings.filterwarnings('ignore')

def harmonizar_id_meli(val):
    if pd.isna(val) or str(val).lower() == 'nan': return None
    s = str(val).strip().split('.')[0]
    if s == '' or s == 'None': return None
    # Regla: si empieza con 2, pad a 16 ceros post-primer dígito
    if 0 < len(s) < 16 and s.startswith('2'):
        gap = 16 - len(s)
        return s[0] + ('0' * gap) + s[1:]
    return s

def clean_numeric(val):
    if pd.isna(val) or val == '': return 0.0
    if isinstance(val, (int, float)): return float(val)
    
    s = str(val).strip()
    
    # Caso 1: Tiene punto y coma (ej. 1.234,56 -> LatAm standard)
    if ',' in s and '.' in s:
        s = s.replace('.', '').replace(',', '.')
    # Caso 2: Solo tiene coma (ej. 1234,56 -> Simple LatAm decimal)
    elif ',' in s:
        s = s.replace(',', '.')
    # Caso 3: Solo tiene punto (ej. 6343689.60 -> Standard Technical)
    # No removemos el punto porque es el decimal real de los datos raw de ML.
    else:
        pass
        
    try:
        # Limpieza final de espacios o basura
        return float(s)
    except:
        return 0.0

def clean_numeric_cols(df, cols):
    for col in cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_numeric)
    return df

# ==========================================
# 1. EXTRACTORES
# ==========================================

def load_all_liberaciones():
    print("Step 1: Cargando Liberaciones (Meli)...")
    files = glob.glob(os.path.join(LIBERACIONES_PATH, "**/*.xlsx"), recursive=True)
    dfs = []
    for f in files:
        try:
            df = pd.read_excel(f, dtype=str)
            df.columns = [c.strip() for c in df.columns]
            monto_cols = ["MONTO NETO ACREDITADO","MONTO NETO DEBITADO","MONTO BRUTO DE LA OPERACIÓN","COSTO DE ENVÍO"]
            df = clean_numeric_cols(df, monto_cols)
            if 'FECHA DE LIBERACIÓN' in df.columns:
                df['FECHA DE LIBERACIÓN'] = pd.to_datetime(df['FECHA DE LIBERACIÓN'], errors='coerce').dt.date
            dfs.append(df)
        except Exception as e:
            print(f"  Error cargando Liberación {f}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def load_all_ff():
    print("Step 2: Cargando Liquidación FF (MeliFF)...")
    files = glob.glob(os.path.join(LIQUIDACION_FF_PATH, "**/*.xlsx"), recursive=True)
    dfs = []
    for f in files:
        try:
            df = pd.read_excel(f, dtype=str)
            if 'fecha' in df.columns:
                df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce').dt.date
            df = clean_numeric_cols(df, ['monto'])
            dfs.append(df)
        except Exception as e:
            print(f"  Error cargando FF {f}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def load_sap():
    print("Step 6: Cargando SAP ML (Recursivo)...")
    files = glob.glob(os.path.join(SAP_ML_PATH, "**/*.xlsx"), recursive=True)
    if not files: 
        print("  [ADVERTENCIA] No se encontraron archivos SAP en", SAP_ML_PATH)
        # Retornar DF vacío con columnas esperadas para evitar KeyErrors
        return pd.DataFrame(columns=['Orden de Venta', 'Tipo Sap', 'Valor Sap', 'Numerador', 'Fecha'])
    
    dfs = []
    for f in files:
        print(f"  Cargando SAP: {os.path.basename(f)}")
        df = pd.read_excel(f, dtype=str)
        if 'Orden de Venta' in df.columns:
            df['Orden de Venta'] = df['Orden de Venta'].apply(harmonizar_id_meli)
        if 'Total Sin Despacho' in df.columns:
            df = clean_numeric_cols(df, ['Total Sin Despacho', 'Saldo Pendiente', 'Despacho', 'Total Documento'])
            df['Valor Sap'] = df['Total Sin Despacho']
        if 'Tipo' in df.columns:
            df = df.rename(columns={'Tipo': 'Tipo Sap'})
        dfs.append(df)
    
    df_sap = pd.concat(dfs, ignore_index=True)
    return df_sap[df_sap['Orden de Venta'].notna()].reset_index(drop=True)

def load_all_facturacion():
    print("Step 9: Cargando Facturación Fiscal (Meli Facturación)...")
    files = glob.glob(os.path.join(ML_FACTURACION_PATH, "*.xlsx"))
    if not files: return pd.DataFrame()
    dfs = []
    for f in files:
        try:
            df = pd.read_excel(f, dtype=str)
            df.columns = [c.strip() for c in df.columns]
            num_cols = ["Valor del cargo", "Subtotal sin descuento", "IVA y otros impuestos", "Precio unitario", "Total de la venta"]
            df = clean_numeric_cols(df, num_cols)
            if 'Fecha del cargo' in df.columns:
                df['Fecha del cargo'] = pd.to_datetime(df['Fecha del cargo'], errors='coerce').dt.date
            dfs.append(df)
        except Exception as e:
            print(f"  Error cargando Facturación {f}: {e}")
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

# ==========================================
# 2. LOGICA
# ==========================================

def get_meli_fees_logic(df_fact):
    """Procesa facturación para obtener comisiones y factura fiscal por orden"""
    print("Step 10: Procesando Comisiones y Facturas Fiscales...")
    if df_fact.empty: return pd.DataFrame()
    
    df = df_fact.copy()
    df['ID_Orden_Fact'] = df['Número de venta'].apply(harmonizar_id_meli)
    
    # Agrupar para obtener la Factura Fiscal (primera encontrada) y el total de comisiones
    fees = df.groupby('ID_Orden_Fact', as_index=False).agg(
        Factura_Fiscal=('N° de factura fiscal', 'first'),
        Comision_Meli=('Valor del cargo', 'sum'),
        Fecha_Factura=('Fecha del cargo', 'min')
    )
    return fees

def get_rmeli_logic(df_lib):
    """Query 3: Solo Fulfillment (me2)"""
    print("Step 3: Procesando RMeli (Fulfillment me2)...")
    if df_lib.empty: return pd.DataFrame()
    df = df_lib.copy()
    mask = (df['MODO DE ENVÍO'] == 'me2') & df['OPERATION_TAGS'].str.contains('fulfillment', na=False, case=False)
    df = df[mask].copy()
    df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].replace({'Pago': 'Venta', 'Mediación': 'Devolución', 'Envío': 'Venta'})
    df = df[df['DESCRIPCIÓN'].isin(['Venta', 'Devolución'])]
    
    df = df.rename(columns={
        "ID DE LA ORDEN": "ID_OrdenMeli", "ID DEL PAQUETE": "ID_PaqueteMeli", 
        "ITEM_ID": "ID_ItemMeli", "CÓDIGO DE PRODUCTO SKU": "SKU_Meli", 
        "DESCRIPCIÓN": "Tipo_Meli", "MONTO BRUTO DE LA OPERACIÓN": "Valor_Meli", 
        "FECHA DE LIBERACIÓN": "Fecha_Meli"
    })
    df['ID_OrdenMeli'] = df['ID_OrdenMeli'].apply(harmonizar_id_meli)
    df['ID_PaqueteMeli'] = df['ID_PaqueteMeli'].apply(harmonizar_id_meli)
    return df

def get_rmeliff_logic(df_ff):
    """Query 4: Liquidación FF normalizada"""
    print("Step 4: Procesando RMeliFF...")
    if df_ff.empty: return pd.DataFrame()
    df = df_ff.copy()
    df['tipo documento'] = df['tipo documento'].replace({'BOLETA': 'Venta', 'FACTURA': 'Venta', 'NOTA_CREDITO': 'Devolución'})
    df = df[df['descripcion'] != 'Costo de envío']
    df = df.rename(columns={
        "fecha": "Fecha_MeliFF", "venta": "ID_OrdenMeliFF", 
        "tipo documento": "Tipo_MeliFF", "monto": "Valor_MeliFF", 
        "sku": "SKU_MeliFF", "código del producto": "ID_ItemMeliFF"
    })
    df = clean_numeric_cols(df, ["Valor_MeliFF"])
    df['ID_OrdenMeliFF'] = df['ID_OrdenMeliFF'].apply(harmonizar_id_meli)
    return df.groupby(["Fecha_MeliFF", "ID_OrdenMeliFF", "ID_ItemMeliFF", "SKU_MeliFF", "Tipo_MeliFF"], as_index=False)["Valor_MeliFF"].sum()

def get_melimp_logic(df_lib):
    """Query 7: Marketplace (Marketplace tags)"""
    print("Step 7: Procesando MeliMP (Marketplace)...")
    if df_lib.empty: return pd.DataFrame()
    df = df_lib.copy()
    mask = df['OPERATION_TAGS'].str.contains('cross_docking|self_service', na=False, case=False)
    df = df[mask].copy()
    df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].replace({'Pago': 'Venta', 'Mediación': 'Devolución', 'Envío': 'Venta'})
    df = df[df['DESCRIPCIÓN'].isin(['Venta', 'Devolución'])]
    df = df.rename(columns={
        "FECHA DE LIBERACIÓN": "Fecha MeliMP", "ID DE LA ORDEN": "ID_ORDER", 
        "ID DEL PAQUETE": "ID_PACK", "DESCRIPCIÓN": "Tipo MeliMP", 
        "MONTO BRUTO DE LA OPERACIÓN": "Valor MeliMP"
    })
    df['ID_ORDER'] = df['ID_ORDER'].apply(harmonizar_id_meli)
    df['ID_PACK'] = df['ID_PACK'].apply(harmonizar_id_meli)
    return df.groupby(["Fecha MeliMP", "ID_ORDER", "ID_PACK", "Tipo MeliMP"], as_index=False)["Valor MeliMP"].sum()

# ==========================================
# 3. JOINS
# ==========================================

def conciliar_ff(df_rmeli, df_rmeliff):
    """Query 5: Conciliación FF"""
    print("Step 5: Ejecutando Conciliación FF...")
    if df_rmeli.empty or df_rmeliff.empty: return pd.DataFrame()
    
    m1 = df_rmeli.rename(columns={'ID_OrdenMeli': 'ClaveConciliacion'})[['ClaveConciliacion', 'ID_ItemMeli', 'SKU_Meli', 'Tipo_Meli', 'Fecha_Meli', 'Valor_Meli']].copy()
    m1['OrigenClave'] = 'ID Orden'
    m2 = df_rmeli.rename(columns={'ID_PaqueteMeli': 'ClaveConciliacion'})[['ClaveConciliacion', 'ID_ItemMeli', 'SKU_Meli', 'Tipo_Meli', 'Fecha_Meli', 'Valor_Meli']].copy()
    m2['OrigenClave'] = 'ID Paquete'
    
    meli_all = pd.concat([m1, m2], ignore_index=True).dropna(subset=['ClaveConciliacion'])
    meli_agg = meli_all.groupby(['ClaveConciliacion', 'ID_ItemMeli'], as_index=False).agg(
        Valor_Meli=('Valor_Meli', 'sum'),
        Fecha_Meli=('Fecha_Meli', 'min'),
        SKU_Meli=('SKU_Meli', 'first'),
        Tipo_Meli=('Tipo_Meli', 'first'),
        OrigenClave=('OrigenClave', 'first'),
        Valor_Meli_List=('Valor_Meli', lambda x: list(x))
    )
    
    # Identificar Reversas
    meli_agg['HasPos'] = meli_agg['Valor_Meli_List'].apply(lambda l: any(v > 0 for v in l))
    meli_agg['HasNeg'] = meli_agg['Valor_Meli_List'].apply(lambda l: any(v < 0 for v in l))

    res = pd.merge(df_rmeliff, meli_agg, left_on=['ID_OrdenMeliFF', 'ID_ItemMeliFF'], right_on=['ClaveConciliacion', 'ID_ItemMeli'], how='left')
    res['Diferencia'] = res['Valor_MeliFF'] - res['Valor_Meli'].fillna(0)
    
    def status_ff_net(row):
        if pd.isna(row['Valor_Meli']): return "No Conciliado"
        # Lógica de Reversas
        if row['HasPos'] and row['HasNeg']:
            if abs(row['Valor_Meli']) < 1: return "Reversa Total"
            return "Reversa Parcial"
        # Lógica Estándar
        if abs(row['Diferencia']) <= 1: return "Conciliado"
        return "Discrepancia"
    
    res['Detalle Conciliación'] = res.apply(status_ff_net, axis=1)
    return res

def conciliar_sap_mp(df_sap, df_melimp):
    """Query 8: Conciliacion SAP vs MP"""
    print("Step 8: Ejecutando Conciliación SAP vs Marketplace...")
    if df_sap.empty or df_melimp.empty: return df_sap
    
    m1 = df_melimp.rename(columns={'ID_ORDER': 'Clave'}).groupby(['Clave', 'Tipo MeliMP'], as_index=False).agg({'Valor MeliMP': 'sum', 'Fecha MeliMP': 'min'})
    m1['OrigenClave'] = 'ID Orden'
    m2 = df_melimp.rename(columns={'ID_PACK': 'Clave'}).groupby(['Clave', 'Tipo MeliMP'], as_index=False).agg({'Valor MeliMP': 'sum', 'Fecha MeliMP': 'min'})
    m2['OrigenClave'] = 'ID Paquete'
    
    meli_all = pd.concat([m1, m2], ignore_index=True).dropna(subset=['Clave'])
    
    # Agrupar detectando reversas (Named Aggregation)
    meli_final = meli_all.groupby(['Clave', 'Tipo MeliMP'], as_index=False).agg(
        Valor_MeliMP=('Valor MeliMP', 'sum'),
        Fecha_MeliMP=('Fecha MeliMP', 'min'),
        OrigenClave=('OrigenClave', 'first')
    ).rename(columns={'Valor_MeliMP': 'Valor MeliMP', 'Fecha_MeliMP': 'Fecha MeliMP'})
    
    res = pd.merge(df_sap, meli_final, left_on=['Orden de Venta', 'Tipo Sap'], right_on=['Clave', 'Tipo MeliMP'], how='left')
    
    # No obstante, detectamos reversas a nivel de SAP (si la orden aparece n veces)
    # Pero el usuario se refiere al detalle neto.
    
    def status_sap_mp_net(row):
        if pd.isna(row['Valor MeliMP']): return "No Conciliado"
        
        # Si Valor MeliMP tiene componentes neto cero
        # (Aunque el Join es por Tipo Sap, por lo que Venta y Devolución están en filas diferentes de SAP)
        # Si el usuario quiere ver "Reversa Total" cuando una factura de SAP tiene monto 0 por compensación:
        
        if abs(row['Valor Sap']) < 1 and abs(row['Valor MeliMP']) < 1:
            return "Reversa Total"
            
        if abs(row['Valor Sap'] - row['Valor MeliMP']) < 1: return "Conciliado"
        return "Discrepancia"
        
    res['Detalle Conciliación'] = res.apply(status_sap_mp_net, axis=1)
    return res

def format_latam_numeric(df):
    """Convierte columnas numéricas a formato LatAm y Fechas a formato corto (YYYY-MM-DD)"""
    new_df = df.copy()
    for col in new_df.columns:
        # Formato de Números
        if pd.api.types.is_numeric_dtype(new_df[col]):
            new_df[col] = new_df[col].apply(
                lambda x: "{:,.2f}".format(x).replace(',', 'X').replace('.', ',').replace('X', '.') 
                if pd.notna(x) and x != 0 else ("0,00" if x == 0 else "")
            )
        # Formato de Fechas (donde el nombre contenga 'Fecha')
        elif 'Fecha' in col:
            new_df[col] = pd.to_datetime(new_df[col], errors='coerce').dt.strftime('%Y-%m-%d')
            new_df[col] = new_df[col].astype(str).replace('NaT', '').replace('nan', '')
            
    return new_df

def main():
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    # Extraction
    lib = load_all_liberaciones()
    ff_raw = load_all_ff()
    sap = load_sap()
    fact_raw = load_all_facturacion()
    
    # Logic
    rmeli = get_rmeli_logic(lib)
    rmeliff = get_rmeliff_logic(ff_raw)
    melimp = get_melimp_logic(lib)
    meli_fees = get_meli_fees_logic(fact_raw)
    
    # Conciliation
    conci_ff = conciliar_ff(rmeli, rmeliff)
    conci_mp = conciliar_sap_mp(sap, melimp)
    
    # Cruzar Facturación Fiscal (Ffees/Comisiones)
    print("Step 11: Integrando Facturación Fiscal al Reporte 360...")
    if not meli_fees.empty:
        # En FF
        conci_ff = pd.merge(conci_ff, meli_fees, left_on='ID_OrdenMeliFF', right_on='ID_Orden_Fact', how='left').drop(columns=['ID_Orden_Fact'])
        # En MP vs SAP
        conci_mp = pd.merge(conci_mp, meli_fees, left_on='Orden de Venta', right_on='ID_Orden_Fact', how='left').drop(columns=['ID_Orden_Fact'])
    
    # Export con Formato Visual LatAm
    print("\nGuardando reportes con formato coma decimal...")
    if not conci_ff.empty:
        df_ff_visual = format_latam_numeric(conci_ff)
        df_ff_visual.to_excel(os.path.join(OUTPUT_DIR, '01_Conciliacion_FF_Full_Trazabilidad.xlsx'), index=False)
    
    if not conci_mp.empty:
        df_mp_visual = format_latam_numeric(conci_mp)
        df_mp_visual.to_excel(os.path.join(OUTPUT_DIR, '02_Conciliacion_Marketplace_vs_SAP.xlsx'), index=False)
    
    # SAP NO CONCILIADO
    if not conci_mp.empty:
        sap_pendiente = conci_mp[conci_mp['Detalle Conciliación'] == 'No Conciliado']
        df_sap_visual = format_latam_numeric(sap_pendiente)
        df_sap_visual.to_excel(os.path.join(OUTPUT_DIR, '03_SAP_Sin_Liquidacion_Marketplace.xlsx'), index=False)
    
    print("\n[OK] Motor de Conciliación 360 finalizado.")
    print(f"  - Registros FF: {len(conci_ff)}")
    print(f"  - Registros SAP/MP: {len(conci_mp)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print("\n[ERROR EN EL MOTOR]:")
        traceback.print_exc()
