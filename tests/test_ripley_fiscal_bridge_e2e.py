"""
LOOP_P0_RIPLEY_INVOICE_TO_SII_CLOSURE — Test 5: fiscal bridge E2E.
End-to-end validation that:
1. Settlement invoices (Número de factura) ARE the ledger folio_xml values.
2. The settlement namespace (500346-602050) is DISJOINT from the SII DTE folio
   namespace (108927-53395064) — no documentary bridge exists.
3. Therefore the fiscal bridge invoice->SII folio cannot be closed: verdict is
   PARTIAL_WITH_PROVEN_BLOCKER (internal chain certified, fiscal link absent).
"""
import csv
import json
import os

BASE = r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine'
EVID = os.path.join(BASE, 'evidence', 'p0_ripley_invoice_sii')


def _json(name):
    with open(os.path.join(EVID, name), encoding='utf-8') as f:
        return json.load(f)


def _csv_rows(name):
    with open(os.path.join(EVID, name), encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def test_evidence_files_present():
    required = ['key_intersections.json', 'matching_contract.json', 'ripley_invoice_map.csv',
                'transaction_logs_inventory.csv', 'referential_documents.csv',
                'dte_reference_extract.csv', 'sample_validation.json',
                'unmatched_results.csv', 'financial_integrity.json']
    for f in required:
        assert os.path.exists(os.path.join(EVID, f)), f"missing evidence: {f}"


def test_settlement_disjoint_from_sii():
    ki = _json('key_intersections.json')
    assert ki['seller_cap_dte_truth'] == []
    assert ki['seller_cap_xml'] == []
    assert ki['ledger_cap_dte_truth'] == []


def test_settlement_equals_ledger_folios():
    ki = _json('key_intersections.json')
    assert len(ki['seller_cap_ledger']) == ki['seller_invoice_set_size']
    assert ki['seller_invoice_set_size'] == 52


def test_xml_is_dte_truth_source():
    ki = _json('key_intersections.json')
    # all 407 dte_truth folios exist among the 472 XML element folios
    assert len(ki['xml_cap_dte_truth']) == ki['dte_truth_folio_set_size']


def test_contract_verdict():
    c = _json('matching_contract.json')
    assert c['verdict'] == 'PARTIAL_WITH_PROVEN_BLOCKER'
    assert 'disjoint' in c['blocker'].lower()


def test_invoice_map_all_unmatched():
    rows = _csv_rows('ripley_invoice_map.csv')
    assert all(r['match_status'] == 'NO_DTE_FOUND' for r in rows)


def test_financial_integrity_zero_delta():
    fi = _json('financial_integrity.json')
    assert fi['financial_delta'] == 0.0
    assert fi['official_tables_modified'] == 0
    assert fi['official_db_sha256'].startswith('311c78e2')
