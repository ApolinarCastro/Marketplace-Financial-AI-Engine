# PFO XML/DTE E2E — EVIDENCE (METADATA GAP FAIL)

## Task Info

```
TASK_ID: PFO-XML-DTE-E2E-001
DATE: 2026-10-06
HEAD_BEFORE: e90c39adcdb4dd82e1e7d27c2aaa4ad247fd9e61
BRANCH: main
```

## Fixture (synthetic, integrity 4/4 PASS)

```
tests/golden/xml_dte_e2e/input/PFO_SYNTH_DTE_90000001.xml
  SHA256: a245fbe53370bbc03fe8134b4f49d16fe887c8ce2006e7ec243c6bfe6a404473
  Folio 90000001 / TipoDTE 33 / MntNeto 4789 / IVA 911 / MntTotal 5700
  FchEmis 2026-06-02 / RUT 76000000-0 / PFO SYNTHETIC
tests/golden/xml_dte_e2e/input/PFO_SYNTH_DTE_90000002_NEG.xml
  Folio 90000002 / MntTotal 5702 (delta 2 > tolerance 1; reserved for negative control)
tests/golden/xml_dte_e2e/expected/expected_xml_dte.json + README.md + integrity test
```

## Execution (steps 4-6, real DTEMatcher, redirected ROOT, fresh TEMP_DB)

```
XML_PARSE: PASS (namespace http://www.sii.cl/SiiDte, all fields extracted)
DTE_TRUTH_ROWS: 1
  folio=90000001 / monto_neto=4789.0 / monto_iva=911.0 / monto_total=5700.0
  fecha_emision=2026-06-02 / emisor_rut=76000000-0 / emisor_nombre=PFO SYNTHETIC
  marketplace=NULL / tipo_dte=NULL
```

Bonus finding: fresh DB lacks `dte_certified_match_v1` table
(MISSING_TABLE CatalogException) — same fresh-DDL gap class as document_match_v1 was.

## Verdict (per task §16)

```
STATUS: FAIL
FIRST_BLOCKER: DTE_TRUTH_INGESTION_METADATA_GAP
  load_dtes() INSERT sets 7 columns only (folio/montos/fecha/rut/nombre);
  marketplace + tipo_dte stay NULL;
  DTELedgerMatcher requires dte_truth_v1 WHERE marketplace='ML' → zero rows matchable.
Steps 7-12 (ledger link, matcher, traceability, negative control) NOT executed
(conditional on step 6 PASS). No engine files modified. No auto-repair.
```

## Classification Levels (task §14, honest assessment)

```
XML_PARSE_VALIDATION: PASS (proven this task)
DTE_TRUTH_INGESTION: FAIL (metadata gap proven)
FINANCIAL_DTE_MATCH: NOT_TESTED (blocked)
LEDGER_DTE_TRACEABILITY: NOT_TESTED (blocked)
ELECTRONIC_SIGNATURE_VALIDATION: NOT_IMPLEMENTED (see gate below)
```

## Electronic Signature Gate (task §13, static + runtime proof)

```
XMLDSIG_VALIDATION: NOT_IMPLEMENTED in executed chain.
  - Module engine/.../electronic_certification/signature_validator.py EXISTS
    and IS wired into ElectronicCertificationEngine (line 75 calls validate).
  - BUT runtime has_deps=False (signxml/lxml/cryptography NOT installed) →
    lines 37-40 return status PASS with "Degraded Mode" warning WITHOUT any
    verification (fail-open bypass).
  - AND neither dte_matcher.py nor dte_ledger_matcher.py references the
    validator at all → the XML→truth→match chain performs ZERO signature
    validation, not even degraded.
TED_FRMT_VALIDATION: NOT_IMPLEMENTED (zero references in matcher path).
CAF_VALIDATION: NOT_IMPLEMENTED (zero references).
XSD_VALIDATION: NOT_IMPLEMENTED (zero references).
SII_STATUS_VALIDATION: NOT_IMPLEMENTED (zero references).
DOCUMENTAL_XML_TRACEABILITY: NOT_TESTED (blocked at ingestion metadata).
ELECTRONIC_SIGNATURE_CERTIFICATION: NOT_IMPLEMENTED.
```

The degraded-PASS-on-missing-deps (lines 37-40) is recorded as a
fail-open design finding for a future hardening task. Not modified here.

## Non-Contamination

```
PRODUCTION_DB_MODIFIED: FALSE (SHA 4efcaa8a... identical before/after)
REAL_RAW_MODIFIED: FALSE (no XML copied to 01_Raw/)
TEMP_DIR data/db/tmp_pfo_xml_dte/: REMOVED
Script tmp_xml_step6_run.py: REMOVED
```

## Next Exact Action

Dedicated metadata repair task: populate marketplace + tipo_dte in
load_dtes() (or a certified post-ingestion enrichment), add
dte_certified_match_v1 to fresh DDL, then re-execute steps 6-12.
Separately: harden/fix degraded-PASS signature bypass + wire validation
into the match chain before any electronic-certification claim.
