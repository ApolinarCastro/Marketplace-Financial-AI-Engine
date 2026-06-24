# DATA FRESHNESS ROOT CAUSE

**Status:** FAIL
**Date:** 2026-06-06
**Scope:** All 4 marketplaces

---

## Root Cause: No Automated Pipeline

**No loader was invoked after the initial load.**

`pipeline_log` = 0 rows (empty). `file_registry` = 0 rows (empty). There is zero evidence of any automated or periodic execution.

The pipeline must be triggered manually for each marketplace via `SurgicalLoader.load_marketplace(MP)`. No scheduler, no watcher, no CI/CD.

---

## File Existence per Marketplace

| MP | Raw file exists for Junio 2026 | Loader path correct | Picked up |
|---|---|---|---|
| ML | ✅ Liberaciones (1 jun-5 jun), Poscobro (1 jun-6 jun) | ❌ `DIR_FACTURACION` broken | **NO** |
| PARIS | ✅ Dropshipping (06-06-2026), Fulfillment (1 jun-5 jun) | ✅ `01_Raw/PARIS/Transacciones/**/*.xlsx` | **NO** |
| FALABELLA | ✅ Orders (1 jun-5 jun) | ✅ `01_Raw/FALABELLA/**/*.xlsx` | **NO** |
| RIPLEY | ❌ No Junio files exist | ✅ `01_Raw/RIPLEY/**/*.xlsx` | N/A |

---

## Pipeline Trace (Junio 2026)

```
RAW (files exist)  →  Loader  →  Ledger  →  Clasificación  →  Cierre  →  Auditoría
       ✅                 ❌         ❌           ❌              ❌          ❌

First breakpoint: LOADER was never re-executed after May 2026
```

### ML
| Step | Detail | Status |
|---|---|---|
| RAW files | `01_Raw/ML/Poscobro/1 junio 2026 - 6 junio 2026.xlsx` exists | ✅ |
| Loader | `run()` only loads ML via `load_facturacion()` + `load_poscobro()` | ❌ Never re-run |
| **Path bug** | `DIR_FACTURACION = "01_Raw/ML/ML_Facturacion"` **DOES NOT EXIST** | ❌ |
| Ledger | 425 rows exist in Junio 2026 (only from Poscobro) | Partial |
| Revenue Junio | REAL $0 — 425 entries are all adjustment/payout (no Cargo por venta) | ❌ |

### PARIS
| Step | Detail | Status |
|---|---|---|
| RAW files | `01_Raw/PARIS/Transacciones/Dropshipping/06-06-2026.xlsx` exists | ✅ |
| RAW files | `01_Raw/PARIS/Transacciones/Fulfillment/1 jun 2026 - 5 jun 2026.xlsx` exists | ✅ |
| Loader | `load_paris()` reads all XLSX recursively | ❌ Never re-run |
| Ledger | Last data = 2026-04-30. May+Jun 2026 missing entirely | ❌ |

### FALABELLA
| Step | Detail | Status |
|---|---|---|
| RAW files | `01_Raw/FALABELLA/Órdenes y Transacciones/1 junio 2026 al 5 junio 2026.xlsx` exists | ✅ |
| Loader | `load_falabella()` reads all XLSX recursively | ❌ Never re-run |
| Ledger | Last data = 2026-04-30. May+Jun 2026 missing entirely | ❌ |

### RIPLEY
| Step | Detail | Status |
|---|---|---|
| RAW files | No Junio 2026 files exist | ❌ |
| Loader | `load_ripley()` reads all XLSX recursively | N/A |
| Ledger | Last data = 2026-05-26. Junio 2026 = 0 rows | N/A |

---

## Structural Failures

| # | Failure | Location | Evidence |
|---|---|---|---|
| 1 | No orchestration | `Scripts/pipeline_cli.py` broken (imports non-existent `engine.v4.pipeline`) | ImportError on `AntigravityEngineV4` |
| 2 | ML facturacion path broken | `surgical_loader.py:11` | `DIR_FACTURACION = ROOT / "01_Raw" / "ML" / "ML_Facturacion"` — directory DOES NOT EXIST |
| 3 | pipeline_log empty | DB table `pipeline_log` | 0 rows — no execution record exists |
| 4 | file_registry empty | DB table `file_registry` | 0 rows — no file tracking exists |
| 5 | Loader `run()` only processes ML | `surgical_loader.py:501-509` | No orchestration loads PARIS/RIPLEY/FALABELLA |

---

## Verdict

| Certification | Result |
|---|---|
| **Data Freshness Root Cause** | **FAIL** — No automated loading. No scheduler. No file watcher. Each MP must be loaded manually. ML facturacion path is broken. |
