# P32R7 — Single Financial Truth Certification

**Date:** 2026-07-07
**Scope:** Validate Ledger == Clasificado == Cierre for all marketplaces

## Level 1: Ledger == Clasificado

| Metric | Value |
|--------|-------|
| Ledger rows | 402,089 |
| Clasificado rows | 402,089 |
| Ledger total | $3,381,794,665.45 |
| Clasificado total | $3,381,794,665.45 |
| **Delta** | **$0.00 ✅** |

**Verdict: PERFECT** — 0 row delta, $0 amount delta. ETL fidelity maintained.

## Level 2: Ledger (financial) vs Cierre

Ledger with `financial_group IS NOT NULL`:

| Marketplace | Ledger | Cierre | Delta | Status |
|-------------|--------|--------|-------|--------|
| FALABELLA | $2,568,906 | $8,596,975 | **-$6,028,069** | ❌ FAIL |
| ML | $621,960,122 | $610,179,330 | **$11,780,792** | ⚠️ EXPLAINED |
| PARIS | $337,594,474 | $355,671,316 | **-$18,076,842** | ❌ FAIL |
| RIPLEY | $2,115,376,191 | $337,005,407 | **$1,778,370,784** | ❌ FAIL |

**Verdict: BROKEN** ❌ — Only ML has an explained delta. Other 3 MPs fail.

## Delta Analysis by MP

### FALABELLA (-$6M)
- Ledger shows $2.6M but cierre claims $8.6M
- Cierre includes periods not reflected in ledger
- **POSSIBLE ROOT CAUSE:** Cierre calculated from different subset or additional data

### PARIS (-$18M)
- Ledger $338M vs Cierre $356M
- Gap is 5.3% — material
- **POSSIBLE ROOT CAUSE:** Cierre formula includes signal/noise filtering differences

### RIPLEY ($1.78B)
- Ledger $2,115M vs Cierre $337M
- Ledger includes `tesoreria` ($674M, non-P&L) and 199,012 NOISE rows
- Even excluding tesoreria: $1,441M vs $337M ($1.1B gap)
- **ROOT CAUSE:** Structural — 54.1% of RIPLEY rows designated as NOISE and excluded from cierre
- 12 SIGNAL subcategories only (16,271 rows) vs 32 total subcategories (215,283 rows)

### ML ($12M)
- Ledger $622M vs Cierre $610M (1.9% delta)
- **EXPLAINED:** Cierre formula difference vs flat sum (documented in Phase 14)

## Level 3: Unclassified Rows

| Metric | Value |
|--------|-------|
| Rows with NULL financial_group | 14,560 |
| % of total | 3.6% |
| Potential impact | Unknown |

## Trend vs P30

| Metric | P30 | P32R7 | Delta |
|--------|-----|-------|-------|
| Ledger total | $3.38B | $3.38B | $0 |
| Cierre total | $1.31B | $1.31B | $0 |
| Gap | $2.07B | $2.07B | $0 |
| RIPLEY gap | $1.8B | $1.78B | -$20M |

Data has NOT changed between P30 and P32R7. All deltas are identical.

## Verdict

**FAIL** ❌ — Single Financial Truth is NOT certified. Only Level 1 (Ledger==Clasificado) passes. All 4 MPs have material delta between Ledger and Cierre.
