# RIPLEY DTE Bridge Forensics — Certification Report

> **Fecha:** 2026-06-03
> **Tipo:** Forense — READ ONLY
> **Hipótesis:** `RIP_<numero>_` en `id_transaccion` contiene Folio DTE
> **Estado:** **HIPÓTESIS FALSADA — No existe puente reutilizable**

---

## Resumen Ejecutivo

**NO existe puente directo entre los Folios DTE (SII) y el ledger RIPLEY.**

El patrón `RIP_<n>_` en `id_transaccion` contiene el **`folio_xml`** proveniente del archivo XLSX (número de "orden de pedido"), **NO** el Folio SII DTE.

Tras analizar 407 XMLs y 62,502 filas del ledger:

| Métrica | Resultado |
|---------|-----------|
| Filas con patrón `RIP_<n>_` | **62,502/62,502 (100%)** |
| Valores distintos de `<n>` | **46** (idénticos a `folio_xml`) |
| Overlap con Folios DTE XML | **0** |
| XMLs con match directo | **1/407 (0.2%)** — coincidencia accidental |
| Ordenes de pedido distintas | **10,555** — ninguna coincide con Folio DTE |

---

## P1: Filas con patrón `RIP_<numero>_`

**Evidencia:**

La estructura completa del `id_transaccion` es:

```
RIP_{folio_xml}_{order_id}-A_{concepto}
```

Ejemplo real:
```
RIP_592974_24628430501-A_importedelpedido
```

| Estructura | Ejemplo | Significado |
|------------|---------|-------------|
| `RIP_` | `RIP_` | Prefijo marketplace |
| `{folio_xml}` | `592974` | Número de orden de pedido (XLSX) |
| `_` | `_` | Separador |
| `{order_id}` | `24628430501` | ID interno de transacción |
| `-A_` | `-A_` | Separador |
| `{concepto}` | `importedelpedido` | Concepto económico |

**Todas las 62,502 filas (100%) cumplen este patrón.**

---

## P2: Valores distintos de `<n>`

**46 valores distintos**, exactamente los mismos que `folio_xml` en la columna homónima.

```
500346, 503106, 505930, 508667, 511338, 514115, 517031, 519418,
521993, 524491, 526971, 529315, 531516, 533710, 535997, 538209,
540610, 543422, 546116, 548494, 550779, 551904, 553661, 554612,
556626, 557771, 560350, 561221, 562946, 564540, 566213, 567819,
569570, 571181, 572859, 574264, 575911, 577566, 579224, 580832,
582603, 586105, 587807, 589546, 591235, 592974
```

**Confirmado: 46 = 46 (`folio_xml`). Coincidencia exacta.**

---

## P3: Coincidencia con Folios XML

**0 coincidencias directas.**

Los Folios DTE en los XML son números de 6-8 dígitos en rangos distintos:

| Sistema | Rango | Ejemplos |
|---------|-------|----------|
| Ledger `folio_xml` | 500,346 — 592,974 | 517031, 567819, 592974 |
| XML Folio (DTE 33) | 1,978,496 — 2,416,663 | 1978496, 2143381, 2416663 |
| XML Folio (DTE 43) | 108,927 — 124,476 | 108927, 119107, 122728 |
| XML Folio (DTE 52) | 48,452,291 — 53,395,064 | 48452291, 53395061 |
| XML Folio (DTE 61) | 6,837,014 — 7,707,465 | 6837014, 7707230 |

**Los rangos no se intersectan.** El `folio_xml` del ledger (500K-593K) está en un rango intermedio que no corresponde a ningún tipo DTE.

---

## P4: Porcentaje de XMLs con referencia en ledger

**0.2% — coincidencia accidental, no estructural.**

De 407 XMLs, solo **1** (Folio DTE 2412920, $27,000) mostró coincidencia en el ledger — y fue identificada como **falsa positiva** porque el número 2412920 aparece como substring dentro de un `order_id` más grande: `24129208201`.

**49/50 XMLs de la muestra estadística fueron RECHAZADOS.**

| Clasificación | XMLs | Monto | % |
|--------------|------|-------|---|
| CERTIFIED | 1 | $27,000 | 0.1% |
| PROBABLE | 0 | $0 | 0.0% |
| REJECTED | 49 | $23,174,539 | 99.9% |

---

## P5: Porcentaje del monto ledger cubierto

**0.0% — Ningún peso del ledger está vinculado a un Folio DTE mediante esta relación.**

| Fuente | Monto | Cubierto por DTE Folio |
|--------|-------|----------------------|
| Ledger total | $413,893,686 | **$0** |
| Ledger P&L | $206,946,843 | **$0** |
| XML total | $186,705,151 | **$0** (sin bridge) |

---

## P6: Otros patrones equivalentes

### 6.1 `folio_xml` (columna directa)

| Atributo | Valor |
|----------|-------|
| Filas con valor | 62,502/62,502 (100%) |
| Valores distintos | 46 (idénticos al primer número de `id_transaccion`) |
| Coincide con Folio DTE | **NO** (sistemas de numeración distintos) |

### 6.2 `order_id` (segundo segmento de `id_transaccion`)

| Atributo | Valor |
|----------|-------|
| Valores distintos | **10,555** |
| Coincide con Folio DTE | **NO** (0/10,555 matchean) |

### 6.3 Otros campos explorados

| Campo | Resultado |
|-------|-----------|
| `numero_liquidacion` | No existe en ledger |
| `referencia_dte` | No existe en ledger |
| `estado_xml` | 100% NULL |
| Cualquier campo con "folio" | Solo `folio_xml` (ya analizado) |
| Cualquier campo con "dte" | Solo en `estado_xml` y `asociacion_xml` (NULL) |

### 6.4 Estructura completa de `id_transaccion`

```
RIP_{folio_xml}_{order_id}-A_{concepto}

folio_xml = 6 dígitos (500346-592974) — ORDEN DE PEDIDO (XLSX)
order_id = 11-14 dígitos — ID INTERNO DE TRANSACCIÓN
-A_       = separador fijo
concepto  = importedelpedido | envio | comisionessobrepedidos | 
            descuentoporcostologistico | apagar | etc.
```

**Ningún segmento de `id_transaccion` contiene el Folio DTE.**

---

## P7: Validación estadística (50 XML aleatorios)

### Metodología

1. Selección aleatoria de 50 XMLs de 407 (semilla 42)
2. Para cada XML:
   - Extraer Folio DTE, FchEmis, MntTotal, Detalle
   - Buscar en ledger: coincidencia directa (substring), coincidencia por monto+fecha (±3 días), coincidencia por agregación diaria
3. Clasificar como:
   - **CERTIFIED**: Coincidencia directa en `id_transaccion` + monto proporcional
   - **PROBABLE**: Coincidencia por monto+fecha con ≤3 folios distintos
   - **REJECTED**: Sin coincidencia

### Resultados

| Clasificación | Cantidad | Monto | % XMLs |
|--------------|----------|-------|--------|
| CERTIFIED | 1 | $27,000 | 2% |
| PROBABLE | 0 | $0 | 0% |
| REJECTED | 49 | $23,174,539 | 98% |

### Falso positivo detectado

El único CERTIFIED (Folio DTE 2412920) se debió a que el número `2412920` aparece dentro de un `order_id` de 14 dígitos (`24129208201`) en el ledger. No es una coincidencia semántica, sino una coincidencia de substring numérico.

**Conclusión: 0 coincidencias reales en la muestra.**

---

## Respuesta a la Hipótesis

| Pregunta | Respuesta | Evidencia |
|----------|-----------|-----------|
| ¿`RIP_<n>_` contiene Folio DTE? | **NO** | Contiene `folio_xml` (XLSX), 0/407 XMLs matchean |
| ¿Existe puente reutilizable? | **NO** | Ningún campo del ledger contiene Folios DTE |
| ¿Coincidencia exacta o accidental? | **ACCIDENTAL** | 1 falso positivo en 50 muestras (substring) |
| ¿La estructura `RIP_<folio>_` es útil? | **SÍ, para bridge XLSX** | Conecta 46 valores de orden de pedido — pero NO con DTE |

---

## Conclusión Final

### 1. Existe puente reutilizable: **NO**

El ledger no contiene Folios DTE SII en ningún campo. La relación `RIP_<n>_` vincula al **folio_xml** (orden de pedido XLSX), no al DTE.

### 2. Cobertura potencial (% filas): **0%**

Ninguna fila del ledger puede vincularse directamente a un XML mediante Folio DTE.

### 3. Cobertura potencial (% monto): **0%**

Ningún monto del ledger está asociado a un Folio DTE.

### 4. Nivel de confianza: **MUY ALTO**

- Muestra estadística de 50/407 XMLs (12.3%)
- 62,502 filas del ledger analizadas (100%)
- 46 valores de folio_xml comparados (100%)
- 10,555 order_id comparados (100%)

### 5. Recomendación para A5

**NO es posible un bridge directo por Folio DTE.** Para Sprint A5, la estrategia debe ser:

1. **Amount + Date matching** (único método viable)
   - Coincidir MntTotal + FchEmis del XML vs fecha + monto del ledger
   - El XML agrupa MÚLTIPLES transacciones del ledger en una sola factura
   - Requiere: `SUM(ledger.monto) WHERE fecha ≈ XML.FchEmis` = `XML.MntTotal`
   - Probado en PARIS: 82.6% de éxito

2. **Revisión de XLSX fuente**
   - Verificar si los archivos XLSX contienen columna con Nro. DTE o Folio
   - En PARIS se descubrieron 2 columnas puente no documentadas

3. **No hay shortcut**
   - La hipótesis del DTE Folio embebido en `id_transaccion` queda **FALSADA**
   - El ledger y los XML operan en sistemas de identificación completamente distintos

---

## Anexo: Estructura de `id_transaccion` vs XML

```
id_transaccion ledger:
  RIP_592974_24628430501-A_importedelpedido
       ^^^^^^
       folio_xml = 592974 (XLSX orden de pedido)
                 ^^^^^^^^^^^^^
                 order_id = 24628430501 (ID interno)

XML DTE:
  <Folio>1978496</Folio>  ← SII DTE Folio (7 dígitos)
  
NO HAY RELACIÓN ENTRE AMBOS SISTEMAS DE NUMERACIÓN
```

**La llave DTE no está oculta en el ledger. No existe atajo.**
