# E1.1 — Project Confidence Matrix

**Date:** 2026-06-03  
**Mode:** READ ONLY — corrected values, double-count removed

---

## Matrix: Evidence × Control × Variability

| Project | EV | Historical Evidence | Eccsa Control | Variability | Confidence Score |
|---|---|---|---|---|---|
| P4 PARIS Stock Antiguo | $267,582 | 10 months, 11 rows | FULL | Low (±10%) | **ALTO** |
| P1+P2 RIPLEY Penalidades | $3,323,255 | 17 months, 10,555 GMV rows | FULL | Medium (±30%) | **MEDIO** |
| P3 PARIS Retiro Stock | $652,320 | 5 months, 5 rows | FULL | Medium (±25%) | **MEDIO** |
| P5 ML Ajuste Poscobro | $466,299 | 23 months, 634 rows | PARTIAL | High (±50%) | **BAJO** |
| **CORRECTED PORTFOLIO** | **$4,709,456** | | | | |

---

## Detailed Confidence Analysis

### P4 — PARIS Stock Antiguo Elimination ($267,582)

| Factor | Assessment | Rationale |
|---|---|---|
| **Evidence quality** | ALTO | 10 months of recurring monthly charges. Clear pattern of $15K-$66K/month. |
| **Control** | COMPLETO | Eccsa controls inventory rotation. No external dependency. |
| **Solution clarity** | CLARO | FIFO enforcement + aging alerts. Operational SOP change. |
| **Implementation risk** | MUY BAJO | No system change. No contract change. No external parties. |
| **Recovery certainty** | ALTA | $314K charges are 100% avoidable with proper rotation. |
| **Confidence** | **85-95%** | |

**Verdict:** Execute immediately. Highest confidence in portfolio.

### P1+P2 — RIPLEY Penalidades ($3,323,255)

| Factor | Assessment | Rationale |
|---|---|---|
| **Evidence quality** | ALTO | GMV base of $353M across 17 months is solid. Current $33K confirmed. |
| **Control** | COMPLETO | Penalty policy is Eccsa's commercial decision. |
| **Solution clarity** | CLARA | Industry standard 1%. Implementation path known. |
| **Implementation risk** | BAJO | System change is configuration, not development. |
| **Recovery certainty** | MEDIA | Actual collection may be 0.5-1.5% depending on seller mix and compliance. |
| **Confidence** | **65-95%** | |

**Range analysis:**
- Worst case (0.5% of GMV): $1,765,802 - $33,440 = $1,732,362 × 95% = **$1,645,744**
- Expected (1.0% of GMV): **$3,323,255**
- Best case (2.0% of GMV): $7,063,206 - $33,440 = $7,029,766 × 95% = **$6,678,278**

**Verdict:** Start immediately but report as range ($1.6M - $6.7M).

### P3 — PARIS Retiro Stock ($652,320)

| Factor | Assessment | Rationale |
|---|---|---|
| **Evidence quality** | BAJO | Only 5 data points across 5 months. Thin sample. |
| **Control** | COMPLETO | Eccsa controls inventory and logistics process. |
| **Solution clarity** | MEDIA | Retiro stock root cause not fully diagnosed. May have structural component. |
| **Implementation risk** | BAJO | Process change only. |
| **Recovery certainty** | MEDIA | 50% reduction is educated estimate. Could be 20-80%. |
| **Confidence** | **55-80%** | |

**Range analysis:**
- Worst case (20% reduction): $326,160 × 80% = **$260,928**
- Expected (50% reduction): **$652,320**
- Best case (80% reduction): $1,304,640 × 80% = **$1,043,712**

**Verdict:** Proceed but monitor first 30 days to validate reduction trajectory.

### P5 — ML Ajuste Poscobro ($466,299)

| Factor | Assessment | Rationale |
|---|---|---|
| **Evidence quality** | ALTO (historical), BAJO (recovery) | $3.1M is well-documented. Recoverability is unknown. |
| **Control** | PARCIAL | Eccsa can audit and claim, but ML must accept. |
| **Solution clarity** | BAJA | No precedent for Poscobro recovery. Unknown if 20% is achievable. |
| **Implementation risk** | MEDIO | Requires finance team effort; may find 0% recoverable. |
| **Recovery certainty** | MUY BAJA | 20% is pure hypothesis. Audit could find 0%. |
| **Confidence** | **5-75%** | |

**Range analysis:**
- Worst case (0% recovery): **$0**
- Expected (20% recovery / 75% prob): **$466,299**
- Best case (50% recovery / 75% prob): $1,554,329 × 75% = **$1,165,747**

**Verdict:** Investigate before committing EV. Report separate from confirmed projects.

---

## Confidence Ranking

| Rank | Project | EV | Confidence | Report on Dashboard? |
|---|---|---|---|---|
| 1 | P4 PARIS Stock Antiguo | $267,582 | **ALTO** (85-95%) | ✓ **Yes** |
| 2 | P1+P2 RIPLEY Penalidades | $3,323,255 | **MEDIO** (65-95%) | ✓ **Yes** (as range) |
| 3 | P3 PARIS Retiro Stock | $652,320 | **MEDIO** (55-80%) | ✓ **Yes** (with caveat) |
| 4 | P5 ML Ajuste Poscobro | $466,299 | **BAJO** (5-75%) | ✗ **No** (investigate first) |

---

## Dashboard Recommendation

| Column | P1+P2 | P3 | P4 | P5 |
|---|---|---|---|---|
| Show on dashboard? | ✓ Yes | ✓ Yes | ✓ Yes | ✗ **No** |
| Display as | Range ($1.6-6.7M) | Single value | Single value | "Under investigation" |
| EV for reporting | **$3,323,255** | **$652,320** | **$267,582** | **$0** (until audit) |
| Confidence label | MEDIO | MEDIO | ALTO | BAJO |

**Adjusted portfolio for executive dashboard:**
- Confirmed: **$4,243,157** (P1+P2 + P3 + P4)
- Under investigation: **$466,299** (P5)
- **Dashboard total: $4,243,157**

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
