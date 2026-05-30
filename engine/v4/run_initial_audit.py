import re
import sys
from pathlib import Path
import glob
import pandas as pd
import logging

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
from engine.v4.utils import load_file, harmonize_series, clean_amount

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("meli.audit_runner")

def _normalize_col_name(s: str) -> str:
    import unicodedata
    t = unicodedata.normalize('NFD', str(s).lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', t)

def _find_col(df, options):
    norm_options = [_normalize_col_name(o) for o in options]
    for col in df.columns:
        col_norm = _normalize_col_name(col)
        for opt_norm in norm_options:
            if opt_norm in col_norm or col_norm in opt_norm:
                return col
    return None

def load_marketplace_ledger_standalone(db):
    base_path = ROOT / "01_Raw"
    total_inserted = 0
    df_unified = []

    # Mercado Libre
    ml_files = glob.glob(str(base_path / "ML/Liberaciones/**/*.xlsx"), recursive=True)
    for fpath in ml_files:
        try:
            df = load_file(fpath)
            col_op = _find_col(df, ["ID DE OPERACIÓN EN MERCADO PAGO", "ID DE OPERACION EN MERCADO PAGO", "ID DE OPERACIN EN MERCADO PAGO"])
            col_ord = _find_col(df, ["ID DE LA ORDEN"])
            col_date = _find_col(df, ["FECHA DE LIBERACIÓN", "FECHA DE LIBERACION", "FECHA DE LIBERACIN"])
            col_desc = _find_col(df, ["DESCRIPCIÓN", "DESCRIPCION", "DESCRIPCIN"])
            col_net = _find_col(df, ["MONTO NETO ACREDITADO"])
            if col_op and col_date:
                col_type = _find_col(df, ["TIPO DE REGISTRO", "TIPO REGISTRO"])
                
                # Exclude summary rows ("Dinero disponible inicial", "Total") and null dates
                mask = pd.to_datetime(df[col_date], errors='coerce').notnull()
                if col_type:
                    mask &= ~df[col_type].astype(str).str.strip().isin(["Dinero disponible inicial", "Total"])
                
                df_filtered = df[mask].copy()
                if df_filtered.empty:
                    continue

                out = pd.DataFrame()
                out["id_orden"] = harmonize_series(df_filtered[col_ord]) if col_ord else None
                out["fecha"] = pd.to_datetime(df_filtered[col_date], errors='coerce').dt.date
                
                # Saneamiento de detalle
                if col_desc:
                    out["detalle"] = df_filtered[col_desc].astype(str).str.strip().apply(lambda x: None if x.lower() in ('nan', 'none', '') else x)
                else:
                    out["detalle"] = None
                
                # Fallback detail for payouts
                if col_type:
                    payout_mask = df_filtered[col_type].astype(str).str.strip() == "Dinero disponible"
                    if col_desc:
                        out["detalle"] = out["detalle"].fillna(df_filtered[col_desc].astype(str).str.strip())
                    out["detalle"] = out["detalle"].fillna(df_filtered[col_type].astype(str).str.strip())
                out["detalle"] = out["detalle"].fillna("Movimiento de Caja")
                
                col_deb = _find_col(df_filtered, ["MONTO NETO DEBITADO"])
                s_cred = df_filtered[col_net].apply(clean_amount) if col_net else 0.0
                s_deb = df_filtered[col_deb].apply(clean_amount) if col_deb else 0.0
                out["monto"] = s_cred - s_deb
                
                # Avoid NaNs propagating in ID concatenation by filling with fallback indexes
                op_series = harmonize_series(df_filtered[col_op])
                fallback_id = pd.Series("PAYOUT_" + Path(fpath).name + "_" + df_filtered.index.astype(str), index=df_filtered.index)
                out["id_transaccion"] = op_series.fillna(fallback_id)
                
                out["tipo_movimiento"] = "ML_LIQUIDACION"
                out["archivo_origen"] = Path(fpath).name
                out["folio_xml"] = None
                out["estado_xml"] = "PENDIENTE"
                out["load_ts"] = pd.Timestamp.now()
                out["marketplace"] = "ML"
                df_unified.append(out)
        except Exception as e:
            logger.error(f"Error ML {fpath}: {e}")

    # Paris
    paris_files = glob.glob(str(base_path / "PARIS/Transacciones/**/*.xlsx"), recursive=True)
    for fpath in paris_files:
        try:
            df = load_file(fpath)
            col_op = _find_col(df, ["ID"])
            col_ord = _find_col(df, ["NÚMERO ORDEN", "NUMERO ORDEN"])
            col_date = _find_col(df, ["FECHA"])
            col_desc = _find_col(df, ["TIPO"]) or _find_col(df, ["DESCRIPCIÓN", "DESCRIPCION"])
            col_net = _find_col(df, ["MONTO", "MONTO A PAGAR"])
            if col_op:
                out = pd.DataFrame()
                out["id_transaccion"] = harmonize_series(df[col_op])
                out["marketplace"] = "PARIS"
                out["id_orden"] = harmonize_series(df[col_ord]) if col_ord else None
                out["fecha"] = pd.to_datetime(df[col_date], errors='coerce').dt.date if col_date else None
                out["detalle"] = df[col_desc].astype(str).str.strip() if col_desc else ""
                out["monto"] = df[col_net].apply(clean_amount) if col_net else 0.0
                out["tipo_movimiento"] = "PARIS_TRANSACCION"
                out["archivo_origen"] = Path(fpath).name
                out["folio_xml"] = None
                out["estado_xml"] = "PENDIENTE"
                out["load_ts"] = pd.Timestamp.now()
                df_unified.append(out)
        except Exception as e:
            logger.error(f"Error Paris {fpath}: {e}")

    # Ripley
    ripley_files = glob.glob(str(base_path / "RIPLEY/**/*.xlsx"), recursive=True)
    for fpath in ripley_files:
        try:
            df = load_file(fpath)
            col_op = _find_col(df, ["NÚMERO DOCUMENTO LIQUIDACIÓN", "NUMERO DOCUMENTO LIQUIDACION"])
            col_ord = _find_col(df, ["ORDEN DE COMPRA"])
            col_date = _find_col(df, ["FECHA OC"])
            
            if col_op:
                # Ripley has horizontal amounts. Need to melt.
                value_vars = [c for c in df.columns if c not in [col_op, col_ord, col_date, 'Shop ID', 'Tienda']]
                melted = df.melt(id_vars=[col_op, col_ord, col_date], value_vars=value_vars, var_name='Detalle', value_name='Monto')
                melted = melted[melted['Monto'].notnull()]
                melted['Monto'] = melted['Monto'].apply(clean_amount)
                melted = melted[melted['Monto'] != 0.0]
                
                out = pd.DataFrame()
                out["id_transaccion"] = harmonize_series(melted[col_op])
                out["marketplace"] = "RIPLEY"
                out["id_orden"] = harmonize_series(melted[col_ord]) if col_ord else None
                out["fecha"] = pd.to_datetime(melted[col_date], errors='coerce').dt.date if col_date else None
                out["detalle"] = melted['Detalle'].astype(str).str.strip()
                out["monto"] = melted['Monto']
                out["tipo_movimiento"] = "RIPLEY_RUBRO"
                out["archivo_origen"] = Path(fpath).name
                out["folio_xml"] = None
                out["estado_xml"] = "PENDIENTE"
                out["load_ts"] = pd.Timestamp.now()
                df_unified.append(out)
        except Exception as e:
            logger.error(f"Error Ripley {fpath}: {e}")

    # Falabella
    falabella_files = glob.glob(str(base_path / "FALABELLA/**/*.xlsx"), recursive=True)
    for fpath in falabella_files:
        try:
            # Check where header is
            for skip in [0, 2, 5]:
                df = pd.read_excel(fpath, skiprows=skip)
                if _find_col(df, ["N° DE ORDEN", "N de orden", "Nº de orden"]) and _find_col(df, ["Monto con IVA", "MONTO A TRANSFERIR", "Monto Total"]):
                    break
            
            col_op = _find_col(df, ["ID ARTÍCULO", "ID ARTICULO", "ID", "Falabella-Id", "Falabella Id"])
            col_ord = _find_col(df, ["N° DE ORDEN", "NRO DE ORDEN", "N DE ORDEN", "N de orden", "Nº de orden"])
            col_date = _find_col(df, ["FECHA CREACIÓN DE LA ORDEN", "FECHA", "Fecha de Transaccion", "Fecha de transacción"])
            col_desc = _find_col(df, ["TIPO DE TRANSACCIÓN", "DETALLE", "Tipo de Transaccion", "Tipo de transacción"])
            col_net = _find_col(df, ["MONTO A TRANSFERIR", "MONTO TOTAL", "Monto con IVA", "Monto (Sin IVA)"])
            
            if col_op:
                out = pd.DataFrame()
                out["id_transaccion"] = harmonize_series(df[col_op])
                out["marketplace"] = "FALABELLA"
                out["id_orden"] = harmonize_series(df[col_ord]) if col_ord else None
                out["fecha"] = pd.to_datetime(df[col_date], errors='coerce').dt.date if col_date else None
                out["detalle"] = df[col_desc].astype(str).str.strip() if col_desc else ""
                out["monto"] = df[col_net].apply(clean_amount) if col_net else 0.0
                out["tipo_movimiento"] = "FALABELLA_TRANSACCION"
                out["archivo_origen"] = Path(fpath).name
                out["folio_xml"] = None
                out["estado_xml"] = "PENDIENTE"
                out["load_ts"] = pd.Timestamp.now()
                df_unified.append(out)
        except Exception as e:
            logger.error(f"Error Falabella {fpath}: {e}")

    db.execute("DELETE FROM marketplace_ledger_v1")
    
    if df_unified:
        final_df = pd.concat(df_unified, ignore_index=True)
        # Filter: solo datos 2025+ (excluir 2023/2024 legacy)
        final_df['fecha_dt'] = pd.to_datetime(final_df['fecha'], errors='coerce')
        final_df = final_df[final_df['fecha_dt'] >= pd.Timestamp('2025-01-01')].drop(columns=['fecha_dt'])
        
        cols = ['marketplace', 'id_transaccion', 'id_orden', 'fecha', 'detalle', 'monto', 'tipo_movimiento', 'archivo_origen', 'folio_xml', 'estado_xml', 'load_ts']
        final_df = final_df[cols]
        
        n = db.insert_df(final_df, "marketplace_ledger_v1")
        return n
    return 0

if __name__ == "__main__":
    db = DatabaseV4.get()
    engine = MarketplaceAuditorEngine()
    
    logger.info("--- PASO 1: Ingestión Multi-Marketplace (2023+) ---")
    rows = load_marketplace_ledger_standalone(db)
    logger.info(f"Insertadas {rows} transacciones en marketplace_ledger_v1.")

    logger.info("--- PASO 2: Clasificación ---")
    c = engine.run_classification()
    logger.info(f"Clasificadas {c} transacciones.")

    logger.info("--- PASO 3: Cierres Financieros ---")
    import calendar
    # Generar iterativamente por meses de 2025-2026
    for year in [2025, 2026]:
        for month in range(1, 13):
            last_day = calendar.monthrange(year, month)[1]
            p_ini = f"{year}-{month:02d}-01"
            p_fin = f"{year}-{month:02d}-{last_day}"
            
            engine.run_financial_closing("ML", p_ini, p_fin)
            engine.run_financial_closing("PARIS", p_ini, p_fin)
            engine.run_financial_closing("RIPLEY", p_ini, p_fin)
            engine.run_financial_closing("FALABELLA", p_ini, p_fin)

    logger.info("--- PASO 4: Auditoría ---")
    a = engine.run_audit()
    logger.info(f"Detectadas {a} desviaciones de auditoría en todos los marketplaces.")
