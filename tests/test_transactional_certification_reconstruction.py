import pytest
from engine.v4.certification.transaction_certification_service import TransactionCertificationService
from engine.v4.certification.transaction_certification_result_v3 import PipelineStage
from engine.v4.database import DatabaseV4

def test_no_xml_pipeline_not_run():
    svc = TransactionCertificationService()
    # pick Falabella without XML
    db = DatabaseV4.get()
    df = db.query("SELECT id_transaccion FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA' AND (folio_xml IS NULL OR folio_xml='None' OR folio_xml='') LIMIT 1")
    assert not df.empty
    tx = df.iloc[0]["id_transaccion"]
    res = svc.certify(tx)
    assert res.xml_status.value == "XML_NOT_LINKED"
    assert res.pipeline["xml"] == "NOT_RUN"
    assert res.pipeline["xsd"] == "NOT_RUN"
    assert res.pipeline["sig"] == "NOT_RUN"
    assert res.pipeline["caf"] == "NOT_RUN"

def test_ripley_pipeline_not_run_and_settlement():
    svc = TransactionCertificationService()
    db = DatabaseV4.get()
    df = db.query("SELECT id_transaccion FROM marketplace_ledger_v1 WHERE marketplace='RIPLEY' LIMIT 1")
    assert not df.empty
    tx = df.iloc[0]["id_transaccion"]
    res = svc.certify(tx)
    assert res.chain_type == "SETTLEMENT"
    assert res.fiscal_status.value == "FISCAL_BLOCKED_EXTERNAL"
    assert res.pipeline["xml"] == "NOT_RUN"
    assert res.overall_status.value == "PARTIALLY_CERTIFIED"

def test_contract_version():
    svc = TransactionCertificationService()
    db = DatabaseV4.get()
    tx = db.query("SELECT id_transaccion FROM marketplace_ledger_v1 LIMIT 1").iloc[0]["id_transaccion"]
    res = svc.certify(tx)
    d = res.to_dict()
    assert d["contract_version"] == "TransactionCertificationResultV3"
    assert "transaction_id" in d
    assert "amount" in d and "canonical_value" in d["amount"]
    assert d["chain_type"] != "UNKNOWN"

def test_provenance_chains():
    svc = TransactionCertificationService()
    for mp, expected_chain in [("ML","DIRECT_LINK"),("RIPLEY","SETTLEMENT"),("PARIS","DOCUMENT_CHAIN"),("FALABELLA","TRANSACTION_CHAIN")]:
        db = DatabaseV4.get()
        df = db.query("SELECT id_transaccion FROM marketplace_ledger_v1 WHERE marketplace=? LIMIT 1", [mp])
        if df.empty:
            continue
        tx = df.iloc[0]["id_transaccion"]
        res = svc.certify(tx)
        assert res.chain_type == expected_chain, f"{mp} chain {res.chain_type} != {expected_chain}"
        assert res.chain_type != "UNKNOWN"

def test_money_precision_falabella_2026_04():
    from engine.v4.database import DatabaseV4
    db = DatabaseV4.get()
    df = db.query("SELECT SUM(monto) as total FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA' AND fecha BETWEEN '2026-04-01' AND '2026-04-30'")
    total = df.iloc[0]["total"]
    from engine.v4.money_canonical import canonical_clp
    canonical = canonical_clp(total)
    df2 = db.query("SELECT monto FROM marketplace_ledger_v1 WHERE marketplace='FALABELLA' AND fecha BETWEEN '2026-04-01' AND '2026-04-30'")
    from decimal import Decimal
    import math
    vals = [v for v in df2["monto"] if v is not None and not (isinstance(v,float) and math.isnan(v))]
    py_sum = int(sum(Decimal(str(v)) for v in vals).quantize(Decimal("1"))) if vals else 0
    assert canonical == py_sum, f"sql canonical {canonical} != py_sum {py_sum} raw {total}"
    # ensure canonical is integer and matches expected rounded value
    assert isinstance(canonical, int)

def test_no_frontend_certification_logic():
    import pathlib
    dash = pathlib.Path("templates/dashboard.html").read_text(encoding="utf-8")
    # frontend should not contain certification calculation logic like if (!xml) FAIL
    assert "if (!xml) FAIL" not in dash
    assert 'or "UNKNOWN"' not in dash or dash.count('or "UNKNOWN"') == 0  # no silent fallback
    # drawer now handles NOT_RUN
    assert "NOT_RUN" in dash

def test_single_authority():
    import pathlib, re
    api = pathlib.Path("api/api.py").read_text(encoding="utf-8")
    # count transactional certification authorities
    handlers = re.findall(r'def get_electronic_certification_status', api)
    assert len(handlers) == 1, f"expected single authority, found {len(handlers)}"
