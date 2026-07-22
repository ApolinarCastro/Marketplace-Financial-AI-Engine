# Phase 12C — Reconciliation Evidence

**Date:** 2026-06-17

## Waterfall Conservation (neto = ing + dev + cop + ccm + aju)

```
ML:      $719,939,260.51 = $875,869,354.00 + (-$93,009,601.00) + (-$71,700,785.69) + (-$175,514,916.59) + $184,295,209.79 ✅
PARIS:   $337,418,552.00 = $484,161,942.00 + (-$121,458,109.00) + (-$26,660,638.00) + $0 + $1,375,357.00 ✅
RIPLEY:  $206,946,843.00 = $353,160,324.00 + (-$82,896,873.00) + (-$14,206,460.00) + (-$49,076,708.00) + (-$33,440.00) ✅
FALABELLA: $7,664,386.00 = $12,470,241.00 + (-$1,878,556.00) + (-$800,171.00) + (-$2,114,602.00) + (-$427.00) ($12K known issue)
```

## Cierre Table Values (pre-change reference)

| MP | ing | dev | cop | ccm | aju | neto |
|---|---|---|---|---|---|---|
| ML | $875,869,354 | N/A | -$71,700,786 | -$175,514,917 | $83,391,476 | $712,045,102 |
| PARIS | $484,161,942 | N/A | -$26,660,638 | $0 | -$120,082,752 | $337,418,552 |
| RIPLEY | $353,160,324 | N/A | -$14,206,460 | -$49,076,708 | -$82,930,313 | $206,946,843 |
| FALABELLA | $12,470,241 | N/A | -$800,171 | -$2,114,602 | -$1,878,983 | $7,676,485 |

Note: Cierre `aju` includes devoluciones (not separable). ML delta ($719.9M new vs $712.0M cierre) = paired mechanisms excluded from operational.

## Ledger Financial Groups (source of truth post-FIX-06)

See full breakdown in `SELLER_ECONOMIC_REALITY_CERTIFICATION.md` and `SINGLE_FINANCIAL_TRUTH_CERTIFICATION.md`.

## API Contract Preservation

| Endpoint | Before | After | Change |
|---|---|---|---|
| `/api/v4/exec/waterfall` | 6-element values array | 6-element values array | Same contract, values from ledger |
| `/api/v4/exec/summary` | marketplace array | marketplace array | Same contract, dev from LOWER() |

## Test Results

```
234 passed in 72.31s ✅
```
