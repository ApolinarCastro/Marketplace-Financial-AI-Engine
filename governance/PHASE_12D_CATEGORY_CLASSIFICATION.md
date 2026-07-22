# Phase 12D — Universal Category Classification Certificate (FIX-12/16/17)

**Date:** 2026-06-17  
**Status:** PASS ✅

## Universal Financial Group Mapping

All financial_group values across all 4 MPs are now classified into the 6-slot waterfall:

| Category | ML | PARIS | RIPLEY | FALABELLA |
|----------|----|-------|--------|-----------|
| **ing** (Ingresos Brutos) | ingresos | ingresos | ingresos | ingresos |
| **dev** (Devoluciones) | devoluciones | — | devoluciones | devoluciones |
| **cop** (Costos Logísticos) | costos_operacionales | — | costos_logisticos | costos_operacionales |
| **ccm** (Comisiones & Comerciales) | costos_comerciales | costos_operacionales* | comisiones | costos_comerciales |
| **aju** (Ajustes & Retenciones) | ajustes, recuperaciones_y_bonificaciones | ajustes | ajustes | ajustes, NULL** |

*\*PARIS costos_operacionales → ccm (no separate costos_comerciales)*  
*\*\*FALABELLA NULL financial_group → aju ($12,099, known pre-existing unclassified row)*

## Internal Conservation

| MP | ing+dev+cop+ccm+aju | neto | Delta |
|---|---------------------|------|-------|
| ALL | $648,842,436 | $648,842,436 | $0 |
| ML | $133,742,925 | $133,742,925 | $0 |
| PARIS | $72,966,754 | $72,966,754 | $0 |
| RIPLEY | $434,468,371 | $434,468,371 | $0 |
| FALABELLA | $7,664,386 | $7,664,386 | $0 |

## Orphan Categories

**0 orphan categories.** Every financial_group value is mapped to exactly one waterfall category. Verified by SQL query.

## Category Appropriateness

Each group assigned to the correct financial category:

- `costos_logisticos` (RIPLEY) → **cop** — logistics costs
- `comisiones` (RIPLEY) → **ccm** — commission costs
- `recuperaciones_y_bonificaciones` (ML) → **aju** — income adjustments
- `NULL` (FALABELLA, $12K) → **aju** — unclassified operational row
- `costos_operacionales` (PARIS) → **ccm** — marketplace charges (commission-equivalent)
