"""
PARIS V2 Backfill — Add monto_bruto and comision_marketplace from source XLSX files
Surgical: only adds columns and backfills. Zero loader modification.
"""
import sys, os, logging
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("paris.backfill")
ROOT = Path("C:/Users/ASUS Zenbook/Documents/Marketplace Financial AI Engine")
DIR_PARIS = ROOT / "01_Raw" / "PARIS" / "Transacciones"

def normalize(text):
    if not isinstance(text, str): return ""
    import unicodedata, re
    t = unicodedata.normalize('NFD', text.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', t)

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
        return best_df
    return None

def find_gross_and_net_columns(df):
    """Find MONTO (gross) and MONTO_A_PAGAR (net) columns reliably.
    Returns (gross_col, net_col) or (None, None) if not found."""
    cols_norm = {c: normalize(str(c)) for c in df.columns}
    
    c_net = None
    c_gross = None
    
    for c, cn in cols_norm.items():
        if 'monto' in cn and 'pagar' in cn:
            c_net = c
        elif cn == 'monto' or (cn.startswith('monto') and 'pagar' not in cn 
                               and 'comision' not in cn and 'total' not in cn
                               and 'factura' not in cn):
            if c_gross is None:
                c_gross = c
    
    return c_gross, c_net

def backfill_paris():
    from engine.v4.database import DatabaseV4
    db = DatabaseV4.get()
    
    # Step 1: Add columns if not exist
    for col in ['monto_bruto', 'comision_marketplace']:
        try:
            db.execute(f"ALTER TABLE marketplace_ledger_v1 ADD COLUMN {col} DOUBLE")
            logger.info(f"Added column {col}")
        except Exception as e:
            logger.info(f"Column {col} already exists: {e}")
    
    # Step 2: Read source XLSX files
    files = sorted(list(DIR_PARIS.glob("**/*.xlsx")), key=lambda x: x.name, reverse=True)
    logger.info(f"Found {len(files)} PARIS source files")
    
    total_updated = 0
    
    for f in files:
        df = read_excel_auto(f, ['id', 'tipo', 'monto a pagar'])
        if df is None:
            continue
        
        c_id = None
        for c in df.columns:
            cn = normalize(str(c)) 
            if cn == 'id':
                c_id = c
                break
        
        c_gross, c_net = find_gross_and_net_columns(df)
        
        if not c_id or not c_net:
            logger.warning(f"Skipping {f.name}: missing id/net columns")
            continue
        
        if not c_gross:
            # No gross column — use net (commission=0, shouldn't happen for PARIS)
            c_gross = c_net
        
        logger.info(f"{f.name}: gross='{c_gross}', net='{c_net}', id='{c_id}'")
        
        batch = []
        for idx, row in df.iterrows():
            trans_id = str(row[c_id])
            try:
                gross = float(pd.to_numeric(row[c_gross], errors='coerce') or 0.0)
                net = float(pd.to_numeric(row[c_net], errors='coerce') or 0.0)
                commission = round(gross - net, 2)
                batch.append((gross, commission, trans_id))
            except:
                continue
        
        if not batch:
            continue
        
        # Batch UPDATE via DuckDB registered temp table (native, no parquet)
        df_batch = pd.DataFrame(batch, columns=['monto_bruto', 'comision_marketplace', 'id_transaccion'])
        temp_name = f"paris_batch_{os.getpid()}_{id(df_batch)}"
        
        try:
            with db.lock:
                db.conn.register(temp_name, df_batch)
                sql = f"""
                    UPDATE marketplace_ledger_v1 
                    SET monto_bruto = sub.monto_bruto,
                        comision_marketplace = sub.comision_marketplace
                    FROM {temp_name} sub
                    WHERE marketplace_ledger_v1.id_transaccion = sub.id_transaccion
                      AND marketplace_ledger_v1.marketplace = 'PARIS'
                      AND marketplace_ledger_v1.archivo_origen = ?
                """
                db.conn.execute(sql, [f.name])
                db.conn.unregister(temp_name)
            total_updated += len(batch)
            logger.info(f"  Updated {len(batch)} rows from {f.name}")
        except Exception as e:
            logger.error(f"Error for {f.name}: {e}")
            import traceback
            traceback.print_exc()
            # Cleanup
            try: db.conn.unregister(temp_name)
            except: pass
    
    # Verify
    result = db.query("""
        SELECT 
            COUNT(*) as total_rows,
            COUNT(monto_bruto) as rows_with_bruto,
            COUNT(comision_marketplace) as rows_with_comision,
            ROUND(SUM(monto_bruto), 2) as total_bruto,
            ROUND(SUM(monto), 2) as total_neto,
            ROUND(SUM(comision_marketplace), 2) as total_comision
        FROM marketplace_ledger_v1 WHERE marketplace = 'PARIS'
    """)
    logger.info(f"\n=== BACKFILL RESULT ===")
    logger.info(f"Rows with bruto: {result['rows_with_bruto'].iloc[0]} / {result['total_rows'].iloc[0]}")
    logger.info(f"Total MONTO (gross): ${result['total_bruto'].iloc[0]:,.2f}")
    logger.info(f"Total MONTO_A_PAGAR (net): ${result['total_neto'].iloc[0]:,.2f}")
    logger.info(f"Total Commission: ${result['total_comision'].iloc[0]:,.2f}")
    
    return result

if __name__ == "__main__":
    backfill_paris()
