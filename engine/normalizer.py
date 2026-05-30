import re
from dateutil import parser as date_parser

import pandas as pd


COLUMN_MAPPINGS = {
    'event_date': [
        'date', 'fecha', 'fecha_pago', 'fecha_operacion', 'transaction_date',
        'date_created', 'fecha_creacion', 'date_time', 'datetime', 'fechahora'
    ],
    'amount_signed': [
        'amount', 'monto', 'total', 'net_amount', 'payout', 'valor', 
        'importe', 'monto_neto', 'monto_bruto', 'monto_total', 'amount_total'
    ],
    'currency': [
        'currency', 'moneda', 'currency_code', 'codigo_moneda'
    ],
    'order_id_mp': [
        'order_id', 'id_orden', 'nro_orden', 'external_reference', 'order_reference',
        'orden_id', 'order_number', 'nro_pedido', 'pedido_id'
    ],
    'shipment_id_mp': [
        'shipment_id', 'id_envio', 'nro_envio', 'shipping_id', 'envio_id',
        'shipment_number', 'nro_shipment'
    ],
    'payment_id_mp': [
        'payment_id', 'id_pago', 'cust_id', 'payment_number', 'nro_pago',
        'transaccion_id', 'transaction_id'
    ],
    'document_id_mp': [
        'document_id', 'nro_boleta', 'nro_factura', 'document_number',
        'numero_documento', 'factura_id', 'boleta_id'
    ],
    'detail_id_mp': [
        'detail_id', 'id_detalle', 'detail_number', 'nro_detalle',
        'line_id', 'linea_id'
    ],
    'sku': [
        'sku', 'seller_custom_field', 'listing_id', 'product_sku',
        'codigo_producto', 'codigo', 'product_code', 'item_sku'
    ],
    'item_id_mp': [
        'item_id', 'id_item', 'product_id', 'item_number', 'nro_item',
        'product_reference', 'ref_producto'
    ],
    'concept_raw': [
        'concept', 'concepto', 'type', 'tipo', 'transaction_type',
        'event_type', 'tipo_operacion', 'operacion', 'description'
    ]
}


def normalize_column_name(col: str) -> str:
    """Normalize column name: trim, uppercase, replace spaces with underscore."""
    col = str(col).strip()
    col = col.upper()
    col = re.sub(r'[\s\-]+', '_', col)
    col = re.sub(r'[^A-Z0-9_]', '', col)
    return col


def detect_column_type(df: pd.DataFrame, col_name: str) -> str:
    """Detect column type: DATE, AMOUNT, ID, or STRING."""
    if col_name not in df.columns:
        return 'UNKNOWN'
    
    sample = df[col_name].dropna().head(100)
    if sample.empty:
        return 'STRING'
    
    sample_str = sample.astype(str)
    
    date_patterns = [
        r'^\d{4}-\d{2}-\d{2}',
        r'^\d{2}/\d{2}/\d{4}',
        r'^\d{2}-\d{2}-\d{4}',
        r'^\d{2}/\d{2}/\d{2,4}'
    ]
    if any(sample_str.str.match(p).any() for p in date_patterns):
        return 'DATE'
    
    amount_patterns = [
        r'^\d{1,3}(,\d{3})*(\.\d+)?$',
        r'^\d+(\.\d+)?$',
        r'^-?\d{1,3}(,\d{3})*(\.\d+)?$'
    ]
    if sample_str.str.replace('.', '', 1).str.replace(',', '').str.match(r'^-?\d+$').any():
        if df[col_name].dtype in ['float64', 'int64'] or col_name.lower() in ['amount', 'monto', 'total', 'valor']:
            return 'AMOUNT'
    
    id_patterns = ['order', 'id_', '_id', 'nro_', 'number']
    if any(p in col_name.lower() for p in id_patterns):
        return 'ID'
    
    return 'STRING'


def convert_date_column(series: pd.Series) -> pd.Series:
    """Safely convert to datetime."""
    def parse_date(val):
        if pd.isna(val):
            return None
        try:
            return pd.to_datetime(val)
        except:
            try:
                return date_parser.parse(str(val))
            except:
                return None
    
    return series.apply(parse_date)


def convert_amount_column(series: pd.Series) -> pd.Series:
    """Safely convert to numeric."""
    def parse_amount(val):
        if pd.isna(val):
            return None
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip()
        val_str = val_str.replace('.', '').replace(',', '.')
        try:
            return float(val_str)
        except:
            return None
    
    return series.apply(parse_amount)


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DataFrame columns and types.
    - Trim and uppercase column names
    - Detect and convert DATE/AMOUNT columns
    - Add standard metadata columns if not present
    """
    df = df.copy()

    # Keep loader metadata columns untouched.
    meta_cols = [c for c in df.columns if c in ['marketplace', 'source_file', 'load_timestamp', '_file_hash']]
    meta_df = df[meta_cols].copy() if meta_cols else pd.DataFrame(index=df.index)
    df_business = df.drop(columns=meta_cols, errors='ignore')

    original_columns = df_business.columns.tolist()
    new_columns = {col: normalize_column_name(col) for col in original_columns}
    df_business = df_business.rename(columns=new_columns)

    df = pd.concat([df_business, meta_df], axis=1)
    
    for col in df.columns:
        col_type = detect_column_type(df, col)
        
        if col_type == 'DATE':
            df[col] = convert_date_column(df[col])
        elif col_type == 'AMOUNT':
            df[col] = convert_amount_column(df[col])
    
    for meta_col in ['marketplace', 'source_file', 'load_timestamp', '_file_hash']:
        if meta_col not in df.columns:
            df[meta_col] = None
    
    return df


def map_to_standard_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map DataFrame columns to standard schema.
    Returns DataFrame with standardized columns (NULL if not found).
    """
    def find_best_column(aliases: list[str]) -> str | None:
        cols = list(df.columns)
        # Prefer exact normalized matches.
        for alias in aliases:
            alias_norm = normalize_column_name(alias)
            if alias_norm in cols:
                return alias_norm
        # Then token-ish matches.
        for alias in aliases:
            alias_norm = normalize_column_name(alias)
            for c in cols:
                if c == alias_norm:
                    return c
                if c.startswith(alias_norm + '_') or c.endswith('_' + alias_norm) or ('_' + alias_norm + '_') in ('_' + c + '_'):
                    return c
        return None

    result: dict[str, pd.Series] = {}

    for std_col, aliases in COLUMN_MAPPINGS.items():
        col = find_best_column(aliases)
        if col is None:
            result[std_col] = pd.Series([None] * len(df), index=df.index)
        else:
            result[std_col] = df[col]

    # Carry loader metadata
    for meta_col in ['marketplace', 'source_file', 'load_timestamp', '_file_hash']:
        if meta_col in df.columns:
            result[meta_col] = df[meta_col]
        else:
            result[meta_col] = pd.Series([None] * len(df), index=df.index)

    result_df = pd.DataFrame(result)

    # Dynamic fallbacks (no hard assumptions): if key fields are still all-null,
    # pick the first detected DATE/AMOUNT/ID-like column.
    if result_df['event_date'].isna().all():
        for c in df.columns:
            if c in ['marketplace', 'source_file', 'load_timestamp', '_file_hash']:
                continue
            if detect_column_type(df, c) == 'DATE':
                result_df['event_date'] = convert_date_column(df[c])
                break

    if result_df['amount_signed'].isna().all():
        for c in df.columns:
            if c in ['marketplace', 'source_file', 'load_timestamp', '_file_hash']:
                continue
            if detect_column_type(df, c) == 'AMOUNT':
                result_df['amount_signed'] = convert_amount_column(df[c])
                break

    if result_df['order_id_mp'].isna().all():
        for c in df.columns:
            cu = str(c).upper()
            if any(k in cu for k in ['ORDER', 'ORDEN', 'PEDIDO', 'NRO_ORDEN', 'ORDER_NUMBER']):
                result_df['order_id_mp'] = df[c].astype(str)
                result_df.loc[result_df['order_id_mp'].str.lower().isin(['nan', 'none', 'null', '']), 'order_id_mp'] = None
                break
    
    if 'event_date' in result_df.columns:
        result_df['event_date'] = convert_date_column(result_df['event_date'])
    
    if 'amount_signed' in result_df.columns:
        result_df['amount_signed'] = convert_amount_column(result_df['amount_signed'])

    # Normalize IDs as TEXT
    for id_col in ['order_id_mp', 'shipment_id_mp', 'payment_id_mp', 'document_id_mp', 'detail_id_mp', 'sku', 'item_id_mp']:
        if id_col in result_df.columns:
            result_df[id_col] = result_df[id_col].astype(str)
            result_df.loc[result_df[id_col].str.lower().isin(['nan', 'none', 'null']), id_col] = None

    # Expose file_hash as a simple column name downstream.
    result_df['file_hash'] = result_df['_file_hash']
    
    return result_df


def get_concept_column(df: pd.DataFrame) -> str | None:
    """Find concept/type column name."""
    candidates = ['concept', 'concepto', 'type', 'tipo', 'transaction_type', 'event_type', 'tipo_operacion']
    for col in df.columns:
        if col.lower() in candidates:
            return col
    for col in df.columns:
        if any(c in col.lower() for c in ['concept', 'tipo', 'type']):
            return col
    return None
