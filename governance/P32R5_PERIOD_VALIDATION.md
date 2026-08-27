# P32R5 PERIOD VALIDATION

## Validación Independiente Obligatoria (Directiva 7)

Se creó y ejecutó el script `validate_endpoints.py` que recorrió las siguientes combinaciones:

- Marketplaces: `ML`, `Paris`, `Ripley`, `Falabella`
- Periodos: `2025-01`, `2026-01`

### Resultados de la Verificación

1. **Sin Contaminación Cruzada:** 
   Cada llamada a los 4 endpoints (`coverage`, `document-gap`, `risk-summary`, `status`) demostró que los filtros SQL aplican `marketplace` y `periodo` correspondientes en el scope de la request (visto en logs).
2. **Propagación Uniforme:**
   Al omitir `periodo` explícitamente y ejecutar pruebas directas, los endpoints devolvieron estrictamente `"NO DISPONIBLE"`, evadiendo la lectura implícita o global.
3. **Comprobación Cruzada (Exit Gate):**
   - [x] Cobertura heredada eliminada
   - [x] Riesgo infinito eliminado
   - [x] Recomendaciones de otro periodo eliminadas
   - [x] Datos de otro marketplace aislados
   - [x] Caché cruzado evitado
   - [x] SQL con filtro temporal estricto (BETWEEN/>=)
   - [x] Parámetros no ignorados (obligatorios en `DocumentGapEngine` y `DocumentCertificationEngine`)
   - [x] Valores reutilizados nulos

Se verificó que los cuatro endpoints recibieron exactamente el mismo marketplace y periodo en la cascada de llamadas correspondientes a las dependencias inyectadas.
