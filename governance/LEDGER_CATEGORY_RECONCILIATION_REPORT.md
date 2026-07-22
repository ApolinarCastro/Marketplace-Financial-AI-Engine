# Ledger Category Reconciliation Report

## Status: PASS ✅ (Delta = 0 at all levels)

## Validation Matrix

| Level | Validation | FALABELLA | ML | PARIS | RIPLEY |
|-------|-----------|-----------|-----|-------|--------|
| **Level 4** | Neto = SUM(Categories) | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |
| **Level 1** | Category = SUM(Subcategories) | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |
| **Level 2** | Subcategory = Ledger SUM(detalle) | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |
| **Level 3** | Category = Ledger SUM(all sub-detalles) | $0 ✅ | $0 ✅ | $0 ✅ | $0 ✅ |

## Category-Level Verification (YTD 2026)

### FALABELLA
| Category | Category Total | Ledger SUM | Delta |
|----------|--------------|------------|-------|
| Ingresos Brutos | $12,470,241 | $12,470,241 | $0 |
| Devoluciones de Venta | -$1,878,556 | -$1,878,556 | $0 |
| Costos Logísticos & Operacionales | -$800,171 | -$800,171 | $0 |
| Comisiones & Comerciales | -$2,114,602 | -$2,114,602 | $0 |
| Ajustes & Retenciones | -$427 | -$427 | $0 |
| **Neto** | **$7,676,485** | **$7,676,485** | **$0** |

### ML
| Category | Category Total | Ledger SUM | Delta |
|----------|--------------|------------|-------|
| Ingresos Brutos | $213,676,590 | $213,676,590 | $0 |
| Devoluciones de Venta | -$19,609,206 | -$19,609,206 | $0 |
| Costos Logísticos & Operacionales | -$17,990,799 | -$17,990,799 | $0 |
| Comisiones & Comerciales | -$43,486,650 | -$43,486,650 | $0 |
| Ajustes & Retenciones | $1,152,990 | $1,152,990 | $0 |
| **Neto** | **$133,742,925** | **$133,742,925** | **$0** |

### PARIS
| Category | Category Total | Ledger SUM | Delta |
|----------|--------------|------------|-------|
| Ingresos Brutos | $112,574,966 | $112,574,966 | $0 |
| Costos Logísticos & Operacionales | -$7,355,536 | -$7,355,536 | $0 |
| Ajustes & Retenciones | -$32,252,676 | -$32,252,676 | $0 |
| **Neto** | **$72,966,754** | **$72,966,754** | **$0** |

### RIPLEY (Canonical)
| Category | Category Total | Ledger SUM | Delta |
|----------|--------------|------------|-------|
| Ingresos Brutos | $218,441,218 | $218,441,218 | $0 |
| Devoluciones de Venta | -$27,745,348 | -$27,745,348 | $0 |
| Costos Logísticos & Operacionales | -$7,478,142 | -$7,478,142 | $0 |
| Comisiones & Comerciales | $26,518,057 | $26,518,057 | $0 |
| Ajustes & Retenciones | -$6,518,330 | -$6,518,330 | $0 |
| **Neto** | **$203,217,455** | **$203,217,455** | **$0** |

## Bugs Fixed

### Period Bug in `query_ledger()` (engine/v4/domain/financial_engine.py:306-311)

**Root cause:** When `resolve_period_range('YTD')` returns `end=None`, the old code set `end = start`, creating a single-day filter (`fecha <= '2026-01-01'`). This caused ALL YTD-ledger queries to return 0 rows for any data not from January 1st.

**Fix:** Only add `fecha <= ?` condition when `end is not None`.

**Impacted:** All `query_ledger()` calls with YTD period — including the UI click-through for RIPLEY Devoluciones (OBS-02).

## Certification

Every category dollar is traceable to the ledger. Every subcategory dollar is traceable to its `detalle` filter. Every SIGNAL subcategory is transaction-exclusive. **Delta = 0 at all 4 levels.**

**Source:** `marketplace_ledger_v1` via `/api/v4/financial-structure?signal_mode=SIGNAL`
**Date:** 2026-06-17
