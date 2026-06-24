# Decisiones Registradas

## DEC-001 — Financial Truth Consolidation

| Campo | Valor |
|-------|-------|
| **ID** | DEC-001 |
| **Fecha** | 2026-06-05 |
| **Título** | Financial Truth Consolidation |
| **RFC Origen** | `governance/RFC_FINANCIAL_TRUTH_CONSOLIDATION.md` |
| **Estado** | APPROVED |

### Decisión
Marketplace Financial reemplaza **Reporte_Gerencial_Marketplaces** como fuente oficial corporativa de verdad financiera.

### Motivación
Existían dos sistemas financieros activos con KPIs de nombre idéntico pero significado y cifras distintas (Ventas, Devoluciones, Cobros, Disponible). Esto generaba múltiples verdades financieras, imposibilitaba la conciliación automática y erosionaba la confianza en los reportes.

La decisión elimina la ambigüedad estableciendo una única fuente certificada con trazabilidad RAW → ETL → Ledger → API → Dashboard.

### Resultado
- Single Financial Truth certificada
- 4 KPIs corporativos definidos con source, fórmula y alcance explícitos
- Reporte_Gerencial_Marketplaces → LEGACY (preservado, no modificado)
- Toda conciliación futura debe realizarse contra Marketplace Financial
- Documentación governance actualizada (CLAUDE.md, TRUTH_CONSOLIDATION_APPROVAL.md, KPI_DEFINITIONS_V1.md)

### Restricciones
- NO modificar código fuente
- NO modificar base de datos
- NO modificar APIs
- NO modificar cálculos financieros
- NO modificar clasificación de datos

### Archivos Relacionados
- `governance/RFC_FINANCIAL_TRUTH_CONSOLIDATION.md`
- `governance/TRUTH_CONSOLIDATION_APPROVAL.md`
- `governance/KPI_DEFINITIONS_V1.md`
- `governance/DECISIONS_LOG.md`
- `CLAUDE.md`
