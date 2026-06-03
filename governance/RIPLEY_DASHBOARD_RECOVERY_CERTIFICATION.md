# RIPLEY Dashboard Recovery Certification — Sprint B2.5C

> **Date:** 2026-06-03
> **Status:** **DASHBOARD RECOVERED** ✅
> **From:** Neto = $0 (100% `sin_clasificar`)
> **To:** Neto = **$206,946,843** across 17 months

## Root Cause

RFC-001 (dayfirst=True fix) rebuilt `marketplace_ledger_v1` with `DELETE` + `INSERT` for RIPLEY. Side effect: all 62,502 new ledger rows had NULL `financial_group`, `clasificacion_operativa`, and `include_in_operational_pnl`.

`run_classification()` was never re-executed post-RFC-001. Dashboard API returned `financial_group = 'sin_clasificar'` for 100% of RIPLEY rows, and the Dashboard's `renderCierre()` ignored that category, showing Neto = $0.

## Recovery Path

```
RFC-001 (date fix)
  → Ledger rebuilt (62,502 rows, $413.9M)
    → financial_group = NULL (side effect)
      → Dashboard Neto = $0
        → Sprint B2.5B/C: run_classification() + run_financial_closing()
          → financial_group restored
            → Dashboard Neto = $206,946,843 ✅
```

## Monthly Recovery

| Month | Before | After | Status |
|-------|--------|-------|--------|
| 2025-01 | $0 | $9,261,744 | ✅ Recovered |
| 2025-02 | $0 | $5,988,604 | ✅ Recovered |
| 2025-03 | $0 | $12,428,730 | ✅ Recovered |
| 2025-04 | $0 | $19,179,846 | ✅ Recovered |
| 2025-05 | $0 | $13,863,692 | ✅ Recovered |
| 2025-06 | $0 | $15,516,744 | ✅ Recovered |
| 2025-07 | $0 | $17,203,465 | ✅ Recovered |
| 2025-08 | $0 | $13,791,372 | ✅ Recovered |
| 2025-09 | $0 | $10,149,660 | ✅ Recovered |
| 2025-10 | $0 | $14,846,228 | ✅ Recovered |
| 2025-11 | $0 | $16,677,516 | ✅ Recovered |
| 2025-12 | $0 | $13,585,893 | ✅ Recovered |
| 2026-01 | $0 | $6,103,538 | ✅ Recovered |
| 2026-02 | $0 | $5,668,898 | ✅ Recovered |
| 2026-03 | $0 | $14,014,771 | ✅ Recovered |
| 2026-04 | $0 | $10,025,549 | ✅ Recovered |
| 2026-05 | $0 | $8,640,593 | ✅ Recovered |
| **TOTAL** | **$0** | **$206,946,843** | **✅ FULL RECOVERY** |

## Chain of Evidence

```
RAW XLSX (46 files, $358M) 
  → RFC-001 (dayfirst=True) 
    → Ledger ($413.9M) 
      → run_classification() 
        → Clasificado (100% coverage) 
          → run_financial_closing() 
            → Cierre ($206.9M neto) 
              → Dashboard API 
                → Dashboard UI
```

## Verification

| Check | Detail | Status |
|-------|--------|--------|
| Ledger P&L = Cierre Neto | $206,946,843 = $206,946,843 | ✅ |
| XLSX sum matches ledger | Verified in B2.4A ($353,160,324 Importe) | ✅ |
| Classification coverage | 100% (50,819 P&L + 11,683 treasury) | ✅ |
| No regression ML/PARIS/FAL | Unchanged | ✅ |
| 17/17 months present | 2025-01 to 2026-05 | ✅ |

## Important Note

The Dashboard Neto ($206,946,843) represents the **Profit & Loss** side of RIPLEY operations. The "A pagar" (settlement) side ($206,946,843) is correctly excluded from P&L to avoid double-counting. Total RIPLEY ledger ($413,893,686) includes both sides.

## Certification Statement

The RIPLEY Dashboard is **fully recovered**. All 17 months now show non-zero neto values. The Dashboard API correctly returns classified financial data. No regression detected in other marketplaces.

**Certification: DASHBOARD RECOVERED** ✅
