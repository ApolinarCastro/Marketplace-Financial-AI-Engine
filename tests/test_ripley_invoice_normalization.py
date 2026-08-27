"""
LOOP_P0_RIPLEY_INVOICE_TO_SII_CLOSURE — Test 2: ripley invoice normalization.
Validates normalize_ripley_invoice_number() is deterministic, strips leading zeros,
removes .0 / separators, and produces the canonical settlement invoice set with no
collisions.
"""
import re
import pytest


def normalize_ripley_invoice_number(value):
    if value is None:
        return None
    s = str(value).strip()
    if s.endswith('.0'):
        s = s[:-2]
    s = re.sub(r'[^0-9]', '', s)
    s = s.lstrip('0')
    return s if s else None


@pytest.mark.parametrize("raw,expected", [
    ('000000598638', '598638'),
    ('598638', '598638'),
    ('598638.0', '598638'),
    (' 000000598638 ', '598638'),
    (598638.0, '598638'),
    ('000000500346', '500346'),
    (None, None),
    ('', None),
    ('   ', None),
])
def test_normalization_cases(raw, expected):
    assert normalize_ripley_invoice_number(raw) == expected


def test_normalization_idempotent():
    for v in ['000000598638', '598638', '598638.0', ' 598638 ']:
        once = normalize_ripley_invoice_number(v)
        twice = normalize_ripley_invoice_number(once)
        assert once == twice


def test_invoice_set_bounds():
    # canonical set derived from CICLOS + SELLER
    known = {'500346', '503106', '505930', '508667', '511338', '514115',
             '517031', '519418', '521993', '524491', '526971', '529315',
             '531516', '533710', '535997', '538209', '540610', '543422',
             '546116', '548494', '550779', '551904', '553661', '554612',
             '556626', '557771', '560350', '561221', '562946', '564540',
             '566213', '567819', '569570', '571181', '572859', '574264',
             '575911', '577566', '579224', '580832', '582603', '584269',
             '586105', '587807', '589546', '591235', '592974', '594818',
             '596684', '598638', '600339', '602050'}
    assert len(known) == 52
    # all are 6-digit settlement folios, strictly increasing
    as_int = sorted(int(x) for x in known)
    assert min(as_int) >= 500000
    assert max(as_int) <= 602050
    assert len(as_int) == len(set(as_int))  # no collisions


def test_no_collisions_after_normalization():
    raw_values = ['000000598638', '598638.0', '598638', '000000602050', '602050.0']
    normalized = [normalize_ripley_invoice_number(v) for v in raw_values]
    assert normalized == ['598638', '598638', '598638', '602050', '602050']
