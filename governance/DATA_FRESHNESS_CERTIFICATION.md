# DATA_FRESHNESS_CERTIFICATION — Go-Live Audit

**Status:** FAIL
**Date:** 2026-06-06
**Scope:** All 4 operational marketplaces (ML, PARIS, RIPLEY, FALABELLA)

---

## Pipeline Flow Verification

```
RAW ──→ LEDGER ──→ CLASIFICACIÓN ──→ CIERRE ──→ AUDITORÍA
```

### 1. Last RAW File Loaded

| Marketplace | Last RAW File | Date | Status |
|---|---|---|---|
| ML | Poscobro files | 2026-05-01 (file name) | ✅ Loaded |
| PARIS | *(not tracked)* | — | 🟡 No file_registry |
| RIPLEY | Resumen financiero files | Up to May 2026 | ✅ Loaded |
| FALABELLA | Órdenes y Transacciones | 2026-04-01 (Abril) | ✅ Loaded |

**Note:** `file_registry` table is EMPTY. No record of files loaded exists for any marketplace. This is a governance gap.

### 2. Last Date in Ledger (`marketplace_ledger_v1`)

| Marketplace | Min Date | Max Date | Last Revenue Month | Rows | Total ($) |
|---|---|---|---|---|---|
| ML | 2025-01-01 | 2026-12-04 | 2026-05 | 101,603 | 842,250,301 |
| PARIS | 2025-01-01 | 2026-04-30 | 2026-04 | 42,487 | 378,104,933 |
| RIPLEY | 2025-01-01 | 2026-05-26 | 2026-05 | 62,502 | 413,893,686 |
| FALABELLA | 2026-03-14 | 2026-04-30 | 2026-04 | 1,008 | 2,583,016 |

**Critical:** ML ledger contains FUTURE dates (2026-06 to 2026-12) with $0 revenue — only projected adjustment entries.

### 3. Last Date in Classification (`marketplace_ledger_clasificado_v1`)

| Marketplace | Max Date | Rows Match Ledger | Status |
|---|---|---|---|
| ML | 2026-12-04 | ✅ 101,603 / 101,603 | 100% coverage |
| PARIS | 2026-04-30 | ✅ 42,487 / 42,487 | 100% coverage |
| RIPLEY | 2026-05-26 | ✅ 62,502 / 62,502 | 100% coverage |
| FALABELLA | 2026-04-30 | ✅ 1,008 / 1,008 | 100% coverage |

### 4. Last Date in Closing (`marketplace_cierre_financiero_v1`)

| Marketplace | Last Revenue Period | Last Period (any) | Active Months |
|---|---|---|---|
| ML | 2026-05 | 2026-12 | 17 (2025-01 to 2026-05) |
| PARIS | 2026-04 | 2026-12 | 16 (2025-01 to 2026-04) |
| RIPLEY | 2026-05 | 2026-12 | 17 (2025-01 to 2026-05) |
| FALABELLA | 2026-04 | 2026-12 | 2 (2026-03 to 2026-04) |

**Note:** Future periods (2026-06 to 2026-12) exist with $0 revenue — are structural placeholder rows.

### 5. Last Date in Audit (`marketplace_auditoria_v1`)

| Marketplace | Max Detected | Rows | Active Checks |
|---|---|---|---|
| ML | — | 0 | ❌ No audit rows for ML |
| PARIS | 2026-06-03 | 4,222 | cargo_sin_respaldo_legal |
| RIPLEY | 2026-06-03 | 11,670 | cargo_sin_respaldo_legal |
| FALABELLA | 2026-06-03 | 55 | cargo_sin_respaldo_legal |

**Critical:** ML has ZERO audit rows. The largest marketplace ($842M, 60% of total) has no audit trail.

---

## Answer: ¿Junio 2026 está completamente incorporado?

**FAIL.**

| Marketplace | Junio 2026 Revenue | Junio 2026 Ledger | Junio 2026 Closing |
|---|---|---|---|
| ML | ❌ (0 rows) | ✅ ($1.8M in ajustes only) | ✅ ($1.8M RN, $0 ingresos) |
| PARIS | ❌ (0 rows) | ❌ | ❌ |
| RIPLEY | ❌ (0 rows) | ❌ | ❌ |
| FALABELLA | ❌ (0 rows) | ❌ | ❌ |

**Breakdown per marketplace:**

| Marketplace | Cutoff | Gap | Root Cause |
|---|---|---|---|
| **ML** | 2026-05-31 | May 2026 loaded, June 2026 empty | Future projections loaded, actual June data pending |
| **PARIS** | 2026-04-30 | May + June 2026 missing | Source files not loaded — last file is April 2026 |
| **RIPLEY** | 2026-05-26 | June 2026 missing | May 2026 partially loaded (cuts at 26th) |
| **FALABELLA** | 2026-04-30 | May + June 2026 missing | Source files not loaded — last file is April 2026 |

### Flow Cut: Where does the pipeline break?

```
RAW ──→ LEDGER ──→ CLASIFICACIÓN ──→ CIERRE ──→ AUDITORÍA
         ↓            ↓                  ↓           ↓
      FAILS ✓      FAILS ✓           FAILS ✓      FAILS (ML)

RAW → LEDGER:       PASS (data flows through)
LEDGER → CLASIFIC:  PASS (100% coverage)
CLASIFIC → CIERRE:  PASS (all periods covered)
CIERRE → AUDITORÍA: FAIL (ML has 0 audit rows)

DATA FRESHNESS:     FAIL (Junio 2026 not incorporated for ANY MP)
```

---

## Verdict

| Certification | Result |
|---|---|
| **Data Freshness** | **FAIL** — Junio 2026 no incorporado. PARIS y FALABELLA cortan en Abril 2026. |
| **Pipeline Integrity** | **PASS** — RAW→Ledger→Clasificación→Cierre flows correctly for all loaded data. |
| **Audit Coverage** | **FAIL** — ML has 0 audit rows. Largest marketplace has no audit trail. |
| **File Registry** | **FAIL** — file_registry table is empty. No traceability of what was loaded or when. |
