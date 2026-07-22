# DEC-022: Financial Engine Authority

**Status**: CERTIFIED  
**Date**: 2026-06-16  
**Author**: System (Phase 11)

## Decision

`engine/v4/domain/financial_engine.py` is declared the **single certified entry point** for all financial data queries. All API endpoints must route through it.

## Rationale

- Eliminates duplicated SQL in api.py (6 MP-specific branches removed, ~220 lines)
- Single point of logic change — reduces regression surface
- All 35 FinancialEngine tests PASS with $0 delta

## Scope

- `LEDGER`: `/api/v4/ledger` → `FinancialEngine.query_ledger()`
- `CIERRE`: `/api/v4/cierre` → `FinancialEngine.query_cierre()`
- `DESGLOSE`: `/api/v4/cierre/desglose` → `FinancialEngine.query_desglose()`
- `COBROS_BREAKDOWN`: `/api/v4/exec/cobros-breakdown` → `FinancialEngine.query_cobros_breakdown()`
- `WATERFALL`: `/api/v4/exec/waterfall` → `FinancialEngine.query_waterfall()`
- `EXEC_SUMMARY`: `/api/v4/exec/summary` → `FinancialEngine.query_exec_summary()`

## Frozen Interface

```python
class FinancialEngine:
    def resolve_period_range(periodo) -> tuple
    def query_ledger(marketplace, periodo, ...) -> dict
    def query_cierre(marketplace, periodo) -> dict
    def query_desglose(marketplace, periodo, exclude_non_operational) -> list
    def query_cobros_breakdown(marketplace, periodo) -> list
    def query_waterfall(marketplace, periodo) -> dict
    def query_exec_summary(marketplace, periodo) -> dict
    def query_audit(marketplace, periodo, ...) -> dict
```

## Rollback

Set `api.py` to use direct SQL (pre-Phase 1 pattern). Not recommended.
