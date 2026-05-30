import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

ROOT_DIR = Path(__file__).parent.parent


def get_file_hash(file_path: str) -> str:
    """Generate SHA256 hash for duplicate detection."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def detect_file_type(file_path: str) -> str:
    """Detect file type from extension."""
    ext = Path(file_path).suffix.lower()
    if ext == '.csv':
        return 'csv'
    elif ext in ['.xlsx', '.xls']:
        return 'excel'
    elif ext == '.parquet':
        return 'parquet'
    return 'unknown'


def load_file(file_path: str, marketplace: str = None) -> pd.DataFrame:
    """
    Load file and return pandas DataFrame with metadata.
    Supports: csv, xlsx, xls, parquet
    """
    file_type = detect_file_type(file_path)
    
    if file_type == 'csv':
        # Be permissive on encodings; keep deterministic content.
        try:
            df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, sep=None, engine='python', encoding='latin-1')
    elif file_type == 'excel':
        # xls support may require extra libs; keep a clear error.
        try:
            df = pd.read_excel(file_path, engine='openpyxl' if file_path.endswith('.xlsx') else None)
        except Exception:
            df = pd.read_excel(file_path)
    elif file_type == 'parquet':
        df = pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
    
    file_hash = get_file_hash(file_path)
    timestamp = datetime.now()
    
    df = df.copy()

    # Spec metadata columns
    df['marketplace'] = marketplace if marketplace else 'UNKNOWN'
    df['source_file'] = os.path.basename(file_path)
    df['load_timestamp'] = timestamp

    # Internal metadata used for incremental processing
    df['_file_hash'] = file_hash
    
    return df


def save_curated_parquet(df: pd.DataFrame, marketplace: str, period: str, file_hash: str) -> str:
    """Save curated parquet file to 02_Curated/"""
    curated_dir = ROOT_DIR / "02_Curated"
    curated_dir.mkdir(parents=True, exist_ok=True)
    
    safe_period = period.replace('/', '_')
    filename = f"{marketplace}_{safe_period}_{file_hash[:8]}.parquet"
    filepath = curated_dir / filename
    
    # Safety rule: don't overwrite curated files.
    if filepath.exists():
        return str(filepath)

    try:
        df.to_parquet(filepath, index=False, engine='pyarrow')
    except Exception as e:
        raise RuntimeError(
            "Failed to write parquet. Ensure 'pyarrow' is installed. "
            f"Original error: {e}"
        )
    return str(filepath)


def scan_raw_files(raw_dir: str = None) -> list:
    """
    Recursively scan 01_Raw/ for marketplace files.
    Returns list of file metadata dicts.
    """
    if raw_dir is None:
        raw_dir_path = ROOT_DIR / "01_Raw"
    else:
        raw_dir_path = Path(raw_dir)
    
    if not raw_dir_path.exists():
        return []
    
    files = []
    for root, dirs, filenames in os.walk(raw_dir_path):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, raw_dir_path)
            parts = relative_path.split(os.sep)
            
            if len(parts) < 3:
                continue
            
            marketplace = parts[0].upper()
            year = parts[1] if len(parts) > 1 else "0000"
            month = parts[2] if len(parts) > 2 else "00"
            period = f"{year}/{month}"
            
            file_ext = Path(filename).suffix.lower()
            if file_ext not in ['.csv', '.xlsx', '.xls', '.parquet']:
                continue
            
            file_hash = get_file_hash(full_path)
            
            files.append({
                'file_path': full_path,
                'file_name': filename,
                'marketplace': marketplace,
                'period': period,
                'file_hash': file_hash,
                'load_timestamp': datetime.now(),
                'status': 'PENDING'
            })
    
    return files


def get_registry_df(db) -> pd.DataFrame:
    """Get current file registry from DuckDB."""
    try:
        return db.df_query("SELECT * FROM stg_file_registry")
    except Exception:
        return pd.DataFrame(columns=['file_path', 'file_name', 'marketplace', 'period', 'file_hash', 'load_timestamp', 'status'])


def register_files(db, new_files: list):
    """Register new files in DuckDB registry."""
    if not new_files:
        return
    
    df = pd.DataFrame(new_files)
    df = df.drop(columns=['status'], errors='ignore')
    df['status'] = 'PENDING'
    
    existing = get_registry_df(db)
    if not existing.empty and 'file_hash' in existing.columns:
        existing_hashes = existing['file_hash'].dropna().astype(str).unique().tolist()
        df = df[~df['file_hash'].astype(str).isin(existing_hashes)]
    
    if not df.empty:
        db.insert_from_dataframe(df, 'stg_file_registry', mode='append')


def get_pending_files(db) -> pd.DataFrame:
    """Get files pending processing."""
    try:
        return db.df_query("SELECT * FROM stg_file_registry WHERE status = 'PENDING'")
    except Exception:
        return pd.DataFrame()


def mark_file_processed(db, file_path: str, status: str = 'PROCESSED'):
    """Update file status in registry."""
    db.execute(f"UPDATE stg_file_registry SET status = '{status}' WHERE file_path = ?", [file_path])
