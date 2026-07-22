# BPP Residual Fix Report

**Date:** 2026-06-06
**Classification:** PASS — residual eliminated
**Reference:** governance/BPP_RESIDUAL_CERTIFICATION.md

---

## Summary

Applied surgical fix to `marketplace_auditor.py:420` — added 4 missing BPP detalle patterns to `ml_mandatory_exclusions` that were previously undocumented.

## Fix Applied

**File:** `engine/v4/marketplace_auditor.py:420-430`

Added (4 patterns):
- `"bpp_covered"` — 37 rows, $921,722
- `"partially_bpp_refunded"` — 5 rows, $263,920
- `"ppv_covered_melienvio"` — 4 rows, $111,960
- `"ppv_valid"` — 1 row, $39,990

Zero existing rules modified. Zero root events touched.

## Results

| Metric | Before | After | Delta |
|---|---|---|---|
| BPP rows visible (global) | 47 ($1,337,592) | 0 ($0) | -$1,337,592 |
| BPP rows visible (ML 2026-01) | 3 ($58,970) | 0 ($0) | -$58,970 |
| ML RN | $712,045,128 | $712,045,128 | $0 |
| Root events visible | 5,260 rows | 5,260 rows | 0 |
| 30/30 tests | PASS | PASS | — |

## Snapshot

Pre-fix: `snapshot_pre_bpp_residual_fix_20260606_145106/` (SHA256 `e8202cb4`)
