import pandas as pd
from datetime import datetime
from database.duckdb_manager import get_db

TOLERANCE_CLP = 1.0

EXCEPTION_SEVERITY = {
    'SIN_LLAVE': 'ERROR',
    'DUPLICADO': 'ERROR',
    'DIFERENCIA_MONTO': 'ERROR',
    'POR_CLASIFICAR': 'WARNING',
}


def detect_exceptions() -> pd.DataFrame:
    """
    Detect exceptions in ledger data.
    Rules:
    - missing keys -> SIN_LLAVE
    - difference > tolerance -> DIFERENCIA_MONTO
    - duplicate hash -> DUPLICADO
    - unknown concept -> POR_CLASIFICAR
    """
    db = get_db()
    
    try:
        ledger = db.df_query("SELECT * FROM fact_ledger_movimientos")
    except Exception:
        return pd.DataFrame()
    
    if ledger.empty:
        return pd.DataFrame()
    
    exceptions = []
    
    key_columns = ['order_id_mp', 'payment_id_mp', 'shipment_id_mp', 'document_id_mp']
    
    ledger['has_key'] = False
    for col in key_columns:
        ledger['has_key'] = ledger['has_key'] | (
            ledger[col].notna() & 
            (ledger[col].astype(str).str.strip() != '') &
            (ledger[col].astype(str).str.lower() != 'none') &
            (ledger[col].astype(str).str.lower() != 'nan')
        )
    
    missing_keys = ledger[~ledger['has_key']]
    for _, row in missing_keys.iterrows():
        cause = 'SIN_LLAVE'
        exceptions.append({
            'marketplace': row.get('marketplace'),
            'event_date': row.get('event_date'),
            'amount': row.get('amount_signed'),
            'order_id': row.get('order_id_mp'),
            'cause_std': cause,
            'severity': EXCEPTION_SEVERITY.get(cause, 'ERROR'),
            'hash': row.get('hash'),
            'load_timestamp': datetime.now()
        })
    
    if 'hash' in ledger.columns:
        duplicates = ledger[ledger.duplicated(subset=['hash'], keep=False)]
        seen_hashes = set()
        for _, row in duplicates.iterrows():
            h = row.get('hash')
            if h and h in seen_hashes:
                cause = 'DUPLICADO'
                exceptions.append({
                    'marketplace': row.get('marketplace'),
                    'event_date': row.get('event_date'),
                    'amount': row.get('amount_signed'),
                    'order_id': row.get('order_id_mp'),
                    'cause_std': cause,
                    'severity': EXCEPTION_SEVERITY.get(cause, 'ERROR'),
                    'hash': h,
                    'load_timestamp': datetime.now()
                })
            seen_hashes.add(h)
    
    unclassified = ledger[
        ledger['event_type_std'].isna() | 
        (ledger['event_type_std'] == '') |
        (ledger['event_type_std'].astype(str).str.upper() == 'NO_CLASIFICADO')
    ]
    for _, row in unclassified.iterrows():
        cause = 'POR_CLASIFICAR'
        exceptions.append({
            'marketplace': row.get('marketplace'),
            'event_date': row.get('event_date'),
            'amount': row.get('amount_signed'),
            'order_id': row.get('order_id_mp'),
            'cause_std': cause,
            'severity': EXCEPTION_SEVERITY.get(cause, 'WARNING'),
            'hash': row.get('hash'),
            'load_timestamp': datetime.now()
        })
    
    exc_df = pd.DataFrame(exceptions)
    
    if not exc_df.empty:
        exc_df = exc_df.drop_duplicates()
        
        db.truncate_table('fact_excepciones')
        db.insert_from_dataframe(exc_df, 'fact_excepciones', mode='append')
        
        import os
        os.makedirs('05_Excepciones', exist_ok=True)
        output_path = '05_Excepciones/fact_excepciones.parquet'
        exc_df.to_parquet(output_path, index=False)
        print(f"Exceptions detected: {len(exc_df)} records")
    
    return exc_df


def reconcile_and_detect_differences(tolerance: float = TOLERANCE_CLP) -> pd.DataFrame:
    """Detect amount differences in reconciliation."""
    db = get_db()
    
    try:
        conc = db.df_query("SELECT * FROM fact_conc_sap_vs_marketplace")
    except Exception:
        return pd.DataFrame()
    
    if conc.empty:
        return pd.DataFrame()
    
    diff_records = conc[conc['status'] == 'DIFERENCIA']
    
    exceptions = []
    for _, row in diff_records.iterrows():
        cause = 'DIFERENCIA_MONTO'
        exceptions.append({
            'marketplace': 'SAP',
            'event_date': None,
            'amount': row.get('difference'),
            'order_id': row.get('mp_order_id') or row.get('sap_order_id'),
            'cause_std': cause,
            'severity': EXCEPTION_SEVERITY.get(cause, 'ERROR'),
            'hash': None,
            'load_timestamp': datetime.now()
        })
    
    if exceptions:
        exc_df = pd.DataFrame(exceptions)
        
        existing = db.df_query("SELECT * FROM fact_excepciones")
        if not existing.empty:
            combined = pd.concat([existing, exc_df], ignore_index=True)
        else:
            combined = exc_df
        
        combined = combined.drop_duplicates()
        
        db.truncate_table('fact_excepciones')
        db.insert_from_dataframe(combined, 'fact_excepciones', mode='append')
        
        import os
        os.makedirs('05_Excepciones', exist_ok=True)
        output_path = '05_Excepciones/fact_excepciones.parquet'
        combined.to_parquet(output_path, index=False)
        print(f"Updated exceptions with differences: {len(exceptions)} records")
    
    return pd.DataFrame(exceptions)
