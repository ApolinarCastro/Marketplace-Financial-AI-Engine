import pandas as pd
from pathlib import Path
import logging
import warnings
import re

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
logger = logging.getLogger("surgical.loader")

ROOT = Path(r"C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine")
DIR_FACTURACION = ROOT / "01_Raw" / "ML" / "ML_Facturacion"
DIR_POSCOBRO = ROOT / "01_Raw" / "ML" / "Poscobro"

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
    ─────────────────────────
    Convención de signos: positivo = a favor del vendedor, negativo = costo/pérdida.

    Para "Cargo por venta":
      → INGRESO_VENTA  = +Total de la venta (lo que pagó el comprador)
      → EGRESO_COMISION = -Valor del cargo  (comisión que ML cobra)

    Para "Anulación del cargo por venta":
      → DEVOLUCION_VENTA  = -Total de la venta  (se pierde la venta)
      → REVERSA_COMISION  = -Valor del cargo     (Valor ya es negativo → -(-x) = +x, ML devuelve)

    Para todos los demás cargos:
      → CARGO = -Valor del cargo  (positivo en Excel = costo para vendedor)
      → Las anulaciones de envío/devolución tienen Valor negativo → -(-x) = +x = ajuste a favor
    """

    def __init__(self):
        from engine.v4.database import DatabaseV4
        self.db = DatabaseV4.get()

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

    def load_facturacion(self):
        logger.info("Loading ML_Facturacion...")
        files = sorted(list(DIR_FACTURACION.glob("*.xlsx")), key=lambda x: x.name, reverse=True)
        mandatory_cols = ['venta', 'factura', 'detalle', 'cargo', 'monto', 'fecha']

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

                # 1. Registro de Ventas únicas (tabla ventas_marketplace)
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

                # 2. Construir Ledger Atómico
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
                    
                    valor_cargo = float(pd.to_numeric(row[c_val_cargo], errors='coerce') or 0) if c_val_cargo else 0.0
                    total_venta = float(pd.to_numeric(row[c_tot_venta], errors='coerce') or 0) if c_tot_venta else 0.0

                    is_cargo_venta = "cargoporventa" in det_norm and "anulacion" not in det_norm
                    is_anulacion_venta = "anulacion" in det_norm and "cargoporventa" in det_norm

                    if is_cargo_venta:
                        # VENTA: ingreso bruto + comisión cobrada
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
                            'monto': -valor_cargo,  # valor_cargo=5199 → monto=-5199 (costo)
                            'tipo_movimiento': 'EGRESO_COMISION',
                            'archivo_origen': f.name, 'folio_xml': folio
                        })

                    elif is_anulacion_venta:
                        # DEVOLUCIÓN: se pierde la venta + ML devuelve comisión
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
                            'detalle': "Anulación del cargo por venta",
                            'monto': -valor_cargo,  # valor_cargo=-5199 → monto=+5199 (ML devuelve)
                            'tipo_movimiento': 'AJUSTE',
                            'archivo_origen': f.name, 'folio_xml': folio
                        })

                    else:
                        # TODOS LOS DEMÁS CARGOS: envíos, publicidad, fullfilment, etc.
                        # -valor_cargo: si cargo=3420 → monto=-3420 (costo)
                        # si es anulación de envío: cargo=-3420 → monto=+3420 (ML devuelve)
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
                    df_ledger = self._filter_old_years(df_ledger)
                    self.db.insert_df(df_ledger, "marketplace_ledger_v1")

            except Exception as e:
                logger.error(f"Error {f.name}: {e}")

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
                    try: fecha = pd.to_datetime(row[c_dat]) if c_dat else None
                    except: fecha = None
                    
                    # Prevent 'nan' and get a valid detail string
                    raw_det = str(row[c_det]).strip() if c_det and pd.notna(row[c_det]) else ""
                    raw_stat = str(row[c_stat]).strip() if c_stat and pd.notna(row[c_stat]) else ""
                    
                    if raw_det and raw_det.lower() != "nan":
                        final_det = raw_det
                    elif raw_stat and raw_stat.lower() != "nan":
                        final_det = raw_stat
                    else:
                        final_det = "Ajuste Poscobro"

                    # Generar id_transaccion único robusto
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
                    # Deduplicar por (operation_id, detalle) — el Excel fuente tiene filas repetidas
                    df_ledger['_op_id'] = df_ledger['id_transaccion'].str.extract(r'POS_(\d+)_', expand=False)
                    antes = len(df_ledger)
                    df_ledger = df_ledger.drop_duplicates(subset=['_op_id', 'detalle', 'monto', 'fecha'])
                    despues = len(df_ledger)
                    if antes != despues:
                        logger.info(f"Poscobro dedup: {antes} → {despues} filas ({antes - despues} duplicados eliminados)")
                    df_ledger = df_ledger.drop(columns=['_op_id'])
                    self.db.insert_df(df_ledger, "marketplace_ledger_v1")
            except Exception as e:
                logger.error(f"Error Poscobro {f.name}: {e}")

    def load_paris(self):
        logger.info("Loading Paris...")
        dir_paris = ROOT / "01_Raw" / "PARIS" / "Transacciones"
        if not dir_paris.exists():
            logger.warning("Paris raw folder does not exist")
            return
        files = sorted(list(dir_paris.glob("**/*.xlsx")), key=lambda x: x.name, reverse=True)
        
        mandatory_cols = ['id', 'tipo', 'número orden', 'monto a pagar']
        for f in files:
            logger.info(f"Processing Paris: {f.name}")
            try:
                df = read_excel_auto(f, mandatory_cols)
                if df is None: continue
                
                c_id = get_col_name(df, ['id'])
                c_tipo = get_col_name(df, ['tipo', 'descripción'])
                c_ord = get_col_name(df, ['número orden', 'nro orden'])
                c_monto = get_col_name(df, ['monto a pagar', 'monto'])
                c_fecha = get_col_name(df, ['fecha'])
                c_folio = get_col_name(df, ['número factura', 'factura'])
                
                if not c_id or not c_monto: continue
                
                # Register unique sales into ventas_marketplace
                if c_tipo:
                    sales_mask = df[c_tipo].astype(str).str.lower().str.contains('pago normal', na=False)
                    if sales_mask.any() and c_ord:
                        df_v = df[sales_mask]
                        df_ventas = pd.DataFrame({
                            'order_id': df_v[c_ord].astype(str),
                            'sku': 'UNKNOWN',
                            'quantity': 1,
                            'unit_price': pd.to_numeric(df_v[c_monto], errors='coerce').fillna(0),
                            'gross_amount': pd.to_numeric(df_v[c_monto], errors='coerce').fillna(0),
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
                    monto = float(pd.to_numeric(row[c_monto], errors='coerce') or 0.0)
                    folio = str(row[c_folio]) if c_folio and pd.notna(row[c_folio]) and str(row[c_folio]).lower() != 'nan' else None
                    
                    tipo_mov = "PAGO" if "pago" in detail.lower() else "CARGO"
                    
                    ledger.append({
                        'marketplace': 'PARIS', 'id_transaccion': trans_id,
                        'id_orden': order_id, 'fecha': fecha,
                        'detalle': detail, 'monto': monto,
                        'tipo_movimiento': tipo_mov, 'archivo_origen': f.name,
                        'folio_xml': folio
                    })
                if ledger:
                    df_ledger = pd.DataFrame(ledger)[LEDGER_COLS]
                    df_ledger = self._filter_old_years(df_ledger)
                    self.db.insert_df(df_ledger, "marketplace_ledger_v1")
            except Exception as e:
                logger.error(f"Error Paris {f.name}: {e}")

    def load_ripley(self):
        logger.info("Loading Ripley...")
        dir_ripley = ROOT / "01_Raw" / "RIPLEY"
        if not dir_ripley.exists():
            logger.warning("Ripley raw folder does not exist")
            return
        files = sorted(list(dir_ripley.glob("**/*.xlsx")), key=lambda x: x.name, reverse=True)
        
        mandatory_cols = ['Fecha OC', 'Número documento liquidación', 'Orden de compra', 'A pagar']
        for f in files:
            logger.info(f"Processing Ripley: {f.name}")
            try:
                df = read_excel_auto(f, mandatory_cols)
                if df is None: continue
                
                c_liq = get_col_name(df, ['Número documento liquidación', 'NUMERO DOCUMENTO LIQUIDACION'])
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
                        'sale_date': pd.to_datetime(df[c_fecha], errors='coerce') if c_fecha else None,
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
                    try: fecha = pd.to_datetime(row[c_fecha]) if c_fecha else None
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
            except Exception as e:
                logger.error(f"Error Ripley {f.name}: {e}")

    def load_falabella(self):
        logger.info("Loading Falabella...")
        dir_falabella = ROOT / "01_Raw" / "FALABELLA"
        if not dir_falabella.exists():
            logger.warning("Falabella raw folder does not exist")
            return
        files = sorted(list(dir_falabella.glob("**/*.xlsx")), key=lambda x: x.name, reverse=True)
        
        mandatory_cols = ['Fecha de Transaccion', 'N de orden', 'Tipo de Transaccion', 'Monto con IVA']
        for f in files:
            logger.info(f"Processing Falabella: {f.name}")
            try:
                df = read_excel_auto(f, mandatory_cols)
                if df is None: continue
                
                c_id = get_col_name(df, ['Falabella-Id', 'Falabella Id'])
                c_ord = get_col_name(df, ['N de orden', 'Nº de orden', 'Nro de orden', 'N° de orden'])
                c_fecha = get_col_name(df, ['Fecha de transacción', 'Fecha de Transaccion', 'Fecha de transaccion', 'Fecha creación de la orden'])
                c_tipo = get_col_name(df, ['Tipo de Transaccion', 'Tipo de transacción', 'Tipo de transaccion'])
                c_monto = get_col_name(df, ['Monto (Sin IVA)', 'Monto con IVA', 'Monto a transferir', 'Monto Total'])
                c_sku = get_col_name(df, ['SKU vendedor', 'sku'])
                c_folio = get_col_name(df, [' N° Documento Tributario ', 'Documento Tributario'])
                
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
            except Exception as e:
                logger.error(f"Error Falabella {f.name}: {e}")

    def load_marketplace(self, marketplace):
        logger.info(f"Ingesting marketplace: {marketplace}")
        self.reset_db(marketplace)
        if marketplace == 'ML':
            self.load_facturacion()
            self.load_poscobro()
        elif marketplace == 'PARIS':
            self.load_paris()
        elif marketplace == 'RIPLEY':
            self.load_ripley()
        elif marketplace == 'FALABELLA':
            self.load_falabella()
        else:
            logger.error(f"Unsupported marketplace: {marketplace}")

    def run(self):
        from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
        self.load_marketplace('ML')
        logger.info("Running classification and audit...")
        auditor = MarketplaceAuditorEngine()
        auditor.run_classification()
        auditor.run_audit()
        res = auditor.run_financial_closing('ML', '2025-12-01', '2025-12-31')
        logger.info(f"CLOSED DEC 2025: Net Result = {res['neto']}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    SurgicalLoader().run()
