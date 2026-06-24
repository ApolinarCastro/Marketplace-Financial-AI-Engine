# E1.1 — Executive Assumption Register

**Date:** 2026-06-03  
**Mode:** READ ONLY — every assumption in the portfolio, listed and evaluated

---

## Assumption Register

Every EV in the E1.0 portfolio depends on assumptions. This register lists all 11 assumptions, their basis, and the risk of being wrong.

### Assumption 1 — 1% of GMV penalty target

| Field | Value |
|---|---|
| **Used in** | P1+P2 — RIPLEY Penalidades |
| **Assumption** | 1% of GMV is an achievable penalty collection rate |
| **Basis** | Industry standard for marketplace seller compliance programs |
| **Source** | General marketplace practice (not from this DB) |
| **If wrong (low)** | 0.5% actual → EV drops to $1,645,744 (-50%) |
| **If wrong (high)** | 2% actual → EV rises to $6,678,278 (+101%) |
| **Risk** | MEDIO — depends on seller mix and compliance willingness |
| **Mitigation** | Phase in over 6 months; adjust target based on actual collection |

### Assumption 2 — 95% probability (P1+P2)

| Field | Value |
|---|---|
| **Used in** | P1+P2 — RIPLEY Penalidades |
| **Assumption** | 95% certainty that penalidades policy will be implemented and enforced |
| **Basis** | Eccsa controls the policy entirely — no external dependency |
| **Source** | Commercial judgment |
| **If wrong** | 50% actual → EV drops to $1,749,081 (-47%) |
| **Risk** | BAJO — policy change is administrative |
| **Mitigation** | CEO mandate; implementation is 4 weeks |

### Assumption 3 — 50% retiro stock reduction

| Field | Value |
|---|---|
| **Used in** | P3 — PARIS Retiro Stock |
| **Assumption** | Better inventory rotation can reduce stock retrievals by 50% |
| **Basis** | Operational hypothesis; root cause not fully diagnosed |
| **Source** | Commercial judgment |
| **If wrong (low)** | 20% reduction → EV drops to $260,928 (-60%) |
| **If wrong (high)** | 80% reduction → EV rises to $1,043,712 (+60%) |
| **Risk** | MEDIO — thin data (5 data points) |
| **Mitigation** | Audit root cause first; adjust target after 30 days |

### Assumption 4 — 80% probability (P3)

| Field | Value |
|---|---|
| **Used in** | P3 — PARIS Retiro Stock |
| **Assumption** | 80% chance of achieving 50% reduction |
| **Basis** | Operational feasibility — process change |
| **Source** | Commercial judgment |
| **If wrong** | 50% probability → EV drops to $407,700 (-38%) |
| **Risk** | MEDIO — 5 data points is thin evidence |
| **Mitigation** | Weekly tracking in first month |

### Assumption 5 — 100% stock antiguo elimination

| Field | Value |
|---|---|
| **Used in** | P4 — PARIS Stock Antiguo |
| **Assumption** | Aging inventory charges can be eliminated entirely |
| **Basis** | FIFO enforcement + clearance triggers. Avoidable expense. |
| **Source** | Operational analysis |
| **If wrong (low)** | 50% elimination → EV drops to $133,791 (-50%) |
| **Risk** | BAJO — most controllable project in portfolio |
| **Mitigation** | Alerts + monthly review |

### Assumption 6 — 85% probability (P4)

| Field | Value |
|---|---|
| **Used in** | P4 — PARIS Stock Antiguo |
| **Assumption** | 85% chance of full elimination |
| **Basis** | Standard inventory management practice |
| **Source** | Commercial judgment |
| **If wrong** | 50% probability → EV drops to $157,401 (-41%) |
| **Risk** | BAJO — pure operations fix |
| **Mitigation** | Process SOP + management accountability |

### Assumption 7 — 20% Poscobro recovery rate

| Field | Value |
|---|---|
| **Used in** | P5 — ML Ajuste Poscobro |
| **Assumption** | 20% of post-collection adjustments are reclaimable |
| **Basis** | Hypothesis only — no precedent in this system |
| **Source** | Commercial judgment |
| **If wrong (low)** | 0% recovery → EV drops to $0 (-100%) |
| **If wrong (high)** | 50% recovery → EV rises to $1,165,747 (+150%) |
| **Risk** | ALTO — no evidence to support any recovery rate |
| **Mitigation** | Audit phase must precede commitment |

### Assumption 8 — 75% probability (P5)

| Field | Value |
|---|---|
| **Used in** | P5 — ML Ajuste Poscobro |
| **Assumption** | 75% chance of achieving 20% recovery |
| **Basis** | No data support; speculative |
| **Source** | Commercial judgment |
| **If wrong** | 25% probability → EV drops to $155,433 (-67%) |
| **Risk** | ALTO — no empirical basis |
| **Mitigation** | Exclude from dashboard until audit completed |

---

## Assumption Heatmap

| # | Assumption | Impact if Wrong | Evidence | Risk |
|---|---|---|---|---|
| A1 | 1% penalty target | ±$3.3M | Industry benchmark | **MEDIO** |
| A2 | 95% probability P1+P2 | ±$1.7M | Internal control | **BAJO** |
| A3 | 50% retiro reduction | ±$0.4M | 5 data points | **MEDIO** |
| A4 | 80% probability P3 | ±$0.2M | Ops judgment | **MEDIO** |
| A5 | 100% antiguo elimination | ±$0.1M | Industry standard | **BAJO** |
| A6 | 85% probability P4 | ±$0.1M | Ops judgment | **BAJO** |
| A7 | 20% Poscobro recovery | ±$0.5M | No precedent | **ALTO** |
| A8 | 75% probability P5 | ±$0.3M | No precedent | **ALTO** |

### Assumptions by Confidence

| Confidence | Count | Assumptions | Combined EV at Risk |
|---|---|---|---|
| **ALTO** | 3 | A2, A5, A6 | $3,854,418 |
| **MEDIO** | 3 | A1, A3, A4 | $4,296,503 |
| **BAJO** | 2 | A7, A8 | $466,299 |

---

## What Changes If Assumptions Are Wrong

### Worst Case (all assumptions fail low)

| Project | Adjusted EV |
|---|---|
| P1+P2 at 0.5% GMV, 50% prob | $1,645,744 |
| P3 at 20% reduction, 50% prob | $260,928 |
| P4 at 50% elimination, 50% prob | $133,791 |
| P5 at 0% recovery, 25% prob | $0 |
| **Worst case total** | **$2,040,463** |

### Best Case (all assumptions succeed high)

| Project | Adjusted EV |
|---|---|
| P1+P2 at 2% GMV, 95% prob | $6,678,278 |
| P3 at 80% reduction, 80% prob | $1,043,712 |
| P4 at 100% elimination, 85% prob | $267,582 |
| P5 at 50% recovery, 75% prob | $1,165,747 |
| **Best case total** | **$9,155,319** |

---

## Assumption Impact on Portfolio

```
Worst Case    Expected      Best Case
$2.0M ────── $4.7M ────── $9.2M
  │            │             │
  └── 57% ──── ┘    ┌── 95% ──┘
                    (upside)
```

**Key insight:** The portfolio has 57% downside risk ($2.0M floor) and 95% upside potential ($9.2M ceiling). The asymmetry favors execution — even in the worst case, $2.0M is recovered with near-zero effort.

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
