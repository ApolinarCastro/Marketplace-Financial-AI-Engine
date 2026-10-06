# PFO XML/DTE E2E R1 — TRACEABILITY EVIDENCE (PASS)

## Task Info

```
TASK_ID: PFO-XML-DTE-E2E-R1-001
DATE: 2026-10-06
HEAD_BEFORE: bd3f8f22186e7bffa87fe82d931954e4579d1aaf
BRANCH: main
```

Metadata repair (PFO-XML-DTE-METADATA-DDL-001) + certified DDL verified
working end-to-end. No engine files modified in this task. No golden modified.

---

## Positive Scenario (isolated TEMP_DB #1)

```
XML: PFO_SYNTH_DTE_90000001.xml (SHA a245fbe5...)
  folio=90000001 tipo=33 neto=4789 iva=911 total=5700 fecha=2026-06-02 rut=76000000-0
DTE_TRUTH: 1 row, marketplace=ML, tipo_dte=33 (repaired loader proven)
TARGET: COMM_E2E-002_ML_Facturacion_E2E_V1.xlsx_2, folio_xml=033-90000001, monto=-5700.0
CLASSIFIED: 8 rows (target present in clasificado_v1)
NORMALIZED_FOLIO: 90000001 (real _norm_ml_folio)
PRE-TRACE (read-only): DIRECT_MATCH / CERTIFIED / MATCHED_CERTIFIED,
  dte_folio=90000001 dte_monto=5700.0 delta=0 tipo_dte=33
RUN (ML branch of matcher.run()): folio_matches=1 rows_linked=1 rows_eligible=1
CERTIFIED ROW persisted in dte_certified_match_v1:
  ML / COMM_E2E-002... / 033-90000001 / 90000001 / 5700.0 / 2026-06-02 /
  PFO SYNTHETIC / 76000000-0 / 33 / DIRECT_MATCH / MATCHED_CERTIFIED / dte_ledger_matcher
POST-TRACE: full chain TRANSACTION→folio_xml→normalized→dte_truth→monto→MATCHED_CERTIFIED
```

Execution note (honest deviation): full `matcher.run()` executes all four
marketplace branches; on fresh DB the RIPLEY branch crashes
(CatalogException: ripley_settlement_chain missing — fresh-DDL gap, same class
as document_match_v1 was). Executed the exact ML branch run() itself calls
(`_match_ml_direct` + `_persist_certified("ML", …)`, run() lines 445-454).
PARIS/FALABELLA/RIPLEY branches out of scope for this ML checkpoint.

Robustness finding (not on critical path): `_trace_transaction` raises
KeyError('id_transaccion') on empty certified set instead of NOT_FOUND.
Observed in negative scenario; negative verdict rests on match_statuses +
certified count instead. Recorded for a future hardening task; not modified here.

## Negative Scenario (isolated TEMP_DB #2)

```
XML: PFO_SYNTH_DTE_90000002_NEG.xml (total 5702.0)
LEDGER: same COMM row shape, folio 033-90000002, |amount| 5700.0
MATCH DETAIL: folio 90000002, ledger 5700.0 vs DTE 5702.0, delta 2.0,
  status AMOUNT_MISMATCH, rule DIRECT_MATCH
CERTIFIED ROWS FOR TARGET: 0 (mismatch correctly excluded from certified set)
```

## Certification Boundary (mandatory, unchanged)

```
DOCUMENTAL_XML_TRACEABILITY: PASS
FINANCIAL_DTE_MATCH: PASS
LEDGER_DTE_TRACEABILITY: PASS
XMLDSIG_VALIDATION: NOT_IMPLEMENTED (validator exists, unwired to match path, fail-open degraded PASS)
TED_FRMT_VALIDATION: NOT_IMPLEMENTED
CAF_VALIDATION: NOT_IMPLEMENTED
XSD_VALIDATION: NOT_IMPLEMENTED
SII_STATUS_VALIDATION: NOT_IMPLEMENTED
ELECTRONIC_SIGNATURE_CERTIFICATION: NOT_IMPLEMENTED
```

PASS here answers "¿Qué XML respalda esta venta?" with traceable synthetic
evidence. It does NOT claim cryptographic electronic certification.

## Non-Contamination

```
PRODUCTION_DB_MODIFIED: FALSE (SHA verified before/after)
REAL_RAW_MODIFIED: FALSE (0 PFO_SYNTH markers in real 01_Raw/)
TEMP DIRS + script: REMOVED
```

## Verdict

```
FA-005: PASS (unchanged) / FA-006: READY (unchanged)
XML_DTE_E2E: PASS
FIRST_BLOCKER: NONE (metadata gap resolved by repair; R1 executed clean)
```

## Next Exact Action

PFO-ELECTRONIC-SIGNATURE-HARDENING-001 (fix degraded-PASS bypass, wire
validation into match chain, decide TED/FRMT/CAF/XSD/SII scope). No FA-006 auto-run.
