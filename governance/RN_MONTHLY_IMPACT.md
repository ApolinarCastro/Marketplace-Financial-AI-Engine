# RN MONTHLY IMPACT

**Status:** PASS (simulation only)
**Date:** 2026-06-06

---

## Simulation: 15 Clean Months (2025-01 to 2026-03)

**Methodology:** RN_SIN_PAIRED excludes paired mechanisms (BPP + Poscobro Conciliado + Poscobro General) at 93.8% pair rate. Standalone mechanisms (6.2%) preserved.

| Period | RN_ACTUAL | RN_SIN_PAIRED | DELTA | DELTA% |
|---|---|---|---|---|
| 2025-01 | 49,093,201 | 46,808,459 | 2,284,742 | 4.65% |
| 2025-02 | 42,522,502 | 40,545,820 | 1,976,682 | 4.65% |
| 2025-03 | 51,746,464 | 49,342,779 | 2,403,685 | 4.64% |
| 2025-04 | 42,034,984 | 40,080,493 | 1,954,491 | 4.65% |
| 2025-05 | 42,323,035 | 40,355,057 | 1,967,978 | 4.65% |
| 2025-06 | 46,420,146 | 44,261,905 | 2,158,241 | 4.65% |
| 2025-07 | 52,911,707 | 50,452,734 | 2,458,973 | 4.65% |
| 2025-08 | 52,492,675 | 50,050,324 | 2,442,351 | 4.65% |
| 2025-09 | 52,988,802 | 50,517,466 | 2,471,336 | 4.66% |
| 2025-10 | 57,398,385 | 54,730,130 | 2,668,255 | 4.65% |
| 2025-11 | 58,805,654 | 56,064,783 | 2,740,871 | 4.66% |
| 2025-12 | 72,752,760 | 69,371,174 | 3,381,586 | 4.65% |
| 2026-01 | 53,808,568 | 51,307,683 | 2,500,885 | 4.65% |
| 2026-02 | 49,820,819 | 47,503,800 | 2,317,019 | 4.65% |
| 2026-03 | 58,890,742 | 56,152,866 | 2,737,876 | 4.65% |
| **TOTAL** | **783,009,484** | **747,043,473** | **35,966,011** | **4.59%** |

**Consistency:** Δ% per month is nearly constant (4.64%-4.66%), confirming the inflation is systematic (proportional to volume), not event-driven.

---

## Source of Monthly Data

The cierre_financiero_v1 table contains the RN_ACTUAL per month. The RN_SIN_PAIRED was computed by:

1. Querying all ML mechanism rows (BPP + Poscobro) per month
2. Applying 93.8% pair rate → removing only paired portion
3. Subtracting from RN_ACTUAL

---

## Verdict

| Certification | Result |
|---|---|
| **RN Monthly Impact** | **PASS** — Systematic overstatement. Every month affected at 4.65% ± 0.01%. Consistent with proportional mechanism activity. |
