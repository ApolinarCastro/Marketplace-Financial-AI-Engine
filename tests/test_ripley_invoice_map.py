"""
LOOP_P0_RIPLEY_INVOICE_TO_SII_CLOSURE — Test 1: ripley_invoice_map_v1.
Validates that the controlled DB mapping table exists, contains all 52 settlement
invoices, and that every row is NO_DTE_FOUND (no invented fiscal links).
Read-only: only touches data/work/ripley_invoice_sii_controlled_*.db.
"""
import pytest
import duckdb
import glob
import os

CONTROLLED = os.path.join(
    r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine',
    'data', 'work', 'ripley_invoice_sii_controlled_20260806_155949.db'
)

@pytest.fixture(scope='module')
def controlled_db():
    assert os.path.exists(CONTROLLED), f"controlled DB missing: {CONTROLLED}"
    con = duckdb.connect(CONTROLLED, read_only=True)
    yield con
    con.close()

def test_map_table_exists(controlled_db):
    tables = [r[0] for r in controlled_db.execute("SHOW TABLES").fetchall()]
    assert 'ripley_invoice_map_v1' in tables

def test_map_has_52_invoices(controlled_db):
    n = controlled_db.execute("SELECT COUNT(*) FROM ripley_invoice_map_v1").fetchone()[0]
    assert n == 52, f"expected 52 settlement invoices, got {n}"

def test_all_rows_no_dte_found(controlled_db):
    bad = controlled_db.execute(
        "SELECT COUNT(*) FROM ripley_invoice_map_v1 WHERE match_status != 'NO_DTE_FOUND'"
    ).fetchone()[0]
    assert bad == 0, f"{bad} rows invented a DTE link"

def test_no_fabricated_folios(controlled_db):
    bad = controlled_db.execute(
        "SELECT COUNT(*) FROM ripley_invoice_map_v1 WHERE folio_sii IS NOT NULL"
    ).fetchone()[0]
    assert bad == 0, f"{bad} rows have a folio_sii assigned without evidence"

def test_map_covers_ledger_folios(controlled_db):
    invs = set(r[0] for r in controlled_db.execute("SELECT invoice_number FROM ripley_invoice_map_v1").fetchall())
    assert '596684' in invs and '602050' in invs
