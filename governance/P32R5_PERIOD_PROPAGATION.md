# P32R5 PERIOD PROPAGATION

## Resumen de Cambios

Se ha centralizado la resolución de periodos en `engine/v4/period_utils.py` mediante la función `_resolve_period_range`. 
Esta función ha sido purificada para cumplir estrictamente con la Directiva 2:
- Nunca infiere fechas de la base de datos.
- Prohíbe el uso de "ALL" o periodos vacíos.
- Retorna tuplas explícitas `(fecha_inicio, fecha_fin, label)`.

## Endpoints Afectados

1. `/api/v4/documentary/coverage`
2. `/api/v4/dte/document-gap`
3. `/api/v4/dte/risk-summary`
4. `/api/v4/electronic_certification/status/{transaction_id}`

Todos los endpoints han sido modificados para requerir y propagar el parámetro `periodo` hacia `DocumentGapEngine` y `DocumentCertificationEngine`.

## Motores Afectados

- `DocumentGapEngine`: `get_document_gaps` y `get_risk_summary` ahora exigen `periodo` y aplican filtros de fecha (`fecha BETWEEN ? AND ?`) usando consultas preparadas (`params`).
- `DocumentCertificationEngine`: Todos sus métodos (`get_all_certifications`, `_certify_paris`, `_certify_ripley`, `_certify_falabella_transaction_chain`, `_certify_direct`) exigen el parámetro `periodo` y aplican los filtros correspondientes a la consulta del ledger.

## Reglas de Disponibilidad (Directiva 6)

Si `periodo` no es provisto o si no existen registros, los sistemas retornan:
- Cobertura: `NO DISPONIBLE`
- Riesgo: `NO DISPONIBLE` / listas vacías
- Recomendaciones: Vacío
- XML: `NO DISPONIBLE`
