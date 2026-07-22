# P32R4 DOCUMENT TRACE

| Component | Before (Regresion) | After (Fix) | Source Engine |
|---|---|---|---|
| Document Coverage | Hardcoded "87.5%" | Mapeo 1:1 desde `DocumentCertificationEngine` por marketplace | `DocumentCertificationEngine` |
| Tax Risk | "Cargando riesgos..." (ausencia de objeto `risk_levels`) | Cálculo dinámico sumando severidad de `gaps` (CRÍTICO, ALTO, MEDIO) | `DocumentGapEngine` |
| Gaps (Missing/Invalid) | Variables `undefined` (`gapRes.missing_xml_count`) en frontend | Retorno unificado de conteos (ej. `missing_xml_count`) desde backend | `DocumentGapEngine` |
| Recommendations | Hardcoded "No backend source available" | Consumo de `top_risks` desde `get_risk_summary()` del motor | `DocumentGapEngine` |

### Evidencia
- Se consumen motores existentes sin duplicación.
- Los valores de cobertura y riesgo son 100% dinámicos y dependientes de la base de datos real.
