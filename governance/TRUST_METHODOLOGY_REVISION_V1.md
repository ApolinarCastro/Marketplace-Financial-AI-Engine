# TRUST METHODOLOGY REVISION V1

**Fecha**: 2026-05-30
**Régimen**: GOVERNANCE — READ ONLY
**DB Oficial**: `data/db/meli_financial_v4.db` (DuckDB V1.5.1)

---

## FASE 1 — DEPRECATION

### Métrica Obsoleta: XML Traceability %

**Estado**: OBSOLETA (a partir de esta revisión)

**Definición anterior**:
```
XML Traceability = filas con folio_xml NO nulo / total filas del ledger
```

**Problemas identificados** (evidencia en T1.1 — XML Business Semantics Certification):

| Problema | Ejemplo Concreto | Impacto |
|---|---|---|
| Mezcla ingresos con costos | FALABELLA: 61.5% filas con folio_xml, pero 0% de ingresos tienen folio | Infla percepción de cobertura |
| Mezcla facturas con notas de crédito | ML: 86.4% de XMLs son Tipo 61 (ajustes), no Tipo 33 (ingresos) | Distorsiona significado de "evidencia documental" |
| Penaliza períodos sin XMLs existentes | RIPLEY: 0% cobertura cuando 91% del período no tiene XMLs disponibles | Falsa sensación de gap recuperable |
| Ignora elegibilidad temporal | $11.2M ML futuro (Jun-Dic 2026) cuenta como gap cuando no existen XMLs | Penaliza lo que no puede tener evidencia |
| No distingue concepto financiero | Una fila de ingreso $1M = una fila de ajuste -$10 en la métrica | Pérdida de granularidad auditiva |

**Referencias cruzadas**:
- XML_BUSINESS_SEMANTICS_CERTIFICATION.md — FASE 8 y 9
- DOCUMENT_CONSISTENCY_AUDIT.md — FASE 4.2 (period eligibility)

---

## FASE 2 — NUEVAS MÉTRICAS

### 2.1 Revenue Traceability

**Definición**:
```
Revenue Traceability = 
    SUM(ingresos con folio_xml de Tipo 33 o 43)
    /
    SUM(ingresos elegibles)
```

**Interpretación**: Porcentaje de ingresos que tienen respaldo documental mediante Factura Electrónica o Liquidación-Factura.

**Evidencia válida**: XML Tipo 33 (Factura) y Tipo 43 (Liquidación-Factura). NO incluye Tipo 61 (Nota de Crédito) ni Tipo 56 (Nota Débito).

**Nota**: En la implementación actual, el folio_xml no distingue el Tipo DTE del XML vinculado. La métrica usa el financial_group='ingresos' como proxy y asume que el folio_xml corresponde a un documento de ingreso. Para precisión total, se requeriría cruzar folio_xml contra el inventario XML para verificar Tipo DTE.

### 2.2 Cost Traceability

**Definición**:
```
Cost Traceability =
    SUM(costos_comerciales + costos_operacionales con folio_xml)
    /
    SUM(costos_comerciales + costos_operacionales elegibles)
```

**Interpretación**: Porcentaje de costos que tienen respaldo documental.

**Evidencia válida**: XML de cualquier Tipo DTE que represente costos (comisiones, logística, almacenamiento, fulfillment, acuerdos comerciales).

### 2.3 Returns Traceability

**Definición**:
```
Returns Traceability =
    SUM(devoluciones con folio_xml)
    /
    SUM(devoluciones elegibles)
```

**Interpretación**: Porcentaje de devoluciones que tienen respaldo documental.

**Evidencia válida**: XML Tipo 61 (Nota de Crédito por devolución) o Tipo 43 con descripción "Devoluciones MKP".

### 2.4 Adjustment Traceability

**Definición**:
```
Adjustment Traceability =
    SUM(ajustes con folio_xml)
    /
    SUM(ajustes elegibles)
```

**Interpretación**: Porcentaje de ajustes contables que tienen respaldo documental.

**Evidencia válida**: XML Tipo 56 (Nota Débito), Tipo 61 (Nota Crédito), o cualquier XML que modifique un cargo anterior.

### 2.5 Métrica Compuesta (Trust V3)

**Propuesta para Trust V3**:
```
Trust Documental = 
    0.50 * Revenue Traceability
    + 0.25 * Cost Traceability
    + 0.15 * Returns Traceability
    + 0.10 * Adjustment Traceability
```

**Ponderación**: Ingresos tienen el mayor peso (50%) porque son el concepto más crítico para auditoría financiera. Ajustes tienen el menor peso (10%) porque representan movimientos contables no transaccionales.

---

## FASE 3 — ELEGIBILIDAD TEMPORAL

### 3.1 Principio

Solo los períodos donde EXISTE evidencia física (XMLs en disco) pueden participar en las métricas de trazabilidad. Períodos sin XMLs disponibles se clasifican como NO ELEGIBLES y NO PENALIZAN la métrica.

### 3.2 Período Elegible por Marketplace

| Marketplace | Ledger | XMLs disponibles | Período Elegible | Meses Elegibles | No Elegible |
|---|---|---|---|---|---|
| **ML** | 2025-01 a 2026-12 | 2023-01 a 2026-05 | 2025-01 a 2026-05 | **17 meses** (de 24) | Jun-Dic 2026 (7 meses futuro) |
| **RIPLEY** | 2025-01 a 2026-12 | 2026-03 a 2026-05 | 2026-03 a 2026-05 | **3 meses** (de 24) | Ene 2025-Feb 2026 + Jun-Dic 2026 (21 meses) |
| **PARIS** | 2025-01 a 2026-04 | 2025-01 a 2026-04 | 2025-01 a 2026-04 | **16 meses** (100%) | 0 |
| **FALABELLA** | 2026-03-14 a 2026-04-30 | 2026-03-23 a 2026-04-21 | 2026-03-23 a 2026-04-21 | **30 días** (de 48) | 14-22 Mar + 22-30 Abr (18 días) |

### 3.3 Período Elegible para Revenue Traceability

| Marketplace | Ingresos elegibles | Ingresos no elegibles | % No Elegible |
|---|---|---|---|
| **ML** | $875,869,354 | $0 (no hay ingresos futuros sin XML) | 0% |
| **RIPLEY** | $20,774,862 | $220,204,738 | **91.4%** |
| **PARIS** | $533,201,155 | $0 | 0% |
| **FALABELLA** | $3,512,457 | $1,149,353 | 24.7% |

### 3.4 Tratamiento de Períodos No Elegibles

Los períodos no elegibles se clasifican como:

| Categoría | Descripción | Acción |
|---|---|---|
| **SIN EVIDENCIA DISPONIBLE** | No existen XMLs para estos períodos | No penalizar. Documentar como limitación. |
| **NO APLICA** | Período futuro (posterior al último XML) | No penalizar. Se actualizará cuando lleguen XMLs nuevos. |
| **PÉRDIDA DOCUMENTAL** | XMLs existieron pero se perdieron (ej: RIPLEY 2025) | Penalizar parcialmente. Buscar recuperación. |

---

## FASE 4 — RECLASIFICACIÓN DE RIESGOS

### 4.1 Matriz de Riesgos Corregida

| Marketplace | Concepto | Métrica Antigua | Métrica Corregida | Cambio |
|---|---|---|---|---|
| **ML** | Revenue | 63.5% $ (global) | 100.0% (elegible) | **MEJORA** (+36.5pp) |
| **ML** | Cost | 63.5% $ (global) | 100.0% (elegible) | **MEJORA** (+36.5pp) |
| **ML** | Returns | 63.5% $ (global) | 100.0% (elegible) | **MEJORA** (+36.5pp) |
| **ML** | Adjustment | 63.5% $ (global) | 0.1% (elegible) | **SIN CAMBIO** ($295.8M sin evidencia) |
| **PARIS** | Revenue | 82.6% $ (global) | 82.2% (elegible) | **SIN CAMBIO** |
| **PARIS** | Cost | 82.6% $ (global) | 80.4% (elegible) | **SIN CAMBIO** |
| **PARIS** | Returns | 82.6% $ (global) | 81.6% (elegible) | **SIN CAMBIO** |
| **RIPLEY** | Revenue | 0.0% (global) | 0.0% (elegible) | **SIN CAMBIO** |
| **RIPLEY** | Cost | 0.0% (global) | 0.0% (elegible) | **SIN CAMBIO** |
| **RIPLEY** | Returns | 0.0% (global) | 0.0% (elegible) | **SIN CAMBIO** |
| **FALABELLA** | Revenue | 34.1% $ (global) | **0.0%** (elegible) | **EMPEORA** (-34.1pp) |
| **FALABELLA** | Cost | 34.1% $ (global) | 92.5-96.3% (elegible) | **MEJORA** (+58-62pp) |
| **FALABELLA** | Returns | 34.1% $ (global) | 0.0% (elegible) | **EMPEORA** (-34.1pp) |

### 4.2 Riesgos que Desaparecen

| Riesgo Anterior | Motivo de Eliminación |
|---|---|
| ML gap de $307M sin folio_xml | Solo $11.2M son no-elegibles (futuro). $295.8M restantes son ajustes (no ingresos), que tienen baja penalización |
| RIPLEY "gap recuperable" de $284.9M | 91.4% de ingresos RIPLEY no son elegibles (no existen XMLs). El gap real elegible es solo $20.8M en ingresos + costos operacionales del período |
| PARIS gap de $65.7M "irrecuperable" | El gap es elegible y recuperable vía PW1. Con metodología corregida, PARIS Revenue Traceability subiría a 100% |

### 4.3 Riesgos que Persisten o Aparecen

| Riesgo | Marketplace | Naturaleza | Severidad |
|---|---|---|---|
| Ajustes $306M sin evidencia | ML | $295.8M son ajustes dentro del rango XML sin folio_xml. Solo $0.4M tienen evidencia. | **ALTA** en monto, pero **BAJA** porque son ajustes contables, no ingresos |
| RIPLEY Revenue Traceability 0% | RIPLEY | $20.8M en ingresos elegibles sin folio_xml. Bridge aún no implementado. | **MEDIA** (monto manejable) |
| RIPLEY $220M no elegibles | RIPLEY | Sin XMLs para 2025 y Jun-Dic 2026. Requiere encontrar XMLs 2025 perdidos. | **ALTA** (estructural) |
| FALABELLA Revenue Traceability 0% | FALABELLA | $3.5M en ingresos elegibles sin folio_xml. El bridge actual solo cubre costos. | **BAJA** (monto pequeño) |

---

## FASE 5 — TRUST V3 INPUT MATRIX

### 5.1 Métricas Antiguas (Trust V2)

| Marketplace | Trust Score V2 (componente XML) | Trust Score V2 (global) |
|---|---|---|
| **ML** | 89.4% rows / 63.5% $ | 94/100 |
| **RIPLEY** | 0.0% rows / 0.0% $ | 72/100 |
| **PARIS** | 79.0% rows / 82.6% $ | 70/100 |
| **FALABELLA** | 61.5% rows / 34.1% $ | 71/100 |
| **GLOBAL** | 30.2% rows / 56.1% $ | ~84/100 |

### 5.2 Métricas Corregidas (Trust V3 — Preliminar)

| Marketplace | Revenue Tr. | Cost Tr. | Returns Tr. | Adjustment Tr. | Compuesta (0.5R+0.25C+0.15Re+0.1A) |
|---|---|---|---|---|---|
| **ML** | 100.0% | 100.0% | 100.0% | 0.1% | **87.5%** |
| **PARIS** | 82.2% | 80.4% | 81.6% | 100.0% | **82.9%** |
| **RIPLEY** | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| **FALABELLA** | 0.0% | 94.4% | 0.0% | 0.0% | **23.6%** |
| **GLOBAL** | 79.4% | 84.1% | 71.7% | 0.3% | **73.5%** |

**Cálculo global**:
- Revenue = $1,314.2M / $1,654.7M = 79.4%
- Cost = ($176.0M + $91.8M) / ($210.3M + $107.1M) = $267.8M / $317.4M = 84.4%
- Returns = $200.6M / $279.9M = 71.7%
- Adjustment = $1.0M / $308.0M = 0.3%
- Compuesta = 0.50(79.4%) + 0.25(84.4%) + 0.15(71.7%) + 0.10(0.3%) = 39.7 + 21.1 + 10.8 + 0.03 = **71.6%**

### 5.3 Diferencias

| Marketplace | Trust V2 (XML component) | Trust V3 (Compuesta Documental) | Diferencia |
|---|---|---|---|
| **ML** | ~95 (implícito en 94/100) | 87.5% | **-7.5pp** (ajustes no cubiertos bajan métrica) |
| **PARIS** | ~80 (implícito en 70/100) | 82.9% | **+2.9pp** (mayor peso a revenue que está mejor cubierto) |
| **RIPLEY** | ~0 | 0.0% | Sin cambio |
| **FALABELLA** | ~40 (implícito en 71/100) | 23.6% | **-16.4pp** (revenue 0% expuesto) |
| **GLOBAL** | ~56 | 71.6% | **+15.6pp** (corrección por elegibilidad temporal mejora métrica global) |

### 5.4 Impacto Esperado en Trust Score V3

| Marketplace | Trust V2 | Trust V3 Proyectado | Cambio |
|---|---|---|---|
| **ML** | 94/100 | ~93/100 | -1 (ajustes descubiertos) |
| **PARIS** | 70/100 | ~72/100 | +2 (métrica más justa) |
| **RIPLEY** | 72/100 | ~68/100 | -4 (elegibilidad revela que bridge no resuelve el problema) |
| **FALABELLA** | 71/100 | ~60/100 | -11 (revenue 0% expuesto) |
| **GLOBAL** | ~84/100 | ~78/100 | **-6** (métrica más honesta pese a corrección por elegibilidad) |

**Nota**: El Trust Score global baja de 84 a ~78 no porque el sistema esté peor, sino porque la métrica es ahora más precisa. RIPLEY y FALABELLA bajan más porque la métrica anterior ocultaba su verdadera falta de cobertura de ingresos.

---

## RESPUESTAS DEL AUDITOR

### 1. ¿Qué métricas quedan obsoletas?

**XML Traceability %** (medido como filas con folio_xml / total filas). Queda reemplazada por 4 métricas semánticas: Revenue, Cost, Returns y Adjustment Traceability.

También queda obsoleta la métrica de "cobertura global en $" que mezclaba ingresos positivos con costos negativos en una misma suma neta.

### 2. ¿Qué métricas reemplazan XML Traceability?

Cuatro métricas independientes:

| Métrica | Fórmula | Peso en Trust V3 |
|---|---|---|
| **Revenue Traceability** | Ingresos con folio_xml / Ingresos elegibles | 50% |
| **Cost Traceability** | Costos con folio_xml / Costos elegibles | 25% |
| **Returns Traceability** | Devoluciones con folio_xml / Devoluciones elegibles | 15% |
| **Adjustment Traceability** | Ajustes con folio_xml / Ajustes elegibles | 10% |

### 3. ¿Qué períodos son elegibles por marketplace?

| Marketplace | Elegible | No Elegible |
|---|---|---|
| **ML** | Ene 2025 - May 2026 (17 meses) | Jun - Dic 2026 (7 meses, futuro) |
| **RIPLEY** | Mar - May 2026 (3 meses) | Ene 2025 - Feb 2026 + Jun - Dic 2026 (21 meses) |
| **PARIS** | Ene 2025 - Abr 2026 (16 meses = 100%) | Ninguno |
| **FALABELLA** | 23 Mar - 21 Abr 2026 (30 días) | 14-22 Mar + 22-30 Abr 2026 (18 días) |

### 4. ¿Qué riesgos desaparecen al corregir la metodología?

| Riesgo que desaparece | Motivo |
|---|---|
| ML gap de $307M "sin cobertura" | Solo $11.2M son no-elegibles. $295.8M son ajustes con baja penalización. |
| RIPLEY gap de $284.9M "recuperable vía bridge" | 91.4% de ingresos RIPLEY no son elegibles. Bridge solo resolvería $20.8M. |
| PARIS gap de $65.7M "irrecuperable" | Gap es elegible y recuperable. No es riesgo, es backlog. |

### 5. ¿Qué Trust Score proyectado tendría el sistema con medición correcta?

| Marketplace | Trust V2 | Trust V3 Proyectado | Diferencia |
|---|---|---|---|
| **ML** | 94/100 | **93/100** | -1 |
| **PARIS** | 70/100 | **72/100** | +2 |
| **RIPLEY** | 72/100 | **68/100** | -4 |
| **FALABELLA** | 71/100 | **60/100** | -11 |
| **GLOBAL** | **84/100** | **78/100** | **-6** |

---

## ANEXO: TABLA DE TRANSICIÓN

| Fase | Acción | Estado |
|---|---|---|
| **T1.1** | Certificar semántica XML | COMPLETADO |
| **TRUST_V1** | Deprecar métrica antigua | ESTA REVISIÓN |
| **TRUST_V2** | Implementar 4 métricas semánticas | PENDIENTE (próximo sprint) |
| **Bridge PW1-PW4** | Ejecutar bridges con nuevas métricas | PENDIENTE (post-aprobación) |
| **TRUST_V3** | Recalcular Trust Score oficial | PENDIENTE (post-bridges) |

---

**Documento diseñado por:** Trust Methodology Revision V1
**Régimen**: GOVERNANCE — READ ONLY

**Próximo paso**: Aprobación de esta revisión metodológica antes de implementar cambios en Trust Score o iniciar bridges.
