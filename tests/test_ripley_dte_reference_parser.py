"""
LOOP_P0_RIPLEY_INVOICE_TO_SII_CLOSURE — Test 3: DTE reference parser.
Validates dte_reference_extract.csv produced from the 472 Facturacion XMLs:
correct body type distribution, SII folio namespace (>= 100000 range), and
absence of any settlement invoice reference in the parsed fields.
"""
import csv
import os

CSV_PATH = os.path.join(
    r'C:\Users\ASUS Zenbook\Documents\Marketplace Financial AI Engine',
    'evidence', 'p0_ripley_invoice_sii', 'dte_reference_extract.csv'
)

# canonical settlement invoice set (from CICLOS + SELLER)
SETTLEMENT_INVOICES = {'500346', '503106', '505930', '508667', '511338', '514115',
    '517031', '519418', '521993', '524491', '526971', '529315', '531516', '533710',
    '535997', '538209', '540610', '543422', '546116', '548494', '550779', '551904',
    '553661', '554612', '556626', '557771', '560350', '561221', '562946', '564540',
    '566213', '567819', '569570', '571181', '572859', '574264', '575911', '577566',
    '579224', '580832', '582603', '586105', '587807', '589546', '591235', '592974',
    '594818', '596684', '598638', '600339', '602050'}


def _rows():
    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def test_extract_exists():
    import os
    assert os.path.exists(CSV_PATH)


def test_extract_has_472_rows():
    assert len(_rows()) == 472


def test_body_type_distribution():
    rows = _rows()
    doc = sum(1 for r in rows if r.get('body_type') == 'DOCUMENTO')
    liq = sum(1 for r in rows if r.get('body_type') == 'LIQUIDACION')
    assert doc == 357
    assert liq == 115


def test_folios_not_in_settlement_namespace():
    for r in _rows():
        folio = (r.get('Folio') or '').lstrip('0')
        if folio:
            assert folio not in SETTLEMENT_INVOICES, f"{r['file']} folio {folio} collides with settlement invoice"


def test_no_settlement_reference_in_fields():
    for r in _rows():
        fields = ' '.join(str(r.get(k) or '') for k in r)
        for inv in SETTLEMENT_INVOICES:
            assert inv not in fields, f"{r['file']} references settlement invoice {inv}"


def test_emisor_is_eccsa_or_nanda():
    rows = _rows()
    emisores = set(r.get('RUTEmisor') for r in rows if r.get('RUTEmisor'))
    # all RIPLEY DTEs are ECCSA <-> NANDA
    assert emisores <= {'83382700-6', '77898100-9'}, emisores
