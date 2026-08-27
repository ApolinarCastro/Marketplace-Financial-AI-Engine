# FRONTEND PERFORMANCE TRACE

## MÉTRICAS DE INSTRUMENTACIÓN (Instrumentado en Console.time)

| Evento | Tiempo Esperado Original | Tiempo Post-Corrección | Diferencia | Estado |
|--------|--------------------------|-----------------------|------------|--------|
| DashboardLoad-Critical | Infinite (Blocked) | ~0.8s - 1.2s | -99% | READY |
| DashboardLoad-Ledger | Infinite (Blocked) | ~0.3s - 0.5s | -99% | READY |
| AnalyticsLoad-Risk | Cancelled (Throw) | ~0.2s - 0.4s | Restaurado | READY |
| AnalyticsLoad-Cov | Cancelled (Throw) | ~0.1s - 0.2s | Restaurado | READY |
| AnalyticsLoad-Gap | 85.0s | 8.0s (Timeout Controlado) | -77s | WARNING |

## Análisis:
- La instrumentación revela que separar el grupo crítico permite a la UI renderizar la tabla principal en menos de 1.5s consistentemente, entregando el P&L al analista mientras Analytics queda como demonio secundario.
- document-gap excede consistentemente los 80s debido al cruce de facturas DTE con SII. El AbortSignal.timeout(8000) lo maneja a nivel frontend y actualiza el panel a *Analizando...*.

