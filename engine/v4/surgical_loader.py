import os
import pandas as pd
from pathlib import Path
import logging
import warnings
import re
import hashlib
import datetime as dt

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
logger = logging.getLogger("surgical.loader")

ROOT = Path(os.environ.get("MF_PROJECT_ROOT", Path(__file__).parent.parent.parent))
DIR_FACTURACION = ROOT / "01_Raw" / "ML" / "Facturacion"
DIR_POSCOBRO = ROOT / "01_Raw" / "ML" / "Poscobro"
DIR_LIBERACIONES = ROOT / "01_Raw" / "ML" / "Liberaciones"

LEDGER_COLS = ['marketplace', 'id_transaccion', 'id_orden', 'fecha', 'detalle', 'monto', 'tipo_movimiento', 'archivo_origen', 'folio_xml']
VENTAS_COLS = ['order_id', 'sku', 'quantity', 'unit_price', 'gross_amount', 'sale_date', 'marketplace', 'source_file']

def normalize(text):
    if not isinstance(text, str): return ""
    import unicodedata
    t = unicodedata.normalize('NFD', text.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')  # Strip accent marks
    return re.sub(r'[^a-z0-9]', '', t)

def get_col_name(df, possible_names):
    cols_norm = [normalize(str(c)) for c in df.columns]
    for p in possible_names:
        pn = normalize(p)
        for i, cn in enumerate(cols_norm):
            if pn in cn:
                return df.columns[i]
    return None

def read_excel_auto(fpath, possible_header_cols):
    norm_possible = [normalize(p) for p in possible_header_cols]
    best_h, max_found, best_df = 0, 0, None
    try:
        df_raw = pd.read_excel(fpath, engine='calamine', header=None)
        all_values = df_raw.head(15).values.tolist()
    except Exception as e:
        logger.error(f"Load error {fpath.name}: {e}")
        return None
    for h in range(len(all_values)):
        try:
            cols = [normalize(str(c)) for c in all_values[h]]
            found = sum(1 for p in norm_possible if any(p in c for c in cols))
            if found > max_found:
                max_found, best_h = found, h
                best_df = df_raw.iloc[h+1:].copy()
                best_df.columns = df_raw.iloc[h]
            if max_found >= 4: break
        except: continue
    if max_found >= 3:
        logger.info(f"Header row {best_h} for {fpath.name} ({max_found} cols)")
        return best_df
    return None


class SurgicalLoader:
    """
    Modelo Contable Correcto:
    â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    ConvenciÃ³n de signos: positivo = a favor del vendedor, negativo = costo/pÃ©rdida.

    Para "Cargo por venta":
      â†’ INGRESO_VENTA  = +Total de la venta (lo que pagÃ³ el comprador)
      â†’ EGRESO_COMISION = -Valor del cargo  (comisiÃ³n que ML cobra)

    Para "AnulaciÃ³n del cargo por venta":
      â†’ DEVOLUCION_VENTA  = -Total de la venta  (se pierde la venta)
      â†’ REVERSA_COMISION  = -Valor del cargo     (Valor ya es negativo â†’ -(-x) = +x, ML devuelve)

    Para todos los demÃ¡s cargos:
      â†’ CARGO = -Valor del cargo  (positivo en Excel = costo para vendedor)
      â†’ Las anulaciones de envÃ­o/devoluciÃ³n tienen Valor negativo â†’ -(-x) = +x = ajuste a favor
    """

    def __init__(self, db=None):
        if db is None:
            from engine.v4.database import DatabaseV4
            db = DatabaseV4.get()
        self.db = db

    def _register_file(self, filename, marketplace, row_count):
        """Registra archivo procesado en file_registry para tracking operacional."""
        try:
            if isinstance(filename, Path):
                file_hash = hashlib.sha256(filename.read_bytes()).hexdigest()
                file_name = filename.name
            else:
                file_hash = hashlib.sha256(filename.encode()).hexdigest()[:16]
                file_name = filename
            self.db.conn.execute("""
                INSERT OR REPLACE INTO file_registry (file_hash, file_name, source, rows_processed, processed_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, [file_hash, file_name, marketplace, row_count])
        except Exception:
            pass  # Non-critical, no interrumpir ETL por file_registry
    def _filter_old_years(self, df, date_col='fecha'):
        """Elimina filas con fecha en 2023 o 2024 (datos legacy excluidos del sistema)."""
        if date_col in df.columns:
            def _is_valid(d):
                if d is None: return True
                try:
                    y = d.year if hasattr(d, 'year') else pd.to_datetime(d).year
                    return y >= 2025
                except:
                    return True
            before = len(df)
            df = df[df[date_col].apply(_is_valid)]
            after = len(df)
            if before != after:
                logger.info(f"Filtradas {before - after} filas de 2023/2024 (columna '{date_col}')")
        return df

    def reset_db(self, marketplace='ML'):
        logger.info(f"Resetting tables for {marketplace}...")
        self.db.execute("DELETE FROM ventas_marketplace WHERE marketplace = ? OR (marketplace IS NULL AND ? = 'ML')", [marketplace, marketplace])
        self.db.execute("DELETE FROM marketplace_ledger_v1 WHERE marketplace = ? OR (marketplace IS NULL AND ? = 'ML')", [marketplace, marketplace])
        self.db.execute("DELETE FROM marketplace_ledger_clasificado_v1 WHERE marketplace = ? OR (marketplace IS NULL AND ? = 'ML')", [marketplace, marketplace])

    def load_facturacion(self, files=None, execution_id=None):
        logger.info("Loading ML_Facturacion...")
        files = files or sorted(list(DIR_FACTURACION.glob("*.xlsx")), key=lambda x: x.name, reverse=True)
        mandatory_cols = ['venta', 'factura', 'detalle', 'cargo', 'monto', 'fecha']
        total_inserted = 0

        for f in files:
            logger.info(f"Processing: {f.name}")
            try:
                df = read_excel_auto(f, mandatory_cols)
                if df is None: continue

                c_ord = get_col_name(df, ['numerodeventa', 'orderid', 'venta'])
                c_sku = get_col_name(df, ['publicacion', 'sku', 'itemid'])
                c_tot_venta = get_col_name(df, ['totaldelaventa', 'valordelacompra'])
                c_val_cargo = get_col_name(df, ['valordelcargo', 'monto'])
                c_detalle = get_col_name(df, ['detalle', 'description'])
                c_fecha = get_col_name(df, ['fechadelcargo', 'fecha'])
                c_folio = get_col_name(df, ['facturafiscal', 'folio', 'factura'])
                if not c_ord or not c_detalle: continue

                # 1. Registro de Ventas Ãºnicas (tabla ventas_marketplace)
                ventas_mask = df[c_detalle].apply(normalize).str.contains('cargoporventa', na=False)
                anulacion_mask = df[c_detalle].apply(normalize).str.contains('anulacion', na=False)
                solo_ventas = ventas_mask & ~anulacion_mask
                if solo_ventas.any() and c_tot_venta:
                    df_v = df[solo_ventas]
                    df_ventas = pd.DataFrame({
                        'order_id': df_v[c_ord].astype(str),
                        'sku': df_v[c_sku].astype(str) if c_sku else 'UNKNOWN',
                        'quantity': 1,
                        'unit_price': pd.to_numeric(df_v[c_tot_venta], errors='coerce').fillna(0),
                        'gross_amount': pd.to_numeric(df_v[c_tot_venta], errors='coerce').fillna(0),
                        'sale_date': pd.to_datetime(df_v[c_fecha], errors='coerce'),
                        'marketplace': 'ML', 'source_file': f.name
                    }).drop_duplicates(subset=['order_id'])
                    self.db.insert_df(self._filter_old_years(df_ventas[VENTAS_COLS], 'sale_date'), "ventas_marketplace", dedup_cols=['order_id'])

                # 2. Construir Ledger AtÃ³mico
                ledger = []
                for idx, row in df.iterrows():
                    det_orig = str(row[c_detalle]) if c_detalle else "Cargo"
                    det_norm = normalize(det_orig)
                    order_id = str(row[c_ord])
                    try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
                    except: fecha = None
                    folio = None
                    if c_folio and pd.notna(row[c_folio]):
                        raw_folio = str(row[c_folio]).strip()
                        if raw_folio and raw_folio.lower() != 'nan' and raw_folio not in ('0', '0.0'):
                            folio = raw_folio
                    
                    _vc = pd.to_numeric(row[c_val_cargo], errors='coerce') if c_val_cargo else 0.0
                    valor_cargo = float(_vc) if pd.notna(_vc) else 0.0
                    _tv = pd.to_numeric(row[c_tot_venta], errors='coerce') if c_tot_venta else 0.0
                    total_venta = float(_tv) if pd.notna(_tv) else 0.0

                    is_cargo_venta = "cargoporventa" in det_norm and "anulacion" not in det_norm
                    is_anulacion_venta = "anulacion" in det_norm and "cargoporventa" in det_norm

                    if is_cargo_venta:
                        # VENTA: ingreso bruto + comisiÃ³n cobrada
                        ledger.append({
                            'marketplace': 'ML', 'id_transaccion': f"SALE_{order_id}_{f.name}_{idx}",
                            'id_orden': order_id, 'fecha': fecha,
                            'detalle': "Cargo por venta (Venta)",
                            'monto': total_venta,  # +positivo = ingreso
                            'tipo_movimiento': 'INGRESO_VENTA',
                            'archivo_origen': f.name, 'folio_xml': folio
                        })
                        ledger.append({
                            'marketplace': 'ML', 'id_transaccion': f"COMM_{order_id}_{f.name}_{idx}",
                            'id_orden': order_id, 'fecha': fecha,
                            'detalle': "Cargo por venta (Comisión)",
                            'monto': -valor_cargo,  # valor_cargo=5199 â†’ monto=-5199 (costo)
                            'tipo_movimiento': 'EGRESO_COMISION',
                            'archivo_origen': f.name, 'folio_xml': folio
                        })

                    elif is_anulacion_venta:
                        # DEVOLUCIÃ“N: se pierde la venta + ML devuelve comisiÃ³n
                        ledger.append({
                            'marketplace': 'ML', 'id_transaccion': f"REFUND_{order_id}_{f.name}_{idx}",
                            'id_orden': order_id, 'fecha': fecha,
                            'detalle': "Devolución de venta",
                            'monto': -total_venta,  # -negativo = se pierde el ingreso
                            'tipo_movimiento': 'DEVOLUCION',
                            'archivo_origen': f.name, 'folio_xml': folio
                        })
                        ledger.append({
                            'marketplace': 'ML', 'id_transaccion': f"REVCOMM_{order_id}_{f.name}_{idx}",
                            'id_orden': order_id, 'fecha': fecha,
                            'detalle': "AnulaciÃ³n del cargo por venta",
                            'monto': -valor_cargo,  # valor_cargo=-5199 â†’ monto=+5199 (ML devuelve)
                            'tipo_movimiento': 'AJUSTE',
                            'archivo_origen': f.name, 'folio_xml': folio
                        })

                    else:
                        # TODOS LOS DEMÃS CARGOS: envÃ­os, publicidad, fullfilment, etc.
                        # -valor_cargo: si cargo=3420 â†’ monto=-3420 (costo)
                        # si es anulaciÃ³n de envÃ­o: cargo=-3420 â†’ monto=+3420 (ML devuelve)
                        ledger.append({
                            'marketplace': 'ML', 'id_transaccion': f"CHG_{f.name}_{idx}",
                            'id_orden': order_id, 'fecha': fecha,
                            'detalle': det_orig,
                            'monto': -valor_cargo,
                            'tipo_movimiento': 'CARGO',
                            'archivo_origen': f.name, 'folio_xml': folio
                        })

                if ledger:
                    df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                    if execution_id:
                        df_ledger['execution_id'] = execution_id
                    df_ledger = self._filter_old_years(df_ledger)
                    self.db.execute("DELETE FROM marketplace_ledger_v1 WHERE archivo_origen = ?", [f.name])
                    total_inserted += self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    if not execution_id:
                        self._register_file(f.name, "ML", len(df_ledger))

            except Exception as e:
                logger.error(f"Error {f.name}: {e}")
        return total_inserted

    def load_poscobro(self):
        logger.info("Loading ML_Poscobro...")
        for f in DIR_POSCOBRO.glob("*.xlsx"):
            logger.info(f"Processing: {f.name}")
            try:
                df = read_excel_auto(f, ['order', 'monto', 'operation'])
                if df is None: continue
                c_ord = get_col_name(df, ['orderid', 'orden', 'transaccion'])
                c_op = get_col_name(df, ['operationid', 'operacionid'])
                c_amt = get_col_name(df, ['operation_amount', 'amount', 'monto'])
                c_dev = get_col_name(df, ['montodevolucion', 'devolucion'])
                c_det = get_col_name(df, ['reasondetail', 'motivo', 'detalle'])
                c_stat = get_col_name(df, ['statusdetail'])
                c_dat = get_col_name(df, ['datecreated', 'fecha'])
                if not c_ord: continue

                ledger = []
                for idx, row in df.iterrows():
                    monto_raw = float(pd.to_numeric(row[c_amt], errors='coerce') or 0) if c_amt else 0
                    monto_dev = float(pd.to_numeric(row[c_dev], errors='coerce') or 0) if c_dev else 0
                    val = monto_dev * -1 if monto_dev != 0 else monto_raw
                    fecha = pd.to_datetime(row[c_dat], dayfirst=True, errors="coerce") if c_dat else None
                    
                    # Prevent 'nan' and get a valid detail string
                    raw_det = str(row[c_det]).strip() if c_det and pd.notna(row[c_det]) else ""
                    raw_stat = str(row[c_stat]).strip() if c_stat and pd.notna(row[c_stat]) else ""
                    
                    if raw_det and raw_det.lower() != "nan":
                        final_det = raw_det
                    elif raw_stat and raw_stat.lower() != "nan":
                        final_det = raw_stat
                    else:
                        final_det = "Ajuste Poscobro"

                    # Generar id_transaccion Ãºnico robusto
                    c_op_val = str(row[c_op]).strip() if c_op and pd.notna(row[c_op]) else ""
                    if c_op_val and c_op_val.lower() not in ['', '0', '0.0', 'nan', 'none']:
                        trans_id = f"POS_{c_op_val}_{f.name}_{idx}"
                    else:
                        trans_id = f"POS_{f.name}_{idx}"

                    ledger.append({
                        'marketplace': 'ML',
                        'id_transaccion': trans_id,
                        'id_orden': str(row[c_ord]), 'fecha': fecha,
                        'detalle': final_det,
                        'monto': val, 'tipo_movimiento': 'PAGO',
                        'archivo_origen': f.name, 'folio_xml': None
                    })
                if ledger:
                    df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                    df_ledger = self._filter_old_years(df_ledger)
                    # Deduplicar por (operation_id, detalle) â€” el Excel fuente tiene filas repetidas
                    df_ledger['_op_id'] = df_ledger['id_transaccion'].str.extract(r'POS_(\d+)_', expand=False)
                    antes = len(df_ledger)
                    df_ledger = df_ledger.drop_duplicates(subset=['_op_id', 'detalle', 'monto', 'fecha'])
                    despues = len(df_ledger)
                    if antes != despues:
                        logger.info(f"Poscobro dedup: {antes} â†’ {despues} filas ({antes - despues} duplicados eliminados)")
                    df_ledger = df_ledger.drop(columns=['_op_id'])
                    self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    self._register_file(f.name, "ML", len(df_ledger))
            except Exception as e:
                logger.error(f"Error Poscobro {f.name}: {e}")

    def load_liberaciones(self):
        logger.info("Loading ML_Liberaciones...")
        for f in DIR_LIBERACIONES.glob("**/*.xlsx"):
            logger.info(f"Processing: {f.name}")
            try:
                df = read_excel_auto(f, ['ID DE OPERACIÃ“N EN MERCADO PAGO', 'ID DE LA ORDEN', 'MONTO NETO ACREDITADO'])
                if df is None: continue
                
                from engine.v4.utils import harmonize_series, clean_amount
                
                def _find_col(d, options):
                    from engine.v4.run_initial_audit import _normalize_col_name
                    norm_options = [_normalize_col_name(o) for o in options]
                    for col in d.columns:
                        col_norm = _normalize_col_name(col)
                        if any(opt in col_norm or col_norm in opt for opt in norm_options): return col
                    return None
                    
                col_op = _find_col(df, ["ID DE OPERACIÃ“N EN MERCADO PAGO"])
                col_ord = _find_col(df, ["ID DE LA ORDEN"])
                col_date = _find_col(df, ["FECHA DE LIBERACIÃ“N"])
                col_net = _find_col(df, ["MONTO NETO ACREDITADO"])
                col_deb = _find_col(df, ["MONTO NETO DEBITADO"])
                col_type = _find_col(df, ["TIPO DE REGISTRO"])
                
                if not col_op or not col_date: continue
                
                mask = pd.to_datetime(df[col_date], errors='coerce').notnull()
                if col_type:
                    mask &= ~df[col_type].astype(str).str.strip().isin(["Dinero disponible inicial", "Total"])
                
                df_filtered = df[mask].copy()
                if df_filtered.empty: continue
                
                s_cred = df_filtered[col_net].apply(clean_amount) if col_net else 0.0
                s_deb = df_filtered[col_deb].apply(clean_amount) if col_deb else 0.0
                monto = s_cred - s_deb
                
                ledger = []
                for idx, row in df_filtered.iterrows():
                    m = monto.loc[idx]
                    if pd.isna(m) or m == 0: continue
                    # Retiro de fondos / Liberaciones map a Tesoreria
                    ledger.append({
                        'marketplace': 'ML',
                        'id_transaccion': f"PAYOUT_{row[col_op] if pd.notna(row[col_op]) else f'{f.name}_{idx}'}",
                        'id_orden': str(row[col_ord]) if col_ord and pd.notna(row[col_ord]) else None,
                        'fecha': pd.to_datetime(row[col_date]).date(),
                        'detalle': "Retiro de dinero", # Mapea a Tesoreria
                        'monto': m,
                        'tipo_movimiento': 'ML_LIQUIDACION',
                        'archivo_origen': f.name,
                        'folio_xml': None
                    })
                if ledger:
                    df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                    df_ledger = self._filter_old_years(df_ledger)
                    self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    self._register_file(f.name, "ML", len(df_ledger))
            except Exception as e:
                logger.error(f"Error Liberaciones {f.name}: {e}")

    def load_paris(self):
        logger.info("Loading Paris...")
        dir_paris = ROOT / "01_Raw" / "PARIS" / "Transacciones"
        if not dir_paris.exists():
            logger.warning("Paris raw folder does not exist")
            return
        files = sorted([f for f in dir_paris.glob("**/*.xlsx") if not f.name.startswith("~$")], key=lambda x: x.name, reverse=True)
        
        mandatory_cols = ['id', 'tipo', 'nÃºmero orden', 'monto a pagar']
        for f in files:
            logger.info(f"Processing Paris: {f.name}")
            try:
                df = read_excel_auto(f, mandatory_cols)
                if df is None: continue
                
                c_id = get_col_name(df, ['id'])
                c_tipo = get_col_name(df, ['tipo', 'descripciÃ³n'])
                c_ord = get_col_name(df, ['nÃºmero orden', 'nro orden'])
                
                # Obtenemos la columna de monto neto (monto a pagar) y la de bruto (monto)
                c_monto_neto = get_col_name(df, ['monto a pagar'])
                # Buscamos 'monto' de forma exacta para evitar que capture 'monto a pagar'
                c_monto_bruto = None
                for c in df.columns:
                    cn = normalize(str(c))
                    if cn == 'monto':
                        c_monto_bruto = c
                        break
                
                c_fecha = get_col_name(df, ['fecha'])
                c_folio = get_col_name(df, ['nÃºmero factura', 'factura'])
                
                if not c_id or not c_monto_neto: 
                    logger.warning(f"Faltan columnas de montos en Paris: c_id={c_id}, c_monto_neto={c_monto_neto}")
                    continue
                
                # Si no hay columna 'monto' separada, usamos monto neto como bruto (comisiÃ³n = 0)
                if not c_monto_bruto:
                    c_monto_bruto = c_monto_neto
                
                # Register unique sales into ventas_marketplace
                if c_tipo:
                    sales_mask = df[c_tipo].astype(str).str.lower().str.contains('pago normal', na=False)
                    if sales_mask.any() and c_ord:
                        df_v = df[sales_mask]
                        df_ventas = pd.DataFrame({
                            'order_id': df_v[c_ord].astype(str),
                            'sku': 'UNKNOWN',
                            'quantity': 1,
                            'unit_price': pd.to_numeric(df_v[c_monto_bruto], errors='coerce').fillna(0),
                            'gross_amount': pd.to_numeric(df_v[c_monto_bruto], errors='coerce').fillna(0),
                            'sale_date': pd.to_datetime(df_v[c_fecha], errors='coerce') if c_fecha else None,
                            'marketplace': 'PARIS', 'source_file': f.name
                        }).drop_duplicates(subset=['order_id'])
                        self.db.insert_df(self._filter_old_years(df_ventas[VENTAS_COLS], 'sale_date'), "ventas_marketplace", dedup_cols=['order_id'])

                ledger = []
                for idx, row in df.iterrows():
                    trans_id = str(row[c_id])
                    order_id = str(row[c_ord]) if c_ord else None
                    try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
                    except: fecha = None
                    detail = str(row[c_tipo]) if c_tipo else "Cobro/Pago Paris"
                    
                    monto_neto = float(pd.to_numeric(row[c_monto_neto], errors='coerce') or 0.0)
                    monto_bruto = float(pd.to_numeric(row[c_monto_bruto], errors='coerce') or 0.0)
                    comision = monto_neto - monto_bruto
                    
                    folio_val = row[c_folio] if c_folio else None
                    folio = str(int(float(folio_val))) if folio_val and pd.notna(folio_val) and str(folio_val).lower() != 'nan' and float(folio_val) > 0 else None
                    
                    tipo_mov = "PAGO" if "pago" in detail.lower() else "CARGO"
                    
                    # 1. Registro del Monto Bruto (Venta/Cargo)
                    ledger.append({
                        'marketplace': 'PARIS', 'id_transaccion': f"{trans_id}_GROSS",
                        'id_orden': order_id, 'fecha': fecha,
                        'detalle': detail, 'monto': monto_bruto,
                        'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
                        'folio_xml': folio
                    })
                    
                    # 2. Registro de la ComisiÃ³n (si existe diferencia)
                    if abs(comision) > 0.01:
                        ledger.append({
                            'marketplace': 'PARIS', 'id_transaccion': f"{trans_id}_COMM",
                            'id_orden': order_id, 'fecha': fecha,
                            'detalle': "Cargo por venta (Comisión)", 'monto': comision,
                            'tipo_movimiento': 'EGRESO_COMISION', 'archivo_origen': f.name,
                            'folio_xml': folio
                        })
                        
                if ledger:
                    df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                    df_ledger = self._filter_old_years(df_ledger)
                    self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    self._register_file(f.name, "ML", len(df_ledger))
            except Exception as e:
                logger.error(f"Error Paris {f.name}: {e}")

    def load_ripley(self):
        logger.info("Loading Ripley...")
        dir_ripley = ROOT / "01_Raw" / "RIPLEY"
        if not dir_ripley.exists():
            logger.warning("Ripley raw folder does not exist")
            return
        files = sorted(list(dir_ripley.glob("**/*.xlsx")), key=lambda x: x.name, reverse=True)
        
        mandatory_cols = ['Fecha OC', 'NÃºmero documento liquidaciÃ³n', 'Orden de compra', 'A pagar']
        for f in files:
            logger.info(f"Processing Ripley: {f.name}")
            try:
                df = read_excel_auto(f, mandatory_cols)
                if df is None: continue
                
                c_liq = get_col_name(df, ['NÃºmero documento liquidaciÃ³n', 'NUMERO DOCUMENTO LIQUIDACION'])
                c_ord = get_col_name(df, ['Orden de compra', 'orden compra'])
                c_fecha = get_col_name(df, ['Fecha OC', 'fecha'])
                c_total = get_col_name(df, ['A pagar'])
                c_gross = get_col_name(df, ['Importe del pedido'])
                
                if not c_ord or not c_total: continue
                
                # Register unique sales into ventas_marketplace
                if c_gross:
                    df_ventas = pd.DataFrame({
                        'order_id': df[c_ord].astype(str),
                        'sku': 'UNKNOWN',
                        'quantity': 1,
                        'unit_price': pd.to_numeric(df[c_gross], errors='coerce').fillna(0),
                        'gross_amount': pd.to_numeric(df[c_gross], errors='coerce').fillna(0),
                        'sale_date': pd.to_datetime(df[c_fecha], dayfirst=True, errors='coerce') if c_fecha else None,
                        'marketplace': 'RIPLEY', 'source_file': f.name
                    }).drop_duplicates(subset=['order_id'])
                    self.db.insert_df(self._filter_old_years(df_ventas[VENTAS_COLS], 'sale_date'), "ventas_marketplace", dedup_cols=['order_id'])

                value_vars = [c for c in df.columns if c not in [c_liq, c_ord, c_fecha, 'Shop ID', 'Tienda']]
                melted = df.melt(id_vars=[c_liq, c_ord, c_fecha], value_vars=value_vars, var_name='Detalle', value_name='Monto')
                
                melted = melted[melted['Monto'].notnull()]
                melted['Monto'] = pd.to_numeric(melted['Monto'], errors='coerce').fillna(0.0)
                melted = melted[melted['Monto'] != 0.0]
                
                ledger = []
                for idx, row in melted.iterrows():
                    order_id = str(row[c_ord])
                    liq_doc = str(row[c_liq])
                    detail = str(row['Detalle'])
                    monto = float(row['Monto'])
                    try: fecha = pd.to_datetime(row[c_fecha], dayfirst=True) if c_fecha else None
                    except: fecha = None
                    
                    trans_id = f"RIP_{liq_doc}_{order_id}_{normalize(detail)}"
                    tipo_mov = "PAGO" if "importe del pedido" in detail.lower() or "abono" in detail.lower() or "a pagar" in detail.lower() else "CARGO"
                    
                    ledger.append({
                        'marketplace': 'RIPLEY', 'id_transaccion': trans_id,
                        'id_orden': order_id, 'fecha': fecha,
                        'detalle': detail, 'monto': monto,
                        'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
                        'folio_xml': liq_doc
                    })
                if ledger:
                    df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                    df_ledger = self._filter_old_years(df_ledger)
                    self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    self._register_file(f.name, "ML", len(df_ledger))
            except Exception as e:
                logger.error(f"Error Ripley {f.name}: {e}")

        # PROCESAMIENTO DE CSV (Ciclos de facturaciÃ³n)
        dir_ciclos = dir_ripley / "CICLOS"
        
        if dir_ciclos and dir_ciclos.exists():
            csv_files = sorted(list(dir_ciclos.glob("*.csv")), key=lambda x: x.name, reverse=True)
            for f in csv_files:
                logger.info(f"Processing Ripley CSV: {f.name}")
                try:
                    df = pd.read_csv(f, encoding='utf-8', sep=';', engine='python')
                    
                    c_liq = get_col_name(df, ['numero de factura'])
                    c_ord = get_col_name(df, ['order number'])
                    c_fecha = get_col_name(df, ['date created'])
                    c_sku = get_col_name(df, ['product sku'])
                    c_qty = get_col_name(df, ['quantity'])
                    
                    c_sub = get_col_name(df, ['subtotal de articulos'])
                    c_total = get_col_name(df, ['precio total con impuestos'])
                    c_com = get_col_name(df, ['commission excluding taxes'])
                    c_imp = get_col_name(df, ['impuestos sobre la comision'])
                    c_trans = get_col_name(df, ['amount transferred to tienda'])
                    
                    if not c_ord: continue
                    
                    # Ventas Marketplace update (more granular)
                    if c_sku and c_qty and c_sub:
                        def parse_amt_series(s):
                            return pd.to_numeric(s.astype(str).str.replace(',', '.'), errors='coerce').fillna(0)

                        df_ventas = pd.DataFrame({
                            'order_id': df[c_ord].astype(str),
                            'sku': df[c_sku].astype(str),
                            'quantity': pd.to_numeric(df[c_qty], errors='coerce').fillna(1),
                            'unit_price': parse_amt_series(df[c_sub]),
                            'gross_amount': parse_amt_series(df[c_sub]),
                            'sale_date': pd.to_datetime(df[c_fecha], errors='coerce') if c_fecha else None,
                            'marketplace': 'RIPLEY', 'source_file': f.name
                        }).drop_duplicates(subset=['order_id', 'sku'])
                        
                        self.db.insert_df(self._filter_old_years(df_ventas[VENTAS_COLS], 'sale_date'), "ventas_marketplace", dedup_cols=['order_id', 'sku'])
                    
                    ledger = []
                    for idx, row in df.iterrows():
                        order_id = str(row[c_ord])
                        liq_doc = str(row[c_liq]) if c_liq and pd.notna(row[c_liq]) else None
                        try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
                        except: fecha = None
                        
                        def parse_amt(val):
                            if pd.isna(val): return 0.0
                            val_str = str(val).replace(',', '.')
                            return float(pd.to_numeric(val_str, errors='coerce') or 0.0)
                            
                        amts = {
                            'Subtotal': parse_amt(row[c_sub]) if c_sub else 0.0,
                            'Precio total': parse_amt(row[c_total]) if c_total else 0.0,
                            'ComisiÃ³n': parse_amt(row[c_com]) if c_com else 0.0,
                            'Impuestos': parse_amt(row[c_imp]) if c_imp else 0.0,
                            'Amount transferred to tienda': parse_amt(row[c_trans]) if c_trans else 0.0
                        }
                        
                        for detail, monto in amts.items():
                            if monto == 0.0: continue
                            trans_id = f"RIP_CSV_{liq_doc}_{order_id}_{idx}_{normalize(detail)}"
                            tipo_mov = "PAGO" if "Amount" in detail or "Subtotal" in detail or "Precio total" in detail else "CARGO"
                            
                            ledger.append({
                                'marketplace': 'RIPLEY', 'id_transaccion': trans_id,
                                'id_orden': order_id, 'fecha': fecha,
                                'detalle': detail, 'monto': monto,
                                'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
                                'folio_xml': liq_doc
                            })
                            
                    if ledger:
                        df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                        df_ledger = self._filter_old_years(df_ledger)
                        self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    self._register_file(f.name, "ML", len(df_ledger))
                except Exception as e:
                    logger.error(f"Error Ripley CSV {f.name}: {e}")

        # PROCESAMIENTO DE HISTORIAL DE TRANSACCIONES
        dir_historial = dir_ripley / "TH"
        if dir_historial.exists():
            hist_files = sorted(list(dir_historial.glob("*.csv")), key=lambda x: x.name, reverse=True)
            for f in hist_files:
                logger.info(f"Processing Ripley Transaction History CSV: {f.name}")
                try:
                    df = pd.read_csv(f, encoding='utf-8', sep=';', engine='python', on_bad_lines='skip')
                    
                    c_ord = get_col_name(df, ['numero de pedido', 'nÃºmero de pedido'])
                    c_liq = get_col_name(df, ['numero de factura', 'nÃºmero de factura'])
                    c_fecha = get_col_name(df, ['fecha de creaciÃ³n', 'fecha de creacion'])
                    c_tipo = get_col_name(df, ['tipo', 'type'])
                    c_detalle = get_col_name(df, ['descripcion', 'descripciÃ³n'])
                    c_importe = get_col_name(df, ['importe', 'amount'])
                    
                    if not c_tipo or not c_importe: continue
                    
                    ledger = []
                    for idx, row in df.iterrows():
                        order_id = str(row[c_ord]) if c_ord and pd.notna(row[c_ord]) else None
                        liq_doc = str(row[c_liq]) if c_liq and pd.notna(row[c_liq]) else None
                        
                        try: fecha = pd.to_datetime(row[c_fecha], dayfirst=True) if c_fecha else None
                        except: fecha = None
                        
                        detail = str(row[c_tipo]) if c_tipo else "Transaction"
                        
                        def parse_amt(val):
                            if pd.isna(val): return 0.0
                            val_str = str(val).replace(',', '.')
                            return float(pd.to_numeric(val_str, errors='coerce') or 0.0)
                            
                        monto = parse_amt(row[c_importe])
                        
                        if monto == 0.0: continue
                        
                        trans_id = f"RIP_TH_{idx}_{normalize(detail)}"
                        tipo_mov = "PAGO" if monto > 0 else "CARGO"
                        
                        ledger.append({
                            'marketplace': 'RIPLEY', 'id_transaccion': trans_id,
                            'id_orden': order_id, 'fecha': fecha,
                            'detalle': detail, 'monto': monto,
                            'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
                            'folio_xml': liq_doc
                        })
                        
                    if ledger:
                        df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                        df_ledger = self._filter_old_years(df_ledger)
                        self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    self._register_file(f.name, "ML", len(df_ledger))
                except Exception as e:
                    logger.error(f"Error Ripley Transaction History CSV {f.name}: {e}")

        # PROCESAMIENTO DE FULFILLMENT CSV
        dir_ff = dir_ripley / "FF"
        if dir_ff.exists():
            ff_files = sorted(list(dir_ff.glob("*.csv")), key=lambda x: x.name, reverse=True)
            for f in ff_files:
                logger.info(f"Processing Ripley FF CSV: {f.name}")
                try:
                    df = pd.read_csv(f, encoding='utf-8', sep=None, engine='python')
                    
                    c_ord = get_col_name(df, ['order_id', 'order id'])
                    c_fecha = get_col_name(df, ['date_created', 'date created', 'accounting_document_creation_date'])
                    
                    if not c_ord: continue
                    
                    ledger = []
                    
                    # Identificar columnas financieras (fees, amounts, descuentos, devoluciones, otros)
                    fin_cols = []
                    for c in df.columns:
                        cn = str(c).lower()
                        if 'amount' in cn or 'fee' in cn or 'descuento' in cn or 'devoluci' in cn or 'otros' in cn:
                            fin_cols.append(c)
                            
                    for idx, row in df.iterrows():
                        order_id = str(row[c_ord])
                        try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
                        except: fecha = None
                        
                        def parse_amt(val):
                            if pd.isna(val): return 0.0
                            val_str = str(val).replace(',', '.')
                            return float(pd.to_numeric(val_str, errors='coerce') or 0.0)
                            
                        for c in fin_cols:
                            monto = parse_amt(row[c])
                            if monto == 0.0: continue
                            
                            detail = str(c)
                            # Create a unique transaction ID for FF
                            trans_id = f"RIP_FF_{order_id}_{idx}_{normalize(detail)}"
                            
                            # Keep original signs. tipo_movimiento helps categorization but is not strictly evaluated algebraically in v4 if amounts already have signs.
                            # Standard: PAGO if positive or looks like transfer. CARGO if negative or fee. 
                            tipo_mov = "PAGO" if ("transfer" in cn or "amount" in cn) else "CARGO"
                            
                            ledger.append({
                                'marketplace': 'RIPLEY', 'id_transaccion': trans_id,
                                'id_orden': order_id, 'fecha': fecha,
                                'detalle': detail, 'monto': monto,
                                'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
                                'folio_xml': None # FF typically does not have folio_xml
                            })
                            
                    if ledger:
                        df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                        df_ledger = self._filter_old_years(df_ledger)
                        self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    self._register_file(f.name, "ML", len(df_ledger))
                except Exception as e:
                    logger.error(f"Error Ripley FF CSV {f.name}: {e}")

    def load_falabella(self):
        logger.info("Loading Falabella...")
        dir_falabella = ROOT / "01_Raw" / "FALABELLA"
        if not dir_falabella.exists():
            logger.warning("Falabella raw folder does not exist")
            return
        files = sorted(list(dir_falabella.glob("**/*.xlsx")) + list(dir_falabella.glob("**/*.csv")), key=lambda x: x.name, reverse=True)
        
        mandatory_cols = ['Fecha de Transaccion', 'N de orden', 'Tipo de Transaccion', 'Monto con IVA']
        for f in files:
            logger.info(f"Processing Falabella: {f.name}")
            try:
                df = read_excel_auto(f, mandatory_cols)
                if df is None: continue
                
                c_id = get_col_name(df, ['Falabella-Id', 'Falabella Id'])
                c_ord = get_col_name(df, ['N de orden', 'NÂº de orden', 'Nro de orden', 'NÂ° de orden'])
                c_fecha = get_col_name(df, ['Fecha de transacciÃ³n', 'Fecha de Transaccion', 'Fecha de transaccion', 'Fecha creaciÃ³n de la orden'])
                c_tipo = get_col_name(df, ['Tipo de Transaccion', 'Tipo de transacciÃ³n', 'Tipo de transaccion'])
                c_monto = get_col_name(df, ['Monto (Sin IVA)', 'Monto con IVA', 'Monto a transferir', 'Monto Total'])
                c_sku = get_col_name(df, ['SKU vendedor', 'sku'])
                c_folio = get_col_name(df, [' NÂ° Documento Tributario ', 'Documento Tributario'])
                
                if not c_ord or not c_monto: continue
                
                sales_mask = df[c_tipo].astype(str).str.lower().str.contains('precio del producto', na=False)
                if sales_mask.any():
                    df_v = df[sales_mask]
                    df_ventas = pd.DataFrame({
                        'order_id': df_v[c_ord].astype(str),
                        'sku': df_v[c_sku].astype(str) if c_sku else 'UNKNOWN',
                        'quantity': 1,
                        'unit_price': pd.to_numeric(df_v[c_monto], errors='coerce').fillna(0),
                        'gross_amount': pd.to_numeric(df_v[c_monto], errors='coerce').fillna(0),
                        'sale_date': pd.to_datetime(df_v[c_fecha], errors='coerce') if c_fecha else None,
                        'marketplace': 'FALABELLA', 'source_file': f.name
                    }).drop_duplicates(subset=['order_id'])
                    self.db.insert_df(self._filter_old_years(df_ventas[VENTAS_COLS], 'sale_date'), "ventas_marketplace", dedup_cols=['order_id'])
                
                ledger = []
                for idx, row in df.iterrows():
                    trans_id = str(row[c_id]) if c_id else f"FAL_{f.name}_{idx}"
                    order_id = str(row[c_ord])
                    try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
                    except: fecha = None
                    detail = str(row[c_tipo])
                    monto = float(pd.to_numeric(row[c_monto], errors='coerce') or 0.0)
                    
                    folio_val = row[c_folio] if c_folio else None
                    folio = str(int(float(folio_val))) if folio_val and pd.notna(folio_val) and str(folio_val).lower() != 'nan' and float(folio_val) > 0 else None
                    
                    tipo_mov = "PAGO" if "pago" in detail.lower() or "precio del producto" in detail.lower() else "CARGO"
                    
                    ledger.append({
                        'marketplace': 'FALABELLA', 'id_transaccion': trans_id,
                        'id_orden': order_id, 'fecha': fecha,
                        'detalle': detail, 'monto': monto,
                        'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
                        'folio_xml': folio
                    })
                if ledger:
                    df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                    df_ledger = self._filter_old_years(df_ledger)
                    self.db.insert_df(df_ledger, "marketplace_ledger_v1")
                    self._register_file(f.name, "FALABELLA", len(df_ledger))
            except Exception as e:
                logger.error(f"Error Falabella {f.name}: {e}")

    def load_file(self, file_path, marketplace="ML", execution_id=None):
        path = Path(file_path) if isinstance(file_path, str) else file_path
        files = [path]
        mp = (marketplace or "ML").upper()
        norm_name = normalize(path.name)
        if mp == "ML":
            if "poscobro" in norm_name:
                return self.load_poscobro(files=files, execution_id=execution_id)
            elif "liberac" in norm_name:
                return self.load_liberaciones(files=files, execution_id=execution_id)
            else:
                return self.load_facturacion(files=files, execution_id=execution_id)
        elif mp == "PARIS":
            return self.load_paris(files=files, execution_id=execution_id)
        elif mp == "RIPLEY":
            return self.load_ripley(files=files, execution_id=execution_id)
        elif mp == "FALABELLA":
            return self.load_falabella(files=files, execution_id=execution_id)
        return self.load_facturacion(files=files, execution_id=execution_id)

    def load_marketplace(self, marketplace):
        logger.info(f"Ingesting marketplace: {marketplace}")
        self.reset_db(marketplace)
        if marketplace == 'ML':
            self.load_facturacion()
            self.load_poscobro()
            self.load_liberaciones()
        elif marketplace == 'PARIS':
            self.load_paris()
        elif marketplace == 'RIPLEY':
            self.load_ripley()
        elif marketplace == 'FALABELLA':
            self.load_falabella()
        else:
            logger.error(f"Unsupported marketplace: {marketplace}")

    def run(self):
        self.load_marketplace("ML")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    SurgicalLoader().run()
