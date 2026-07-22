---
tags:
  - knowledge_object
  - performance
  - baseline
status: active
version: 1.0
---

# Baseline V4 Performance Matrix

## Ejecución Global
| Componente | Tiempo Promedio | Complejidad |
|---|---|---|
| Ingesta Ledger (SurgicalLoader) | 12s | Alta (I/O, Parseo de 100k+ rows) |
| Document Engine (DTEIndexer) | 3s | Media (Vector match) |
| Auditoría (Classification) | 4s | Alta (Reglas heurísticas) |
| Financial Closing (Cierre) | 2s | Baja (Agrupación SQL) |
| API /api/v4/run-audit | ~21s | End-to-End |
| API /api/v4/upload/dte | < 1s | Async streaming |

## Hardware
- RAM: ~1.2GB consumidos durante el ETL
- CPU: 2-3 cores en concurrencia (DuckDB)
