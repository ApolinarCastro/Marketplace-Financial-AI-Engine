import os
import hashlib
from pathlib import Path
from datetime import datetime

import pandas as pd

from engine.loader import load_file, save_curated_parquet, get_pending_files, mark_file_processed
from engine.normalizer import normalize_dataframe, map_to_standard_columns
from engine.sap_importer import import_sap_file
from database.duckdb_manager import get_db


ROOT_DIR = Path(__file__).parent.parent


def detect_report_type(file_path: str, df: pd.DataFrame) -> str:
    """Detect report type from filename."""
    filename = os.path.basename(file_path).lower()
    
    if any(k in filename for k in ['billing', 'factura', 'invoice']):
        return 'BILLING'
    elif any(k in filename for k in ['settlement', 'liquidacion', 'pago']):
        return 'SETTLEMENT'
    elif any(k in filename for k in ['shipment', 'envio', 'shipping']):
        return 'SHIPMENT'
    elif any(k in filename for k in ['refund', 'reembolso', 'devolucion']):
        return 'REFUND'
    elif any(k in filename for k in ['fee', 'comision', 'cargo']):
        return 'FEE'
    
    return 'GENERAL'


def process_file_to_curated(file_path: str, marketplace: str, period: str, file_hash: str) -> pd.DataFrame:
    """Load, normalize, and map a file to standard columns."""
    df = load_file(file_path, marketplace)
    
    df = normalize_dataframe(df)
    
    df_mapped = map_to_standard_columns(df)
    
    report_type = detect_report_type(file_path, df_mapped)
    df_mapped['report_type'] = report_type
    
    _ = save_curated_parquet(df_mapped, marketplace, period, file_hash)
    
    return df_mapped


def _row_hash(file_hash: str, row: pd.Series) -> str:
    """Deterministic row hash: file hash + core values."""
    core_cols = [
        'marketplace', 'event_date', 'amount_signed', 'currency', 'order_id_mp',
        'shipment_id_mp', 'payment_id_mp', 'document_id_mp', 'detail_id_mp',
        'sku', 'item_id_mp', 'report_type', 'source_file'
    ]
    def _is_null_scalar(x) -> bool:
        if x is None:
            return True
        # pandas / numpy missing values
        try:
            if isinstance(x, float) and x != x:
                return True
        except Exception:
            pass
        return False

    parts = [file_hash]
    for c in core_cols:
        v = row.get(c)
        parts.append('' if _is_null_scalar(v) else str(v))
    return hashlib.sha256("|".join(parts).encode('utf-8')).hexdigest()


def build_master_ledger(incremental: bool = True):
    """
    Build master ledger from all curated parquet files.
    If incremental=True, only process new files.
    """
    db = get_db()
    
    curated_dir = ROOT_DIR / "02_Curated"
    if not curated_dir.exists():
        curated_dir.mkdir(parents=True, exist_ok=True)
        print("No curated files found.")
        return
    
    parquet_files = list(curated_dir.glob("*.parquet"))
    
    if not parquet_files:
        print("No parquet files in 02_Curated/")
        return
    
    existing_hashes: set[str] = set()
    if incremental:
        try:
            existing = db.df_query("SELECT hash FROM fact_ledger_movimientos WHERE hash IS NOT NULL")
            existing_hashes = set(existing['hash'].astype(str).tolist())
        except Exception:
            existing_hashes = set()

    all_records = []
    
    for pf in parquet_files:
        try:
            df = pd.read_parquet(pf)

            # SAP is imported into cur_sap_ov; keep it out of the marketplace ledger.
            if 'marketplace' in df.columns:
                mp0 = df['marketplace'].iloc[0]
                if mp0 is not None and str(mp0).upper() == 'SAP':
                    continue
            
            # Ensure required columns exist.
            for col in [
                'marketplace', 'event_date', 'amount_signed', 'currency', 'order_id_mp',
                'shipment_id_mp', 'payment_id_mp', 'document_id_mp', 'detail_id_mp',
                'sku', 'item_id_mp', 'report_type', 'source_file', 'load_timestamp', 'file_hash'
            ]:
                if col not in df.columns:
                    df[col] = None

            # event_type_std comes from classifier step; keep NULL here.
            if 'event_type_std' not in df.columns:
                df['event_type_std'] = None

            # Build ledger rows.
            for _, row in df.iterrows():
                file_hash = row.get('file_hash')
                if file_hash is None or (isinstance(file_hash, float) and file_hash != file_hash):
                    # Fallback to curated filename if file_hash not present.
                    file_hash = pf.stem

                h = _row_hash(str(file_hash), row)
                if incremental and h in existing_hashes:
                    continue

                all_records.append({
                    'marketplace': row.get('marketplace'),
                    'event_date': row.get('event_date'),
                    'event_type_std': row.get('event_type_std'),
                    'amount_signed': row.get('amount_signed'),
                    'currency': row.get('currency'),
                    'order_id_mp': row.get('order_id_mp'),
                    'shipment_id_mp': row.get('shipment_id_mp'),
                    'payment_id_mp': row.get('payment_id_mp'),
                    'document_id_mp': row.get('document_id_mp'),
                    'detail_id_mp': row.get('detail_id_mp'),
                    'sku': row.get('sku'),
                    'item_id_mp': row.get('item_id_mp'),
                    'report_type': row.get('report_type'),
                    'source_file': row.get('source_file'),
                    'load_timestamp': row.get('load_timestamp'),
                    'hash': h,
                })
            
        except Exception as e:
            print(f"Error processing {pf.name}: {e}")
    
    if all_records:
        ledger_df = pd.DataFrame(all_records)

        if not incremental:
            db.truncate_table('fact_ledger_movimientos')

        db.insert_from_dataframe(ledger_df, 'fact_ledger_movimientos', mode='append')
        print(f"Master ledger inserted: {len(ledger_df)} new rows")

        # Write full ledger output.
        full_ledger = db.df_query("SELECT * FROM fact_ledger_movimientos")
        output_path = ROOT_DIR / "03_Ledger" / "fact_ledger_movimientos.parquet"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        full_ledger.to_parquet(output_path, index=False)
        print(f"Ledger saved to {output_path}")
    else:
        print("No records to add to ledger.")


def load_pending_files():
    """Load and process pending files from registry."""
    db = get_db()
    
    pending = get_pending_files(db)
    
    if pending.empty:
        print("No pending files to process.")
        return
    
    processed_count = 0
    
    for _, row in pending.iterrows():
        try:
            file_path = str(row['file_path'])
            marketplace = str(row['marketplace']).upper()
            period = str(row['period'])
            file_hash = str(row['file_hash'])

            # Always curate to parquet for caching.
            _ = process_file_to_curated(file_path, marketplace, period, file_hash)

            # SAP also gets imported to cur_sap_ov.
            if marketplace == 'SAP':
                import_sap_file(file_path, file_hash)
            
            mark_file_processed(db, file_path, 'PROCESSED')
            processed_count += 1
            
            print(f"Processed: {file_path}")
            
        except Exception as e:
            print(f"Error processing {row['file_path']}: {e}")
            mark_file_processed(db, str(row['file_path']), 'ERROR')
    
    print(f"Processed {processed_count} files.")
    return processed_count
