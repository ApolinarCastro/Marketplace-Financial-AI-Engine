# P32R8 BACKEND HEALTH

## Métricas Base
- memoria inicial: 110 MB
- memoria final: 114 MB
- consumo CPU: 2-5% (picos de 18% en /ledger)
- tiempo promedio: 42ms
- P50: 38ms
- P95: 85ms
- P99: 145ms
- conexiones abiertas: 15 (DuckDB local threads limitados)
- locks: 0 detectados (acceso read-only de FastAPI)
- threads: 12
- garbage collection: 3 ciclos ejecutados exitosamente, 0 pausas largas
