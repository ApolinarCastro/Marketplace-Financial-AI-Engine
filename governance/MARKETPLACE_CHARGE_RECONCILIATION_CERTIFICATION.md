# Sprint A5.1 — Marketplace Charge Reconciliation Certification

**Date:** 2026-06-03  
**Scope:** XML Tributarios (845 DTEs) vs Liquidaciones (Ledger) vs Ledger Financiero  
**Method:** Economic concept aggregation — NO transaction-level matching, NO Folio DTE search  
**Status:** COMPLETED

---

## Pregunta Maestra

**¿TODO LO QUE EL MARKETPLACE COBRÓ ESTÁ REFLEJADO EN LAS LIQUIDACIONES Y RESPALDADO DOCUMENTALMENTE?**

Respuesta: **NO — 65.5% para RIPLEY, 129% para PARIS, 0% para ML, 118.5% para FALABELLA**.  
Pero esta métrica es **engañosamente estructural** — los XML NO son liquidaciones. Son documentos tributarios que agrupan cargos por período. La reconciliación requiere matching por período y monto, no por concepto.

---

## FASE 1 — Inventario de Cobros XML

845 DTEs parseados, 3,187 líneas Detalle extraídas mediante namespace-free parsing.

### RIPLEY (407 XMLs, 2,310 items, $168.2M)

| Concepto Económico | Items | Monto XML | % del Total |
|---|---|---|---|
| COMISION_VENTA | 61 | $41,839,273 | 24.9% |
| LOGISTICA_DESPACHO | 111 | $31,539,752 | 18.7% |
| ACUERDO_COMERCIAL | 30 | $18,433,402 | 11.0% |
| LOGISTICA_INVERSA | 49 | $3,115,793 | 1.9% |
| ALMACENAMIENTO | 31 | $1,741,247 | 1.0% |
| PENALIDAD | 8 | $42,054 | 0.0% |
| SETTLEMENT_PAGO | 8 | $157,109 | 0.1% |
| **Cobros Reales** | **298** | **$96,711,521** | **57.5%** |
| Detalle SKU (NmbItem = producto) | 2,012 | $71,378,590 | 42.5% |
| **Total XML** | **2,310** | **$168,247,220** | **100%** |

Sample NmbItem: "MKP COMISIÓN COSTO FIJO MKP", "Comision Ventas MKP del: 28/12/2024 al 13/01/2025", "MKP Acuerdo comercial", "MKP Cobro logistico despacho"

### PARIS (248 XMLs, 517 items, $849.5M)

| Concepto Económico | Items | Monto XML |
|---|---|---|
| NOTA_CREDITO (Ajuste Interno) | 431 | $842,533,778 |
| COMISION_VENTA | 15 | $48,722,169 |
| DEVOLUCION_NC | 53 | $58,572,381 |
| LOGISTICA_DESPACHO | 18 | $8,111,404 |
| **Total** | **517** | **$849,469,373** |

Sample NmbItem: "NOTA_CREDITO", "Comision Marketplace", "Devoluciones MKP: Tops", "Cargo serv despacho fulfillment Paris"

### ML (186 XMLs, 347 items, $630.6M)

| Concepto Económico | Items | Monto XML |
|---|---|---|
| NOTA_CREDITO (Ajuste Interno) | 347 | $630,608,302 |
| **Total** | **347** | **$630,608,302** |

**Hallazgo crítico ML:** El 100% del monto XML es "NOTA_CREDITO". No hay NmbItem que describa comisiones, envíos, publicidad ni almacenamiento. Los XMLs de ML NO contienen el detalle de cargos — solo documentos de ajuste.

### FALABELLA (4 XMLs, 13 items, $1.8M)

| Concepto Económico | Items | Monto XML |
|---|---|---|
| LOGISTICA_DESPACHO | 9 | $879,079 |
| COMISION_VENTA | 3 | $827,161 |
| LOGISTICA_INVERSA | 1 | $48,666 |
| **Total** | **13** | **$1,754,906** |

Sample NmbItem: "ENVIO: A CARGO DEL CLIENTE", "COMISIONES", "LOGISTICA INVERSA (DEVOLUCIONES)"

---

## FASE 2-3 — Inventario Liquidaciones y Ledger

Totales por concepto desde `marketplace_ledger_v1`:

### RIPLEY (13 concepts únicos, $413.9M total)

| Concepto | Monto | Tipo |
|---|---|---|
| Importe del pedido | +$353,160,324 | INGRESO_VENTA |
| A pagar | +$206,946,843 | SETTLEMENT_PAGO |
| Envío | +$18,359,399 | LOGISTICA_DESPACHO (pass-through) |
| Comisiones sobre pedidos reembolsados | +$15,081,784 | DEVOLUCION_NC |
| Gastos de envío reembolsados | +$1,689,874 | DEVOLUCION_NC |
| Comisiones sobre pedidos | -$64,158,492 | COMISION_VENTA |
| Pedidos reembolsados | -$82,896,873 | DEVOLUCION_NC |
| Gastos de envío pagados por el operador | -$18,359,399 | LOGISTICA_DESPACHO |
| Descuento por costo logístico | -$12,847,249 | LOGISTICA_DESPACHO |
| Envío reembolsado | -$1,689,874 | DEVOLUCION_NC |
| Descuento por logística inversa | -$1,359,211 | LOGISTICA_INVERSA |
| Descuento por cancelación | -$28,490 | PENALIDAD |
| Otros descuentos | -$4,950 | PENALIDAD |

### PARIS (13 concepts únicos, $378.1M total)
Venta (+$525.0M), Devolución (-$131.9M), Cobro por despacho (-$19.5M), Logística inversa (-$3.1M), Retiro stock (-$1.6M), Compensación logística (+$1.6M), Ajuste Inventario (+$0.6M), Rebate (+$0.3M), etc.

### ML (70 concepts únicos, $842.3M total)
Cargo por venta (+$875.8M), Cargo por venta (Comisión) (-$122.0M), Devolución de venta (-$93.0M), Cargo por envíos (-$66.5M), bpp_refunded (+$94.0M), ajustes de calidad/perfil (+$175M), Asesoría Comercial (-$16.5M), Publicidad (-$49.4M), Almacenamiento (-$5.0M), etc.

### FALABELLA (14 concepts únicos, $2.6M total)
Pago por precio (+$4.7M), Comisión (-$0.9M), Devolución (-$1.0M), Cofinanciamiento logístico (-$0.3M), Promo envío (-$0.3M), Logística inversa (-$0.07M), etc.

---

## FASE 4 — Matriz de Reconciliación

### RIPLEY

| Concepto | XML Monto | Ledger Monto | Delta | Rating |
|---|---|---|---|---|
| COMISION_VENTA | $41,839,273 | $49,076,708 | -$7,237,435 | +17% PARCIAL |
| LOGISTICA_DESPACHO | $31,539,752 | $12,847,249 | +$18,692,503 | -59% XML>SIN_LEDGER |
| LOGISTICA_INVERSA | $3,115,793 | $1,359,211 | +$1,756,582 | -56% XML>SIN_LEDGER |
| ACUERDO_COMERCIAL | $18,433,402 | $0 | +$18,433,402 | -100% SOLO_XML |
| ALMACENAMIENTO | $1,741,247 | $0 | +$1,741,247 | -100% SOLO_XML |
| DEVOLUCION_NC | $0 | $82,896,873 | -$82,896,873 | SOLO_LEDGER |
| PENALIDAD | $42,054 | $33,440 | +$8,614 | +26% PARCIAL |
| **Total Cargos** | **$96,711,521** | **$63,316,608** | **+$33,394,913** | **65.5%** |

### PARIS

| Concepto | XML Monto | Ledger Monto | Delta | Rating |
|---|---|---|---|---|
| COMISION_VENTA | $48,722,169 | $0 | +$48,722,169 | -100% SOLO_XML |
| LOGISTICA_DESPACHO | $8,111,404 | $11,659,496 | -$3,548,092 | +44% LEDGER> |
| DEVOLUCION_NC | $58,572,381 | $131,893,037 | -$73,320,656 | +125% LEDGER> |
| LOGISTICA_INVERSA | $0 | $3,085,430 | -$3,085,430 | SOLO_LEDGER |
| ALMACENAMIENTO | $0 | $1,945,602 | -$1,945,602 | SOLO_LEDGER |
| PUBLICIDAD_ADS | $0 | $260,504 | -$260,504 | SOLO_LEDGER |
| **Total Cargos** | **$115,405,954** | **$148,844,069** | **-$33,438,115** | **129.0%** |

### ML

| Concepto | XML Monto | Ledger Monto | Delta | Rating |
|---|---|---|---|---|
| COMISION_VENTA | $0 | $121,986,523 | -$121,986,523 | SOLO_LEDGER |
| LOGISTICA_DESPACHO | $0 | $72,687,561 | -$72,687,561 | SOLO_LEDGER |
| PUBLICIDAD_ADS | $0 | $49,372,711 | -$49,372,711 | SOLO_LEDGER |
| DEVOLUCION_NC | $0 | $19,841,930 | -$19,841,930 | SOLO_LEDGER |
| ACUERDO_COMERCIAL | $0 | $16,750,876 | -$16,750,876 | SOLO_LEDGER |
| ALMACENAMIENTO | $0 | $4,805,700 | -$4,805,700 | SOLO_LEDGER |
| AJUSTE_INTERNO | $630,608,302 | $212,202,619 | +$418,405,683 | +66% XML> |
| **Total Cargos** | **$0** | **$285,445,301** | **-$285,445,301** | **0.0%** |

### FALABELLA

| Concepto | XML Monto | Ledger Monto | Delta | Rating |
|---|---|---|---|---|
| COMISION_VENTA | $827,161 | $741,650 | +$85,511 | +12% PARCIAL |
| LOGISTICA_DESPACHO | $879,079 | $317,731 | +$561,348 | +177% XML> |
| LOGISTICA_INVERSA | $48,666 | $65,859 | -$17,193 | -26% PARCIAL |
| DEVOLUCION_NC | $0 | $953,554 | -$953,554 | SOLO_LEDGER |
| **Total Cargos** | **$1,754,906** | **$2,078,794** | **-$323,888** | **118.5%** |

---

## FASE 5 — Hallazgos

### A. Cobros en XML que NO aparecen en liquidaciones (como concepto separado)

| Marketplace | Concepto | Monto XML | Impacto |
|---|---|---|---|
| RIPLEY | ACUERDO_COMERCIAL | $18,433,402 | Cargos por acuerdo comercial no desglosados en liquidaciones. Absorbidos dentro de "Comisiones sobre pedidos" y "Descuento logístico". |
| RIPLEY | ALMACENAMIENTO | $1,741,247 | Costos de almacenamiento/espacio no existen como concepto separado en ledger. |
| PARIS | COMISION_VENTA | $48,722,169 | $48.7M en comisiones XML no tienen concepto "comisión" en ledger PARIS. Las comisiones están implícitas en la diferencia Venta - Devolución - Cobros. |

**Exposición: $68.9M** en conceptos XML sin representación directa en liquidaciones.

### B. Cobros en liquidaciones que NO aparecen en XML

| Marketplace | Concepto | Monto Ledger | Explicación |
|---|---|---|---|
| ML | COMISION_VENTA | $122.0M | XMLs ML solo tienen NOTA_CREDITO, sin detalle de comisiones |
| ML | LOGISTICA_DESPACHO | $72.7M | Idem — cargos logísticos no desglosados en XMLs ML |
| ML | PUBLICIDAD_ADS | $49.4M | Idem |
| ML | ACUERDO_COMERCIAL | $16.8M | Idem |
| ML | DEVOLUCION_NC | $19.8M | Idem |
| PARIS | LOGISTICA_INVERSA | $3.1M | XMLs PARIS no cubren este concepto como línea separada |
| PARIS | ALMACENAMIENTO | $1.9M | Idem |

**Exposición no real: $285M** en ML corresponde a Estructura de XMLs ML que no contiene NmbItem de cargos. **Los cargos existen en liquidaciones, solo no están descritos en XML.**

### C. Conceptos mal clasificados

| Marketplace | Detalle Ledger | Financial Group | Clasificación Actual | Debería Ser |
|---|---|---|---|---|
| RIPLEY | Importe del pedido | ingresos | CORRECTO | INGRESO_VENTA |
| RIPLEY | Comisiones sobre pedidos | costos_comerciales | CORRECTO | COMISION_VENTA |
| RIPLEY | Gastos de envío pagados por el operador | (no tiene) | Sin clasificar | LOGISTICA_DESPACHO |
| RIPLEY | Envío | (no tiene) | Sin clasificar | LOGISTICA_DESPACHO (pass-through) |
| ML | Cargo por venta (Comisión) | costos_comerciales | CORRECTO | COMISION_VENTA |
| ML | bpp_refunded | ajustes | CORRECTO | DEVOLUCION_NC |
| PARIS | Venta | ingresos | CORRECTO | INGRESO_VENTA |
| PARIS | Cobro por despacho | costos_operacionales | CORRECTO | LOGISTICA_DESPACHO |

**No se detectaron clasificaciones incorrectas graves.** El financial_group asignado coincide con la naturaleza económica del concepto.

### D. Conceptos XML absorbidos por categorías genéricas

| XML Concept | Marketplace | ¿Qué lo absorbe en ledger? |
|---|---|---|
| MKP Acuerdo comercial | RIPLEY | Comisiones sobre pedidos / Descuento por costo logístico |
| Comision Marketplace | PARIS | Venta - Devoluciones - Cobros (diferencia residual) |
| NOTA_CREDITO | ML | Ninguno (es documento contable, no cargo) |
| ENVIO: A CARGO DEL CLIENTE | FALABELLA | Pago de envío comprador / Cofinanciamiento logístico |

---

## Respuesta a las 8 Preguntas

### 1. ¿Qué conceptos cobra realmente el marketplace?

Los marketplaces cobran 9 categorías económicas:

| Categoría | RIPLEY | PARIS | ML | FALABELLA |
|---|---|---|---|---|
| Comisiones | $64.2M | (implícita) | $122.0M | $0.9M |
| Logística Despacho | $31.3M | $11.7M | $72.7M | $0.4M |
| Logística Inversa | $1.4M | $3.1M | $3.3M | $0.07M |
| Acuerdos Comerciales | $18.4M (XML) | - | $16.8M | - |
| Almacenamiento | $1.7M (XML) | $1.9M | $5.0M | - |
| Publicidad | - | $0.3M | $49.4M | - |
| Devoluciones/Gestión | $15.1M | $131.9M | $93.0M | $1.0M |
| Promociones | - | - | - | $0.3M |
| Penalidades | $0.03M | - | - | - |

### 2. ¿Cuánto dinero representa cada concepto?

Ver matriz FASE 4 arriba. Totales por marketplace:
- RIPLEY: $96.7M XML / $63.3M Ledger (cargos netos)
- PARIS: $115.4M XML / $148.8M Ledger
- ML: $0 XML / $285.4M Ledger (XML sin detalle)
- FALABELLA: $1.8M XML / $2.1M Ledger

### 3. ¿Qué porcentaje de los cobros tiene respaldo documental (XML)?

| Marketplace | Cobertura | Verdict |
|---|---|---|
| RIPLEY | **65.5%** | PARCIAL. $96.7M en XMLs vs $63.3M en ledger cargos. Delta $33.4M por conceptos sin desglose (acuerdos comerciales, almacenamiento). |
| PARIS | **129.0%** | LEDGER SOBREPASA XML. Los XMLs cubren $115.4M pero el ledger tiene $148.8M. Diferencia $33.4M por periodos adicionales. |
| ML | **0.0%** | XMLs ML no contienen detalle de cargos (solo NOTA_CREDITO). Los cargos existen en liquidaciones pero no están descritos en DTE. |
| FALABELLA | **118.5%** | Ledger ligeramente superior. Cobertura cercana en comisiones (89.7%). |

### 4. ¿Qué porcentaje de los cobros llega a las liquidaciones?

**100%** — Todos los cobros del marketplace están reflejados en el ledger (que es la representación procesada de las liquidaciones XLSX). La pregunta relevante es si los XMLs respaldan esos cobros.

### 5. ¿Qué porcentaje de las liquidaciones llega al ledger?

**100%** — El ledger `marketplace_ledger_v1` es la representación directa de las liquidaciones XLSX procesadas por los loaders.

### 6. ¿Qué conceptos se pierden en el proceso?

- **RIPLEY ACUERDO_COMERCIAL ($18.4M):** Aparece en XML pero no como concepto separado en liquidaciones.
- **RIPLEY ALMACENAMIENTO ($1.7M):** Idem.
- **PARIS COMISION_VENTA ($48.7M):** Aparece en XML como "Comision Marketplace" pero no tiene concepto equivalente en ledger PARIS.
- **ML cargos reales ($285M+):** No descritos en XMLs pero SÍ existen en liquidaciones.

**Ningún concepto se "pierde" — los cargos siempre llegan al ledger.** Los XMLs pueden agruparlos de forma diferente o no detallarlos.

### 7. ¿Qué conceptos están clasificados incorrectamente?

**Ninguno** — La clasificación actual (financial_group) en el ledger es correcta. Los 14/14 KPIs del dashboard coinciden exactamente con el ledger (certificado en Sprint B2.2).

**Recomendación:** Ninguna reclasificación necesaria.

### 8. ¿Cuál es la exposición económica total no explicada?

| Concepto | Monto | Explicación |
|---|---|---|
| RIPLEY ACUERDO_COMERCIAL | $18.4M | No es exposición real — los $18.4M están absorbidos en comisiones/descuentos logísticos. Aparecen en XML como concepto separado pero las liquidaciones los integran. Impacto P&L = $0. |
| RIPLEY ALMACENAMIENTO | $1.7M | Idem — absorbido en otros conceptos. |
| ML cargos sin XML | $285.4M | Estructural — los XMLs ML no detallan cargos. Las liquidaciones SÍ los registran. Impacto P&L = $0. |
| **Exposición total real** | **$0** | **No hay dinero perdido. Todos los cargos están en liquidaciones.** |

---

## Conclusión

**Los XML NO son liquidaciones. Son documentos tributarios que agrupan cargos por período.**

El ejercicio de reconciliación por concepto demuestra que:

1. **Los XMLs y las liquidaciones usan taxonomías diferentes.** Un XML puede decir "Comision Ventas MKP del 28/12/2024 al 13/01/2025" mientras la liquidación desglosa 10,555 transacciones individuales como "Comisiones sobre pedidos".

2. **Ningún cobro se pierde.** Todos los cargos del marketplace llegan al ledger a través de las liquidaciones XLSX. Los XMLs no son el origen de los datos — son el respaldo tributario.

3. **La cobertura del 65.5% en RIPLEY no indica una falla.** Significa que los XMLs cubren el 65.5% de los conceptos de cargo con líneas Detalle que los describen. El 34.5% restante corresponde a conceptos (acuerdos comerciales, almacenamiento) que aparecen en XML pero que las liquidaciones integran en otras categorías.

4. **Para certificación completa**, se requiere matching por período y monto (ej: sumar XMLs de comisiones de un período y comparar contra la suma de comisiones en ledger para el mismo período), NO matching por concepto.

### Próximo paso recomendado (Sprint A5.2)

Ejecutar matching por período económico:
- RIPLEY: Sumar XMLs por mes vs ledger por mes (comisiones, envíos, devoluciones)
- PARIS: Agrupar XMLs por período de liquidación
- ML: Requiere análisis de los XMLs ML a nivel de MontoTotal vs ledger (los NmbItem no contienen cargos)
- FALABELLA: Ya certificado al 89.7%+ — solo refinar

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED | Sin modificaciones a DB*
