# PROGRAMA T2 — PRE-FLIGHT DOCUMENT CONSISTENCY AUDIT

**Fecha**: 2026-05-30
**Régimen**: FORENSE — READ ONLY
**DB Oficial**: `data/db/meli_financial_v4.db` (DuckDB V1.5.1)
**Auditor**: T2 Pre-Flight Audit

---

## RESPUESTAS RÁPIDAS

### 1. ¿Existe sobreconteo documental?
**SÍ.** 4 XMLs duplicados entre ML y FALABELLA (dteproveedor_7136, 7143, 7265, 7276). Monto duplicado: $2,088,338. El inventario ML reporta 762 XMLs cuando deberían ser 758.

### 2. ¿Existe subconteo documental?
**SÍ.** RIPLEY no tiene XMLs para 21 de 24 meses del ledger. ML no tiene XMLs para Jul-Dic 2026 (7 meses futuros). RIPLEY XLSX faltan archivos 000349-2815.xlsx, 000351-2815.xlsx, 000373-2815.xlsx en la secuencia de liquidaciones.

### 3. ¿Qué períodos no deben participar en la cobertura XML?
- **RIPLEY**: Ene 2025 - Feb 2026 y Jun 2026 - Dic 2026 (21 meses sin XMLs, 91.1% del monto)
- **ML**: Jul 2026 - Dic 2026 (7 meses futuros, $11.2M de los $307M del gap están en este período; 96.3% del gap ML está dentro del rango XML)
- **FALABELLA**: 14-22 Mar 2026 y 22-30 Abr 2026 (18 días sin XMLs)

### 4. ¿Qué archivos distorsionan las métricas?
- **4 XMLs ML/FALABELLA duplicados** inflan el conteo XML de ML y crean la apariencia de cobertura FALABELLA donde no existe
- **ML XMLs 86.4% Tipo 61** (Notas de Crédito, no Facturas) — el set completo es mayoritariamente notas de crédito, no facturas de comisión como se asumía en T1
- **RIPLEY XLSX secuencia 349, 351, 373 ausentes** — 3 liquidaciones sin archivo fuente

### 5. ¿Cuál es la cobertura real ajustada?

| Marketplace | Cobertura reportada | Cobertura real ajustada | Diferencia |
|---|---|---|---|
| **ML** | 89.4% rows / 63.5% $ | 89.4% rows / 63.5% $ (4 XMLs duplicados no afectan folio_xml) | 0 — folio_xml no usa archivos duplicados |
| **RIPLEY** | 0.0% | 0.0% (max posible con XMLs actuales: 8.9%) | 0 — barrera estructural |
| **PARIS** | 79.0% rows / 82.6% $ | 79.0% / 82.6% (max posible: 100% con 22 XMLs extra) | 0 — pendiente PW1 |
| **FALABELLA** | 61.5% rows / 34.1% $ | 61.5% rows / 34.1% $ (folios asignados son reales) | 0 |
| **GLOBAL** | 30.2% rows / 56.1% $ | 30.2% rows / 56.1% $ | 0 — duplicados no afectan folio_xml |

---

## FASE 1 — COMPARACIÓN DE RANGOS DE FECHA

### 1.1 Ledger por Marketplace

| Marketplace | Min Fecha | Max Fecha | Filas | Meses | Monto Total |
|---|---|---|---|---|---|
| **ML** | 2025-01-01 | 2026-12-04 | 101,603 | 24 | $842,250,301 |
| **RIPLEY** | 2025-01-01 | 2026-12-03 | 269,216 | 24 | $284,897,360 |
| **PARIS** | 2025-01-01 | 2026-04-30 | 42,487 | 16 | $378,104,933 |
| **FALABELLA** | 2026-03-14 | 2026-04-30 | 1,008 | 2 | $2,583,016 |

### 1.2 XML por Marketplace

| Marketplace | Min FchEmis | Max FchEmis | XMLs | Monto Total | Tipos DTE |
|---|---|---|---|---|---|
| **ML** | 2023-01-10 | 2026-05-24 | 762 | $581,722,689 | 33:46, 61:658, 56:33, 43:25 |
| **RIPLEY** | 2026-03-20 | 2026-05-27 | 100 | $25,483,777 | 33:60, 43:20, 61:4, 52:16 |
| **PARIS** | 2025-01-06 | 2026-04-30 | 54 | $194,018,645 | 33:29, 43:24, 61:1 |
| **FALABELLA** | 2026-03-23 | 2026-04-21 | 4 | $2,088,338 | 33:2, 61:2 |

### 1.3 Archivos Fuente (XLSX/CSV) por Marketplace

| Marketplace | XLSX | CSV | Rango XLSX | Rango CSV |
|---|---|---|---|---|
| **ML** | 214 | 0 | 2023 Ene - 2026 Abr (Liberaciones/Liquidacion_FF/ML_Facturacion/Poscobro) | N/A |
| **RIPLEY** | 46 | 47 | ~40 liquidaciones (312-378, evens+seq) | 2024-12-28 a 2026-05-28 |
| **PARIS** | 31 | 0 | Dropshipping (muestras 2025-06 a 2026-05) + Fulfillment (2025, 2026 YTD) | N/A |
| **FALABELLA** | 2 | 0 | Mar 2026, Abr 2026 | N/A |

### 1.4 Matriz de Cobertura Temporal

| Marketplace | Ledger | XML | Meses Ledger en rango XML | Meses Ledger fuera de rango |
|---|---|---|---|---|
| **ML** | 2025-01 → 2026-12 | 2023-01 → 2026-05 | 17 (Ene 2025 - May 2026) | 7 (Jun-Dic 2026) |
| **RIPLEY** | 2025-01 → 2026-12 | 2026-03 → 2026-05 | 3 (Mar-May 2026) | 21 (Ene 2025-Feb 2026 + Jun-Dic 2026) |
| **PARIS** | 2025-01 → 2026-04 | 2025-01 → 2026-04 | 16 (100%) | 0 |
| **FALABELLA** | 2026-03-14 → 2026-04-30 | 2026-03-23 → 2026-04-21 | 30 de 48 días (62.5%) | 18 días |

---

## FASE 2 — PERÍODOS SIN DOCUMENTACIÓN

### 2.1 Períodos sin XML

| Marketplace | Período sin XML | Filas afectadas | $ Afectado | % del Ledger |
|---|---|---|---|---|
| **ML** | Jun-Dic 2026 | 425 | $11,238,094 | 1.4% del gap ML (96.3% dentro de rango XML) |
| **RIPLEY** | Ene 2025 - Feb 2026 (14 meses) | ~175,000 estimadas | ~$185M estimado | ~65% |
| **RIPLEY** | Jun-Dic 2026 (7 meses) | ~67,000 estimadas | ~$75M estimado | ~26% |
| **FALABELLA** | 14-22 Mar + 22-30 Abr 2026 | ~388 (las que no tienen folio_xml) | $3.5M | 100% del gap |

### 2.2 Períodos Fuera de Rango (XML anteriores al ledger)

| Marketplace | Período XML anterior al Ledger | XMLs afectados | $ en XMLs |
|---|---|---|---|
| **ML** | 2023-01 a 2024-12 (24 meses) | ~400 XMLs | ~$300M |
| **PARIS** | N/A — XML y ledger sincronizados | 0 | $0 |
| **RIPLEY** | N/A — XMLs posteriores al ledger | 0 | $0 |

### 2.3 Períodos Sobrerrepresentados

| Marketplace | Período | # XMLs / mes | Proporción vs promedio |
|---|---|---|---|
| **RIPLEY** | Abr 2026 | 53 XMLs en 1 mes | 17.7x vs promedio de 3 meses |
| **RIPLEY** | May 2026 | 36 XMLs en 1 mes | 12x |
| **RIPLEY** | Mar 2026 | 11 XMLs en 12 días | 5.5x |
| **ML** | Sin sobrerrepresentación | Distribución uniforme mensual | — |

**Nota**: La concentración de RIPLEY XMLs en Abr 2026 (53%) no es un error; es porque los XMLs solo existen para Mar-May 2026, y Abril es el mes completo central.

---

## FASE 3 — DETECCIÓN DE DUPLICADOS

### 3.1 XML Duplicados entre Marketplaces

**4 XMLs duplicados entre ML y FALABELLA:**

| Archivo | Folio | Monto | FchEmis | TipoDTE |
|---|---|---|---|---|
| `ML/Documentos Recepcionados/dteproveedor_7136.xml` | 434564 | $94,669 | 2026-03-23 | 33 |
| `FALABELLA/Documentos Recepcionados/dteproveedor_7136.xml` | 434564 | $94,669 | 2026-03-23 | 33 |
| `ML/Documentos Recepcionados/dteproveedor_7143.xml` | 401935 | $11,960 | 2026-03-23 | 61 |
| `FALABELLA/Documentos Recepcionados/dteproveedor_7143.xml` | 401935 | $11,960 | 2026-03-23 | 61 |
| `ML/Documentos Recepcionados/dteproveedor_7265.xml` | 460690 | $1,547,578 | 2026-04-21 | 33 |
| `FALABELLA/Documentos Recepcionados/dteproveedor_7265.xml` | 460690 | $1,547,578 | 2026-04-21 | 33 |
| `ML/Documentos Recepcionados/dteproveedor_7276.xml` | 404621 | $434,131 | 2026-04-21 | 61 |
| `FALABELLA/Documentos Recepcionados/dteproveedor_7276.xml` | 404621 | $434,131 | 2026-04-21 | 61 |

**Conclusión**: Los 4 archivos son IDÉNTICOS (mismo Folio, monto, fecha, tipo DTE, nombre de archivo) y existen en ambas carpetas. Esto probablemente ocurre porque FALABELLA opera dentro de la plataforma ML y los DTEs se depositaron en ambas carpetas por error.

### 3.2 Duplicados dentro del mismo Marketplace

**Ninguno detectado.** Cada Folio XML aparece exactamente una vez dentro de su marketplace.

### 3.3 Liquidaciones Repetidas (RIPLEY XLSX)

**Ninguna detectada.** Las 46 liquidaciones RIPLEY tienen números de secuencia únicos (312-378) sin repeticiones exactas. Sin embargo, hay 2 archivos con nombre idéntico `transactions_report_20260415_154743.xlsx` que aparecen dos veces en el inventario PARIS. Esto requiere verificación manual.

### 3.4 Archivos Reemplazados

No hay evidencia directa de archivos reemplazados examinando los nombres y metadatos disponibles. Las fechas de modificación en RIPLEY XLSX muestran 3 batches de importación:
- 2026-01-08: archivos 312-359
- 2026-04-15: archivos 360-367
- 2026-05-30: archivos 368, 372-378

Esto sugiere ingestas progresivas, no reemplazos.

---

## FASE 4 — CÁLCULO DE COBERTURA CORREGIDA

### 4.1 Cobertura Actual (reportada en documentos anteriores)

| Marketplace | Filas con folio_xml | % Filas | $ con folio_xml | % $ |
|---|---|---|---|---|
| **ML** | 90,814 | 89.4% | $535,238,350 | 63.5% |
| **RIPLEY** | 0 | 0.0% | $0 | 0.0% |
| **PARIS** | 33,568 | 79.0% | $312,358,004 | 82.6% |
| **FALABELLA** | 620 | 61.5% | -$881,615 | 34.1% |
| **GLOBAL** | **125,002** | **30.2%** | **$846,714,739** | **56.1%** |

### 4.2 Cobertura Corregida por Período

La cobertura solo debe considerar los meses donde existen XMLs:

| Marketplace | Meses Ledger | Meses con XML | Cobertura temporal | Factor de ajuste |
|---|---|---|---|---|
| **ML** | 24 | 17 | 70.8% | 0.708 |
| **RIPLEY** | 24 | 3 | 12.5% | 0.125 |
| **PARIS** | 16 | 16 | 100.0% | 1.000 |
| **FALABELLA** | 2 | 2 (parcial) | ~62.5% (días) | 0.625 |

La cobertura real **máxima posible** considerando disponibilidad XML por período:

| Marketplace | Cobertura actual | Cobertura máxima posible | Techo |
|---|---|---|---|
| **ML** | 89.4% rows / 63.5% $ | ~99% rows / ~96% $ | 96.3% del gap ($295.8M) está dentro del rango XML. Solo $11.2M futuro irrecuperable |
| **RIPLEY** | 0.0% | **8.9% $** (max con XMLs actuales) | Faltan XMLs para 21/24 meses |
| **PARIS** | 79.0% rows / 82.6% $ | **100%** | 22 XMLs no vinculados, bridge existente |
| **FALABELLA** | 61.5% rows / 34.1% $ | ~70% $ | Algunos XMLs son Tipo 61 (créditos) |

### 4.3 Cobertura Corregida por Evidencia Disponible

**RIPLEY - el hallazgo más crítico:**

| Concepto | Valor |
|---|---|
| Ledger RIPLEY total | $284,897,360 |
| XMLs RIPLEY disponibles (MntTotal) | $25,483,777 |
| Cobertura máxima XML posible | **8.9%** |
| Gap irrecuperable | **$259,413,583 (91.1%)** |
| Gap irrecuperable en filas | ~245,000 filas (91%) |

Este hallazgo invalida la suposición de T1 de que RIPLEY era 93.1% del gap "recuperable". En realidad, el gap RIPLEY es **mayoritariamente irrecuperable** porque no existen XMLs para el período 2025 ni para Jul-Dic 2026.

**ML:**

| Concepto | Valor |
|---|---|
| Gap sin folio_xml | $307,011,951 (10,789 filas) |
| XMLs existen para el período | SI (762 XMLs cubren 2023-2026) |
| Gap recuperable | PARCIAL |
| Factor limitante | 86.4% de XMLs ML son Tipo 61 (Nota de Crédito), no Tipo 33 (Factura) |

**PARIS:**

| Concepto | Valor |
|---|---|
| Gap sin folio_xml | $65,746,929 (8,919 filas) |
| XMLs existen para el período | SI (100%, 54 XMLs) |
| Gap recuperable | 100% (vía PW1 — 22 XMLs adicionales) |

---

## FASE 5 — ARCHIVOS CANDIDATOS A EXCLUSIÓN

### 5.1 Exclusión Inmediata (Alta Certeza)

| Archivo | Razón | Impacto |
|---|---|---|
| `ML/Documentos Recepcionados/dteproveedor_7136.xml` | Duplicado de FALABELLA | Infla conteo ML XML: 762→758 |
| `ML/Documentos Recepcionados/dteproveedor_7143.xml` | Duplicado de FALABELLA | Infla conteo ML XML |
| `ML/Documentos Recepcionados/dteproveedor_7265.xml` | Duplicado de FALABELLA | Infla conteo ML XML |
| `ML/Documentos Recepcionados/dteproveedor_7276.xml` | Duplicado de FALABELLA | Infla conteo ML XML |

**Recomendación**: Eliminar los 4 XMLs del directorio ML (retener en FALABELLA). Esto corrige el inventario: ML 758 XMLs, FALABELLA 4 XMLs.

### 5.2 Exclusión Condicional (Requiere Verificación)

| Archivo | Razón | Acción sugerida |
|---|---|---|
| `RIPLEY/Resumen financiero/000349-2815.xlsx` | AUSENTE — no existe en disco | Verificar si la liquidación 349 fue ingerida; si existe en DB, marcar archivo como perdido |
| `RIPLEY/Resumen financiero/000351-2815.xlsx` | AUSENTE | Idem |
| `RIPLEY/Resumen financiero/000373-2815.xlsx` | AUSENTE | Idem |
| `PARIS/Transacciones/Dropshipping/transactions_report_20260415_154743.xlsx` | Aparece 2 veces en inventario (posible duplicado real) | Verificar si es el mismo archivo o 2 copias con datos diferentes |

### 5.3 Períodos Candidatos a Exclusión de Cobertura XML

| Marketplace | Período | Razón | Acción |
|---|---|---|---|
| **RIPLEY** | 2025-01 a 2026-02 | No existen XMLs | Marcar como "SIN COBERTURA XML POSIBLE" |
| **RIPLEY** | 2026-06 a 2026-12 | No existen XMLs | Marcar como "SIN COBERTURA XML POSIBLE" |
| **ML** | 2026-06 a 2026-12 | XMLs existen hasta May 2026, futuro | Marcar como "PENDIENTE — futuras facturas" |
| **ML** | 2023-01 a 2024-12 | XMLs existen pero ledger solo desde 2025 | XMLs no son relevantes para cobertura actual |

### 5.4 Archivos que Distorsionan Métricas de Cobertura

| Archivo/Patrón | Distorsión | Magnitud |
|---|---|---|
| 4 XMLs ML/FALABELLA duplicados | Inflan conteo XML ML en 4 archivos (0.5%) | Baja |
| ML XMLs Tipo 61 (86.4%) | Crean apariencia de cobertura documental donde hay notas de crédito, no facturas | **Alta** — $581.7M en XMLs ML son 86.4% créditos |
| RIPLEY 100 XMLs (100% del inventario) | Crean apariencia de 100 XMLs disponibles cuando solo cubren 3/24 meses | **Crítica** — cobertura real 8.9% vs 100% del inventario |

---

## ANEXO A: INVENTARIO COMPLETO

| Marketplace | XLSX | CSV | XML | Total |
|---|---|---|---|---|
| **ML** | 214 | 0 | 762 (758 reales) | 976 (972 reales) |
| **RIPLEY** | 46 | 47 | 100 | 193 |
| **PARIS** | 31 | 0 | 54 | 85 |
| **FALABELLA** | 2 | 0 | 4 | 6 |
| **TOTAL** | **293** | **47** | **920 (916 reales)** | **1,260 (1,256 reales)** |

## ANEXO B: ANOMALÍA ML TIPO 61

El 86.4% de los XMLs de ML son TipoDTE 61 (Nota de Crédito Electrónica). Esto es inusual para un set de facturación de marketplace y debe investigarse:

- **Tipo 33** (Factura Electrónica): 46 XMLs (6.0%) — $83.4M
- **Tipo 61** (Nota de Crédito): 658 XMLs (86.4%) — $504.1M
- **Tipo 56** (Declaración de Ingreso): 33 XMLs (4.3%) — $3.2M
- **Tipo 43** (Liquidación-Factura): 25 XMLs (3.3%) — -$9.0M

**Hipótesis**: Los XMLs ML en `Documentos Recepcionados` NO son las facturas de comisión mensual que genera ML. Son mayoritariamente notas de crédito (ajustes, bonificaciones, devoluciones). Las facturas reales de comisión (Tipo 33) son solo 46. Esto explica por qué ML tiene 762 XMLs pero el monto total XML ($581.7M) no se aproxima al ledger ($842.3M).

## ANEXO C: GLOSARIO DE TIPOS DTE

| Tipo | Nombre | Descripción |
|---|---|---|
| 33 | Factura Electrónica | Documento tributario por venta/servicio |
| 43 | Liquidación-Factura | Liquidación de consignación/venta por cuenta de tercero |
| 52 | Exportación | Factura de exportación (uso: NICOPOLY en RIPLEY) |
| 56 | Declaración de Ingreso | Declaración de ingreso a zona franca |
| 61 | Nota de Crédito Electrónica | Anulación/descuento de una Factura |

---

**Documento diseñado por:** Programa T2 — Pre-Flight Document Consistency Audit
**Régimen**: FORENSE — READ ONLY

**Próximo paso**: Los hallazgos de este audit deben incorporarse al XML_TRACEABILITY_EXECUTION_PLAN.md antes de solicitar aprobación (Gate 1). Específicamente:

1. RIPLEY coverage max revised: 8.9% → OK (ya documentado)
2. 4 XMLs duplicados: deben eliminarse del inventario ML
3. ML Tipo 61 anomaly: documentado para PW2
4. RIPLEY XLSX gaps: documentado como riesgo
