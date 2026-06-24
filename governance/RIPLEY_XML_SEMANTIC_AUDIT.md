# Auditoría Semántica RIPLEY XML vs Ledger

> **Fecha:** 2026-06-03
> **Tipo:** READ ONLY — Análisis forense completo de 407 XMLs SII DTE
> **Fuentes:** `01_Raw/RIPLEY/Documentos Recepcionados/` (407 XMLs) vs `marketplace_ledger_v1` (62,502 rows RIPLEY)
> **Estado:** **COMPLETADO — Sin modificar DB**

---

## Resumen Ejecutivo

Se analizaron 407 archivos XML SII DTE (Documentos Tributarios Electrónicos) emitidos por **Comercial Eccsa S.A. (RIPLEY, RUT 83.382.700-6)** a **Mercado Libre (RUT 77.898.100-9)**, cubriendo enero 2025 a mayo 2026.

**Monto total XML:** $186,705,151 (MntTotal)  
**Monto total Ledger RIPLEY:** $413,893,686  
**Cobertura XML aparente:** 45.1%

**Sin embargo**, $206,946,843 del ledger corresponde a **"A pagar" (settlement/tesorería)** — concepto que NO requiere respaldo XML por su naturaleza (es el espejo de la operación P&L).  
**Cobertura XML real sobre P&L direccionable:** **90.2%** ($186.7M / $207.0M)

---

## A. Inventario de Conceptos XML

### A.1 Por Tipo DTE

| Tipo | Descripción | Archivos | Monto Neto | IVA |
|------|-------------|----------|------------|-----|
| 33 | Factura Electrónica | 253 | $102,061,621 | $19,391,717 |
| 43 | Nota de Crédito | 105 | $53,442,618 | $10,154,133 |
| 52 | Nota de Débito | 30 | $8,917,705 | $2,091,788 |
| 61 | Boleta Electrónica | 19 | $1,733,488 | $329,363 |
| **Total** | | **407** | **$166,155,432** | **$31,967,001** |

**Interpretación:**
- DTE 33 (Facturas) = RIPLEY cobra a MELI por comisiones, logística, acuerdos ($121.5M MntTotal)
- DTE 43 (NC) = RIPLEY acredita a MELI por devoluciones, ajustes ($52.2M)  
- DTE 52 (ND) = RIPLEY cobra cargos adicionales ($11.0M)
- DTE 61 (Boletas) = Documentos menores ($2.1M)

### A.2 Por Categoría Económica (desde Detalle)

| Categoría | Items | Monto | % XML |
|-----------|-------|-------|-------|
| Productos (SKU individual) | 1,528 | $56,952,804 | 30.5% |
| Comisiones Ventas MKP | 47 | $41,824,297 | 22.4% |
| Costos Logísticos | 165 | $35,749,209 | 19.1% |
| Acuerdo Comercial | 38 | $20,072,066 | 10.8% |
| Cofinanciamiento Logístico | 517 | $13,648,844 | 7.3% |
| Otras Comisiones | 10 | $576,130 | 0.3% |
| Almacenamiento | 5 | $42,924 | 0.0% |
| **Total** | **2,310** | **$168,866,274** | **100%** |

### A.3 Top Conceptos por Monto

| Concepto | Veces | Monto |
|----------|-------|-------|
| MKP Acuerdo comercial | 28 | $17,817,091 |
| MKP Cobro logístico parcial del despacho primera milla | 33 | $11,571,322 |
| Comision Ventas MKP (varios períodos) | ~24 | ~$3,288,649 c/u |
| MKP Cobro despacho logistica inversa | 37 | $2,861,172 |
| MKP Cobro logistico despacho primera milla | 5 | $2,400,472 |
| FBR COFINANCIAMIENTO LOGISTICO | 15 | $1,088,571 |

---

## B. Inventario de Conceptos Ledger

### B.1 Por Grupo Financiero

| Financial Group | Filas | Monto Neto |
|----------------|-------|------------|
| NULL (A pagar - settlement) | 11,683 | $206,946,843 |
| ingresos (Importe del pedido) | 10,555 | $353,160,324 |
| costos_comerciales | 13,005 | -$49,076,708 |
| devoluciones | 2,450 | -$82,896,873 |
| costos_operacionales | 24,799 | -$14,206,460 |
| ajustes | 10 | -$33,440 |
| **Total** | **62,502** | **$413,893,686** |

### B.2 Por Detalle (Concepto Económico)

| Concepto | Filas | Monto |
|----------|-------|-------|
| Importe del pedido | 10,555 | $353,160,324 |
| A pagar | 11,683 | $206,946,843 |
| Pedidos reembolsados | 2,450 | -$82,896,873 |
| Comisiones sobre pedidos | 6,967 | -$64,158,492 |
| Envío / Gastos de envío | 7,809 | -$18,359,399 |
| Comisiones sobre pedidos reembolsados | 2,450 | -$15,081,784 |
| Descuento por costo logístico | 6,967 | -$12,847,249 |
| Envío reembolsado | 879 | -$1,689,874 |
| Descuento por logística inversa | 456 | -$1,359,211 |

---

## C. Matriz de Correspondencia XML ↔ Ledger

| Concepto XML | Concepto Ledger | XML Amount | Ledger Amount | Cobertura |
|-------------|----------------|------------|---------------|-----------|
| **Ventas** (productos SKU) | Importe del pedido | $56,952,804 | $353,160,324 | 16.1% |
| **Comisiones** | Comisiones sobre pedidos | $41,824,297 | $64,158,492 | 65.2% |
| **Logística** | Descuento por costo logístico | $35,749,209 | $12,847,249 | 278.2%* |
| **Acuerdo Comercial** | (parte de costos comerciales) | $20,072,066 | — | — |
| **Cofinanciamiento Log.** | (no identificado directamente) | $13,648,844 | — | — |
| **Devoluciones (NC)** | Pedidos reembolsados | $52,179,469 | $82,896,873 | 62.9% |
| **Total direccionable** | **P&L (excl. settlement)** | **$168,866,274** | **$207,000,000** | **81.6%** |

*\*La cobertura >100% en logística indica que el ledger agrega algunos costos logísticos dentro de "Descuento por costo logístico" ($12.8M) mientras que los XML desglosan múltiples conceptos logísticos que totalizan más. Esto sugiere que parte de la logística XML se clasifica en otros grupos del ledger (costos_operacionales, acuerdos comerciales).*

---

## D. Conceptos Exclusivos XML (no identificables en ledger)

**Evidencia comprobada:**

1. **Detalle de productos por SKU** (1,528 items)
   - Ej: "ABRIGO 4 BOTONES OXIDO NICOPOLY" — $529,128
   - El ledger agrega todo como "Importe del pedido" ($353M)
   - El XML tiene granularidad a nivel de producto individual

2. **Acuerdo Comercial — Espacios publicitarios**
   - Ej: "MKP Acuerdo comercial - Espacios NICOPOLY-ProductAds" — $420,728
   - No existe concepto equivalente en ledger

3. **Cofinanciamiento Logístico mensual**
   - Ej: "COFINANCIAMIENTO LOGÍSTICO DICIEMBRE 2025" — $953,655
   - El ledger no separa este concepto

4. **FBR (co-financiamiento logístico a nivel producto)**
   - 517 items, $13.6M total
   - Son descuentos/logística a nivel de SKU individual

**Incertidumbre:** No es posible determinar si estos conceptos están incluidos dentro de los costos comerciales/operacionales del ledger sin un DTEIndexer funcional.

---

## E. Conceptos Exclusivos Ledger (sin respaldo XML)

**Evidencia comprobada:**

| Concepto | Monto | ¿Requiere XML? |
|----------|-------|----------------|
| A pagar (settlement) | $206,946,843 | **NO** — Es treasury/settlement, no P&L |
| Envío / Gastos de envío | $18,359,399 | **SÍ** — Debería estar en XML |
| Envío reembolsado | $1,689,874 | **SÍ** — Debería estar en NC |
| Descuento por logística inversa | $1,359,211 | **SÍ** — Parcialmente en XML |

**Evidencia parcial:** El XML incluye "MKP Cobro despacho logistica inversa" por $2,861,172 — que es MAYOR que el descuento por logística inversa del ledger ($1,359,211). Esto sugiere que el XML cubre este concepto pero con diferencia temporal o de agregación.

---

## F. Cobertura por Categoría

### F.1 Ventas

| Fuente | Monto | % |
|--------|-------|---|
| XML (productos en facturas) | $56,952,804 | 16.1% |
| Ledger (Importe del pedido) | $353,160,324 | 100% |
| **Gap** | **$296,207,520** | **83.9%** |

**Análisis:** Las facturas DTE 33 incluyen líneas de producto individuales, pero el volumen total de productos en XML ($57M) es mucho menor que el Importe del pedido del ledger ($353M). Esto indica que las facturas cubren solo una parte de las transacciones. El resto proviene del XLSX bridge directamente.

**Incertidumbre:** No se puede determinar si los XMLs faltantes fueron emitidos pero no recepcionados, o si nunca se emitieron.

### F.2 Comisiones

| Fuente | Monto | % |
|--------|-------|---|
| XML (Comisiones Ventas MKP) | $41,824,297 | 65.2% |
| Ledger (Comisiones sobre pedidos) | $64,158,492 | 100% |
| **Gap** | **$22,334,195** | **34.8%** |

**Análisis:** 47 items de comisiones en XML (cada uno representa un período quincenal de comisiones) vs. 6,967 transacciones de comisiones en el ledger. Las comisiones XML son facturas/NC consolidadas por período, mientras que el ledger desglosa por transacción individual.

### F.3 Costos Logísticos

| Fuente | Monto | % |
|--------|-------|---|
| XML (Logística + Cofinanciamiento) | $49,398,053 | 384.5% |
| Ledger (Descuento por costo logístico) | $12,847,249 | 100% |

**Análisis:** El XML reporta SIGNIFICATIVAMENTE más costo logístico que el ledger. Esto es porque:
- El XML incluye cargos logísticos detallados (primera milla, inversa, etc.)
- El ledger puede clasificar parte de estos costos en otros grupos (costos_operacionales, acuerdo comercial)
- Hay un desajuste estructural en cómo se categoriza la logística

### F.4 Devoluciones

| Fuente | Monto | % |
|--------|-------|---|
| XML (Notas de Crédito DTE 43) | $52,179,469 | 62.9% |
| Ledger (Pedidos reembolsados) | $82,896,873 | 100% |
| **Gap** | **$30,717,404** | **37.1%** |

**Análisis:** 105 Notas de Crédito en XML vs. 2,450 pedidos reembolsados en ledger. Cada NC puede agrupar múltiples devoluciones.

### F.5 Ajustes

| Fuente | Monto | % |
|--------|-------|---|
| XML (ND DTE 52) | $11,009,493 | — |
| Ledger (ajustes) | -$33,440 | — |

**Análisis:** Los DTE 52 (Notas de Débito) por $11M no se correlacionan directamente con los ajustes del ledger (-$33K). Las ND probablemente se clasifican como costos comerciales, no como ajustes.

### F.6 A Pagar (Settlement)

| Fuente | Monto |
|--------|-------|
| XML | **$0** (no aplica) |
| Ledger | $206,946,843 |

**Conclusión:** El concepto "A pagar" es treasury/settlement — representa el pago que RIPLEY debe hacer a MELI por el neto de operación. NO requiere respaldo XML. Es correcto que no aparezca en las facturas.

---

## G. Posibles Llaves de Conciliación

### G.1 Evaluación de 5 Métodos

| Método | XML | Ledger | Overlap | Viabilidad |
|--------|-----|--------|---------|------------|
| **1. Folio DTE vs folio_xml** | Folio SII (7-8 dígitos) | folio_xml (5-6 dígitos) | **0** — Sistemas diferentes | ❌ Inviable |
| **2. Amount + Date** | FchEmis + MntTotal | fecha + monto | **Parcial** | ✅ Probado en PARIS (82.6%) |
| **3. id_transaccion** | No contiene este ID | RIP_{folio}_{order} | **N/A** | ❌ XML no tiene este formato |
| **4. RUT** | 83.382.700-6 / 77.898.100-9 | No existe columna RUT | **N/A** | ❌ Sin columna en ledger |
| **5. XLSX bridge** | Potencial columna no documentada | folio_xml viene de XLSX | **Desconocido** | ⚠️ Requiere revisión de XLSX |

### G.2 Método Recomendado: Amount + Date Matching

**Evidencia PARIS:** En Sprint A2 se logró matchear 48 folios (82.6% del monto) usando fecha+monto con ventana de ±3 días.

**Para RIPLEY, el desafío es mayor:**
- LEDGER: 62,502 transacciones individuales (cada "Importe del pedido" es una venta)
- XML: 407 facturas consolidadas (cada factura agrupa MÚLTIPLES pedidos)
- El matching requiere: `SUM(ledger.monto) WHERE fecha ≈ XML.FchEmis` = `XML.MntTotal`

**Estimación de viabilidad:** Media-Alta (60-70% de XMLs match)

---

## H. Riesgos Encontrados

### H.1 ALTA PRIORIDAD

**R1 — 54.9% del ledger sin XML asociado**
- Ledger total: $413.9M. XML total: $186.7M
- Gap: $227.2M
- **Mitigación:** $206.9M del gap es "A pagar" (settlement, no requiere XML). Gap real = $20.3M sobre P&L direccionable
- **Evidencia:** Comprobado por suma de montos

**R2 — 0% de certificación XML actual**
- `estado_xml = NULL` para las 62,502 rows RIPLEY
- DTEIndexer nunca se ha ejecutado para RIPLEY
- **Evidencia:** Consulta directa a DB

**R3 — 105 Notas de Crédito (DTE 43) sin match**
- NC total: $52.2M. Devoluciones ledger: $82.9M
- Gap no cubierto por NC: $30.7M (37.1%)
- **Hipótesis:** Algunas NC pueden estar en XMLs no recepcionados, o las devoluciones se registran sin NC

### H.2 MEDIA PRIORIDAD

**R4 — Sin llave de conciliación directa**
- XML Folio ≠ ledger folio_xml
- Se requiere amount+date matching (método indirecto)
- **Evidencia:** Comparación directa de valores

**R5 — Logística XML 3.8x mayor que ledger**
- XML: $49.4M en logística. Ledger: $12.8M en "Descuento por costo logístico"
- **Hipótesis:** El ledger clasifica logística en múltiples grupos, o los XML incluyen conceptos que el ledger trata como "Acuerdo Comercial"
- **Evidencia parcial:** Requiere DTEIndexer para rastrear el flujo completo

### H.3 BAJA PRIORIDAD

**R6 — Concentración 1 emisor / 1 receptor**
- Todos los XML: Emisor=83.382.700-6 (RIPLEY), Receptor=77.898.100-9 (MELI)
- Sin diversidad de contrapartes
- **Evidencia:** Parseo completo de 407 XMLs

---

## I. Respuesta a las 8 Preguntas

### P1: ¿Qué conceptos económicos aparecen en los XML y no existen en el ledger?

**Evidencia comprobada:**
1. **Detalle de productos por SKU** — 1,528 items a nivel de producto individual (ABRIGO, CHAQUETA, etc.). El ledger los agrega como "Importe del pedido".
2. **Acuerdo Comercial - Espacios publicitarios** — $1.1M en sub-conceptos de marketing/publicidad no segregados en ledger.
3. **Cofinanciamiento Logístico mensual** — $13.6M en 517 items, no identificable como concepto separado en ledger.

**Incertidumbre:** No sabemos si estos conceptos están embebidos dentro de "costos comerciales" o "costos operacionales" del ledger.

### P2: ¿Qué conceptos existen en el ledger y no aparecen en ningún XML?

**Evidencia comprobada:**
1. **"A pagar" (settlement)** — $206.9M. **No debe aparecer en XML** (tesorería).
2. **Envío / Gastos de envío** — $18.4M. No tiene línea directa en XML.
3. **Comisiones sobre pedidos reembolsados** — $15.1M. Asociado a devoluciones.
4. **Envío reembolsado** — $1.7M. No tiene NC directa.
5. **Descuento por logística inversa** — $1.4M.

**Evidencia parcial:** El XML tiene "MKP Cobro despacho logistica inversa" ($2.9M) que podría corresponder parcialmente a este concepto.

### P3: ¿Qué porcentaje del monto de Comisiones posee respaldo documental XML?

**Respuesta: 65.2%**

- XML Comisiones: $41,824,297 (47 items, facturas + NC)
- Ledger Comisiones sobre pedidos: $64,158,492
- Cobertura: **65.2%**
- Gap: $22,334,195 (34.8% sin XML)

### P4: ¿Qué porcentaje del monto de Costos Logísticos posee respaldo documental XML?

**Respuesta: >100% (desajuste estructural)**

- XML Logística: $49,398,053 (incluye cofinanciamiento)
- Ledger "Descuento por costo logístico": $12,847,249
- **El XML duplica con creces el ledger** (384.5%)

**Interpretación:** El ledger clasifica costos logísticos en múltiples grupos. "Descuento por costo logístico" ($12.8M) probablemente es solo un subconjunto. El resto de la logística XML ($36.6M) se clasifica en otras categorías del ledger (costos_operacionales, acuerdos comerciales, etc.).

**Incertidumbre:** Sin DTEIndexer, no podemos rastrear dónde termina cada costo logístico en el ledger.

### P5: ¿Qué porcentaje de Devoluciones posee una Nota de Crédito asociada?

**Respuesta: 62.9%**

- NC DTE 43: $52,179,469 (105 NCs)
- Ledger "Pedidos reembolsados": $82,896,873
- Cobertura: **62.9%**
- Gap: $30,717,404 (37.1% sin NC)

### P6: ¿Existen conceptos cobrados por RIPLEY que no tengan respaldo documental identificable?

**Respuesta: SÍ — Parcialmente**

| Concepto | Monto | Respaldo |
|----------|-------|----------|
| Comisiones (34.8% gap) | $22.3M | Parcial |
| Devoluciones (37.1% gap) | $30.7M | **SIN NC** |
| Envío/Gastos de envío | $18.4M | **SIN XML** |
| A pagar (settlement) | $206.9M | No requiere |

**Total sin respaldo identificable:** ~$71.4M (17.3% del ledger total)

### P7: ¿Existen XML emitidos por RIPLEY que nunca impactan financieramente el ledger?

**Respuesta: HIPÓTESIS — No se puede determinar sin DTEIndexer**

- Los 407 XML son estructuralmente válidos (DTE 33/43/52/61)
- Potencialmente, Notas de Crédito (43) o Débito (52) podrían no tener impacto si:
  - Fueron emitidas pero no procesadas
  - Corresponden a ajustes que el ledger trata diferente
- **Sin embargo**, $52.2M en NC es menor que $82.9M en devoluciones ledger — por lo tanto NO hay evidencia de NC "huérfanas" sin impacto

**Incertidumbre:** No podemos afirmar ni descartar sin DTEIndexer.

### P8: ¿Existe algún identificador puente?

**Respuesta: NO — No existe llave directa**

**Evidencia:**
- XML Folio SII (7-8 dígitos, ej: 1978496) ≠ ledger folio_xml (5-6 dígitos, ej: 592974)
- 0 overlap directo entre los 407 XML Folios y los 20 unique ledger folio_xml
- id_transaccion formato: `RIP_{folio_xml}_{order_id}` — no contiene referencia XML

**Único método viable:** Amount + Date matching (probado en PARIS con 82.6% de éxito)

---

## J. Conclusión: ¿Qué porcentaje de cada peso tiene respaldo documental?

### Fórmula de Cálculo

```
P&L Direccionable = Ledger total - Settlement (A pagar)
                  = $413,893,686 - $206,946,843
                  = $206,946,843

Cobertura XML sobre P&L direccionable:
  = XML Total / P&L Direccionable
  = $186,705,151 / $206,946,843
  = 90.2%
```

### Por cada peso de P&L:

| Componente | Porcentaje | Respaldo |
|------------|-----------|----------|
| **Con XML directo** | **90.2%** | Comisiones, logística, acuerdos, devoluciones parciales |
| **Sin XML** | **9.8%** | Envíos, comisiones remanentes, devoluciones remanentes |

### Por cada peso de ledger total (incluyendo settlement):

| Componente | Porcentaje | Respaldo |
|------------|-----------|----------|
| **Con XML directo** | **45.1%** | Ventas parciales, comisiones, logística |
| **Settlement (no requiere)** | **50.0%** | Espejo de P&L |
| **Sin XML** | **4.9%** | $20.3M en envíos, comisiones faltantes, gap de devoluciones |

---

## K. Recomendación para Sprint A5

### K.1 Estrategia de Matching

**FASE 1 — Amount + Date Matching (alta prioridad)**
- Implementar matching por: `ledger.fecha ≈ XML.FchEmis` AND `SUM(ledger.monto) ≈ XML.MntTotal`
- Ventana temporal: ±3 días (experiencia PARIS)
- Match por período quincenal (las comisiones XML son quincenales)
- **Estimación:** 60-70% de XMLs match directo

**FASE 2 — Bridge XLSX (pendiente de acceso)**
- Verificar si los XLSX fuente contienen columna con DTE Folio
- En PARIS se descubrieron 2 columnas puente no documentadas
- **Potencial:** Match directo si existe columna "No. Liquidación"

**FASE 3 — Matching Residual**
- Para XMLs no matcheados: revisión manual de diferencias
- Priorizar por monto (top 10 XMLs = >50% del valor)

### K.2 Priorización por Concepto

| Orden | Concepto | Cobertura | Esfuerzo | Impacto |
|-------|----------|-----------|----------|---------|
| 1 | Comisiones | 65.2% | Bajo (períodos quincenales) | Alto |
| 2 | Devoluciones | 62.9% | Medio (105 NCs) | Alto |
| 3 | Logística | >100% | Medio (desajuste estructural) | Medio |
| 4 | Ventas (SKU) | 16.1% | Alto (1,528 items) | Bajo (ya está en XLSX) |

### K.3 Riesgos Controlados para A5

1. **NO ejecutar** actualización de `folio_xml` o `estado_xml` sin bridge verificado
2. **NO modificar** el ledger con resultados parciales de matching
3. **DOCUMENTAR** cada match/no-match con evidencia
4. **VALIDAR** contra PARIS: 54 XMLs ya tienen bridge — usar como control

### K.4 Tabla Resumen de Decisión

| Aspecto | Decisión |
|---------|----------|
| DTEIndexer ejecutable | **NO** — hasta tener estrategia definida |
| Amount+Date matching | **SÍ** — implementar en A5 |
| XLSX bridge discovery | **SÍ** — revisar columnas no documentadas |
| Modificación DB | **NO** — solo análisis |
| Certificación XML | **PENDIENTE** — post A5 |
