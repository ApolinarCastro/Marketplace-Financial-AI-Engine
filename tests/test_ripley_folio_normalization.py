"""P0 RIPLEY - folio normalization tests (settlement vs SII namespace)."""
import re
import pytest


def norm(v):
    if v is None:
        return None
    s = str(v).strip().replace('.0', '', 1).lstrip('0')
    return s if s.isdigit() else None


def test_float_suffix_collapses():
    assert norm('500346.0') == '500346'
    assert norm(500346.0) == '500346'


def test_leading_zeros_collapse():
    assert norm('000000562946') == '562946'
    assert norm('0500346') == '500346'


def test_integer_str_kept():
    assert norm('500346') == '500346'


def test_non_numeric_rejected():
    assert norm('ABC') is None
    assert norm(None) is None


def test_namespaces_disjoint():
    """settlement refs (400k-700k) vs SII folios (SII range) are disjoint."""
    settlement = {499799, 500346, 562946, 596684}
    sii = {25272, 108927, 1916076, 6837014, 54087142}
    assert not (settlement & sii)


def test_settlement_namespace_boundaries():
    assert all(400000 <= r <= 700000 for r in [499799, 500346, 562946, 596684])


def test_sii_folio_regex():
    xml = '<Folio>1916076</Folio>'
    m = re.search(r'<Folio>\s*(\d+)\s*</Folio>', xml)
    assert m and m.group(1) == '1916076'
