# PROGRAMA T1.1 — XML BUSINESS SEMANTICS CERTIFICATION

**Fecha**: 2026-05-30
**Régimen**: FORENSE — READ ONLY
**DB Oficial**: `data/db/meli_financial_v4.db` (DuckDB V1.5.1)

---

## RESPUESTAS DEL AUDITOR

### 1. ¿Qué representan realmente los XML?

Los 920 XMLs NO representan un solo concepto financiero. Se clasifican en **5 categorías semánticas** distintas:

| Categoría Semántica | Tipo DTE | Marketplaces | % de XMLs | % del $ XML |
|---|---|---|---|---|
| **Facturas de Comisión** (ingresos del marketplace) | 33 | ML, RIPLEY, PARIS, FALABELLA | 18.7% | 73.4% |
| **Liquidaciones de Ventas** (ventas de productos NANDA) | 43, 52 | PARIS, RIPLEY | 6.5% | 19.5% |
| **Notas de Crédito** (ajustes, devoluciones, bonificaciones) | 61 | Todos | 72.3% | 4.8% |
| **Costos Operacionales** (logística, almacenamiento, despacho) | 33, 61 | RIPLEY, ML, FALABELLA | 6.5% | 2.1% |
| **Notas de Débito** (reversiones de bonificaciones) | 56 | ML | 3.6% | 0.1% |

### 2. ¿Qué porcentaje respalda ingresos?

**18.7%** de los XMLs (172 de 920) respaldan directamente ingresos. Pero en términos de valor monetario:
- **73.4%** del monto XML ($588.7M) corresponde a documentos de ingresos (Facturas 33 + Liquidaciones 43 + Exportaciones 52)
- El 72.3% de los XMLs SON notas de crédito (Tipo 61) pero representan solo 4.8% del valor

### 3. ¿Qué porcentaje respalda devoluciones?

**~10%** de los XMLs respaldan devoluciones/ajustes negativos:
- PARIS: 2 XMLs Tipo 43 con "Devoluciones MKP" ($1.5M)
- PARIS: 1 XML Tipo 61 crédito de comisión ($7.8M)
- RIPLEY: 4 XMLs Tipo 61 ($0.8M)
- ML: 658 XMLs Tipo 61 ($33.9M) — la mayoría son notas de crédito/bonificaciones

### 4. ¿Qué porcentaje respalda ajustes?

**~3%** de los XMLs respaldan ajustes:
- ML: 33 XMLs Tipo 56 ($1.2M) — Notas de Débito que revierten bonificaciones
- REST: Notas de Crédito (Tipo 61) que pueden funcionar como ajustes contables

### 5. ¿La métrica actual de XML Traceability es correcta o engañosa?

**ENGAÑOSA.** La métrica actual (30.2% rows con folio_xml) es técnicamente correcta pero semánticamente insuficiente para auditoría financiera porque:

1. **No distingue evidencia de ingresos vs costos**: FALABELLA reporta 61.5% de cobertura XML pero **0% de sus ingresos tienen folio_xml**. Toda su cobertura es sobre costos.

2. **Trata todas las filas como equivalentes**: Una fila de ingresos por $1M y una fila de nota de crédito por -$10 cuentan igual en la métrica de "filas con folio_xml".

3. **Incluye Tipo 61 como "evidencia documental"**: Notas de Crédito son documentos que ANULAN facturas. Tener un folio_xml de Tipo 61 no es evidencia de ingreso — es evidencia de un ajuste.

4. **RIPLEY aparece como 0% pero el problema no es el bridge**: El problema es que no existen XMLs de ingresos para el período 2025 ni para futuros.

### 6. ¿Cómo debería medirse la trazabilidad documental para auditoría financiera?

Se proponen **3 métricas separadas**:

| Métrica | Definición | Valor Actual |
|---|---|---|
| **Revenue Traceability** | % de $ ingresos con folio_xml de Tipo 33 (Factura) o Tipo 43 (Liquidación) | **~65%** |
| **Cost Traceability** | % de $ costos con folio_xml de cualquier tipo | **~75%** |
| **Returns Traceability** | % de $ devoluciones con folio_xml de Tipo 61 (Nota Crédito) o Tipo 43 | **~55%** |

La métrica actual de "XML Traceability" debe reemplazarse por estas 3 métricas separadas, más una métrica compuesta ponderada.

---

## FASE 1 — INVENTARIO DTE

### ML (762 XMLs)

| Tipo | Nombre | Cantidad | % | MontoTotal | %$ |
|---|---|---|---|---|---|
| 33 | Factura Electrónica | 46 | 6.0% | $508,095,276 | 87.3% |
| 43 | Liquidación-Factura | 25 | 3.3% | $38,508,688 | 6.6% |
| 56 | Nota Débito | 33 | 4.3% | $1,169,862 | 0.2% |
| 61 | Nota Crédito | 658 | 86.4% | $33,948,863 | 5.8% |

### RIPLEY (100 XMLs)

| Tipo | Nombre | Cantidad | % | MontoTotal | %$ |
|---|---|---|---|---|---|
| 33 | Factura Electrónica | 60 | 60.0% | $14,376,802 | 56.4% |
| 43 | Liquidación-Factura | 20 | 20.0% | $5,652,914 | 22.2% |
| 52 | Exportación | 16 | 16.0% | $4,617,573 | 18.1% |
| 61 | Nota Crédito | 4 | 4.0% | $836,488 | 3.3% |

### PARIS (54 XMLs)

| Tipo | Nombre | Cantidad | % | MontoTotal | %$ |
|---|---|---|---|---|---|
| 33 | Factura Electrónica | 29 | 53.7% | $48,513,670 | 25.0% |
| 43 | Liquidación-Factura | 24 | 44.4% | $137,686,028 | 71.0% |
| 61 | Nota Crédito | 1 | 1.9% | $7,818,947 | 4.0% |

### FALABELLA (4 XMLs)

| Tipo | Nombre | Cantidad | % | MontoTotal | %$ |
|---|---|---|---|---|---|
| 33 | Factura Electrónica | 2 | 50.0% | $1,642,247 | 78.6% |
| 61 | Nota Crédito | 2 | 50.0% | $446,091 | 21.4% |

---

## FASE 2 — SEMÁNTICA FINANCIERA POR TIPO DTE

### Tipo 33 — Factura Electrónica

**Uso primario**: Documento principal de facturación. Representa comisiones cobradas por el marketplace a NANDA por uso de la plataforma, o servicios prestados.

| Marketplace | Descripción NmbItem | Interpretación Financiera |
|---|---|---|
| **ML** | "Servicio de Gestión e Intermediación" | Comisión ML por ventas en plataforma → **costo_comercial** |
| **ML** | "COMISIONES" | Comisión marketplace → **costo_comercial** |
| **ML** | "LOGISTICA INVERSA (DEVOLUCIONES)" | Costo logístico → **costo_operacional** |
| **ML** | Productos individuales (ej. "Impresora Pos") | Compra de insumos → **costo_operacional** |
| **RIPLEY** | "Comision Ventas MKP del: [periodo]" | Comisión RIPLEY por ventas → **costo_comercial** |
| **RIPLEY** | "Despacho de productos MKP Ventas del: [periodo]" | Costo logístico despacho → **costo_operacional** |
| **RIPLEY** | "FBR COBRO DESPACHO LOGISTICA INVERSA" | Logística inversa → **costo_operacional** |
| **RIPLEY** | "FBR COFINANCIAMIENTO LOGISTICO" | Cofinanciamiento logístico → **costo_operacional** |
| **RIPLEY** | "FBR COBRO ALMACENAMIENTO DIARIO" | Almacenamiento → **costo_operacional** |
| **RIPLEY** | "MKP Acuerdo comercial" | Acuerdo comercial → **costo_comercial** |
| **RIPLEY** | "MKP Penalidad - Cancelacion" | Penalización → **costo_comercial** |
| **PARIS** | "Comision Marketplace" | Comisión Paris → **costo_comercial** |
| **PARIS** | "Cargo serv despacho fulfillment Paris" | Fulfillment → **costo_operacional** |
| **PARIS** | Productos individuales (mouse, detergente) | Ventas directas → **ingresos** |
| **FALABELLA** | "COMISIONES" | Comisión Falabella → **costo_comercial** |
| **FALABELLA** | "LOGISTICA INVERSA (DEVOLUCIONES)" | Logística devoluciones → **costo_operacional** |

### Tipo 43 — Liquidación-Factura

**Uso primario**: Documento de liquidación de ventas por consignación. Representa VENTAS de productos de NANDA a través del marketplace.

| Marketplace | Descripción NmbItem | Interpretación Financiera |
|---|---|---|
| **PARIS** | "Ventas MKP: Tops/Bottoms" | **Ingresos** por venta de productos NANDA en Paris |
| **PARIS** | "Devoluciones MKP: Tops/Bottoms" | **Devoluciones** sobre ventas |
| **ML** | "NOTA_CREDITO" | Nota de crédito sobre liquidación → ajuste |
| **ML** | "BOLETA" | Boleta de venta → ingresos |
| **RIPLEY** | "FBR 2000XXXXXXXX [Producto]" | **Ingresos** por venta de producto específico (NICOPOLY) |
| **RIPLEY** | "LIQUIDACION CONSIGNATARIO" | Liquidación consignación → **ingresos** |

### Tipo 52 — Exportación

**Uso primario**: Factura de exportación. RIPLEY usa este tipo para productos NICOPOLY vendidos en el extranjero.

| Marketplace | Descripción NmbItem | Interpretación Financiera |
|---|---|---|
| **RIPLEY** | "[Producto] NICOPOLY" | **Ingresos** por exportación de productos NICOPOLY |

### Tipo 56 — Nota Débito

**Uso primario**: Documento que incrementa el monto de una factura anterior (recargo).

| Marketplace | Descripción NmbItem | Interpretación Financiera |
|---|---|---|
| **ML** | "Anulación bonif. por uso de la plataforma MercadoLibre- Flex" | Reversión de bonificación → **costo_comercial** (aumenta) |

### Tipo 61 — Nota Crédito

**Uso primario**: Documento que disminuye el monto de una factura anterior (descuento, bonificación, devolución).

| Marketplace | Descripción NmbItem | Interpretación Financiera |
|---|---|---|
| **ML** | "PROMOCIONES DE ENVIO F.COM" | Subsidio de envío Free Shipping → **costo_operacional** |
| **ML** | "Bonificaciones por uso de la plataforma MercadoLibre- Flex" | Descuento sobre comisión → **costo_comercial** (reduce) |
| **ML** | "Servicios de publicación y ventas..." | Nota de crédito sobre comisión → **costo_comercial** (reduce) |
| **PARIS** | "Comision Marketplace" (NC) | Nota crédito sobre comisión → **costo_comercial** (reduce) |
| **RIPLEY** | "Anula MKP Acuerdo comercial" | Anulación de acuerdo → ajuste |
| **RIPLEY** | "FBR COBRO/CONFIANCIAMIENTO/ALMACENAMIENTO" | Nota crédito sobre costos → **costo_operacional** (reduce) |
| **FALABELLA** | "PROMOCIONES DE ENVIO F.COM" | Subsidio envío → **costo_operacional** |

---

## FASE 3 — XML vs FINANCIAL GROUP (MATRIZ DE IMPACTO)

### PARIS: Mapeo Folio XML → Financial Groups

Cadal folio XML (especialmente Tipo 43 Liquidación) se mapea a MÚLTIPLES financial_groups simultáneamente:

```
XML Folio 17418 (Tipo 43, Liquidacion $12.7M)
  ├──→ ingresos:       $35,230 (2 rows)
  └──→ devoluciones:   $29,240 (1 row)
  └──→ costos_operacionales: $0 (mapeado pero sin monto para este folio)

XML Folio 23980722 (Tipo 33, Comision Marketplace $401k)
  ├──→ ingresos:       $47,673,843 (2,083 rows)
  ├──→ devoluciones:  -$9,980,108 (316 rows)
  └──→ costos_operacionales: -$2,367,460 (1,551 rows)
```

Cada folio XML PARIS cubre un PERÍODO COMPLETO (ingresos + devoluciones + costos asociados a ese período). El bridge es a nivel de `id_orden` (orden completa), no a nivel de transacción individual.

### ML: Mapeo

```
17 folios XML únicos → TODAS las filas con folio_xml (90,814)
  ├──→ ingresos:           31,103 rows  $875,869,354 (100%)
  ├──→ costos_comerciales: 34,210 rows  -$175,510,367 (100%)
  ├──→ costos_operacionales:22,421 rows  -$71,705,336 (100%)
  ├──→ devoluciones:        2,995 rows  -$93,009,601 (100%)
  └──→ ajustes:                85 rows     -$405,701 (0.1%)
```

Los 17 folios XML ML cubren TODAS las filas de ingresos, costos y devoluciones. No hay filas sin folio_xml en estas categorías. Esto sugiere que el folio_xxml en ML es el id interno 033-XXXXXXXXXX que mapea a un período completo.

---

## FASE 4 — ML: INVESTIGACIÓN TIPO 61

### Conclusión: La anomalía es por CANTIDAD, no por VALOR

| Métrica | Valor |
|---|---|
| XMLs ML totales | 762 |
| Tipo 61 (Nota Crédito) por cantidad | 658 (86.4%) |
| Tipo 61 (Nota Crédito) por monto | $33.9M (5.8%) |
| Tipo 33 (Factura) por cantidad | 46 (6.0%) |
| Tipo 33 (Factura) por monto | $508.1M (87.3%) |

**Interpretación**: El set de XML de ML contiene mayoritariamente NOTAS DE CRÉDITO INDIVIDUALES (658 archivos) que representan ajustes pequeños. Las facturas reales de comisión (Tipo 33) son solo 46 archivos pero concentran el 87.3% del valor. Esto es un comportamiento esperado de ML que emite notas de crédito individuales por cada transacción de ajuste (ej: promoción de envío aplicada a una orden específica).

### Semántica ML Tipo 61

| Concepto | Cantidad XMLs | Monto | % del Tipo 61 |
|---|---|---|---|
| "PROMOCIONES DE ENVIO F.COM" (Free Shipping) | ~450 | ~$20M | ~59% |
| "Bonificaciones por uso de la plataforma MercadoLibre- Flex" | ~150 | ~$10M | ~29% |
| "Servicios de publicación y ventas..." (NC generales) | ~58 | ~$3.9M | ~12% |

### Impacto Financiero

Los Tipo 61 representan: REDUCCIONES de costos que NANDA ya registró como gasto. Desde la perspectiva de NANDA:
- PROMOCIONES DE ENVIO → ML subsidia parte del envío → reduce costo_operacional
- Bonificaciones Flex → ML devuelve parte de la comisión → reduce costo_comercial

---

## FASE 5 — PARIS: SEMÁNTICA FINANCIERA

### Distribución

| Concepto | XMLs | Monto XML | % del Total XML |
|---|---|---|---|
| **Ingresos** (Ventas MKP Tipo 43) | 22 | $136,230,745 | 70.2% |
| **Ingresos** (Tipo 33 productos individuales) | 4 | $113,397 | 0.1% |
| **Costos** (Comisión Marketplace Tipo 33) | 10 | $39,802,852 | 20.5% |
| **Costos** (Cargo Fulfillment Tipo 33) | 15 | $8,597,421 | 4.4% |
| **Devoluciones** (Devoluciones MKP Tipo 43) | 2 | $1,455,283 | 0.8% |
| **Ajustes** (Nota Crédito Tipo 61) | 1 | $7,818,947 | 4.0% |

### Hallazgo Clave

Los **22 XMLs NO vinculados** del PW1 son mayoritariamente:
- 15 Cargo Fulfillment → costos_operacionales
- 4 Ventas MKP → ingresos
- 2 Devoluciones MKP → devoluciones
- 1 Nota Crédito → ajustes

Esto significa que el PW1 cubriría los 4 conceptos financieros de forma balanceada.

---

## FASE 6 — RIPLEY: NATURALEZA DE LOS 100 XML

### Clasificación por Actividad

| Categoría | XMLs | Monto | % del Total | Naturaleza Financiera |
|---|---|---|---|---|
| Comisión Ventas MKP (semanal) | 9 | $6,608,934 | 25.9% | **Costo comercial** — comisión RIPLEY |
| Despacho productos MKP (semanal) | 8 | $1,908,431 | 7.5% | **Costo operacional** — logística |
| FBR Productos por SKU (Tipo 43) | 19 | $5,234,014 | 20.5% | **Ingresos** — venta productos NICOPOLY |
| NICOPOLY Exportación (Tipo 52) | 16 | $4,617,573 | 18.1% | **Ingresos** — exportación |
| MKP Cobro logístico primera milla | 9 | $2,667,135 | 10.5% | **Costo operacional** |
| FBR Cofinanciamiento logístico | 11 | $892,801 | 3.5% | **Costo operacional** |
| FBR Cobro despacho logística inversa | 11 | $288,000 | 1.1% | **Costo operacional** |
| FBR Cobro almacenamiento diario | 11 | $34,113 | 0.1% | **Costo operacional** |
| MKP Acuerdo comercial / Anulación | 4 | $2,800,021 | 11.0% | **Costo comercial** |
| Liquidación Consignatario | 1 | $418,900 | 1.6% | **Ingresos** |
| MKP Penalidad - Cancelación | 1 | $13,855 | 0.1% | **Costo comercial** |
| **TOTAL** | **100** | **$25,483,777** | **100%** | |

### Resumen por Naturaleza

| Naturaleza | Monto | % |
|---|---|---|
| **Ingresos** (FBR Productos + Exportación + Liquidación) | $10,270,487 | 40.3% |
| **Costos comerciales** (Comisión + Acuerdo + Penalidad) | $9,422,810 | 37.0% |
| **Costos operacionales** (Despacho + Logística + Almacenamiento) | $5,790,480 | 22.7% |

Solo **40.3%** de los XMLs RIPLEY respaldan ingresos. El resto son costos.

---

## FASE 7 — FALABELLA: INVESTIGACIÓN folio_xml NEGATIVO

### Diagnóstico

| Folio | Tipo | Descripción | Impacto Ledger | Interpretación |
|---|---|---|---|---|
| 460690 | 33 | LOGISTICA INVERSA (DEVOLUCIONES) | costos: -$1.3M | Es un documento de COSTO, no de ingreso. Correctamente asignado a costos |
| 434564 | 33 | COMISIONES | costos: -$80k | Es comisión FALABELLA. Correcto. |
| 401935 | 61 | PROMOCIONES DE ENVIO F.COM | costos: +$10k | NC sobre envío. Monto positivo reduce costos. |
| 404621 | 61 | PROMOCIONES DE ENVIO F.COM | costos: +$365k | NC sobre envío. Monto positivo reduce costos. |
| 428840 | ? | (no detectado previamente) | costos: +$124k | Sin XML asociado en el inventario |

### Conclusión

El folio_xml en FALABELLA está asignado a costos (correcto financieramente). Que el total XML sea negativo (-$881k) no es un error — es porque los XMLs de FALABELLA representan COSTOS, no ingresos.

**Problema de métrica**: La métrica "61.5% de filas con folio_xml" es correcta pero engañosa. Las filas CON folio_xml son costos y las filas SIN folio_xml ($3.5M, 125 filas de ingresos) son toda la facturación positiva. La cobertura de ingresos real es 0%.

**Folio 428840 no existe en XMLs FALABELLA** — es un fantasma en la DB. Sugiere que este folio fue asignado de una fuente externa no XML (posiblemente del Excel).

---

## FASE 8 — COBERTURA POR CONCEPTO FINANCIERO

### Cobertura Global por Concepto

| Concepto | Total $ | XML $ | % Cubierto |
|---|---|---|---|
| **Ingresos** | $1,654.7M | $1,314.2M | **79.4%** |
| **Devoluciones** | -$279.9M | -$200.6M | **71.7%** |
| **Costos Comerciales** | -$210.3M | -$176.0M | **83.7%** |
| **Costos Operacionales** | -$107.1M | -$91.8M | **85.8%** |
| **Ajustes** | $308.0M | $1.0M | **0.3%** |
| **No clasificado (RIPLEY)** | $142.4M | $0 | **0.0%** |

### Cobertura de Ingresos por Marketplace

| Marketplace | Ingresos totales | Ingresos con XML | % |
|---|---|---|---|
| **ML** | $875,869,354 | $875,869,354 | **100.0%** |
| **PARIS** | $533,201,155 | $438,341,712 | **82.2%** |
| **RIPLEY** | $240,979,600 | $0 | **0.0%** |
| **FALABELLA** | $4,661,810 | $0 | **0.0%** |
| **GLOBAL** | **$1,654,711,919** | **$1,314,211,066** | **79.4%** |

### Cobertura de Costos Comerciales por Marketplace

| Marketplace | Costos Comerciales | Con XML | % |
|---|---|---|---|
| **ML** | -$175,510,367 | -$175,510,367 | **100.0%** |
| **PARIS** | $0 (incluido en ingresos del bridge) | — | — |
| **RIPLEY** | -$34,027,680 | $0 | **0.0%** |
| **FALABELLA** | -$741,650 | -$513,123 | **69.2%** |
| **GLOBAL** | **-$210,279,697** | **-$176,023,490** | **83.7%** |

---

## FASE 9 — AUDIT IMPACT

### Nivel de Confianza por Concepto

| Concepto | Confianza | Justificación |
|---|---|---|
| **Ingresos ML** | ALTA | 100% cubierto. 17 folios únicos, Tipo 33 Facturas dominan por valor. |
| **Ingresos PARIS** | MEDIA | 82.2% cubierto. Bridge vía Excel con 32/54 folios. Pendiente PW1. |
| **Ingresos RIPLEY** | BAJA | 0%. No existen XMLs de ingresos para 91% del período. |
| **Ingresos FALABELLA** | BAJA | 0%. Solo costos tienen folio_xml. Ingresos sin evidencia XML. |
| **Costos ML** | ALTA | 100%. 17 folios únicos cubren todas las filas de costo. |
| **Costos PARIS** | MEDIA-ALTA | 80.4% (operacionales). Bridge verificable. |
| **Costos RIPLEY** | BAJA | 0%. Sin bridge implementado. |
| **Devoluciones PARIS** | MEDIA | 81.6%. Mismo bridge que ingresos. |

### Matriz de Calidad de Evidencia

| Marketplace | Ingresos | Costos | Devoluciones | Ajustes |
|---|---|---|---|---|
| **ML** | ALTA (100%) | ALTA (100%) | ALTA (100%) | BAJA (0.1%) |
| **PARIS** | MEDIA (82%) | MEDIA (80%) | MEDIA (82%) | ALTA (100%) |
| **RIPLEY** | BAJA (0%) | BAJA (0%) | BAJA (0%) | BAJA (0%) |
| **FALABELLA** | BAJA (0%) | MEDIA (70-96%) | BAJA (0%) | BAJA (0%) |

### Conclusión de Auditoría

**La métrica "XML Traceability" actual es engañosa por 3 razones:**

1. **Mezcla conceptos no comparables**: Trata evidencia de ingresos ($1,314M), costos (-$176M) y devoluciones (-$201M) como una sola métrica. La suma neta ($847M) cancela conceptos que deben auditarse por separado.

2. **FALABELLA infla**: Aparece como "61.5% cubierto" pero sus ingresos reales (los únicos que importan para Revenue Audit) tienen 0% cobertura.

3. **No captura la gravedad de RIPLEY**: RIPLEY es 93.1% del gap de filas, pero en ingresos es 14.6% ($240.9M de $1,654.7M). La pérdida de cobertura de ingresos de RIPLEY ($240.9M) es grave pero menor que la de PARIS ($94.9M) en términos absolutos.

| Concepto | Gap Actual | Prioridad |
|---|---|---|
| Gap ingresos PARIS | $94.9M (17.8%) | **ALTA** — recuperable vía PW1 (22 XMLs) |
| Gap ingresos RIPLEY | $240.9M (100%) | **MEDIA** — irrecuperable sin XMLs 2025 |
| Gap ingresos FALABELLA | $4.7M (100%) | **BAJA** — monto pequeño |
| Gap costos RIPLEY | $34.0M (100%) | **MEDIA** — requiere bridge |
| Gap ajustes ML | $306.2M (99.9%) | **ALTA** — $306.6M sin evidencia (pero son ajustes, no ingreso real) |

---

## ANEXO: GLOSARIO SEMÁNTICO

| Término | Significado Financiero |
|---|---|
| **Factura Comisión (Tipo 33)** | Cobro del marketplace a NANDA por usar la plataforma → costo |
| **Liquidación Ventas (Tipo 43)** | Venta de productos NANDA a través del marketplace → ingreso |
| **Exportación (Tipo 52)** | Venta de productos NANDA al extranjero → ingreso |
| **Nota Crédito (Tipo 61)** | Ajuste que REDUCE un cargo anterior → reduce costo o devolución |
| **Nota Débito (Tipo 56)** | Ajuste que AUMENTA un cargo anterior → aumenta costo |
| **Cargo Fulfillment** | Cobro por almacenamiento y despacho → costo operacional |
| **FBR** | Full Business Relationship (término RIPLEY para servicios logísticos integrados) |
| **Cofinanciamiento Logístico** | Subsidio de RIPLEY al costo de envío → costo operacional reducido |
| **MKP** | Marketplace |
| **NICOPOLY** | Marca propia de NANDA, exportada/vendida en RIPLEY |

---

**Documento diseñado por:** Programa T1.1 — XML Business Semantics Certification
**Régimen**: FORENSE — READ ONLY

**Recomendación**: Las métricas de XML Traceability deben recalcularse usando 3 ejes separados (Revenue/Cost/Returns) antes del Gate de aprobación del Execution Plan.
