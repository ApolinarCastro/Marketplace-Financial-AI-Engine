# P0 RIPLEY SELLER → XML/DTE → LEDGER — Final Report

- **Execution ID**: `424ecfc0-3c88-4919-aa2b-aa2028b342f4`
- **Commit**: `2d51f5216695388839e15c0ab08dd98af4aa6ce2`
- **Timestamp**: `2026-08-06T12:56:03`
- **Harness**: `1.0.0-r5-p0-ripley-seller-xml`
- **Status**: **PARTIAL_WITH_PROVEN_BLOCKER**
- **Verification**: VERIFIED

## Chain certified (SETTLEMENT_CHAIN_V2)

The settlement chain **SELLER → CICLOS → LEDGER** closes via `order_id`:

| Metric | Value |
|---|---|
| SELLER files (Fulfillment by Seller) | 51 xlsx |
| SELLER distinct orders | 12,543 |
| CICLOS files (recovered from git `7a94360`) | 52 csv |
| CICLOS distinct orders | 14,121 |
| SELLER ∩ CICLOS (order_id bridge) | **11,974** |
| SELLER ∩ LEDGER | 11,956 |
| CICLOS ∩ LEDGER | 13,646 |
| FULL chain orders | 11,499 |
| Ledger rows chained | **287,023 / 287,417 (99.86%)** |
| Distinct orders chained | 14,066 / 14,138 (99.49%) |
| Settlement refs ⊆ ledger folio_xml | ✓ (51 refs, 104 ledger folios, same namespace 499799–602050) |

## Blocker (XML/DTE eslabón — PROVEN)

The **XML/DTE → LEDGER** fiscal eslabón is impossible with the available inventory:

| Check | Result |
|---|---|
| XML folios (Facturacion, 472) | SII range 25,272–54,087,142 |
| dte_truth_v1 RIPLEY folios | 407 (SII namespace) |
| Settlement refs (SELLER/CICLOS/ledger folio_xml) | 52 in 499,799–602,050 |
| XML folio ∩ settlement refs | **0** |
| dte_truth folios ∩ ledger folio_xml | **0** |
| XML files referencing settlement refs or order IDs | **0** |

**Root cause**: RIPLEY ledger `folio_xml` values are **settlement-invoice numbers** from the XLSX/CSV billing-cycle reports — NOT SII fiscal DTE folios. The 472 `Facturacion` XMLs are **ECCSA ↔ NANDA supplier/marketplace-cost invoices** (e.g. "MKP COMISIÓN COSTO FIJO MKP", "Aporte Promocional", "Despacho Flota Propia") in a completely disjoint folio namespace. No key (folio, order, reference) connects the two. The `dte_link_v1` RIPLEY rows (210,232) are all `LEDGER_EXISTING` (folio copied from ledger, `tipo_dte=None`) — this is **not** real DTE certification.

## Controlled writes (official DB untouched)

- `data/work/ripley_dte_matching_controlled_20260806_124337.db`
  - `ripley_seller_xml_map_v1` — 287,417 rows (chain map, additive)
  - `document_match_v1_controlled` — 286,919 rows (CHAIN_ONLY status)
  - `dte_ledger_link_controlled` — materialized view; **0** RIPLEY rows required correction (all settlement-namespace rows already `dte_linked=0`)

## Tests

- 21 new tests (matching / folio normalization / path resolution): **PASS**
- Certification gate: **29/29 PASS**
- Full regression: **944 pass, 10 pre-existing failures** (golden `marketplace_impact` file deleted in commit `7a94360`, prior to this session), **0 new regressions**
- Idempotency: **3 identical runs**

## Verdict

> **PARTIAL_WITH_PROVEN_BLOCKER** — RIPLEY settlement chain (SELLER→CICLOS→LEDGER) is certified at 99.86% rows via order_id. The XML/DTE fiscal eslabón cannot be closed with the available inventory (settlement folios have NO fiscal SII XML backing). No financial value was modified.
