# Golden Fixture XML_DTE_E2E

## DATASET_ID
XML_DTE_E2E

## PURPOSE
Controlled SII-DTE-shaped XML fixture to test the real chain:
XML parse → dte_truth_v1 → folio/monto matching → ledger link →
dte_certified_match_v1 → traceability.

## SOURCE_TYPE
SYNTHETIC. Folios 90000001/90000002 are reserved test markers, never SII
folios. RUT 76000000-0 is a synthetic marker. No production data.

## INPUT_FILES
```
tests/golden/xml_dte_e2e/input/PFO_SYNTH_DTE_90000001.xml (MntTotal 5700, positive control)
tests/golden/xml_dte_e2e/input/PFO_SYNTH_DTE_90000002_NEG.xml (MntTotal 5702, negative control: delta 2 > tolerance 1)
```

Both use namespace `http://www.sii.cl/SiiDte` and the Encabezado/IdDoc/
Emisor/Totales structure consumed by `engine/v4/dte_matcher.py`.

## REAL COMPONENTS UNDER TEST
- `engine/v4/dte_matcher.py::DTEMatcher.load_dtes` (XML → dte_truth_v1)
- `engine/v4/matching/dte_ledger_matcher.py::DTELedgerMatcher` (folio/monto match)
- Traceability read path (transaction → folio → DTE row → amounts)

## KNOWN CONTRACT RISK (to be proven by execution)
`load_dtes()` INSERT sets only folio/montos/fecha/rut/nombre; `marketplace`
and `tipo_dte` stay NULL, while `DTELedgerMatcher` queries
`dte_truth_v1 WHERE marketplace='ML'`. Execution will confirm or refute.

## ELECTRONIC BOUNDARY
No signature/TED/CAF/XSD/SII-online validation is claimed by this fixture.
See task step 13 for the capability gate (NOT_IMPLEMENTED unless code proves otherwise).
