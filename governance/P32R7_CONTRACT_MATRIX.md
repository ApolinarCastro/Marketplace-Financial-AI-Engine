# P32R7 CONTRACT MATRIX

## Matriz de Contratos End-to-End

| Capa | Endpoint / Interfaz | Contrato Esperado | Contrato Recibido | Contrato Renderizado |
|---|---|---|---|---|
| Engine -> API | `DatabaseV4.get_ledger()` | `List[Dict]` estructurado | Cumple | N/A |
| API -> Frontend | `GET /api/v4/ledger` | JSON Array (id, monto, etc) | Cumple | Cumple (Tabla/Lista) |
| API -> Frontend | `GET /api/v4/summary` | JSON Object (métricas agregadas) | Cumple | Cumple (Tarjetas) |

**Conclusión:** Todos los contratos se respetan de manera estricta sin mutaciones indeseadas.
