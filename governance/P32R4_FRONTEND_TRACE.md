# P32R4 FRONTEND TRACE

| UI Component | Before (Regresion) | After (Fix) |
|---|---|---|
| **Platform States** | "En Revisión", "Pendiente" | Estrictamente mapeado a: `SIN DATOS`, `PARCIAL`, `CERTIFICADO` |
| **Document Coverage** | Agregaba `%` incluso si no había datos | Si es `"NO DISPONIBLE"`, no agrega `%`. |
| **Tax Risk Metrics** | Renderizaba `0` u oculto | Usa las métricas del backend o `"NO DISPONIBLE"` explícito. |
| **Recommendations** | Hardcoded | Itera sobre `top_risks` del endpoint, o muestra "No existen recomendaciones...". |

### Evidencia
- El frontend ahora *únicamente renderiza*. Toda la lógica y valores predeterminados provienen del Backend.
- Zero regresiones visuales (mismos colores y selectores).
