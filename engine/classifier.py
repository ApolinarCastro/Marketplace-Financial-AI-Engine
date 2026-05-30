import hashlib
from pathlib import Path

import pandas as pd

from database.duckdb_manager import get_db


ROOT_DIR = Path(__file__).parent.parent


def _row_hash(file_hash: str, row: pd.Series) -> str:
    core_cols = [
        'marketplace', 'event_date', 'amount_signed', 'currency', 'order_id_mp',
        'shipment_id_mp', 'payment_id_mp', 'document_id_mp', 'detail_id_mp',
        'sku', 'item_id_mp', 'report_type', 'source_file'
    ]
    parts = [file_hash]
    for c in core_cols:
        v = row.get(c)
        parts.append('' if pd.isna(v) else str(v))
    return hashlib.sha256("|".join(parts).encode('utf-8')).hexdigest()


def _load_mapping() -> pd.DataFrame:
    mapping_path = ROOT_DIR / "00_Config" / "dim_mapping_conceptos.xlsx"
    if not mapping_path.exists():
        return pd.DataFrame(columns=['concept_raw', 'event_type_std', 'cuenta_contable', 'centro_costo'])
    df = pd.read_excel(mapping_path)
    # Normalize headers
    df.columns = [str(c).strip() for c in df.columns]
    # Normalize concept key
    if 'concept_raw' in df.columns:
        df['concept_raw'] = df['concept_raw'].astype(str).str.strip()
    return df


def classify_concepts_from_curated() -> pd.DataFrame:
    """Classify concepts from curated parquet files and update ledger event_type_std."""
    curated_dir = ROOT_DIR / "02_Curated"
    proposals_dir = ROOT_DIR / "06_IA_Propuestas"
    proposals_dir.mkdir(parents=True, exist_ok=True)

    mapping = _load_mapping()
    if mapping.empty or 'concept_raw' not in mapping.columns or 'event_type_std' not in mapping.columns:
        # Nothing to apply.
        return pd.DataFrame()

    parquet_files = list(curated_dir.glob("*.parquet"))
    if not parquet_files:
        return pd.DataFrame()

    mapping_small = mapping[['concept_raw', 'event_type_std']].dropna().copy()
    mapping_small['concept_raw'] = mapping_small['concept_raw'].astype(str).str.strip()
    map_dict = dict(zip(mapping_small['concept_raw'], mapping_small['event_type_std']))

    updates = []
    unknown_concepts = []

    for pf in parquet_files:
        df = pd.read_parquet(pf)
        if 'concept_raw' not in df.columns:
            continue
        if 'file_hash' not in df.columns:
            continue

        concept_series = df['concept_raw'].astype(str).str.strip()
        event_type = concept_series.map(map_dict)

        # Unknown concepts
        unknown_mask = event_type.isna() & concept_series.notna() & (concept_series != '') & (concept_series.str.lower() != 'nan')
        if unknown_mask.any():
            unknown_concepts.append(
                pd.DataFrame({
                    'concept_raw': concept_series[unknown_mask],
                    'source_file': df.get('source_file', pd.Series([pf.name] * len(df)))[unknown_mask],
                    'marketplace': df.get('marketplace', pd.Series([None] * len(df)))[unknown_mask],
                })
            )

        for idx, row in df.iterrows():
            fh = row.get('file_hash')
            if pd.isna(fh):
                continue
            h = _row_hash(str(fh), row)
            et = event_type.iloc[idx] if idx in event_type.index else None
            if pd.isna(et):
                continue
            updates.append({'hash': h, 'event_type_std': et})

    if unknown_concepts:
        unknown_df = pd.concat(unknown_concepts, ignore_index=True)
        unknown_df = unknown_df.drop_duplicates(subset=['concept_raw'])
        out_path = proposals_dir / "conceptos_no_clasificados.parquet"
        # Safety: don't overwrite. If exists, append by union.
        if out_path.exists():
            existing = pd.read_parquet(out_path)
            unknown_df = pd.concat([existing, unknown_df], ignore_index=True).drop_duplicates(subset=['concept_raw'])
        unknown_df.to_parquet(out_path, index=False)

    if not updates:
        return pd.DataFrame()

    upd_df = pd.DataFrame(updates).drop_duplicates(subset=['hash'])

    db = get_db()
    db.conn.register("_tmp_cls", upd_df)
    db.conn.execute(
        """
        UPDATE fact_ledger_movimientos AS l
        SET event_type_std = c.event_type_std
        FROM _tmp_cls AS c
        WHERE l.hash = c.hash
        """
    )
    db.conn.unregister("_tmp_cls")

    return upd_df
