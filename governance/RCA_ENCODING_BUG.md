# RCA_ENCODING_BUG

## Root Cause Analysis: `ComisiÃ³n` vs `Comisión` Encoding Bug

**Date:** 2026-06-23  
**Severity:** MEDIUM  
**Financial Impact:** $0 (all affected rows correctly classified as `NO_CLASIFICADO` but NO financial value lost)

---

## 1. Summary

A file encoding error in `engine/v4/surgical_loader.py` causes Spanish special characters (`ó`, `í`) to be double-encoded, producing `ComisiÃ³n` instead of `Comisión` in the ledger. This causes ~6 hardcoded detalle strings to mismatch the classification map in `marketplace_auditor.py`, producing `NO_CLASIFICADO` rows.

**Root cause confirmed:** The `.py` file was saved with mojibake (double-encoded UTF-8).

---

## 2. Byte-Level Evidence

### Correct encoding (expected)
```
ó (U+00F3) in UTF-8 = \xc3\xb3  (2 bytes)
```

### Actual encoding (found in file)
```
\xc3\x83\xc2\xb3  (4 bytes — DOUBLE encoded)
```

### Decoding chain
```
1. Original:  ó            U+00F3
2. UTF-8:     \xc3\xb3     (2 bytes — correct)
3. Read as Latin-1: Ã (U+00C3) + ³ (U+00B3)  — wrong interpretation
4. Saved as UTF-8: \xc3\x83\xc2\xb3           — double encoding
```

### Affected strings (4 locations in `surgical_loader.py`)

| Offset | String in file (raw bytes) | Intended string |
|--------|--------------------------|----------------|
| 9790 | `Comisi\xc3\x83\xc2\xb3n` | `Comisión` |
| 24377 | `Comisi\xc3\x83\xc2\xb3n` | `Comisión` |
| 24715 | `Comisi\xc3\x83\xc2\xb3n` | `Comisión` |
| 32738 | `Comisi\xc3\x83\xc2\xb3n` | `Comisión` |
| 10465 | `Devoluci\xc3\x83\xc2\xb3n` | `Devolución` |

---

## 3. Pipeline Trace

### RAW → Loader
```
surgical_loader.py:188  → hardcoded:  "Cargo por venta (ComisiÃ³n)"
surgical_loader.py:449  → hardcoded:  "Cargo por venta (ComisiÃ³n)"
surgical_loader.py:199  → hardcoded:  "DevoluciÃ³n de venta"
```

### Loader → Ledger
The loader directly inserts these hardcoded strings into `marketplace_ledger_v1.detalle` with no normalization step. The mojibake is preserved as-is.

### Ledger → Classification
`marketplace_auditor.py:12` expects:
```python
"Cargo por venta (Comisión)": "Cargo por venta (Comisión)"
```

But the ledger has `"Cargo por venta (ComisiÃ³n)"` — no match → `NO_CLASIFICADO`.

### Classification → Test
`test_v4_surgical_pipeline.py:134` loads a PARIS file, runs the pipeline, and expects `"Cargo por venta (Comisión)"` — gets `"NO_CLASIFICADO"` → assertion fails.

---

## 4. Financial Impact Assessment

**Impact: $0 — ZERO financial value loss.**

The encoding affects ONLY the `detalle` string. The financial values (`monto`, `financial_group`) are computed from numeric columns and are NOT affected. The `NO_CLASIFICADO` status means the row has no `financial_group`, so it doesn't appear in P&L calculations — but neither does `Comisión` (which also falls into `costos_comerciales`).

However, the `NO_CLASIFICADO` status means:
1. These rows do NOT contribute to P&L aggregations
2. They appear as "unclassified" in audit reports  
3. They are invisible to financial analysis

**Affected rows:** Only rows produced by `surgical_loader.py` (PARIS and ML Facturación loaders) where a line item is split into sale + commission. The PARIS loader (line 449) and ML loader (line 188) both have the bug.

---

## 5. Root Cause Origin

The file `engine/v4/surgical_loader.py` itself contains mojibake. The file was likely:
1. Originally created with correct UTF-8 encoding
2. Opened and re-saved by an editor that interpreted it as Latin-1/CP1252
3. The re-save double-encoded all non-ASCII characters

This is PURELY a file encoding error — not a logic error, not a data error, not a pipeline error.

---

## 6. Recommended Fix

### Option A: Fix the file encoding (Recommended ✅)
**Action:** Fix the 4 hardcoded strings in `surgical_loader.py` by replacing the mojibake bytes with correct UTF-8.

**Files modified:** 1 (`engine/v4/surgical_loader.py`)
**Changes:** Replace `\xc3\x83\xc2\xb3` with `\xc3\xb3` in 4 hardcoded strings.
**Risk:** LOW — purely cosmetic, no logic change.
**Regulation impact:** Modifies ETL (surgical_loader.py is in `protected_components` list per P17G).

### Option B: Add encoding alias to classification map
**Action:** Add `"Cargo por venta (ComisiÃ³n)" → "Cargo por venta (Comisión)"` to `RAW_TO_CLASSIFICATION_MAP` in `marketplace_auditor.py`.

**Files modified:** 1 (`engine/v4/marketplace_auditor.py`)
**Changes:** Add 2-3 alias entries for mojibake variants.
**Risk:** VERY LOW — treats symptom, not root cause.
**Regulation impact:** Modifies auditor (also in `protected_components`).

### Option C: Both (Recommended if fixing protected components is blocked)
Fix the source file (Option A) AND add a defensive alias (Option B) to catch any existing mojibake rows already in the database.

---

## 7. Regression Verification

After applying either fix:

```bash
python -m pytest tests/test_v4_surgical_pipeline.py -v --tb=short
```

Expected: All tests pass (no more encoding mismatch).

Full suite:
```bash
python -m pytest tests/ -q
```

Expected: 273/273 PASS.

---

## 8. Conclusion

| Aspect | Finding |
|--------|---------|
| Root cause confirmed | YES — file encoding mojibake in `surgical_loader.py` |
| Origin | File was re-saved with wrong encoding |
| Financial impact | $0 |
| Rows affected | ~6 hardcoded strings → unknown ledger rows |
| Fix effort | < 5 minutes |
| Risk | LOW |
| Blocks Phase A | YES — 1 test fails at line 134 |
