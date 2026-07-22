# Paris Regression Root Cause Analysis

## 1. Problem Description
During Phase 16 stabilization, a regression was identified in the Paris ingestion pipeline. Net settlement values ("MONTO A PAGAR") were written directly into the `monto` column of `marketplace_ledger_v1` without splitting them into gross transaction revenue and marketplace commission. This distorted the gross sales metrics.

## 2. Root Cause Analysis
- **Standalone Ingestion Script**: The standalone loader inside `run_initial_audit.py` did not implement the dual-row splitting model. Instead, it fallback-mapped the Excel records by writing the net amount into the `monto` column.
- **Aggregation Column Logic**: The closing query for Paris had to coalesce columns such as `monto_bruto` and `comision_marketplace`, which added non-standard complexity and deviated from the universal closing query pattern.
- **Violated Constraint**: The gross revenue was originating from the settlement values rather than transaction gross values, violating the Single Financial Truth constraint.

## 3. Resolution
- **Unified Loading**: Standalone ingestion was fully retired and delegated to `SurgicalLoader().load_marketplace('PARIS')`.
- **Anatomic Splitting**: The loader parses raw spreadsheet rows and emits two separate ledger rows for each order: one gross row (`_GROSS`) with `monto = monto_bruto` (mapped to `ingresos`) and one commission row (`_COMM`) with `monto = comision_marketplace` (mapped to `costos_comerciales`).
- **Standardized Closures**: Paris's closing aggregation now uses the standard universal closing query, resolving all deltas.

---
**Verified by:** Antigravity AI Auditor Engine  
**Status:** SOLVED
