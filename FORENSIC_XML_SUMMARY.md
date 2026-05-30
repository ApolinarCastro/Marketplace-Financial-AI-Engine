# FORENSIC XML SUMMARY (Recalculado 29-May-2026) — RIPLEY V2

> Universo depurado post-limpieza de duplicados. RIPLEY recalculado desde cero con 5 fuentes:
> XML, CSV2025 (Historial), PEDIDOS CSV, Liquidaciones originales (vía Ledger), Ledger.
> Encoding normalizado (ASCII fold + leading zero strip). Solo igualdad exacta.

---

## FASE 1: INVENTARIO DOCUMENTAL

| Metrica | PARIS | RIPLEY |
|---------|-------|--------|
| XML fisicos | 154 | 100 |
| XML unicos (MD5) | 154 | 100 |
| Duplicados internos | 0 | 0 |
| Folios unicos | 154 | 100 |
| FolioRefs unicos | 42 | 17 |
| TipoDTE 33 | 89 | 60 |
| TipoDTE 43 | 44 | 20 |
| TipoDTE 52 | 16 | 16 |
| TipoDTE 61 | 5 | 4 |

### Cruce PARIS vs RIPLEY

| Metrica | Valor |
|---------|-------|
| XML compartidos (mismo MD5) | 100 |
| XML solo en PARIS | 54 |
| XML solo en RIPLEY | **0** |
| Folios comunes | 100 |
| Folios PARIS exclusivos | 54 |
| Folios RIPLEY exclusivos | **0** |

**Conclusión:** RIPLEY no posee XML propios. Los 100 archivos en su carpeta son copias
exactas (mismo MD5) de XML de PARIS (CENCOSUD RUT 81201000-K). Carpeta RIPLEY es un
subconjunto incompleto de PARIS/Facturacion.

---

## FASE 2: TRAZABILIDAD XML -> EXCEL

### PARIS (31 excels)

| Columna Excel | Hits Folio | Hits FolioRef |
|--------------|-----------|--------------|
| `numero factura` | 31,080 hits | - |
| `numero liq.factura` | 9,012 hits | - |
| `nro solicitud factura` | - | 31,080 hits |

**Folios en Excel: 48/154** (31%):
- Fulfillment: 39/154 (col `numero liq.factura`, Tipo 43 - Liquidacion)
- Dropshipping: 9/154 (col `numero factura`, Tipo 33 - Factura)
- 106 Folios SIN match: 50 Tipo 33 + 5 Tipo 43 + 16 Tipo 52 + 5 Tipo 61

**FolioRefs en Excel: 24/42** (57%):
- Fulfillment: 15/42 (col `nro solicitud factura`)
- Dropshipping: 9/42 (col `nro solicitud factura`)
- 18 FolioRefs SIN match

### RIPLEY (40 excels)

| Columna Excel | Hits Folio | Hits FolioRef |
|--------------|-----------|--------------|
| `A pagar` | 1 falso positivo | - |

**Folios en Excel: 0/100** (1 falso positivo: 122952 en col `A pagar` = monto $122,952)
**FolioRefs en Excel: 0/17**

---

## FASE 3: TRAZABILIDAD EXCEL -> LEDGER

### PARIS

| Campo | Excel | Ledger | Status |
|-------|-------|--------|--------|
| numero factura | Y (col `numero factura`, `numero liq.factura`) | Y (col `folio_xml`) | FULL |
| nro solicitud factura | Y (col `nro solicitud factura`) | N | PARTIAL |
| orden de compra | Y (cols `numero orden`, `nro suborden`) | Y (col `id_orden`) | FULL |
| **folio_xml poblado** | - | **0/42,487** | **NONE** |

### RIPLEY

| Campo | Excel | Ledger | Status |
|-------|-------|--------|--------|
| numero documento liquidacion | Y (col `numero documento liquidacion`) | N | PARTIAL |
| orden de compra | Y (col `orden de compra`) | Y (col `id_orden`) | FULL |
| **folio_xml poblado** | - | **0/269,216** | **NONE** |

---

## FASE 4: MATRIZ FINAL

| Marketplace | XML->Excel | Excel->Ledger | XML->Ledger |
|-------------|-----------|---------------|-------------|
| **PARIS** | **PARTIAL** (48/154 F, 24/42 R) | **NONE** (folio_xml 0/42,487) | **NONE** |
| **RIPLEY** | **NONE** (0/100 F, 0/17 R) | **NONE** (folio_xml 0/269,216) | **NONE** |

### RIPLEY — Trazabilidad 5 Fuentes (recálculo completo)

#### Relaciones entre fuentes NO XML

| Relación | Campo clave | Match |
|----------|------------|-------|
| CSV2025 "Número de pedido" ↔ PEDIDO "Order number" | Order ID | **12,998/13,128 (99%)** |
| CSV2025 "Número de pedido" → Ledger "id_orden" | Order ID | **7,475/13,128 (57%)** |
| PEDIDO "Order number" → Ledger "id_orden" | Order ID | **7,475/13,473 (55%)** |
| CSV2025 "Número de factura" ↔ PEDIDO "Número de factura" | Liquidation ID | **47/108 (43.5%)** — 47/47 (100%) |
| CSV2025 "Número de factura" → Ledger "id_transaccion" | Liquidation ID | **40/108 (37%)** — 40/40 (100%) |
| PEDIDO "Número de factura" → Ledger "id_transaccion" | Liquidation ID | **40/47 (85.1%)** — 40/40 (100%) |

Las fuentes CSV2025 ↔ PEDIDO ↔ LEDGER están conectadas entre sí por dos llaves:
- `Order number` ↔ `id_orden` (order ID, formato `NNNNNNNNNNN-A`)
- `Número de factura` ↔ `id_transaccion` (ID de liquidación CENCOSUD, 6 dígitos)

#### Relaciones XML vs todo lo demás

| Relación | Match Folio XML | Match FolioRef XML |
|----------|----------------|-------------------|
| ↔ CSV2025 "Número de factura" (108 IDs) | **0/100** | **0/17** |
| ↔ CSV2025 "Número de pedido" (13,128) | **0/100** | **0/17** |
| ↔ CSV2025 "Número de transacción" (1,256) | **0/100** | **0/17** |
| ↔ PEDIDO "Número de factura" (47) | **0/100** | **0/17** |
| ↔ PEDIDO "Order number" (13,473) | **0/100** | **0/17** |
| ↔ Ledger "id_orden" (7,475) | **0/100** | **0/17** |
| ↔ Ledger "id_transaccion" (40) | **0/100** | **0/17** |
| ↔ Ledger "folio_xml" | **0/100** | **0/17** |

#### Universos de identificadores (disjuntos)

| Sistema | Tipo ID | Ejemplos | Rango |
|---------|---------|----------|-------|
| XML Folio | Folio DTE (SII) | 122727, 53136438 | 6-8 dígitos |
| XML FolioRef | FolioRef DTE (SII) | 02410103, 13761166 | 8 dígitos |
| CSV2025/PEDIDO Factura | ID Liquidación CENCOSUD | 499799, 500346, 589546 | 6 dígitos |
| CSV2025/PEDIDO Order | Order ID Ripley | NNNNNNNNNNN-A | 11 dígitos + "-A" |
| Ledger id_transaccion | ID Liquidación CENCOSUD | 500346, 580832 | 6 dígitos |
| Ledger id_orden | Order ID Ripley | NNNNNNNNNNN-A | 11 dígitos + "-A" |

**No hay intersección entre XML y el resto.** Los Folios DTE (122727–53136430) no aparecen
en ninguna columna de CSV2025, PEDIDOS, ni Ledger. Los FolioRef (02410103–13761166)
tampoco. CSV2025, PEDIDO y Ledger comparten sus propios IDs (liquidación CENCOSUD +
Order ID Ripley), que son conceptos comerciales distintos al Folio tributario.

### Conclusión — Raíz del problema

RIPLEY usa **dos sistemas de identificación paralelos y desconectados**:

| Sistema | Propósito | Lo emite |
|---------|-----------|----------|
| Folio DTE (XML) | Documento Tributario Electrónico | Proveedor (vendedor) ante SII |
| ID Liquidación CENCOSUD (CSV/Ledger) | Liquidación comercial del marketplace | CENCOSUD/Ripley |

Los XML (DTE) son emitidos por los proveedores con su propia numeración de Folio SII.
Las liquidaciones (Excel/CSV) son generadas por CENCOSUD con su numeración interna
de liquidación. Ambas numeraciones son secuenciales independientes sin relación.

**No existe columna puente** porque los datos provienen de dos sistemas distintos que
nunca compartieron un identificador común. Para conectar XML ↔ Liquidaciones se
necesitaría un cruce por monto + fecha + RUT (prohibido por reglas forenses), o que
CENCOSUD incluyera el Folio DTE en sus reportes de liquidación.

### Veredicto Final RIPLEY: **NONE**

| Cadena | Estado |
|--------|--------|
| XML → CSV2025 | **NONE** (0/100 Folios, 0/17 FolioRef) |
| XML → PEDIDO | **NONE** (0/100 Folios, 0/17 FolioRef) |
| XML → Ledger | **NONE** (0/100 Folios, 0/17 FolioRef, 0/269,216 folio_xml) |
| PEDIDO → Ledger | **FULL** (7,475/13,473 Order numbers en id_orden) |
| CSV2025 → Ledger | **FULL** (7,475 Orders, 40 Facturas) |
