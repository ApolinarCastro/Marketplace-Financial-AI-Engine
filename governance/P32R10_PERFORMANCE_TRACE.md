# P32R10 — PERFORMANCE TRACE

## End-to-End Timing (DuckDB V1.5.1, Windows)

### Pre-Fix (2026-06-19)

```
exec/summary: 16,000–23,000ms
```

### Post-Fix (2026-06-19)

```
exec/summary:       23–24ms   ✅ PASS (<500ms)
query_waterfall:     2–5ms
query_exec_summary:  3–8ms
get_executive_breakdown: 18–42ms
query_desglose:      1–8ms
get_risk_summary:    20–27ms
```

## Breakdown por Componente

### SQL Puro (DuckDB)

| Consulta | Tiempo |
|----------|--------|
| MAX(periodo_inicio) | 0.7ms |
| SUM(CASE...) per group | 3.5ms |
| GROUP BY marketplace | 5.0ms |
| COUNT(*) | 2.0ms |
| GROUP BY financial_group | 3.1ms |
| Risk counts (SQL-only) | 3–8ms |

### Engine

| Método | Tiempo |
|--------|--------|
| `get_executive_breakdown` | 18–42ms (depende de señal RIPLEY) |
| `get_risk_summary` | 20–27ms |
| `_build_signal_filter` (cached) | ~0ms (1ra llamada: ~2ms) |

### File I/O (ELIMINADO)

| Operación | Tiempo Pre-Fix |
|-----------|---------------|
| glob('01_Raw/Falabella/*.xlsx') + read_excel | ~8,000ms |
| glob('01_Raw/Ripley/SELLER/*.xlsx') + read_excel | ~6,000ms |
| glob('01_Raw/Ripley/Ciclos/*.csv') + read_csv | ~5,000ms |
| **Total file I/O** | **~19,000ms** |

## Cuello de Botella Principal

**100% del tiempo pre-fix era file I/O en `DocumentGapEngine.get_document_gaps()`.**

Las consultas SQL individuales nunca fueron el problema (<5ms cada una). El problema era que `get_risk_summary()` → `get_document_gaps()` leía docenas de archivos Excel/CSV desde disco en cada request.

## Verificación de Conservación

| Endpoint | Relación | Delta |
|----------|----------|-------|
| waterfall neto = ledger neto | Conservación exacta | $0 |
| exec summary neto = ledger neto | Conservación exacta | $0 |
| waterfall neto = exec summary neto | Conservación exacta | $0 |
| financial-structure ≠ ledger neto | JOIN-based, esperado | Ver SFT_RECONCILIATION |

## Exit Gate Compliance

| Criterio | Estado |
|----------|--------|
| exec/summary < 500ms | **PASS** (24ms) |
| 0 consultas SQL duplicadas | **PASS** |
| 0 loops innecesarios | **PASS** (per-MP loop → GROUP BY) |
| 0 recalculaciones | **PASS** (certificaciones compartidas) |
| Consistencia funcional EB-WF-LD | **PASS** ($0 delta, ver SFT_RECONCILIATION.md) |
