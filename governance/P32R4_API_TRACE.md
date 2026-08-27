# P32R4 API TRACE

| Component | Before (Regresion) | After (Fix) | Source Engine |
|---|---|---|---|
| `/api/v4/documentary/coverage` | Retornaba `87.5%`, `92.1%` hardcodeado | Retorna valor de `DocumentCertificationEngine` o `"NO DISPONIBLE"` | `DocumentCertificationEngine` |
| `/api/v4/dte/document-gap` | Retornaba una lista (array) | Retorna diccionario con conteos exactos (`missing_xml_count`, etc.) | `DocumentGapEngine` |
| `/api/v4/dte/risk-summary` | Retornaba lista vacía o sin `risk_levels` | Calcula `risk_levels` dinámico usando `self.gap_taxonomy` | `DocumentGapEngine` |

### Evidencia
- Se eliminaron todos los hardcodes.
- Todo dato no existente retorna explícitamente `"NO DISPONIBLE"`.
