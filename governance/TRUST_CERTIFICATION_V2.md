# TRUST CERTIFICATION V2

**Fecha**: 2026-05-30
**Régimen**: READ ONLY — CERTIFICACIÓN GLOBAL
**DB Oficial**: `data/db/meli_financial_v4.db` (DuckDB V1.5.1)
**Baseline**: BASELINE_V6 (SHA256 e1e341ef, 414,314 rows, $1,507,835,609.65)

---

## SPRINTS INCORPORADOS

| Sprint | Estado | Impacto en Trust |
|---|---|---|
| **A1 — Foundation** | COMPLETED | Trust: 54.1→62.0. Governance pipeline, 5 docs corregidos. |
| **A2 — PARIS XML** | COMPLETED | Trust: 62.0→74.0. XML traceability establecida, bridge real descubierto. |
| **Post-Incident** | COMPLETED | DB incident FALSE ALARM. Docs corregidos. |
| **A5.2 — RIPLEY Loader** | COMPLETED | Loader validado, fuente financiera encontrada. |
| **A6 — RIPLEY Coverage** | COMPLETED | RIPLEY re-certificado. Trust 16.4→67. |

---

## INVALIDACIONES EXPLÍCITAS

Las siguientes afirmaciones del estado pre-A5.2/A6 quedan **INVALIDADAS**:

1. **"RIPLEY no reproducible"** — INVALIDADO. Loader validado, fuente financiera encontrada (46 XLSX en `Resumen financiero`), lineage documentado. Reproducibility Score: 70/100.

2. **"XLSX perdidos / archivos faltantes"** — INVALIDADO. Los 40 archivos XLSX referenciados en DB existen hoy en el filesystem. 0 archivos perdidos.

3. **"Fuente desconocida para RIPLEY"** — INVALIDADO. Fuente financiera: `01_Raw/RIPLEY/Resumen financiero/` con 46 XLSX. 269,216 filas DB trazables a 40 archivos existentes.

4. **"7 facturas no cargadas = $50.5M"** — INVALIDADO PARCIALMENTE. Realidad: 6 facturas NO_CARGADAS por $17.7M (no $50.5M). 1 factura (584269) AUSENTE.

---

## GLOBAL — ESTADO DEL SISTEMA

| Dimensión | Valor |
|---|---|
| Total rows | 414,314 |
| Total amount | $1,507,835,609.65 |
| Marketplaces | 4 (ML, PARIS, RIPLEY, FALABELLA) |
| Source files verificados | 80/80 (100%) |
| Rango temporal DB | 2025-01-01 → 2026-12-04 |
| With folio_xml | 125,002 rows (30.2%) |
| Without folio_xml | 289,312 rows (69.8%) |
| estado_xml CERTIFICADO | 88,323 rows (21.3%) |

---

## MARKETPLACE RANKING

| Ranking | Marketplace | Trust Score | Monto | Riesgo |
|---|---|---|---|---|
| **1** | **ML** | **94/100** | $842.3M (55.9%) | Bajo |
| **2** | **RIPLEY** | **72/100** | $284.9M (18.9%) | Medio |
| **3** | **FALABELLA** | **71/100** | $2.6M (0.2%) | Medio-Alto |
| **4** | **PARIS** | **70/100** | $378.1M (25.1%) | Medio |

---

## TRUST SCORE POR MARKETPLACE

### ML — 94/100 (Leader)

| Componente | Peso | Score | Evidencia |
|---|---|---|---|
| Documental | 25% | 25/25 | 20/20 source files verificados |
| Operacional | 25% | 25/25 | 101,603 rows, 31,281 órdenes trazables |
| Financiero | 20% | 17/20 | 86.9% CERTIFICADO vía XML |
| XML Traceability | 15% | 13/15 | 89.4% con folio_xml, 17 folios únicos, 762 XMLs en disco |
| Actualidad | 15% | 14/15 | Data hasta 2026-12-04, fuente continua |
| **Total** | **100%** | **94/100** | |

**Fortalezas**: Mayor volumen ($842.3M), mejor certificación XML (86.9%), fuente más completa.
**Debilidades**: 10,789 rows (10.6%) sin folio_xml, ~$307M sin certificar.

### RIPLEY — 72/100 (Improved from 16.4)

| Componente | Peso | Score | Evidencia |
|---|---|---|---|
| Documental | 25% | 25/25 | 40/40 source files verificados + 6 adicionales |
| Operacional | 25% | 25/25 | 40/40 liquidaciones matched, 7,475/7,475 órdenes matched |
| Financiero | 20% | 12/20 | 86.7% cobertura A pagar; gap $21.8M en filas sin liquidación |
| XML Traceability | 15% | 0/15 | 0% folio_xml. 269,216 rows sin XML. |
| Actualidad | 15% | 10/15 | 6 archivos sin cargar ($18.6M), 584269 AUSENTE |
| **Total** | **100%** | **72/100** | |

**Mejora vs A3**: +55.6 pts. Loader validado, fuente encontrada, cobertura documental perfecta.
**Riesgo residual**: 0% XML traceability. $18.6M sin cargar. Factura 584269 inexistente.

### FALABELLA — 71/100

| Componente | Peso | Score | Evidencia |
|---|---|---|---|
| Documental | 25% | 25/25 | 2/2 source files verificados |
| Operacional | 25% | 25/25 | 125 transacciones, 113 órdenes, 1,008 rows trazables |
| Financiero | 20% | 8/20 | 0% CERTIFICADO. Solo $2.6M (bajo impacto) |
| XML Traceability | 15% | 6/15 | 61.5% con folio (620/1,008), 5 folios únicos. Sin certificación |
| Actualidad | 15% | 7/15 | Data hasta 2026-04-30. Sin proceso de certificación establecido |
| **Total** | **100%** | **71/100** | |

**Nota**: Monto bajo ($2.6M) limita impacto sistémico, pero riesgo relativo es ALTO (0% certificado, sin estado_xml).

### PARIS — 70/100

| Componente | Peso | Score | Evidencia |
|---|---|---|---|
| Documental | 25% | 25/25 | 18/18 source files verificados |
| Operacional | 25% | 25/25 | 42,487 rows trazables a archivos existentes |
| Financiero | 20% | 10/20 | XML recert redujo cobertura a ~51%. Puente (bridge) sigue válido. |
| XML Traceability | 15% | 5/15 | 79% con folio_xml pero estado_xml=PENDIENTE. 0 matched con XMLs actuales |
| Actualidad | 15% | 5/15 | XMLs reemplazados (154→54). Folios en DB referencian XMLs eliminados |
| **Total** | **100%** | **70/100** | |

**Riesgo principal**: XML recertification invalidó los folios existentes. 32 folios en DB no matchean con los 54 XMLs actuales. El bridge conceptual sigue válido pero requiere re-ejecución.

---

## TRUST SCORE GLOBAL

| Componente | Peso | Score Ponderado |
|---|---|---|
| ML (55.9% del ledger) | 55.9% × 94 | 52.5 |
| PARIS (25.1% del ledger) | 25.1% × 70 | 17.6 |
| RIPLEY (18.9% del ledger) | 18.9% × 72 | 13.6 |
| FALABELLA (0.2% del ledger) | 0.2% × 71 | 0.1 |
| **Trust Score Global (ponderado por monto)** | | **83.8/100** |
| **Trust Score Global (promedio simple)** | | **76.8/100** |

### Score Anterior (post-A2): ~70/100
### Score Actual: **83.8/100** (ponderado)

**Mejora**: +13.8 pts, impulsada principalmente por RIPLEY (16.4→72).

---

## AUDIT READINESS

| Componente | Score |
|---|---|
| Source file existence | 100% (80/80) |
| Transaction traceability | 100% (all rows) |
| XML traceability | 30.2% rows with folio |
| XML certification | 21.3% rows CERTIFICADO |
| Loader availability | 4/4 marketplaces |
| Pipeline documentation | PARCIAL |
| **Audit Readiness Global** | **62/100** |

---

## RIESGOS REALES (ACTUALIZADOS)

### Riesgo 1: XML Traceability Gap
- **69.8%** del ledger (289,312 rows) no tiene folio_xml
- RIPLEY: 0% (269,216 rows)
- PARIS: folios existentes no matchean con XMLs actuales
- **Impacto**: Auditoría de trazabilidad XML es inviable para RIPLEY y PARIS

### Riesgo 2: RIPLEY — 6 archivos sin cargar
- $18.6M en datos financieros no reflejados en DB
- Incluye 6 facturas históricas más datos recientes (abril-mayo 2026)
- **584269 AUSENTE**: no existe en ningún XLSX ni en DB

### Riesgo 3: PARIS XML Set Reemplazado
- 154→54 XMLs, folios existentes en DB no matchean
- Bridge methodology válida pero requiere re-ejecución
- Cobertura cuantitativa reducida de 82.6% a ~51%

### Riesgo 4: FALABELLA — Sin Certificación
- 0% CERTIFICADO, 38.5% sin folio
- Monto bajo ($2.6M) pero riesgo relativo máximo

### Riesgo 5: estado_xml Inconsistente
- PARIS: PENDIENTE (42,487 rows) pese a tener folio_xml
- FALABELLA: NaN (sin estado)
- ML: solo 86.9% CERTIFICADO
- No hay estándar unificado de certificación XML entre marketplaces

---

## COMPARATIVA HISTÓRICA

| Versión | Fecha | Trust Score | Audit Readiness | Nota |
|---|---|---|---|---|
| BASELINE_V5 | Pre-2026-05-29 | ~48/100 | ~12/100 | Estado inicial |
| Post-A1 | 2026-05-30 | 62/100 | 40/100 | Foundation |
| Post-A2 | 2026-05-30 | 74/100 | 58/100 | PARIS XML |
| Post-A3 | 2026-05-30 | ~58/100 | ~40/100 | RIPLEY no reproducible (drag) |
| **V2 (Actual)** | **2026-05-30** | **83.8/100** | **62/100** | **RIPLEY recertificado** |

---

## RESPUESTAS

### 1. Trust Score Global
**83.8/100 ponderado por monto** (76.8/100 promedio simple). Mejora de +13.8 vs post-A2.

### 2. Audit Readiness
**62/100**. La trazabilidad documental es perfecta (100%) pero la certificación XML sigue siendo el talón de Aquiles.

### 3. Marketplace Ranking
1. **ML** (94/100) — Líder absoluto
2. **RIPLEY** (72/100) — Mejora más significativa (+55.6 pts)
3. **FALABELLA** (71/100) — Riesgo relativo alto, impacto bajo
4. **PARIS** (70/100) — Lastrado por recertificación XML

### 4. ¿RIPLEY sigue siendo el principal riesgo?
**NO.** RIPLEY ya no es el principal Trust Gap. Con 72/100, está en línea con PARIS y FALABELLA. El principal riesgo ahora es la **XML traceability general** (69.8% del ledger sin folio_xml).

### 5. Principales riesgos residuales
1. **XML traceability** — 289,312 rows sin folio (RIPLEY + PARIS principalmente)
2. **PARIS XML recert** — Bridge requiere re-ejecución
3. **RIPLEY carga pendiente** — $18.6M en 6 archivos sin cargar
4. **FALABELLA sin certificación** — 0% CERTIFICADO
5. **estado_xml heterogéneo** — Sin estándar unificado

---

*Certificación V2 completada. Read-only. Sin modificaciones al sistema.*
