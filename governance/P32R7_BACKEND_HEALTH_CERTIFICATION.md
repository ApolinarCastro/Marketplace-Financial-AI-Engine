# P32R7 — Backend Health Certification

**Date:** 2026-07-07
**Methodology:** Measured 3-run timing for 11 key API endpoints using FastAPI TestClient

## Endpoint Performance

| Endpoint | Status | Avg (ms) | Min-Max | Size | Notes |
|----------|--------|----------|---------|------|-------|
| `/api/v4/ledger?marketplace=ML&periodo=2026-01` | ✅ 200 | 58.3ms | 25.1-124.6 | 6,856b | |
| `/api/v4/cierre` | ✅ 200 | 37.8ms | 35.8-39.8 | 67,845b | |
| `/api/v4/cierre/desglose?marketplace=ML` | ✅ 200 | 18.1ms | 17.3-19.2 | 7,770b | |
| `/api/v4/exec/summary?marketplace=ALL` | ❌ 500 | — | — | — | CRASHES: `get_period_status('ALL','ALL')` → `resolve_period_range('ALL')` → `int('ALL')` ValueError |
| `/api/v4/exec/waterfall-v3?marketplace=ALL` | — | — | — | — | NOT TESTED (summary crash blocked sequential test) |
| `/api/v4/financial-structure?marketplace=ALL` | — | — | — | — | NOT TESTED |
| `/api/v4/dte/count` | — | — | — | — | NOT TESTED |
| `/api/v4/dte/certify` | — | — | — | — | NOT TESTED |
| `/api/v4/intelligence/insights?marketplace=ML` | — | — | — | — | NOT TESTED |
| `/api/v4/auditoria` | — | — | — | — | NOT TESTED |
| `/api/v4/periodos` | — | — | — | — | NOT TESTED |

## Total Registered Routes: 37

## DB Health

| Metric | Value |
|--------|-------|
| DB Path | `data/db/meli_financial_v4.db` |
| DB Size | 125 MB (SHA256 verified) |
| Tables | 25 |
| Ledger rows | 402,089 |
| Ledger total | $3,381,794,665.45 |
| Clasificado rows | 402,089 (same as ledger) |
| Clasificado total | $3,381,794,665.45 ($0 delta ✅) |
| Cierre periods | 246 |
| Date range | 2025-01-01 to 2026-12-06 |

## Financial Groups (7 types)

| Group | Coverage |
|-------|----------|
| ingresos | All 4 MPs |
| devoluciones | All 4 MPs |
| costos_operacionales | All 4 MPs |
| costos_comerciales | FALABELLA, ML, PARIS, RIPLEY |
| ajustes | ML, PARIS, RIPLEY |
| recuperaciones_y_bonificaciones | ML only |
| tesoreria | RIPLEY only |

## Critical Bug Found

**`/api/v4/exec/summary?marketplace=ALL` crashes** because:
1. `get_period_status('ALL', None)` is called
2. `None or 'ALL'` → `periodo='ALL'`
3. `_build_ledger_where('ALL', 'ALL')` calls `resolve_period_range('ALL')`
4. `map(int, 'ALL'.split('-'))` → `ValueError`

This is a real regression in `get_period_status` (financial_engine.py:306)

**Impact:** The Executive Dashboard's summary endpoint is unreachable for `marketplace=ALL` (the default).

## Verdict

**DEGRADED** ⚠️ — 1 endpoint crashes, 10 not fully tested due to crash halting sequential execution. The crash is a real bug, not environment-specific.
