# P32R4 XML TRACE

| Component | Before (Regresion) | After (Fix) | Evidence / Pipeline |
|---|---|---|---|
| Drawer Status (`/api/v4/electronic_certification/status/{id}`) | "PENDIENTE" permanente, valores `null` y `NONE` | "SIN_XML" si no hay XML, Pipeline "NO DISPONIBLE", Evidencia "NO DISPONIBLE" | `marketplace_ledger_v1` (`folio_xml`, `estado_xml`) |
| Hash Generator | Retornaba `None` si no había documento | Retorna `"NO DISPONIBLE"` si no está `CONCILIADO` | Ledger `id_transaccion` |

### Evidencia
- Se previene que un drawer sin XML muestre PENDING infinitamente.
- Se respetan estados `CONCILIADO` y `DOCUMENTADO` usando el hash y pipelines reales.
