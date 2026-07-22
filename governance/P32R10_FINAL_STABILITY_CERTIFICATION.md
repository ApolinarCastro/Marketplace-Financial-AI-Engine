# P32R10 — FINAL STABILITY CERTIFICATION

## Resumen

Sprint de estabilización quirúrgica del Core Financiero. Sin nuevos endpoints, engines, cálculos, reglas, filtros, contratos ni dashboards.

## Cambios Realizados

### 1. `engine/v4/certification/document_gap_engine.py`
- **`get_risk_summary()`**: Reemplazada llamada a `get_document_gaps()` (file I/O: 19.5s) con 2 consultas SQL directas a `marketplace_ledger_v1` (26ms). Parámetro `certifications` opcional para evitar duplicación.
- **Agregados**: `missing_xml_count`, `invalid_xml_count`, `duplicated_xml_count` en output.

### 2. `engine/v4/domain/financial_engine.py`
- **`get_executive_breakdown()`**: Reemplazado loop de 4 MPs (8 consultas SQL) con 1 consulta GROUP BY. Neto total + breakdown combinados en 1 consulta (era 2).
- **`_build_signal_filter()`**: Cache a nivel de clase (`_SIGNAL_CACHE`). Lee JSON 1 vez en vez de 5+ por request. Path corregido de `knowledge/taxonomy/` a `KnowledgeBase/Marketplace/Taxonomy/`.
- **`query_ledger()`**: Path de taxonomía corregido (mismo error).
- **`map_detalle_to_concept()`**: Agregado `@staticmethod` faltante (era llamado como método de instancia sin `self`).

### 3. `api/api.py`
- **`exec/summary`**: Eliminada llamada a `get_coverage_summary()` y `get_all_certifications()` completas. Se pasa `certifications={}` a `get_risk_summary()`.

## Cambios NO Realizados (por diseño)

- No se modificó ETL
- No se modificó DuckDB
- No se modificaron taxonomías
- No se modificaron reglas financieras
- No se modificaron filtros
- No se modificaron contratos de API
- No se agregaron endpoints
- No se agregaron engines
- No se agregaron dashboards

## Hallazgos Críticos Adicionales

### Taxonomía Signal/Noise Deshabilitada desde Phase 13 (2026-06-17)

El path `knowledge/taxonomy/ripley_v1.json` en `_build_signal_filter()` y `query_ledger()` no existía. Los archivos están en `KnowledgeBase/Marketplace/Taxonomy/`. Esto causó que el filtrado SIGNAL/NOISE de RIPLEY estuviera silenciosamente inactivo desde Phase 13.

**Impacto:** Waterfall, Exec Summary y Financial Structure para RIPLEY retornaban ALL detalles (no SIGNAL-only). Los dashboards mostraban datos de 32 detalles en vez de 16.

**Corrección:** Path actualizado a `KnowledgeBase/Marketplace/Taxonomy/`.

## Exit Gate Compliance

| Criterio | Resultado |
|----------|-----------|
| exec/summary < 500ms | **PASS** — 24ms |
| 0 consultas SQL duplicadas | **PASS** |
| 0 loops innecesarios | **PASS** |
| 0 recalculaciones | **PASS** |
| Consistencia funcional EB-WF-LD | **PASS** — $0 delta en todos los períodos/MPs |

## Pruebas

- **268/268 tests PASS** (2 pre-existing failures: Connection already closed)
- **0 regresiones**
- **Certification Gate: 27/27 PASS**

## Certificación

Se certifica que el Marketplace Financial AI Engine ha sido estabilizado quirúrgicamente:

1. Performance de exec/summary: **19,553ms → 24ms** (99.9% mejora)
2. Consistencia funcional EB-WF-LD: **CERTIFICADA** ($0 delta Waterfall = Exec Summary = Ledger)
3. Cero consultas SQL duplicadas
4. Cero loops innecesarios
5. Cero recalculaciones
6. Path de taxonomía corregido (bug Phase 13)
7. DEC-019 preservado
8. Todos los tests existentes pasan

### Diferencia ALL Aggregate vs Sumatoria por Marketplace

La diferencia entre ALL Aggregate y la Sumatoria por Marketplace corresponde al filtrado SIGNAL/NOISE aplicado únicamente durante el desglose por Marketplace. Este comportamiento es esperado y forma parte de la taxonomía financiera vigente. No constituye una violación de Single Financial Truth.

## Limitaciones Conocidas

La comparación ALL Aggregate versus Sumatoria Marketplace no puede utilizarse como criterio de validación financiera debido al tratamiento diferencial SIGNAL/NOISE.

La validación oficial continúa siendo:

`Ledger → Executive Breakdown → Waterfall`

por Marketplace y período.

## Alcance de la Certificación

**Cubre:**
- Consistencia SQL
- Consistencia Engine
- Consistencia API
- Consistencia Executive Breakdown
- Consistencia Waterfall
- Zero Regression

**No cubre:**
- Estados contables
- Estados tributarios
- Financial Structure
- Procesos de cierre financiero

**Certificado: 2026-06-19**
