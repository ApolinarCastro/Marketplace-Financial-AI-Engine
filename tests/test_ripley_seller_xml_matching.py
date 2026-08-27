"""P0 RIPLEY SELLER XML - matching tests (SETTLEMENT_CHAIN_V2)."""
import os, glob
import pandas as pd
import pytest

TMP = r'C:\Users\ASUS Zenbook\AppData\Local\Temp\opencode\ripley_ciclos'
SELLER_GLOB = r'01_Raw\RIPLEY\Fulfillment by Seller\*.xlsx'


def load_seller():
    orders = {}
    refs = set()
    rows = 0
    for f in glob.glob(SELLER_GLOB):
        df = pd.read_excel(f, dtype=str)
        cdoc = [c for c in df.columns if 'documento liquid' in c.lower()][0]
        coc = [c for c in df.columns if 'orden de compra' in c.lower()][0]
        for _, r in df.iterrows():
            ref = str(r[cdoc]).strip() if pd.notna(r[cdoc]) else ''
            oc = str(r[coc]).strip() if pd.notna(r[coc]) else ''
            rows += 1
            if oc:
                orders[oc] = ref
            if ref:
                s = ref.replace('.0', '', 1).lstrip('0')
                if s.isdigit():
                    refs.add(int(s))
    return orders, refs, rows


def load_ciclos():
    orders = {}
    inv = set()
    rows = 0
    for f in glob.glob(TMP + r'\*.csv'):
        df = pd.read_csv(f, delimiter=';', dtype=str)
        cinv = [c for c in df.columns if 'factura' in c.lower()]
        cord = [c for c in df.columns if 'order' in c.lower()]
        cinv = cinv[0] if cinv else None
        cord = cord[0] if cord else None
        for _, r in df.iterrows():
            oc = str(r[cord]).strip() if cord and pd.notna(r[cord]) else ''
            iv = str(r[cinv]).strip() if cinv and pd.notna(r[cinv]) else ''
            rows += 1
            if oc:
                orders[oc] = iv
            if iv:
                s = iv.replace('.0', '', 1).lstrip('0')
                if s.isdigit():
                    inv.add(int(s))
    return orders, inv, rows


@pytest.fixture(scope='module')
def seller_data():
    return load_seller()


@pytest.fixture(scope='module')
def ciclos_data():
    return load_ciclos()


def test_seller_files_exist():
    files = glob.glob(SELLER_GLOB)
    assert len(files) >= 50, f'expected >=50 SELLER files, got {len(files)}'


def test_ciclos_files_exist():
    files = glob.glob(TMP + r'\*.csv')
    assert len(files) >= 50, f'expected >=50 CICLOS csv, got {len(files)}'


def test_seller_order_ids_are_orders(seller_data):
    orders = seller_data[0]
    assert len(orders) >= 12000, f'expected >=12000 SELLER orders, got {len(orders)}'
    assert all(('-A' in o) for o in list(orders)[:100]), 'order id format mismatch'


def test_seller_settlement_refs_in_500k_range(seller_data):
    refs = seller_data[1]
    assert all(400000 <= r <= 700000 for r in refs), 'settlement refs outside namespace'


def test_ciclos_invoices_same_namespace(ciclos_data):
    inv = ciclos_data[1]
    assert all(400000 <= r <= 700000 for r in inv), 'ciclos invoices outside namespace'


def test_seller_ciclos_bridge(seller_data, ciclos_data):
    sorders = seller_data[0]
    corders = ciclos_data[0]
    inter = set(sorders) & set(corders)
    assert len(inter) >= 11000, f'expected >=11000 bridge, got {len(inter)}'


def test_seller_refs_subset_union_ciclos(seller_data, ciclos_data):
    srefs = seller_data[1]
    irefs = ciclos_data[1]
    assert srefs.issubset(irefs) or irefs.issubset(srefs) or (len(srefs & irefs) >= 40)


def test_no_fiscal_xml_in_settlement_namespace():
    """No dte_truth/XML folio lives in settlement range - the blocker."""
    import duckdb
    con = duckdb.connect(r'data\db\meli_financial_v4.db', read_only=True)
    n = con.execute("""
        SELECT COUNT(*) FROM dte_truth_v1
        WHERE marketplace='RIPLEY' AND TRY_CAST(folio AS BIGINT) BETWEEN 400000 AND 700000
    """).fetchone()[0]
    con.close()
    assert n == 0, f'expected 0 dte_truth folios in settlement range, got {n}'
