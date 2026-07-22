# PARIS PHYSICAL SOURCE INVENTORY
**Date:** 2026-06-07
**Certification ID:** PARIS-FORENSIC-FASE1

---

## Directory Structure

```
01_Raw/PARIS/
├── Facturacion/          (62 XML files — SII DTE documents, dteproveedor_*.xml)
└── Transacciones/
    ├── Dropshipping/      (18 XLSX files — 28 columns, monthly detail)
    └── Fulfillment/       (4 XLSX files — 27 columns, annual/partial scope)
```

**Total files: 84 (62 XML + 22 XLSX)**

---

## XLSX Files — Complete Inventory

| File | Type | Rows | monto_gross | monto_pagar | Date Range | SHA256 (first 16) |
|---|---|---|---|---|---|---|
| 01-2025.xlsx | DS | 1,318 | $4,573,516 | $3,557,846 | 2024-11-07 → 2025-01- | 61f7ad1dab5b86ba |
| 02-2025.xlsx | DS | 1,061 | $6,358,042 | $4,938,459 | 2025-01-16 → 2025-02- | 4c6b87aa3c000641 |
| 03-2025.xlsx | DS | 643 | $3,850,673 | $2,973,824 | 2025-02-03 → 2025-03- | 19354259b9ee3329 |
| 04-2025.xlsx | DS | 1,405 | $11,962,330 | $9,306,217 | 2024-01-09 → 2025-04- | 9f35b879a9ef110b |
| 05-2025.xlsx | DS | 795 | $5,015,694 | $3,836,170 | 2025-03-21 → 2025-05- | f64a3e7888260d97 |
| 06-2025.xlsx | DS | 2,056 | $19,315,445 | $15,264,531 | 2025-01-04 → 2025-06- | — |
| 07-2025.xlsx | DS | 2,033 | $21,252,615 | $16,848,274 | 2025-06-20 → 2025-07- | — |
| 08-2025.xlsx | DS | 2,019 | $17,046,749 | $13,631,423 | 2024-06-07 → 2025-08- | — |
| 09-2025.xlsx | DS | 1,461 | $14,958,554 | $12,177,671 | 2025-09-01 → 2025-09- | — |
| 10-2025.xlsx | DS | 3,042 | $29,248,119 | $24,523,378 | 2025-10-01 → 2025-10- | — |
| 11-2025.xlsx | DS | 1,848 | $15,689,690 | $13,129,219 | 2025-09-21 → 2025-11- | — |
| 12-2025.xlsx | DS | 3,222 | $26,991,911 | $22,412,135 | 2025-10-06 → 2025-12- | — |
| 01-2026.xlsx | DS | 1,436 | $8,067,859 | $6,662,000 | 2026-01-01 → 2026-01- | — |
| 02-2026.xlsx | DS | 940 | $7,314,050 | $6,078,788 | 2026-02-01 → 2026-02- | — |
| 03-2026.xlsx | DS | 1,477 | $14,597,580 | $12,119,206 | 2026-03-01 → 2026-03- | — |
| 04-2026.xlsx | DS | 1,876 | $14,828,950 | $12,193,180 | 2026-04-01 → 2026-04- | — |
| 05-2026.xlsx | DS | 1,277 | $10,711,660 | $8,810,080 | 2026-05-01 → 2026-05- | — |
| 1 jun 2026 - 8 jun 2026.xlsx | DS | 1,329 | $20,638,719 | $17,114,498 | 2026-01-06 → 2026-08- | — |
| 1 ene 2025 - 31 dic 2025.xlsx | FF | 14,740 | $150,980,921 | $123,115,343 | 2025-01-02 → 2025-12- | — |
| 1 ene 2026 - 30 abr 2026.xlsx | FF | 1,768 | $11,893,557 | $9,793,944 | 2026-01-01 → 2026-04- | — |
| 1 may 2026 - 31 may 2026.xlsx | FF | 235 | -$904,096 | -$790,116 | 2026-05-01 → 2026-05- | — |
| 1 jun 2026 - 8 jun 2026.xlsx | FF | 109 | $1,160,490 | $962,344 | 2026-01-06 → 2026-08- | — |
| **TOTAL** | | **46,090** | **$415,553,028** | **$338,658,414** | | |

---

## DS vs FF Column Structure

### DS (Dropshipping) — 28 columns
`id`, `descripciÃ³n`, `tipo`, `nÃºmero orden`, `sku`, `monto`, `acuerdo comercial`, `comisiÃ³n`, `monto a pagar`, `monto total factura`, `fecha`, `estado`, `estado del pago`, `nro solicitud pago`, `nro solicitud factura`, `nÃºmero factura`, `link factura`, `fecha factura`, `categoria`, `nro suborden`, `nro solicitud nota crÃ©dito`, `nÃºmero nota crÃ©dito`, `link nota crÃ©dito`, `seller sku`, `fecha de entrega`, `reputacion`, `Descuento Comercial`, `Tipo de Transporte`

**Key mapping:** monto=gross, comisiÃ³n=fee, monto a pagar=net (ledger stores this)

### FF (Fulfillment) — 27 columns
`id`, `descripcion`, `tipo`, `nÃºmero orden`, `sku`, `seller sku`, `monto`, `moneda`, `descuento comercial`, `acuerdo comercial`, `comisiÃ³n`, `monto a pagar`, `monto liq.factura`, `fecha`, `estado`, `estado de liq.factura`, `nro solicitud liq.factura`, `nÃºmero liq.factura`, `link liq.factura`, `fecha liq.factura`, `categoria`, `nro suborden`, `fecha de entrega`, `nro solicitud factura`, `nÃºmero factura`, `link factura`, `fecha factura`

**Key difference:** `descripcion` (without accent) vs `descripciÃ³n` (with accent). Columns in different order.

---

## XML Files (Facturacion/)

62 SII DTE XML documents (dteproveedor_*.xml), total ~64KB.
Named from `dteproveedor_5372.xml` to `dteproveedor_7440.xml`.
These are NOT used by the current V4 ETL pipeline.

---

## Correction from Previous Audits

| Previous Claim | Actual Finding |
|---|---|
| Facturacion has 0 files (EMPTY) | **Facturacion has 62 XML files** (dteproveedor_*.xml) |
| Files "06-06-2026.xlsx" and "1 jun 2026 - 5 jun 2026.xlsx" referenced in ledger | **Files do NOT exist** on disk. Actual files are `1 jun 2026 - 8 jun 2026.xlsx` (DS + FF). Suspect file rename between source generation and loading. 381 ledger duplicate groups reference these non-existent files. |
| Total RAW XLSX rows: ~43,400 | **46,090 XLSX rows** in 22 source files |
