"""
ANTIGRAVITY v4.0 — Utils

Common helpers: file hashing, ID harmonization, numeric cleaning,
schema validation.
"""
import hashlib
import os
import re
import pandas as pd
from pathlib import Path


# ── File Hashing ──────────────────────────────────────────────────────────────

def file_hash(filepath: str | Path) -> str:
    """Fast hash: MD5 of (path + mtime + size). Suitable for change detection."""
    s = os.stat(filepath)
    return hashlib.md5(f"{filepath}{s.st_mtime}{s.st_size}".encode()).hexdigest()


# ── ID Harmonization ──────────────────────────────────────────────────────────

_SCIENTIFIC = re.compile(r"[eE]\+")

def harmonize_id(val) -> str | None:
    """
    Normalize marketplace / SAP order IDs:
    - Handles scientific notation (1.23e+15 → 1230000000000000)
    - Handles float-as-string ('2000007250003636.0' → '2000007250003636')
    - Pads short Meli IDs starting with '2' to 16 digits
    - Returns None for empty / NaN
    """
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None

    if isinstance(val, (int, float)):
        s = f"{val:.0f}"
    else:
        s = str(val).strip()
        if not s or s.lower() in ("nan", "none", "null", ""):
            return None
        if _SCIENTIFIC.search(s) or "." in s:
            try:
                s = f"{float(s):.0f}"
            except ValueError:
                s = s.split(".")[0]

    if not s or s.lower() in ("nan", "none"):
        return None

    # Meli-specific: IDs starting with '2', shorter than 16 chars → pad
    if 0 < len(s) < 16 and s.startswith("2") and s.isdigit():
        gap = 16 - len(s)
        s = s[0] + ("0" * gap) + s[1:]

    return s


def harmonize_series(series: pd.Series) -> pd.Series:
    """Apply harmonize_id to a full Series."""
    return series.apply(harmonize_id)


# ── Numeric Cleaning ──────────────────────────────────────────────────────────

def clean_amount(val) -> float:
    """
    Clean monetary amounts handling LatAm format:
    - '1.234,56'  → 1234.56
    - '1234,56'   → 1234.56
    - '1234.56'   → 1234.56
    - '-1.234,56' → -1234.56
    Returns 0.0 on error.
    """
    if val is None or (isinstance(val, float) and pd.isna(val)) or val == "":
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def clean_amount_cols(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Apply clean_amount to multiple columns."""
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_amount)
    return df


# ── Path Sanitization (Security) ─────────────────────────────────────────────

def sanitize_filename(name: str) -> str:
    """
    Remove directory traversal characters from filename.
    Only allows alphanumeric, dash, underscore, dot.
    """
    return re.sub(r"[^A-Za-z0-9._\-]", "_", Path(name).name)


# ── Schema Validation ─────────────────────────────────────────────────────────

def validate_required_columns(df: pd.DataFrame, required: list[str], source: str) -> list[str]:
    """
    Check that all required columns exist in df.
    Returns list of missing columns. Raises ValueError if any missing.
    """
    df_cols_upper = {c.strip().upper() for c in df.columns}
    missing = [c for c in required if c.upper() not in df_cols_upper]
    if missing:
        raise ValueError(
            f"[{source}] Missing required columns: {missing}. "
            f"Found: {list(df.columns)}"
        )
    return missing


# ── File Loading ──────────────────────────────────────────────────────────────

SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv", ".parquet"}


def load_file(filepath: str | Path, **kwargs) -> pd.DataFrame:
    """
    Load file with format detection. Supports xlsx/xls/csv/parquet.
    Always returns a DataFrame. Raises FileNotFoundError or ValueError.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {ext} ({filepath})")

    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path, dtype=str, engine="calamine", **kwargs)
    elif ext == ".csv":
        try:
            return pd.read_csv(path, dtype=str, encoding="utf-8", **kwargs)
        except UnicodeDecodeError:
            return pd.read_csv(path, dtype=str, encoding="latin-1", **kwargs)
    elif ext == ".parquet":
        return pd.read_parquet(path, **kwargs)
