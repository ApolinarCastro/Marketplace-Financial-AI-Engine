# RIPLEY XML Coverage Discovery Report — Sprint B2.5C

> **Date:** 2026-06-03
> **Type:** Asset discovery — 407 XML files found for RIPLEY
> **Status:** **DISCOVERED — NOT CERTIFIED** (DTEIndexer not executed)

## 1. Executive Summary

A set of **407 SII DTE XML files** was discovered at `01_Raw/RIPLEY/Documentos Recepcionados/`. These are electronic invoices (Documento Tributario Electrónico) issued by RIPLEY/Comercial Eccsa S.A. and cover the full RIPLEY ledger period (2025-01 to 2026-05).

**Current estado_xml in ledger: 100% NULL** — these XMLs have never been processed by DTEIndexer. The matching/bridge between XML and ledger has not been established.

## 2. XML Inventory

| Attribute | Value |
|-----------|-------|
| Total XML files | 407 |
| Location | `01_Raw/RIPLEY/Documentos Recepcionados/` |
| Emisor (RUT) | 83382700-6 (Comercial Eccsa S.A. / RIPLEY) |
| Receptor (RUT) | 77898100-9 |
| Date range | 2025-01-10 to 2026-05-28 |
| Total invoiced (MntTotal) | $186,705,151 |
| Total Detalle line items | 2,310 |

## 3. DTE Types

| Tipo | Description | Count |
|------|-------------|-------|
| 33 | Electronic Invoice (Factura Electrónica) | 253 |
| 43 | Credit Note (Nota de Crédito) | 105 |
| 52 | Debit Note (Nota de Débito) | 30 |
| 61 | Electronic Docket (Boletín Electrónico) | 19 |
| **Total** | | **407** |

## 4. Monthly Coverage

| Month | XMLs | XML Amount | Ledger Amount | Coverage % |
|-------|------|------------|---------------|------------|
| 2025-01 | 7 | $3,213,447 | $18,523,488 | 17.3% |
| 2025-02 | 12 | $7,660,284 | $11,977,208 | 64.0% |
| 2025-03 | 16 | $7,830,645 | $24,857,460 | 31.5% |
| 2025-04 | 26 | $16,042,003 | $38,359,692 | 41.8% |
| 2025-05 | 15 | $13,102,822 | $27,727,384 | 47.3% |
| 2025-06 | 16 | $12,572,670 | $31,033,488 | 40.5% |
| 2025-07 | 18 | $14,066,542 | $34,406,930 | 40.9% |
| 2025-08 | 14 | $10,153,389 | $27,582,744 | 36.8% |
| 2025-09 | 11 | $5,569,804 | $20,299,320 | 27.4% |
| 2025-10 | 23 | $12,501,808 | $29,692,456 | 42.1% |
| 2025-11 | 25 | $14,111,151 | $33,355,032 | 42.3% |
| 2025-12 | 36 | $22,230,937 | $27,171,786 | 81.8% |
| 2026-01 | 28 | $8,750,418 | $12,207,076 | 71.7% |
| 2026-02 | 30 | $5,949,681 | $11,337,796 | 52.5% |
| 2026-03 | 37 | $9,708,053 | $28,029,542 | 34.6% |
| 2026-04 | 53 | $13,552,348 | $20,051,098 | 67.6% |
| 2026-05 | 40 | $9,689,149 | $17,281,186 | 56.1% |
| **TOTAL** | **407** | **$186,705,151** | **$413,893,686** | **45.1%** |

## 5. Cross-Reference Analysis

| Match Method | Result |
|-------------|--------|
| Ledger folio_xml vs XML Folio | NO MATCH (different numbering) |
| XML ID vs id_transaccion | Substring matches exist (coincidental) |
| Amount matching | Partial match possible (future work) |

**Key Gap**: The ledger's `folio_xml` field contains 5-6 digit "orden de pedido" numbers from XLSX files (e.g., 517031, 526971). The XMLs contain SII DTE Folio numbers (e.g., 1978496, 2143381). These are different identification systems with no pre-existing bridge.

## 6. Current Status

| Metric | Value |
|--------|-------|
| XML files on disk | 407 ✅ |
| XML structural validation | Valid SII DTE format ✅ |
| Ledger estado_xml populated | 0% (NULL) ❌ |
| DTEIndexer executed | No (PROHIBIDO) |
| XML-to-Ledger matching | Not established ❌ |
| XML coverage (by amount) | 45.1% of ledger ($186.7M/$413.9M) |

## 7. Recommendation

This discovery is significant. It proves that RIPLEY XML source files exist covering the full operational period. The 45.1% amount coverage provides a foundation for Sprint A5 (DTEIndexer RIPLEY). When authorized, DTEIndexer can bridge these 407 XMLs to ledger rows using:

1. **Amount + date matching**: Cross-reference MntTotal + FchEmis against ledger rows
2. **RUT matching**: All XMLs have consistent RutEmisor/RutReceptor
3. **DTE Folio bridge**: May exist in XLSX source files (unmapped field)

**Current certification: NOT CERTIFIED** (requires Sprint A5 execution)

**Target certification after DTEIndexer: POTENTIALLY 45-100%** depending on bridge discovery
