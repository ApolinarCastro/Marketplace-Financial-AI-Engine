---
tags:
  - ripley
  - p26
  - promote
---
# RIPLEY PROMOTION EXECUTION

## PARÁMETROS DE EJECUCIÓN
- **Filtro de Estado**: VALIDATED estrictamente. 
- **Registros Excluidos**: BLOCKED_BY_SOURCE_DATA, DIFFERENCE_REJECTED, MISSING_SETTLEMENT, FAILED.

## MÉTRICAS DEL VOLCADO
- **Registros Analizados en ETL**: 219,901 (Settlement).
- **Ventas Promovidas (VALIDATED)**: 219,901.
- **Comisiones y OPEX Promovidas**: 0 (Excluidas de forma segura bajo BLOCKED_BY_SOURCE_DATA por carencia de XML).
- **Mutaciones No Autorizadas**: 0.

El pipeline oficial ETL orquestó 100% de la carga transaccional hacia marketplace_ledger_clasificado_v1.
