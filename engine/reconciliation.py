import pandas as pd
from pathlib import Path

from database.duckdb_manager import get_db


ROOT_DIR = Path(__file__).parent.parent


def reconcile_sap_vs_marketplace(tolerance_clp: float = 1.0) -> pd.DataFrame:
    """
    Reconcile SAP (cur_sap_ov) vs marketplaces (fact_ledger_movimientos).
    Match priority:
    1) payment_id_mp
    2) order_id_mp
    3) shipment_id_mp
    4) sku + date
    """
    db = get_db()

    mp = db.df_query(
        """
        SELECT *
        FROM fact_ledger_movimientos
        WHERE marketplace IS NOT NULL AND UPPER(marketplace) <> 'SAP'
        """
    )
    sap = db.df_query("SELECT * FROM cur_sap_ov")

    if mp.empty or sap.empty:
        out = pd.DataFrame(columns=[
            'sap_order_id', 'mp_order_id', 'sap_amount', 'mp_amount', 'difference', 'status'
        ])
        db.truncate_table('fact_conc_sap_vs_marketplace')
        if not out.empty:
            db.insert_from_dataframe(out, 'fact_conc_sap_vs_marketplace', mode='append')
        (ROOT_DIR / '04_Conciliaciones').mkdir(parents=True, exist_ok=True)
        out.to_parquet(ROOT_DIR / '04_Conciliaciones' / 'fact_conc_sap_vs_marketplace.parquet', index=False)
        return out

    mp = mp.copy()
    sap = sap.copy()

    # Normalize ids
    for c in ['order_id_mp', 'payment_id_mp', 'shipment_id_mp', 'sku']:
        if c in mp.columns:
            mp[c] = mp[c].astype(str).str.strip()
            mp.loc[mp[c].str.lower().isin(['nan', 'none', 'null', '']), c] = None
    sap['order_id'] = sap['order_id'].astype(str).str.strip() if 'order_id' in sap.columns else None
    if 'order_id' in sap.columns:
        sap.loc[sap['order_id'].str.lower().isin(['nan', 'none', 'null', '']), 'order_id'] = None

    mp['amount_signed'] = pd.to_numeric(mp.get('amount_signed'), errors='coerce')
    sap['amount_signed'] = pd.to_numeric(sap.get('amount_signed'), errors='coerce')

    # Optional SAP payment/shipment keys if present (dynamic RAW_* columns)
    sap_payment_col = None
    sap_shipment_col = None
    sap_sku_col = None
    for c in sap.columns:
        cu = str(c).upper()
        if sap_payment_col is None and ('PAYMENT' in cu or 'PAGO' in cu):
            sap_payment_col = c
        if sap_shipment_col is None and ('SHIP' in cu or 'ENVIO' in cu or 'DESPACH' in cu):
            sap_shipment_col = c
        if sap_sku_col is None and ('SKU' in cu or 'ITEM' in cu or 'ARTIC' in cu or 'PRODUCT' in cu):
            sap_sku_col = c

    if sap_payment_col:
        sap['payment_id'] = sap[sap_payment_col].astype(str).str.strip()
        sap.loc[sap['payment_id'].str.lower().isin(['nan', 'none', 'null', '']), 'payment_id'] = None
    else:
        sap['payment_id'] = None

    if sap_shipment_col:
        sap['shipment_id'] = sap[sap_shipment_col].astype(str).str.strip()
        sap.loc[sap['shipment_id'].str.lower().isin(['nan', 'none', 'null', '']), 'shipment_id'] = None
    else:
        sap['shipment_id'] = None

    if sap_sku_col:
        sap['sku'] = sap[sap_sku_col].astype(str).str.strip()
        sap.loc[sap['sku'].str.lower().isin(['nan', 'none', 'null', '']), 'sku'] = None
    else:
        sap['sku'] = None

    # Match engine
    results = []
    used_mp_idx = set()

    def _pick_first(df: pd.DataFrame) -> int | None:
        if df.empty:
            return None
        for i in df.index.tolist():
            if i not in used_mp_idx:
                return i
        return None

    for sidx, srow in sap.iterrows():
        sap_amt = srow.get('amount_signed')
        sap_order = srow.get('order_id')

        match_idx = None

        # 1) payment
        if srow.get('payment_id') is not None and 'payment_id_mp' in mp.columns:
            cand = mp[mp['payment_id_mp'] == srow.get('payment_id')]
            match_idx = _pick_first(cand)

        # 2) order
        if match_idx is None and sap_order is not None and 'order_id_mp' in mp.columns:
            cand = mp[mp['order_id_mp'] == sap_order]
            match_idx = _pick_first(cand)

        # 3) shipment
        if match_idx is None and srow.get('shipment_id') is not None and 'shipment_id_mp' in mp.columns:
            cand = mp[mp['shipment_id_mp'] == srow.get('shipment_id')]
            match_idx = _pick_first(cand)

        # 4) sku + date
        if match_idx is None and srow.get('sku') is not None and 'sku' in mp.columns and 'event_date' in mp.columns and 'event_date' in sap.columns:
            cand = mp[(mp['sku'] == srow.get('sku')) & (mp['event_date'] == srow.get('event_date'))]
            match_idx = _pick_first(cand)

        if match_idx is not None:
            used_mp_idx.add(match_idx)
            mrow = mp.loc[match_idx]
            mp_amt = mrow.get('amount_signed')
            diff = None
            if pd.notna(sap_amt) and pd.notna(mp_amt):
                diff = float(sap_amt) - float(mp_amt)

            status = 'NO_CONCILIADO'
            if diff is not None:
                status = 'CONCILIADO' if abs(diff) <= tolerance_clp else 'DIFERENCIA'

            results.append({
                'sap_order_id': sap_order,
                'mp_order_id': mrow.get('order_id_mp'),
                'sap_amount': sap_amt,
                'mp_amount': mp_amt,
                'difference': diff,
                'status': status,
            })
        else:
            results.append({
                'sap_order_id': sap_order,
                'mp_order_id': None,
                'sap_amount': sap_amt,
                'mp_amount': None,
                'difference': None,
                'status': 'NO_CONCILIADO',
            })

    # Unmatched MP rows
    unmatched_mp = mp.loc[[i for i in mp.index.tolist() if i not in used_mp_idx]]
    for _, mrow in unmatched_mp.iterrows():
        results.append({
            'sap_order_id': None,
            'mp_order_id': mrow.get('order_id_mp'),
            'sap_amount': None,
            'mp_amount': mrow.get('amount_signed'),
            'difference': None,
            'status': 'NO_CONCILIADO',
        })

    out = pd.DataFrame(results)

    db.truncate_table('fact_conc_sap_vs_marketplace')
    if not out.empty:
        db.insert_from_dataframe(out, 'fact_conc_sap_vs_marketplace', mode='append')

    (ROOT_DIR / '04_Conciliaciones').mkdir(parents=True, exist_ok=True)
    out.to_parquet(ROOT_DIR / '04_Conciliaciones' / 'fact_conc_sap_vs_marketplace.parquet', index=False)
    return out


def reconcile_cash_balance() -> pd.DataFrame:
    """Compute a simple cash balance timeline per marketplace."""
    db = get_db()
    ledger = db.df_query("SELECT * FROM fact_ledger_movimientos WHERE marketplace IS NOT NULL AND UPPER(marketplace) <> 'SAP'")
    if ledger.empty:
        out = pd.DataFrame(columns=['marketplace', 'event_date', 'event_type', 'amount_signed', 'currency', 'order_id_mp', 'balance_cumulative', 'status'])
        db.truncate_table('fact_conc_caja_total')
        (ROOT_DIR / '04_Conciliaciones').mkdir(parents=True, exist_ok=True)
        out.to_parquet(ROOT_DIR / '04_Conciliaciones' / 'fact_conc_caja_total.parquet', index=False)
        return out

    df = ledger.copy()
    df['amount_signed'] = pd.to_numeric(df.get('amount_signed'), errors='coerce').fillna(0.0)

    def _cat(x: object) -> str:
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return 'OTHER'
        s = str(x).upper()
        if 'PAGO' in s or 'PAY' in s or 'VENTA' in s or 'SALE' in s:
            return 'PAYMENT'
        if 'REEMBOL' in s or 'REFUND' in s or 'DEVOL' in s:
            return 'REFUND'
        if 'COMISI' in s or 'FEE' in s or 'COMMISSION' in s:
            return 'FEE'
        if 'RETIRO' in s or 'WITHDRAW' in s or 'TRANSFER' in s:
            return 'WITHDRAWAL'
        return 'OTHER'

    df['event_category'] = df.get('event_type_std').apply(_cat)
    df.loc[df['event_category'].isin(['REFUND', 'FEE', 'WITHDRAWAL']), 'amount_signed'] *= -1

    out_rows = []
    for mp in sorted(df['marketplace'].dropna().unique().tolist()):
        sub = df[df['marketplace'] == mp].copy()
        sub = sub.sort_values(['event_date', 'source_file'], na_position='last')
        bal = 0.0
        for _, r in sub.iterrows():
            bal += float(r['amount_signed'])
            out_rows.append({
                'marketplace': mp,
                'event_date': r.get('event_date'),
                'event_type': r.get('event_type_std'),
                'amount_signed': r.get('amount_signed'),
                'currency': r.get('currency'),
                'order_id_mp': r.get('order_id_mp'),
                'balance_cumulative': bal,
                'status': 'OK',
            })

    out = pd.DataFrame(out_rows)
    db.truncate_table('fact_conc_caja_total')
    if not out.empty:
        db.insert_from_dataframe(out, 'fact_conc_caja_total', mode='append')

    (ROOT_DIR / '04_Conciliaciones').mkdir(parents=True, exist_ok=True)
    out.to_parquet(ROOT_DIR / '04_Conciliaciones' / 'fact_conc_caja_total.parquet', index=False)
    return out
