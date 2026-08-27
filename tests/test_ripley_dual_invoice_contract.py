"""
LOOP_P0_RIPLEY_INVOICE_TO_SII_CLOSURE — Test 4: dual invoice contract.
Validates the COMMISSION_ONLY / COMMISSION_PLUS_SHIPPING / SHIPPING_ONLY_INVALID /
NO_DTE_FOUND / AMBIGUOUS_DTE_SET contract. Given the proven blocker (settlement
namespace disjoint from SII folios), no invoice can be classified as a dual DTE:
all are NO_DTE_FOUND.
"""
import csv
import os

MAP_CSV = os.path.join(
    r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine',
    'evidence', 'p0_ripley_invoice_sii', 'ripley_invoice_map.csv'
)

VALID_STATUSES = {
    'COMMISSION_ONLY',
    'COMMISSION_PLUS_SHIPPING',
    'SHIPPING_ONLY_INVALID',
    'NO_DTE_FOUND',
    'AMBIGUOUS_DTE_SET',
}


def _rows():
    with open(MAP_CSV, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def test_map_exists_and_has_52_rows():
    assert os.path.exists(MAP_CSV)
    assert len(_rows()) == 52


def test_statuses_within_contract():
    for r in _rows():
        assert r['match_status'] in VALID_STATUSES, r


def test_no_ambiguous_rows():
    amb = [r for r in _rows() if r['match_status'] == 'AMBIGUOUS_DTE_SET']
    assert amb == []


def test_no_false_fiscal_claims():
    # A dual/commission contract requires an SII folio anchor. With the proven
    # blocker, none exist — asserting NO_DTE_FOUND is the honest result.
    found = [r for r in _rows() if r['match_status'] == 'NO_DTE_FOUND']
    assert len(found) == 52


def test_evidence_field_present():
    for r in _rows():
        assert r.get('evidence') and len(r['evidence']) > 10
