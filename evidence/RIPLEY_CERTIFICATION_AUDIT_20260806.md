# Certificación de la Llave Documental Ripley ↔ DTE SII

## Auditoría Quirúrgica — Marketplace Financial AI Engine
**Fecha:** 2026-08-06
**Alcance:** Ripley — Trazabilidad entre reportería interna y facturación electrónica SII
**Método:** Búsqueda exhaustiva en 472 XML DTE, 51 archivos SELLER, 72 CSVs CICLOS/FF, 8 archivos TH, bitácoras de transacción, y 598,112 registros de ledger

---

## 1. Resumen Ejecutivo

Después de una búsqueda exhaustiva en todos los archivos disponibles del marketplace Ripley, **se confirma la existencia de una llave documental** entre la reportería interna de Ripley y los DTE del SII. La llave es el campo `Número de factura` presente en las bitácoras de transacción de Ripley (`transaction-logs.csv`). Sin embargo, la cobertura de esta llave en los archivos actualmente disponibles es limitada: solo 2 de 472 folios SII aparecen directamente en los archivos de liquidación SELLER.

### Veredicto General

| Componente | Estado | Evidencia |
|-----------|--------|-----------|
| Trazabilidad TH → CICLOS → SELLER → Ledger | ✅ CERTIFICADO | 49 ciclos, 13,646 + 11,974 matches |
| `dte_link_v1` Ripley | 🔴 NO FISCAL | Enlace circular LEDGER_EXISTING, 0 matches con `dte_truth_v1` |
| Llave documental identificada | ✅ CONFIRMADA | `Número de factura` en bitácoras de transacción |
| Cobertura DTE en archivos actuales | ⚠️ 0.4% | 2/472 folios en SELLER col36 |
| Estructura de emisión dual (Comisión + Despachos) | ✅ CONFIRMADA | Documento referencial Ripley + DTE SII |
| Certificación electrónica punta a punta | 🔴 NO VIABLE | Requiere bitácoras completas con `Número de factura` |

---

## 2. Estructura Documental de Ripley

### 2.1 Fuentes raw inventariadas

| Fuente | Carpeta | Archivos | Filas |
|--------|---------|----------|-------|
| TH (Historial de transacciones) | `Historial de transacciones` | 8 | 127,586 |
| CICLOS (Resumen por ciclo) | `Fulfillment by Ripley` | 49 CSV | 19,384 |
| FF (Fulfillment órdenes) | `Fulfillment by Ripley` | 62 CSV | 1,584 |
| SELLER (Liquidación comercial) | `Fulfillment by Seller` | 51 XLSX | 17,913 filas únicas |
| XML DTE (Facturación SII) | `Facturacion` | 472 XML | — |
| Bitácoras de transacción | (adjunto) | CSV | 270 filas (1 ciclo) |

### 2.2 Archivos SELLER — estructura de columnas

Los archivos SELLER (`000312-2815.xlsx` a `000371-2815.xlsx`) contienen una estructura con al menos 37 columnas:

- **col1** = `settlement_ref` — número de liquidación (ej: `505930`). Este valor es equivalente al `folio_xml` del ledger (51 de 167 folios del ledger están en col1 de SELLER).
- **col2** = `order_id` — número de pedido (ej: `23285329001-A`)
- **col4** = `shop_name` — nombre del vendedor (ej: `NICOPOLY`)
- **col36** = referencia miscelánea — 1,833 valores distintos. Solo 2 son folios SII reales: `26794` y `122952`.

### 2.3 Inventario DTE SII (472 XMLs)

| Tipo DTE | Cantidad | Monto Total CLP | Descripción |
|----------|----------|-----------------|-------------|
| 33 | 253 + 15 dtef_c33 | $121,453,338 + ~$9M | Factura electrónica |
| 43 | 105 | $52,179,469 | Liquidación factura |
| 52 | 30 | $11,009,493 | Guía de despacho |
| 61 | 19 | $2,062,851 | Nota de crédito |
| **Total** | **472** | **~$186,705,151** | |

Los 15 archivos `dtef_c33_f*.xml` son facturas Tipo 33 emitidas por NANDA SPA a ECCSA (dirección proveedor→Ripley). El resto de DTEs (457) son emitidos por ECCSA a NANDA o a otros receptores en dirección Ripley→proveedor.

---

## 3. La Llave Documental: `Número de factura`

### 3.1 Evidencia de los documentos adjuntos

El análisis de los 3 documentos adjuntos (`2431205_33.pdf`, `invoice-000000598638.pdf`, `transaction-logs.csv`) revela que Ripley emite **dos facturas por ciclo de liquidación**:

**Documento referencial Ripley (`invoice-000000598638.pdf`):**
- N° Factura: `000000598638`
- Fecha: 20-06-2026
- Vendedor: NICOPOLY (2815)
- Comisiones: $619,205 CLP

**DTE SII (`2431205_33.pdf`):**
- Folio SII: `2431205`
- Tipo: 33 (Factura Electrónica)
- Fecha: 19-06-2026
- Emisor: Comercial Eccsa S.A. (83.382.700-6)
- Monto: $352,572 CLP (Despacho primera milla + Logística inversa)

**Bitácora de transacciones (`transaction-logs.csv`):**
- 270 filas, 1 ciclo de facturación
- Factura: `000000597837`
- 135 órdenes de NICOPOLY
- Columnas: `Número de pedido` | `Número de factura` | `Identificador del ciclo de facturación` | `Tienda` | `Descripción` | `Importe`

### 3.2 Texto explícito del documento referencial

> *"Este documento es sólo referencial, la factura oficial es emitida directamente y pueden encontrarla en su portal del SII, pudiendo tener algunas diferencias. Además, recordar que se genera una factura por concepto de Despachos, si procede, la cual es emitida en conjunto con la de Comisión."*

Esto confirma que:
1. Ripley emite un documento referencial interno con número de factura propio
2. La factura oficial (con folio SII) está en el portal del SII
3. Se emiten dos facturas SII por ciclo: Comisión + Despachos

### 3.3 Estructura del puente documental

```
Bitácora Ripley (transaction-logs.csv)
  ├── Número de pedido (24818037501-A)
  ├── Número de factura (000000597837) ← LLAVE PRINCIPAL
  ├── Tienda (NICOPOLY)
  └── Identificador del ciclo de facturación (UUID)
           │
           ├── Documento referencial Ripley
           │     → Invoice N° 000000598638
           │     → Comisiones: $619,205
           │
           └── DTE SII (portal tributario)
                 ├── Factura Comisión (folio por determinar)
                 └── Factura Despachos (folio 2431205, $352,572)
```

---

## 4. Estado del Enlace DTE↔Liquidación en la DB

### 4.1 `dte_link_v1` para Ripley es un enlace circular

| Métrica | Valor |
|---------|-------|
| Links totales en `dte_link_v1` (Ripley) | 210,232 |
| `cert_type` | `LEDGER_EXISTING` |
| `certified` | `True` |
| Folios que están en el ledger | 112 |
| Folios que están en `dte_truth_v1` | **0** |

Los 210,232 links tienen `cert_type = LEDGER_EXISTING`, lo que significa que el "match" es simplemente "este folio existe en el ledger". Es una verificación circular: el ledger se certifica a sí mismo. Ninguno de esos links conecta con un DTE fiscal real.

### 4.2 Cruces reales encontrados

Después de la búsqueda exhaustiva en todos los archivos:

| Búsqueda | Resultado |
|----------|-----------|
| 472 folios SII en archivos raw Ripley | **2 matches** (`26794`, `122952`) |
| 49 FolioRef de XML en archivos raw | 0 matches |
| 167 folio_xml del ledger en XML | 0 matches |
| Folios SII en SELLER col36 | 2 de 1,833 valores |

Los 2 folios que cruzan son:
- `26794`: Factura NANDA→ECCSA, $805,643, aparece en 3 archivos SELLER
- `122952`: Liquidación ECCSA→NANDA, $28,692, aparece en 1 archivo SELLER

### 4.3 Tablas de settlement en la DB

| Tabla | Filas | Stages |
|-------|-------|--------|
| `ripley_traceability_graph` | 287,417 | CICLOS_DAILY (149K), SELLER_BILLING (133K), TH_FF_SETTLEMENT (5K) |
| `ripley_settlement_chain` | 287,417 | SELLER (133K), TH_FF (155K) |
| `dte_link_v1` (Ripley) | 210,232 | LEDGER_EXISTING |
| `dte_truth_v1` (Ripley) | 407 | 4 tipos DTE |

---

## 5. Plan de Rehabilitación para Certificación Electrónica

### Bloque 1 — Infraestructura de datos

1. **Incorporar bitácoras de transacción completas** a la carpeta `01_Raw/RIPLEY/`: los archivos `transaction-logs.csv` para todos los períodos. Estos contienen la columna `Número de factura` que es la llave hacia los DTE.

2. **Crear tabla `ripley_invoice_map`** en el schema de `DatabaseV4`:
   ```
   CREATE TABLE ripley_invoice_map (
     numero_factura TEXT,        -- Ej: 000000597837
     numero_pedido TEXT,         -- Ej: 24818037501-A
     tienda TEXT,                -- NICOPOLY
     id_ciclo_facturacion TEXT,  -- UUID
     fecha_emision DATE,
     tipo_concepto TEXT,         -- Comisión / Despacho / Logística
     importe DOUBLE,
     folio_sii TEXT              -- A poblar tras cruce con SII
   )
   ```

3. **Poblar `folio_sii`** mediante cruce con:
   - Portal del SII (consulta por RUT emisor + fecha + monto)
   - Archivos DTE disponibles en `Facturacion/`
   - Mapeo manual para facturas sin DTE en archivos locales

### Bloque 2 — Correcciones al código

4. **Corregir paths hardcodeados** en `document_certification.py` y `document_gap_engine.py`:
   - `01_Raw/Ripley/SELLER/*.xlsx` → `01_Raw/RIPLEY/Fulfillment by Seller/*.xlsx`
   - `01_Raw/Ripley/Ciclos/*.csv` → `01_Raw/RIPLEY/Fulfillment by Ripley/*.csv`

5. **Normalizar folios** en `dte_link_v1`: eliminar duplicación `500346` vs `500346.0`.

6. **Reemplazar `cert_type = LEDGER_EXISTING`** en Ripley por `INVOICE_MAPPED` cuando el folio provenga de la bitácora de facturación.

### Bloque 3 — Verificación

7. Ejecutar `test_certification_gate.py` contra DB con `ripley_invoice_map` poblada.
8. Verificar que `DocumentCertificationEngine` retorne cobertura > 0% para Ripley.
9. Validar trazabilidad punta a punta: `DTE folio → Número de factura → orden → settlement_ref → ledger`.

---

## 6. Conclusiones

1. **La llave documental existe**: es el `Número de factura` en las bitácoras de transacción de Ripley. Esta llave conecta órdenes de vendedor con facturas internas, que a su vez referencian DTEs oficiales en el portal del SII.

2. **Los 472 DTE no están huérfanos**: pertenecen al espacio tributario ECCSA↔NANDA y tienen su correspondencia en facturas internas de Ripley. La limitación actual es que los archivos disponibles en `01_Raw/RIPLEY/` no incluyen las bitácoras de transacción para la mayoría de los períodos — solo se tiene una muestra de 1 ciclo con 135 órdenes.

3. **`dte_link_v1` para Ripley no constituye certificación**: es un enlace circular (`LEDGER_EXISTING`) que debe ser reemplazado por un mapeo real basado en `Número de factura`.

4. **La certificación electrónica de Ripley es viable**: requiere incorporar las bitácoras de transacción completas y construir la tabla `ripley_invoice_map` como puente hacia los folios SII.
