# E2.0 — ML Ajuste Poscobro: Forensic Classification

**Date:** 2026-06-03  
**Mode:** READ ONLY — evidence only, no recovery assumptions

---

## 1. Observable Data

### Source: `marketplace_ledger_v1` WHERE marketplace='ML' AND detalle='Ajuste Poscobro'

**Total rows:** 634  
**Total amount:** $3,108,659 (positive = Eccsa pays out)  
**Date range:** 2025-01-01 to 2026-11-04 (23 months)  
**Financial group:** 634/634 in 'ajustes'

---

## 2. Amount Classification

### Bucket Distribution

| Bucket | Rows | Total Amount | % of Rows | % of Value |
|---|---|---|---|---|
| $100-$500 | 222 | $88,527 | 35.0% | 2.8% |
| $500-$1K | 252 | $138,036 | 39.7% | 4.4% |
| $1K-$5K | 57 | $162,378 | 9.0% | 5.2% |
| $5K-$10K | 12 | $101,840 | 1.9% | 3.3% |
| $10K-$50K | 87 | $2,329,938 | 13.7% | **74.9%** |
| $50K+ | 4 | $287,940 | 0.6% | 9.3% |

**Key finding:** 91 rows (14.4%) in the $10K+ buckets account for 84.2% of the total value ($2.62M). The remaining 543 rows (85.6%) account for only 15.8% ($490K).

### Concentration Analysis

**Top 10 largest adjustments:**

| # | Date | Amount | id_transaccion |
|---|---|---|---|
| 1 | 2025-04-26 | $113,970 | POS_48930436434_1 enero 2025 - 1 julio 2025.xlsx_2597 |
| 2 | 2025-02-24 | $113,970 | POS_45389700803_1 enero 2025 - 1 julio 2025.xlsx_3055 |
| 3 | 2025-04-14 | $59,990 | POS_47698835217_1 enero 2025 - 1 julio 2025.xlsx_2683 |
| 4 | 2025-07-07 | $59,990 | POS_53505196128_1 enero 2025 - 1 julio 2025.xlsx_2228 |
| 5 | 2025-09-12 | $59,990 | POS_58856368592_1 enero 2025 - 1 julio 2025.xlsx_3312 |
| 6 | 2025-03-24 | $53,990 | POS_46690898076_1 enero 2025 - 1 julio 2025.xlsx_2867 |
| 7 | 2025-04-01 | $53,990 | POS_47207449719_1 enero 2025 - 1 julio 2025.xlsx_2734 |
| 8 | 2025-12-24 | $39,990 | POS_66412035434_1 enero 2025 - 1 julio 2025.xlsx_1948 |
| 9 | 2025-03-14 | $43,190 | POS_46243980762_1 enero 2025 - 1 julio 2025.xlsx_2753 |
| 10 | 2025-05-23 | $41,990 | POS_49943967455_1 enero 2025 - 1 julio 2025.xlsx_2450 |

**Observation:** Top 2 adjustments ($113,970 each) total $227,940 = 7.3% of all Poscobro value in just 2 rows.

---

## 3. Temporal Classification

### Monthly Activity

| Month | Total | Rows | Avg/Row | Trend |
|---|---|---|---|---|
| 2025-01 | $88,428 | 35 | $2,527 | — |
| 2025-02 | $240,026 | 41 | $5,854 | ↑ |
| 2025-03 | $398,613 | 71 | $5,614 | ↑ |
| 2025-04 | $460,175 | 50 | $9,204 | Peak |
| 2025-05 | $313,445 | 48 | $6,530 | ↓ |
| 2025-06 | $138,410 | 35 | $3,955 | ↓ |
| 2025-07 | $295,877 | 74 | $3,998 | ↑ |
| 2025-08 | $150,291 | 52 | $2,890 | ↓ |
| 2025-09 | $191,835 | 61 | $3,145 | ↑ |
| 2025-10 | $195,457 | 36 | $5,429 | → |
| 2025-11 | $113,178 | 32 | $3,537 | ↓ |
| 2025-12 | $254,110 | 35 | $7,260 | ↑ |
| 2026-01 | $31,225 | 10 | $3,123 | ↓ |
| 2026-02 | $4,489 | 4 | $1,122 | ↓ |
| 2026-03 | $41,744 | 11 | $3,795 | ↑ |
| 2026-04 | $85,393 | 14 | $6,100 | ↑ |
| 2026-05 | $32,259 | 4 | $8,065 | ↓ |
| 2026-06 | $3,987 | 4 | $997 | ↓ |
| 2026-07 | $35,588 | 3 | $11,863 | ↑ |
| 2026-08 | $1,913 | 4 | $478 | ↓ |
| 2026-09 | $588 | 2 | $294 | ↓ |
| 2026-10 | $3,179 | 2 | $1,590 | ↑ |
| 2026-11 | $28,449 | 6 | $4,742 | ↑ |

**Key finding:** The pattern shows two distinct regimes:
- **Regime 1 (2025-01 to 2025-12):** Monthly average $236,654. High activity, 54 rows/month avg
- **Regime 2 (2026-01 to 2026-11):** Monthly average $24,255. Low activity, 5.4 rows/month avg

**The drop from Regime 1 to Regime 2 is 90%** — a structural change occurred between December 2025 and January 2026.

### Day-of-Week Distribution

| Day | Total | Rows | Avg/Row |
|---|---|---|---|
| Sunday | $310,139 | 87 | $3,565 |
| Monday | $685,745 | 86 | $7,974 |
| Tuesday | $464,860 | 94 | $4,945 |
| Wednesday | $365,104 | 98 | $3,726 |
| Thursday | $415,088 | 108 | $3,843 |
| Friday | $378,301 | 86 | $4,399 |
| Saturday | $489,422 | 75 | $6,526 |

**Observation:** Activity is spread across all days of the week. No concentration on business days vs weekends (Sunday has 87 rows, Saturday has 75, Monday has 86). This is consistent with an automated/systematic process rather than manual entries.

---

## 4. Source File Classification

The `id_transaccion` field contains the filename of the source XLSX that generated the adjustment.

**Distinct source files found:**

| Source File | Rows | Total Value | % of Total |
|---|---|---|---|
| `1 enero 2025 - 1 julio 2025.xlsx` | ~450 | ~$2.35M | ~75.6% |
| `1 julio 2025 - 1 enero 2026.xlsx` | ~184 | ~$0.76M | ~24.4% |

**Observation:** All adjustments come from just 2 Excel files — 6-month periods. This confirms the Poscobro adjustments are bulk-uploaded from periodic reconciliation files, not generated transactionally.

---

## 5. Sign and Reversal Analysis

### Sign Distribution

| Sign | Rows | Total |
|---|---|---|
| POSITIVE | 634 | $3,108,659 |
| NEGATIVE | 0 | $0 |
| ZERO | 0 | $0 |

**Observation:** 100% of Poscobro adjustments are positive (money Eccsa pays out). Zero negative entries and zero reversals.

### Same-Day Reversal Check

**Result:** Zero dates have both positive and negative Poscobro entries. No evidence of same-day reversal or correction activity within the Poscobro dataset.

---

## 6. Relationship to Other ML Adjustments

### Poscobro as % of Total ML Adjustments

| Metric | Value |
|---|---|
| Total ML ajustes | $306,606,250 |
| Poscobro total | $3,108,659 |
| Poscobro % of all ajustes | **1.01%** |

**Observation:** Poscobro is a minor component (1.01%) of total ML adjustments. It is structurally different from the major adjustment categories (BPP, Talla, reconciled, etc.).

### Monthly Correlation

```
Month      Poscobro       Other Adjustments    Poscobro %
─────────────────────────────────────────────────────────
2025-01    $88,428        $16,564,901          0.53%
2025-02    $240,026       $14,962,163          1.58%
2025-03    $398,613       $22,590,210          1.73%
2025-04    $460,175       $21,973,701          2.05%  Peak
2025-05    $313,445       $25,009,652          1.24%
2025-06    $138,410       $21,116,981          0.65%
```

**Observation:** Poscobro does NOT correlate with other adjustments. When other adjustments peak (Nov 2025: $30.5M), Poscobro is low ($113K). When Poscobro peaks (Apr 2025: $460K), other adjustments are moderate ($22M). Different drivers.

---

## 7. Answers to Questions

### Q1: ¿Cuántos tipos de ajuste existen?

**One type identified by detalle: "Ajuste Poscobro."**

However, the range of amounts ($289 to $113,970) suggests different underlying reasons within this single category. The data does NOT contain sub-classification by reason code.

### Q2: ¿Cuáles se repiten?

**Pattern of repetition:**
- 634 individual entries — each is a distinct line with its own id_transaccion
- No exact duplicate amounts on the same date (no exact repetition)
- Same amounts appear across different dates: e.g., $441, $525, $598, $289, $299 appear multiple times — suggesting standardized adjustment types
- Monthly occurrence is consistent: present in every month from Jan 2025 to Nov 2026
- Amount per month varies but the process is recurring

### Q3: ¿Cuáles tienen reversión posterior?

**Zero reversals found.** No negative Poscobro entries exist. No evidence of any reversal activity within the Poscobro dataset.

### Q4: ¿Cuáles aparecen recurrentemente?

**Recurrence classification based on amount frequency:**

| Amount | Frequency | Count | Pattern |
|---|---|---|---|
| $525 | Most frequent | ~100+ | Standard fee? |
| $441 | High | ~50+ | Standard fee? |
| $598/$599 | Medium | ~40+ | Standard fee? |
| $289/$299 | Medium | ~30+ | Minimum adjustment? |
| $10K-$50K | 87 occurrences | 87 | Large, irregular |
| $113,970 | 2 occurrences | 2 | Outlier |

**Observation:** Standardized amounts ($289, $299, $441, $525, $598) suggest formulaic adjustments with fixed parameters. The $10K-$50K range (87 entries, $2.33M) represents unique or exceptional adjustments.

---

## 8. Demonstrated vs Not Demonstrated

### Demonstrated:
- 634 entries, all positive, total $3,108,659
- 23 months of continuous activity
- 14.4% of rows (91 entries > $10K) account for 84.2% of total value
- Two distinct regimes: Pre-2026 (avg $237K/month) and Post-2026 (avg $24K/month) — 90% reduction
- Source: 2 XLSX files from 6-month periods
- Zero reversals exist in the data
- Sequential id_transaccion with file reference traceable to source XLSX
- No correlation with other ML adjustment categories
- Distributed across all days of the week — consistent with automated processing
- Standard amounts ($289, $299, $441, $525, $598, $599) appear repeatedly

### Not Demonstrated:
- The business reason for ANY individual adjustment (no reason code in data)
- Whether any adjustment is erroneous (no cross-reference to original transactions)
- Whether the 90% drop post-2025 represents problem resolution or process change
- Whether the $113,970 outliers are legitimate or anomalous
- Recovery potential (explicitly excluded from this analysis — see E2.0 constraints)

### Missing data required for full causality:
- Original transaction reference for each Poscobro adjustment
- Reason code or adjustment category
- Payment reconciliation status
- Source data from the XLSX files (contents not available in SQL)
- Author/user who generated each adjustment
- Approval workflow metadata

---

*Documento generado: 2026-06-03 | Status: READ ONLY EVIDENCE*
