# P32R5 SQL LOG

## Auditoría SQL

Se ha implementado la Directiva 4 utilizando el módulo `logging` de Python en `engine/v4/period_utils.py` (`log_sql_audit`).

### Características
- **No invasivo:** No devuelve información de auditoría al frontend en el payload JSON.
- **Trazabilidad total:** Registra `endpoint`, `marketplace`, `periodo`, `SQL ejecutado`, `parámetros`, `cantidad de registros` y `tiempo de ejecución (ms)`.

### Ejemplo de Salida (marketplace_audit_sql.log)

```log
2026-07-07 14:46:36,440 - [ENDPOINT: /api/v4/documentary/coverage] [MARKETPLACE: RIPLEY] [PERIODO: 2025-01] [TIEMPO_MS: 608.45] [FILAS: 1] [SQL: SELECT 
                COALESCE(SUM(ABS(monto)), 0) as total_monto,
                COALESCE(SUM(CASE 
                    ... 
                END), 0) as monto_cert
            FROM marketplace_ledger_v1
            WHERE LOWER(marketplace) = 'ripley'
              AND financial_group IN ('costos_comerciales', 'costos_operacionales', 'ajustes')
              AND l.fecha BETWEEN ? AND ?] [PARAMS: ['2025-01-01', '2025-01-31']]
```
