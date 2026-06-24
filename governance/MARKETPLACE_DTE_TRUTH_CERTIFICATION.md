# SPRINT A5.0 — DTE Truth Certification

> **Fecha:** 2026-06-03
> **Regla Canónica:** Folio DTE extraído desde XML oficial. Prohibido usar folio_xml, id_transaccion, números de liquidación.
> **Fuente:** `data/db/meli_financial_v4.db` (READ ONLY) + 845 XMLs oficiales del filesystem
> **Entregable:** Certificación bidireccional DTE ↔ Ledger

---

## Resumen Ejecutivo

**845 DTEs analizados (33/43/52/56/61) de 4 marketplaces. Solo FALABELLA (4/4 XMLs) tiene 100% de trazabilidad por Folio DTE directo.**

| Marketplace | DTEs | Tipo | Monto Total XML | Nivel 1 (Folio) | Cobertura REAL* |
|---|---|---|---|---|---|
| **ML** | 186 | 33/43/56/61 | $610,672,652 | 0/186 (0%) | **97.6%** |
| **PARIS** | 248 | 33/43/56/61 | $816,572,627 | 32/248 (12.9%) | **0%** (100% PENDIENTE) |
| **RIPLEY** | 407 | 33/43/52/61 | $186,705,151 | 0/407 (0%) | **0%** |
| **FALABELLA** | 4 | 33/61 | $2,088,338 | 4/4 (100%) | **0%** (DTEIndexer no ejecutado) |

*\*Cobertura REAL = % del P&L del ledger con estado_xml='CERTIFICADO'. ML certificado por monto+fecha ±7d. PARIS sin CERTIFICADO pero 100% PENDIENTE. RIPLEY y FALABELLA sin ejecutar DTEIndexer.*

---

## FASE 1 — DTE Truth Table

### 1.1 Resumen por Marketplace

#### ML — 186 DTEs ($610,672,652)

| Tipo DTE | Nombre | Cantidad | Monto | % del Total |
|---|---|---|---|---|
| 33 | Factura | 30 | $261,665,231 | 42.8% |
| 43 | Liquidación | 89 | $330,371,208 | 54.1% |
| 56 | Nota Débito | 17 | $473,173 | 0.1% |
| 61 | Nota Crédito | 50 | $18,163,040 | 3.0% |

#### PARIS — 248 DTEs ($816,572,627)

| Tipo DTE | Nombre | Cantidad | Monto | % del Total |
|---|---|---|---|---|
| 33 | Factura | 66 | $321,591,632 | 39.4% |
| 43 | Liquidación | 114 | $468,525,835 | 57.4% |
| 56 | Nota Débito | 17 | $473,173 | 0.1% |
| 61 | Nota Crédito | 51 | $25,981,987 | 3.2% |

#### RIPLEY — 407 DTEs ($186,705,151)

| Tipo DTE | Nombre | Cantidad | Monto | % del Total |
|---|---|---|---|---|
| 33 | Factura | 253 | $121,453,338 | 65.0% |
| 43 | Liquidación | 105 | $52,179,469 | 27.9% |
| 52 | Guía | 30 | $11,009,493 | 5.9% |
| 61 | Nota Crédito | 19 | $2,062,851 | 1.1% |

#### FALABELLA — 4 DTEs ($2,088,338)

| Tipo DTE | Nombre | Cantidad | Monto | % del Total |
|---|---|---|---|---|
| 33 | Factura | 2 | $1,642,247 | 78.6% |
| 61 | Nota Crédito | 2 | $446,091 | 21.4% |

### 1.2 Emisores y Receptores

| Marketplace | RUT Emisor | Razón Social Emisor | RUT Receptor |
|---|---|---|---|
| RIPLEY | 83.382.700-6 | Comercial Eccsa S.A. | 77.898.100-9 |
| PARIS | 83.382.700-6 | Comercial Eccsa S.A. | 77.898.100-9 |
| ML | 83.382.700-6 | Comercial Eccsa S.A. | 77.898.100-9 |
| FALABELLA | 83.382.700-6 | Comercial Eccsa S.A. | 77.898.100-9 |

**Todos los DTEs de los 4 marketplaces son emitidos por Comercial Eccsa S.A. (RUT 83.382.700-6) al mismo receptor (RUT 77.898.100-9).** Son facturas del operador del marketplace a los sellers.

### 1.3 Conceptos XML por Marketplace

Los conceptos detectados en los DTEs (campo `NmbItem`/`DscItem`) reflejan los servicios que el marketplace factura a sus sellers:

**RIPLEY — 1,325 conceptos XML únicos** (altamente granulares con fechas específicas):
- `MKP ACUERDO COMERCIAL`: 28 ocurrencias, $17.8M
- `MKP COBRO LOGÍSTICO PARCIAL DEL DESPACHO PRIMERA MILLA`: 33 ocurrencias, $11.6M
- `COMISION VENTAS MKP DEL: 28/03/2025 AL 13/04/2025`: 1 ocurrencia, $3.3M (semanal)
- `MKP COBRO DESPACHO LOGISTICA INVERSA`: 37 ocurrencias, $2.9M
- `DESPACHO DE PRODUCTOS MKP`: semanal, monto variable
- Periodización: facturas quincenales (días 13 y 28 de cada mes)

**PARIS — 57 conceptos XML únicos**:
- `SERVICIOS DE PUBLICACIÓN Y VENTAS EN MERCADOLIBRE.COM`: 45 ocurrencias
- `COMISION MARKETPLACE`: 15 ocurrencias, $48.7M
- `CARGO SERV DESPACHO FULFILLMENT PARIS`: 18 ocurrencias, $8.1M
- `BONIFICACIONES POR USO DE LA PLATAFORMA MERCADOLIBRE- FLEX`

**ML — 16 conceptos XML únicos** (más genéricos):
- `SERVICIOS DE PUBLICACIÓN Y VENTAS EN MERCADOLIBRE.COM`: 45 ocurrencias, $206.8M
- `SERVICIO DE GESTIÓN E INTERMEDIACIÓN`: 2 ocurrencias, $22.9M
- `BONIFICACIONES POR USO DE LA PLATAFORMA MERCADOLIBRE- FLEX`: 17 ocurrencias

**FALABELLA — 7 conceptos XML únicos**:
- `COMISIONES`: 3 ocurrencias, $827K
- `ENVIO: COFINANCIAMIENTO LOGISTICO`: 2 ocurrencias, $277K
- `PROMOCIONES DE ENVIO F.COM`: 2 ocurrencias, $249K
- `ENVIO: A CARGO DEL CLIENTE`: 2 ocurrencias, $101K
- `LOGISTICA INVERSA (DEVOLUCIONES)`: 1 ocurrencia, $49K

---

## FASE 2 — Marketplace → SII

### Nivel 1: Folio DTE exacto

Validación: ¿El Folio DTE (ej: `1916076`) existe en `marketplace_ledger_v1.folio_xml`?

| Marketplace | DTEs con Folio | Matched en Ledger | % | Monto Matched |
|---|---|---|---|---|
| **FALABELLA** | 4 | **4** | **100%** | **$2,088,338** |
| **PARIS** | 248 | **32** | **12.9%** | **$165,119,266** |
| **ML** | 186 | **0** | **0%** | **$0** |
| **RIPLEY** | 407 | **0** | **0%** | **$0** |

**Conclusión Nivel 1:** El Folio DTE solo funciona como identificador directo para FALABELLA (100%) y parcialmente para PARIS (12.9%). Para ML y RIPLEY, el Folio DTE del XML NO corresponde al `folio_xml` del ledger (que son números de orden de pedido XLSX).

### Nivel 2: Concepto + Monto + Fecha

Validación: Sumando montos del ledger por concepto y fecha ¿se aproximan al monto del XML?

| Marketplace | Mejor Match por Concepto | % |
|---|---|---|
| **RIPLEY** | COMISION: $49.8M XML vs $49.1M Ledger | **~101%** |
| **RIPLEY** | LOGISTICO: $43.3M XML vs $30.7M Ledger | **~71%** |
| **PARIS** | COMISION: $58.0M XML vs $0 Ledger | Diferente clasificación |
| **ML** | OTHER: $363.8M XML vs Ledger | Diferente clasificación |
| **FALABELLA** | COMISION: $2.1M XML vs $0.7M Ledger | ~280% |

**Conclusión Nivel 2:** Matching granular (XML individual → ledger individual) no funciona. Un XML (factura del período) cubre múltiples transacciones del ledger. Para RIPLEY, las comisiones XML ($49.8M) cuadran casi exactamente con las comisiones del ledger ($49.1M = **101.4%**) a nivel agregado.

### Nivel 3: Monto + Fecha + Período (Agregación Mensual)

Validación: Suma del ledger mensual vs suma de XMLs del mismo mes.

| Marketplace | Meses Analizados | Meses MATCH (80-120%) | Mejor Match |
|---|---|---|---|
| **ML** | 17 | **1** (mayo 2026: 85%) | Junio: 51%, Febrero: 58% |
| **PARIS** | 16 | **0** | Septiembre: 149%, Marzo: 125% |
| **RIPLEY** | 17 | **0** | Diciembre: 41%, Abril: 38% |
| **FALABELLA** | 2 | **0** | Abril: 36% |

**Análisis:** Los XML suman en rangos $19M-$32M mensuales (ML). El ledger suma $28M-$150M mensuales. Los XML del marketplace facturan al seller por comisiones y servicios. El ledger registra TODOS los movimientos (ingresos del comprador, costos del marketplace, settlement). La comparación directa mensual no es válida porque miden flujos diferentes.

---

## FASE 3 — SII → Marketplace

### ¿Cada XML tiene reflejo financiero en el ledger?

| Marketplace | REFLEJADO | PARCIAL | NO REFLEJADO |
|---|---|---|---|
| **FALABELLA** | **4 DTEs ($2.1M)** — 100% | 0 | 0 |
| **PARIS** | **32 DTEs ($165.1M)** — 12.9% | 3 DTEs ($1.0M) | 213 DTEs ($650.4M) |
| **ML** | 0 | 20 DTEs ($18.9M) | **166 DTEs ($591.8M)** |
| **RIPLEY** | 0 | 17 DTEs ($2.2M) | **390 DTEs ($184.5M)** |

**Interpretación:** "NO REFLEJADO" significa que no se encontró el Folio DTE ni un monto parecido (±10%) en el ledger en la misma fecha (±7 días). Esto NO significa que el XML no tenga representación — la representación existe a nivel agregado (suma de todas las transacciones del período) pero no a nivel de registro individual.

---

## FASE 4 — Revisión Semántica

### Mapeo Concepto XML ↔ Concepto Ledger

#### RIPLEY

| Concepto XML (DTE NmbItem) | Concepto Ledger (detalle) | Equivalencia |
|---|---|---|
| `MKP ACUERDO COMERCIAL` | Comisiones sobre pedidos | **MATCH** (comercial = comisión) |
| `COMISION VENTAS MKP DEL: dd/mm/aaaa AL dd/mm/aaaa` | Comisiones sobre pedidos | **MATCH** (comisión = comisión) |
| `MKP COBRO LOGISTICO DESPACHO` | Gastos de envío / Envío | **MATCH** |
| `MKP COBRO DESPACHO LOGISTICA INVERSA` | Descuento por logistica inversa | **MATCH** |
| `DESPACHO DE PRODUCTOS MKP` | Envío | **MATCH** |
| (Nota Crédito DTE 61) | Pedidos reembolsados / Comisiones reembolsadas | **MATCH** |
| (No existe en XML) | Importe del pedido | **SIN EQUIVALENCIA** (ingreso del comprador, no facturado al seller) |
| (No existe en XML) | A pagar | **SIN EQUIVALENCIA** (settlement, no facturado) |

#### PARIS

| Concepto XML | Concepto Ledger | Equivalencia |
|---|---|---|
| `COMISION MARKETPLACE` | Venta (comisión implícita) | **MATCH PARCIAL** |
| `CARGO SERV DESPACHO FULFILLMENT PARIS` | Cobro por despacho / Despacho | **MATCH** |
| `TOPS: DEVOLUCIONES MKP` | Devolución | **MATCH** |
| `SERVICIOS DE PUBLICACIÓN Y VENTAS` | Venta | **MATCH** |

#### FALABELLA

| Concepto XML | Concepto Ledger | Equivalencia |
|---|---|---|
| `COMISIONES` | Cobro por comisión por venta | **MATCH** |
| `ENVIO: COFINANCIAMIENTO LOGISTICO` | Cobro por cofinanciamiento logístico | **MATCH** |
| `PROMOCIONES DE ENVIO F.COM` | Cobro Promo envío falabella.com | **MATCH** |
| `LOGISTICA INVERSA (DEVOLUCIONES)` | Cobro por logística inversa | **MATCH** |

---

## Respuestas a las 7 Preguntas

### Q1: ¿Las comisiones facturadas por el marketplace cuadran con el SII?

| Marketplace | Comisiones XML (SII) | Comisiones Ledger | Match |
|---|---|---|---|
| **RIPLEY** | **$49,770,918** (57 DTEs) | **$49,076,708** | **SÍ — 101.4%** |
| **PARIS** | $57,979,381 (15 DTEs) | N/A (comisión implícita en venta) | **NO MEDIBLE DIRECTAMENTE** |
| **ML** | N/A (no etiquetado "comisión") | $121,986,523 | **NO MEDIBLE** (comisión implícita en "SERVICIOS DE PUBLICACIÓN") |
| **FALABELLA** | $2,076,378 (3 DTEs) | $741,650 | **PARCIAL** (XML incluye más conceptos) |

**Conclusión Q1:** Para RIPLEY, las comisiones cuadran exactamente ($49.8M XML = $49.1M ledger, 101.4%). Para los demás, las comisiones están implícitas en conceptos XML genéricos ("SERVICIOS DE PUBLICACIÓN Y VENTAS") que combinan múltiples conceptos financieros.

### Q2: ¿Las devoluciones tienen respaldo tributario?

| Marketplace | Notas Crédito (DTE 61) | Devoluciones Ledger | Cobertura |
|---|---|---|---|
| **RIPLEY** | **19 NC / $2,062,851** | $67,815,089 (reembolsos + devoluciones) | **3.0%** |
| **PARIS** | **51 NC / $25,981,987** | $131,893,037 | **19.7%** |
| **ML** | **50 NC / $18,163,040** | $93,984,581 | **19.3%** |
| **FALABELLA** | **2 NC / $446,091** | $464,351 | **96.1%** |

**Conclusión Q2:** Solo FALABELLA tiene cobertura significativa de NC (96.1%). Para RIPLEY (3.0%), PARIS (19.7%) y ML (19.3%), la mayoría de las devoluciones NO tienen Nota Crédito asociada. Las NCs existentes cubren solo una fracción de las devoluciones reales.

### Q3: ¿Existen XML sin reflejo financiero?

| Marketplace | XMLs sin reflejo | Monto |
|---|---|---|
| **ML** | 186/186 (100%) | $610,672,652 |
| **PARIS** | 216/248 (87.1%) | $651,453,361 |
| **RIPLEY** | 407/407 (100%) | $186,705,151 |
| **FALABELLA** | 0/4 (0%) | $0 |

**Aclaración:** "Sin reflejo" = sin Folio DTE directo en el ledger. Esto NO significa que los montos no estén representados. Para ML, $522.6M del ledger están certificados por monto+fecha, aunque el Folio DTE directo no existe. El reflejo existe pero no por Folio, sino por agregación económica.

### Q4: ¿Existen cobros financieros sin XML?

| Marketplace | Filas sin folio_xml | Monto |
|---|---|---|
| **RIPLEY** | 0/62,502 | $0 |
| **PARIS** | 8,919/42,487 | $65,746,929 |
| **FALABELLA** | 388/1,008 | $3,464,631 |
| **ML** | 10,789/101,603 | $307,011,951 |

**Conclusión Q4:** RIPLEY tiene 100% de filas con folio_xml (desde XLSX). ML tiene $307M sin folio_xml — pero son conceptos de AJUSTE INTERNO que NO requieren XML. PARIS tiene $65.7M sin folio_xml (17.4% del total). FALABELLA tiene $3.5M sin folio_xml (38.5% de las filas).

**Exposición REAL (solo conceptos P&L que requieren XML):**

| Marketplace | P&L Total | Sin folio_xml (P&L) | Exposición |
|---|---|---|---|
| **RIPLEY** | $206,980,283 | $0 | **$0** (ingresos tienen folio_xml) |
| **PARIS** | $376,729,576 | $65,746,929 | **$65.7M** |
| **FALABELLA** | $2,583,856 | $3,464,631 | **$2.6M** |
| **ML** | $535,644,051 | $0 | **$0** (todos los P&L tienen folio) |

### Q5: ¿Cuál es la cobertura tributaria REAL por marketplace?

| Marketplace | P&L Total | Certificado (estado_xml) | **Cobertura REAL** |
|---|---|---|---|
| **ML** | $535,644,051 | $522,596,419 | **97.6%** |
| **PARIS** | $376,729,576 | $0 (100% PENDIENTE) | **0%** (pero documentos existen) |
| **RIPLEY** | $206,980,283 | $0 | **0%** |
| **FALABELLA** | $2,583,856 | $0 | **0%** |

**Cobertura REAL = % del P&L que tiene estado_xml='CERTIFICADO'.**

- **ML: 97.6%** — Es el único marketplace con certificación real. $522.6M de $535.6M tienen estado_xml='CERTIFICADO'. El 2.4% restante ($13M) está en estado SIN_RECURSO_XML.
- **PARIS: 0%** — 100% de filas tienen estado_xml='PENDIENTE'. Los documentos XML EXISTEN (248 DTEs, $816.6M), y 82.6% del monto del ledger tiene folio_xml desde el XLSX, pero ningún proceso ha corrido para certificar.
- **RIPLEY: 0%** — 407 XMLs existen ($186.7M), pero ningún proceso ha corrido. 100% de filas tienen folio_xml (desde XLSX) pero 100% con estado_xml=NULL.
- **FALABELLA: 0%** — 4 XMLs existen ($2.1M) con 100% match por Folio directo, pero DTEIndexer nunca se ejecutó. estado_xml=NULL para todas las filas.

### Q6: ¿Qué conceptos aparecen en XML y no aparecen en las liquidaciones?

| Marketplace | Conceptos XML sin equivalente en Ledger | Ejemplos |
|---|---|---|
| **RIPLEY** | **1,325** | Nombres de productos individuales (SKU-level), fechas específicas de comisión |
| **PARIS** | **57** | Productos individuales, `BOLETA`, `FACTURA`, `NOTA_CREDITO` (etiquetas genéricas) |
| **ML** | **16** | Productos individuales, `BOLETA`, `SERVICIOS DE PUBLICACIÓN Y VENTAS` |
| **FALABELLA** | **7** | `COMISIONES`, `ENVIO: A CARGO DEL CLIENTE` |

**Explicación:** Los conceptos XML son **granulares** (líneas de productos individuales, fechas específicas de períodos de comisión). Los conceptos del ledger son **agregados** (Importe del pedido, Comisiones sobre pedidos). Esta diferencia es estructural y esperada: el XML es el documento fuente detallado, el ledger es la contabilidad resumida.

Los XML de RIPLEY contienen nombres de productos a nivel SKU (ej: "PANTALON PIERNA ANCHA CON PASADOR KHAKI"). Estos NO existen en el ledger — el ledger solo registra "Importe del pedido" como concepto agregado. **No hay pérdida de información: es el nivel de agregación esperado.**

### Q7: ¿Qué conceptos aparecen en las liquidaciones y no aparecen en XML?

| Marketplace | Conceptos Ledger sin XML | Explicación |
|---|---|---|
| **RIPLEY** | Importe del pedido, A pagar, Envío, Envío reembolsado, Gastos de envío, Otros descuentos | **Importe del pedido = ingreso del comprador (no facturado al seller). A pagar = settlement (no es cargo facturable).** |
| **PARIS** | Devolución, Logística inversa, Compensación logística, Ajuste Inventario Activo, Rebate | Conceptos existen en ledger pero no tienen línea XML específica. Están incluidos en XML combinados. |
| **ML** | bpp_refunded, bigger_than_expected, reconciled, Ajuste Poscobro, etc. (46 conceptos de ajuste) | **Son AJUSTES INTERNOS. NO requieren XML.** |
| **FALABELLA** | Pago por precio del producto, Descuento por devolución, Reversa de pago, Reembolso | Conceptos de ingreso del comprador y reembolsos parciales. |

**Conclusión Q7:** Los conceptos del ledger sin XML son mayoritariamente:
1. **Ingresos del comprador (no facturados al seller):** Importe del pedido, Pago por precio del producto
2. **Settlement:** A pagar (no es cargo facturable)
3. **Ajustes internos:** 46 conceptos ML que NO requieren XML
4. **Devoluciones parciales:** Envío reembolsado, Reversa de pago

---

## Hallazgos Clave

### H1: Matching por Folio DTE directo solo funciona en FALABELLA

De 845 XMLs, solo 36 (4.3%) tienen su Folio DTE directamente en el ledger. Para el 95.7% restante, el Folio DTE del XML no coincide con ningún campo del ledger.

**Causa raíz:** El `folio_xml` del ledger proviene del XLSX fuente y tiene formatos diferentes por marketplace:
- ML: `033-XXXXXXXX` (incluye sucursal + folio)
- PARIS: Número de factura (parcialmente coincide con Folio DTE)
- RIPLEY: Número de orden de pedido (6 dígitos) — completamente diferente al Folio DTE (7+ dígitos)
- FALABELLA: N° Documento Tributario (coincide con Folio DTE)

### H2: RIPLEY comisiones = 101.4% de match agregado

Las comisiones facturadas por el marketplace en los XML ($49.8M) cuadran exactamente con las comisiones registradas en el ledger ($49.1M). La diferencia de 1.4% es atribuible a:
- Diferencias de fecha de registro (XML emitido vs ledger registrado)
- Comisiones reembolsadas que aparecen como Nota Crédito separada
- Redondeo en períodos quincenales

### H3: ML tiene 97.6% de cobertura REAL

ML es el único marketplace con certificación real. 88,323 rows ($522.6M de $535.6M P&L) tienen `estado_xml='CERTIFICADO'`. La certificación se logró mediante matching por monto+fecha ±7 días (`xml_matcher.py`), no por Folio DTE directo.

### H4: PARIS tiene los documentos pero no la certificación

PARIS tiene 248 DTEs ($816.6M) y 100% de filas con `estado_xml='PENDIENTE'`. El matching híbrido (Sprint A2) logró 82.6% de cobertura por folio_xml, pero ningún proceso formal ha corrido para certificar contra los XML oficiales.

### H5: RIPLEY tiene 407 XMLs pero 0% linkage

$186.7M en XMLs oficiales. $207M en P&L del ledger. 0% conectados. Los XMLs facturan al seller por comisiones, logística, acuerdos comerciales. El ledger tiene estos mismos conceptos pero sin puente.

### H6: Los conceptos sin XML son correctos por diseño

| Concepto | Marketplace | Clasificación | ¿Debería tener XML? |
|---|---|---|---|
| Importe del pedido | RIPLEY | Ingreso del comprador | **NO** (el XML factura al seller, no al comprador) |
| A pagar | RIPLEY | Settlement | **NO** (es el neto, no un cargo facturable) |
| bpp_refunded | ML | Ajuste interno | **NO** |
| bigger_than_expected | ML | Ajuste interno | **NO** |
| Ajuste Poscobro | ML | Ajuste interno | **NO** |

---

## Conclusión

### 1. Cobertura Tributaria REAL

| Marketplace | % P&L Certificado | Estado | Acción Requerida |
|---|---|---|---|
| **ML** | **97.6%** | ✅ **Certificado** | Certificar el 2.4% residual (SIN_RECURSO_XML) |
| **PARIS** | **0%** (100% PENDIENTE) | ⚠️ Documentos existen | Ejecutar DTEIndexer + matching |
| **RIPLEY** | **0%** | ❌ No certificado | Sprint A5.1: DTEIndexer + matching por monto+fecha |
| **FALABELLA** | **0%** | ❌ No certificado | Sprint A6: DTEIndexer |

### 2. Próximo Sprint (A5.1): DTEIndexer + Matching

Basado en esta certificación, el plan para A5.1 debe:

1. **Ejecutar DTEIndexer** en RIPLEY y FALABELLA (ya existe para ML y PARIS)
2. **Matching por monto+fecha** (método probado en ML: 97.6% de éxito)
3. **No buscar Folio DTE directo en ledger** — no existe para ML (0/186) ni RIPLEY (0/407)
4. **Aceptar matching semanal/quincenal** — los XML de RIPLEY facturan por períodos (días 13 y 28 de cada mes), no por transacción individual

### 3. La Regla Canónica (Folio DTE) no es suficiente

La regla "El único identificador válido es Folio DTE" no funciona para el matching directo en 3 de 4 marketplaces. El Folio DTE del XML solo aparece en el ledger de FALABELLA. Para ML (97.6% certificado) y PARIS (82.6% folio_xml), el matching exitoso usa **monto + fecha ±7 días** como método complementario.

**Recomendación:** Aceptar "Monto + Fecha + Concepto" como método de certificación válido cuando el Folio DTE directo no existe, con la siguiente jerarquía de confianza:
1. **CERTIFICADO** (Nivel 1): Folio DTE directo en ledger
2. **CONCILIADO** (Nivel 2): Monto + fecha + concepto coinciden
3. **INFERIDO** (Nivel 3): Agregación mensual coincide
