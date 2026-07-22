# ML RAW COVERAGE AUDIT

**Auditor:** Sistema de Agentes
**Fecha:** 2026-06-06
**Alcance:** `01_Raw/ML/` — 100% de archivos, subdirectorios y formatos
**Propósito:** Determinar si toda la información financiera disponible en Raw ML llega al P&L de Mercado Libre.

---

## Executive Summary

**ML_RAW_COVERAGE = FAIL** ❌

**Razón:** `01_Raw/ML/Liquidacion_FF/` (90 archivos, 15,521 filas) NO es procesado por el pipeline V4 activo. Es el único subdirectorio de `01_Raw/ML/` que queda fuera del flujo `Raw → Ledger → Clasificación → Cierre → Dashboard`.

**Impacto financiero estimado: BAJO — las transacciones de Liquidacion_FF están probablemente cubiertas por Facturación, pero NO está certificado.**

---

## FASE 1: Inventario Completo

| Subdirectorio | Archivos | Filas | Período | Formato | Clasificación |
|--------------|----------|-------|---------|---------|---------------|
| Facturación | 18 | 63,166 | Ene 2025 – Jun 2026 | XLSX | Facturación |
| Liquidacion_FF | 90 | 15,521 | Ene 2025 – Jun 2026 | XLSX | Liquidaciones |
| Liberaciones | 18 | ~31,506 | Ene 2025 – Jun 2026 | XLSX | Liberaciones |
| Poscobro | 5 | 15,642* | Ene 2025 – Jun 2026 | XLSX | Poscobro |
| Documentos Recepcionados | 192 | N/A | — | XML | Full (DTEs) |
| **TOTAL** | **323** | **~110,000+** | **18 meses** | **2 formatos** | **5 categorías** |

*\* 11,914 rows según POSCOBRO_DELETION_DECISION + estimación de filas adicionales no contables*

---

## FASE 2: Trazabilidad al Pipeline

### 2a. Facturación — SI ✅

| Pipeline | Archivo | Función | Línea |
|----------|---------|---------|-------|
| Loader V4 | `engine/v4/surgical_loader.py` | `SurgicalLoader.load_facturacion()` | 104-218 |
| Orquestador | `engine/v4/surgical_loader.py` | `SurgicalLoader.load_marketplace('ML')` | 486-491 |
| DTE Indexer | `engine/v4/dte_indexer.py` | `DTEIndexer.__init__()` | 13 |

**Aporte:** Todas las ventas (INGRESO_VENTA), comisiones (EGRESO_COMISION), devoluciones (DEVOLUCION), cargos (CARGO), ajustes (AJUSTE).

### 2b. Poscobro — SI ✅

| Pipeline | Archivo | Función | Línea |
|----------|---------|---------|-------|
| Loader V4 | `engine/v4/surgical_loader.py` | `SurgicalLoader.load_poscobro()` | 220-282 |
| Orquestador | `engine/v4/surgical_loader.py` | `SurgicalLoader.load_marketplace('ML')` | 486-491 |
| Auditor | `engine/v4/marketplace_auditor.py` | RAW_TO_CLASSIFICATION_MAP | 39-108, 252-310 |

**Aporte:** Todos los ajustes (claim, refund, chargeback) al Ledger.

### 2c. Liberaciones — SI ✅ (Cash pipeline)

| Pipeline | Archivo | Función | Línea |
|----------|---------|---------|-------|
| Auditor | `engine/v4/run_initial_audit.py` | `load_marketplace_ledger_standalone()` | 39-96 |

**Aporte:** Cash truth. NO alimenta P&L directamente. Correlacionado con ledger vía SALE_TO_BANK_TRUTH.

### 2d. Documentos Recepcionados — SI ✅

| Pipeline | Archivo | Función | Línea |
|----------|---------|---------|-------|
| XML Justifier | `engine/v4/surgical_xml_justifier.py` | `XMLJustifier.run()` | 28-85 |
| XML Matcher | `engine/v4/xml_matcher.py` | `MeliXMLMatcher.run_matching()` | 73-99 |

**Aporte:** Certificación XML. No altera montos financieros. Puebla `folio_xml` y `estado_xml`.

### 2e. Liquidacion_FF — NO ❌

| Pipeline | Archivo | Función | Línea |
|----------|---------|---------|-------|
| V4 Activo | — | — | — |
| Legacy SOLO | `engine/meli_master_builder.py` | `load_all_ff()` | 78-91 |

**Status:** CERO procesamiento en el pipeline V4 activo. Solo existe en `meli_master_builder.py` (legacy) que referencia una ruta base diferente (`Marketplace_Conciliacion`).

---

## FASE 3: Cobertura Financiera

| Fuente | Ledger | Clasificación | Cierre | Dashboard | Cash |
|--------|--------|---------------|--------|-----------|------|
| Facturación | ✅ 90,814 rows, $535.2M | ✅ | ✅ | ✅ | ❌ (accrual) |
| Poscobro | ✅ 11,384 rows, $327.2M | ✅ | ✅ | ✅ | ❌ (96% noise) |
| Liberaciones | ✅ (audit only) | ❌ | ❌ | ❌ | ✅ Cash Truth |
| Documentos Recepcionados | ❌ (certificación) | ❌ | ❌ | ❌ | ❌ |
| **Liquidacion_FF** | **❌** | **❌** | **❌** | **❌** | **❌** |

---

## FASE 4: Análisis de Omisiones

### Única omisión identificada: Liquidacion_FF

| Métrica | Valor |
|---------|-------|
| Archivos | 90 |
| Filas estimadas | 15,521 |
| Período | Ene 2025 – Jun 2026 |
| Formato | XLSX (weekly) |
| Contenido | Liquidaciones semanales de Fulfillment (FF) |
| Columnas | fecha, tipo_documento, dte, folio, venta (order_id), monto, iva, sku, etc. |

### ¿Es Liquidacion_FF información financiera única?

**Esquema de Liquidacion_FF:**
- `fecha`, `tipo documento`, `dte`, `folio`, `venta` (order_id)
- `descripcion`, `cantidad`, `monto`, `iva`
- `sku`, `código del producto`, `variación`

**Esquema de Facturación:**
- `N° de factura fiscal`, `Fecha del cargo`, `Detalle`
- `Valor del cargo`, `Subtotal sin descuento`
- `Número de venta` (order_id)

**Conclusión:** Liquidacion_FF tiene granularidad semanal (vs mensual Facturación) y datos a nivel ítem (sku, cantidad) que Facturación no tiene. Sin embargo, las transacciones subyacentes ya están en Facturación. Es **redundante en monto pero no en granularidad.**

---

## FASE 5: Reconstrucción del P&L

### ML 2026-01

| Línea P&L | Fuente | Archivo | Monto |
|-----------|--------|---------|-------|
| Ingresos Brutos | Facturación (Venta) | Reporte_Facturacion_...Ene2026.xlsx | $27,646,200 |
| Devoluciones | Facturación (Devolución) | Reporte_Facturacion_...Ene2026.xlsx | -$4,971,696 |
| Costos Comerciales (Comisiones) | Facturación (Comisión) | Reporte_Facturacion_...Ene2026.xlsx | -$7,954,836 |
| Costos Operacionales (Cargos) | Facturación (Cargo) | Reporte_Facturacion_...Ene2026.xlsx | -$2,075,055 |
| Ajustes | Poscobro | Poscobro Ene2026 | $11,457,255 |
| **Ledger Net** | | | **$24,101,868** |
| **Cierre RN** | | | **$19,401,503** |

### ML 2026-05

| Línea P&L | Fuente | Archivo | Monto |
|-----------|--------|---------|-------|
| Ingresos Brutos | Facturación (Venta) | Reporte_Facturacion_...May2026.xlsx | $25,868,400 |
| Devoluciones | Facturación (Devolución) | Reporte_Facturacion_...May2026.xlsx | -$1,938,490 |
| Costos Comerciales (Comisiones) | Facturación (Comisión) | Reporte_Facturacion_...May2026.xlsx | -$5,246,931 |
| Costos Operacionales (Cargos) | Facturación (Cargo) | Reporte_Facturacion_...May2026.xlsx | -$2,400,343 |
| Ajustes | Poscobro | Poscobro May2026 | $14,646,258 |
| **Ledger Net** | | | **$30,928,894** |
| **Cierre RN** | | | **$24,799,677** |

**Todas las líneas del P&L de ML están 100% trazadas a:**
1. Facturación → ingresos, devoluciones, costos_comerciales, costos_operacionales
2. Poscobro → ajustes

**Ninguna línea del P&L proviene de Liquidacion_FF.**

---

## PREGUNTA ÚNICA

### ¿Existe información financiera en 01_Raw/ML que NO está llegando al P&L de ML?

**Respuesta: SÍ, condicional.**

| Archivo | Filas | ¿En P&L? | Impacto |
|---------|-------|----------|---------|
| Liquidacion_FF (90 archivos) | 15,521 | ❌ | **Potencialmente $0 (redundante con Facturación). NO certificado.** |

### Análisis de impacto

**Escenario Pesimista:** Liquidacion_FF contiene transacciones NO capturadas por Facturación.
- Impacto potencial: MONTO NO CUANTIFICADO (depende de diferencias transaccionales semanales vs mensuales)
- Probabilidad: BAJA (Facturación es el reporte oficial mensual de ML)

**Escenario Optimista:** Liquidacion_FF es 100% redundante con Facturación.
- Impacto real: $0
- Probabilidad: ALTA

---

## Veredicto Final

### ML_RAW_COVERAGE = FAIL ❌

**Fundamento:**

El criterio de éxito exige:
> *"PASS si puede demostrarse: Raw ML → Ledger → Clasificación → Cierre → Dashboard sin huecos."*
> *"FAIL si existe cualquier archivo financiero que quede fuera del flujo."*

Liquidacion_FF (90 archivos, 15,521 filas) es un archivo financiero que **queda completamente fuera del flujo V4 activo**. Por definición del criterio, esto constituye FAIL.

**Hallazgos adicionales:**

| Hallazgo | Severidad | Estado |
|----------|-----------|--------|
| Liquidacion_FF no procesado por V4 | ALTA | ❌ NO RESUELTO |
| Facturación cubre todos los conceptos P&L | — | ✅ OK |
| Poscobro cubre todos los ajustes | — | ✅ OK |
| Liberaciones como Cash Truth | — | ✅ OK |
| Documentos Recepcionados para cert XML | — | ✅ OK |
| 323/323 archivos existen en disco | — | ✅ OK |
| 5/5 subdirectorios contienen datos | — | ✅ OK |

**Recomendación:**

1. **Certificar redundancia**: Verificar que Liquidacion_FF no contiene transacciones únicas. Si se confirma redundancia → no requiere acción (FAIL administrativo, no financiero).
2. **O incorporar al pipeline**: Si se requiere trazabilidad granular (sku, weekly), implementar loader V4 para Liquidacion_FF.
3. **Documentar decisión**: Formalizar si Liquidacion_FF es fuente activa o archivo histórico.

---

*"5/5 directorios existen. 4/5 se procesan. 1/5 no. El FAIL es por el hueco documentado, no por pérdida financiera comprobada. La redundancia de Liquidacion_FF con Facturación debe certificarse para cerrar el hallazgo."*
