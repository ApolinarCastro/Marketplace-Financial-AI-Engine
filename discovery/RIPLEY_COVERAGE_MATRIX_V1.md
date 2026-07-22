# RIPLEY COVERAGE MATRIX V1

**Scope:** `scope = RIPLEY`
**Estado:** ANÁLISIS DE COBERTURA (AS-IS)

## 1. Cobertura Actual de Fuentes (RAW a DB)
| Métrica | Valor |
| :--- | :--- |
| **Fuentes Identificadas (RAW)** | 4 (Seller, Ciclos, Fulfillment, XML) |
| **Fuentes Integradas (Loader)** | 1 (Seller XLSX) |
| **Fuentes Ignoradas / No Integradas** | 3 (Ciclos CSV, Fulfillment CSV, XML DTE) |
| **Cobertura Documental Estimada (%)** | **25%** |

## 2. Matriz de Cobertura por Fuente

### 2.1 Fuente: Resumen Financiero Seller (XLSX)
* **¿Existe?** Sí (`01_Raw/RIPLEY/Resumen financiero/`)
* **¿Se carga?** Sí
* **¿Quién la carga?** `engine/v4/surgical_loader.py` (método `load_ripley`)
* **¿A qué tabla llega?** `marketplace_ledger_v1`
* **¿Qué campos aporta?** Importe del pedido, Gastos de envío, Comisiones, Abonos y Descuentos consolidados (ej. Descuento FF - sobreestadía), A Pagar.
* **¿Qué KPI impacta?** Ventas Brutas, Comisiones de Plataforma, Descuentos Logísticos, Pagos Netos (visibles en Dashboard vía `marketplace_cierre_financiero_v1`).
* **¿Se utiliza actualmente?** Sí, en el cierre P&L actual.
* **Estado:** **Completo**

### 2.2 Fuente: Ciclos de Facturación (CSV)
* **¿Existe?** Sí (`01_Raw/RIPLEY/Resumen financiero/Ciclos de facturación/`)
* **¿Se carga?** No
* **¿Quién la carga?** Nadie (Ignorado explícitamente en el loader actual que busca `**/*.xlsx`).
* **¿A qué tabla llega?** Ninguna
* **¿Qué campos aporta?** Order number, Date created, Subtotal, Gastos de envío (con/sin impuestos), Comisiones detalladas, Detalles de SKU y Producto, Direcciones de envío.
* **¿Qué KPI impacta?** Detalle transaccional de la Venta (Unit Economics), Matching contra órdenes tributarias.
* **¿Se utiliza actualmente?** No.
* **Estado:** **No Integrado**

### 2.3 Fuente: Fulfillment (CSV)
* **¿Existe?** Sí (`01_Raw/RIPLEY/Resumen financiero/Fulfillment/`)
* **¿Se carga?** No
* **¿Quién la carga?** Nadie.
* **¿A qué tabla llega?** Ninguna
* **¿Qué campos aporta?** order_id, sku_pmm, refund_commission_fee, múltiples descuentos FF a nivel de línea (Descuento operacional FF, Descuento FF - Otros, Descuento por logística inversa FF, etc).
* **¿Qué KPI impacta?** Costo Logístico Unitario, P&L Operacional. Su ausencia fuerza a depender del consolidado del archivo Seller.
* **¿Se utiliza actualmente?** No.
* **Estado:** **No Integrado**

### 2.4 Fuente: XML DTE (Tipo 33)
* **¿Existe?** Sí (`01_Raw/RIPLEY/Documentos Recepcionados/`)
* **¿Se carga?** No
* **¿Quién la carga?** Nadie (Los parsers de XML no contemplan el flujo de "facturas recibidas" de Ripley).
* **¿A qué tabla llega?** Ninguna
* **¿Qué campos aporta?** `<NroDTE>`, RUT Emisor (Ripley), RUT Receptor (Seller), montos totales cobrados con su validez ante el SII.
* **¿Qué KPI impacta?** Tasa de Conciliación Tributaria.
* **¿Se utiliza actualmente?** No.
* **Estado:** **No Integrado**

## 3. Elementos Faltantes e Ignorados (Gaps)

### 3.1 Archivos Ignorados
Todos los archivos con extensión `.csv` y `.xml` en la carpeta `01_Raw/RIPLEY/` y sus subcarpetas.

### 3.2 Campos Ignorados (en la tabla RAW)
La base de datos actual no captura `Order number`, `order_id` de forma granular para Ripley, lo cual imposibilita trazar un pedido individual o hacer matching cruzado con otras tablas.

### 3.3 Tablas Parcialmente Alimentadas
Las tablas `marketplace_ledger_v1` y `marketplace_ledger_clasificado_v1` carecen de la granularidad requerida y del 75% del universo de datos de Ripley, operando como un simple "vacío de consolidado".

### 3.4 Flujos Muertos / Integraciones Faltantes
* **Matching Logístico (Ciclos <-> Fulfillment):** Muerto/No existe.
* **Matching Tributario (XLSX/CSV <-> XML):** Muerto/No existe.
* **Endpoints consumidos por Dashboard:** Los endpoints (como `/api/v4/cierre/desglose`) devuelven información para Ripley, pero esta información **no representa el flujo financiero completo E2E**, sino solo un subset (el archivo Seller).

## 4. Backlog Priorizado de Integración (Next Steps dentro de Arquitectura V4)

Para completar RIPLEY sin crear nueva arquitectura, el orden de integración debe ser:

1. **Loader de "Ciclos de facturación (CSV)":** Para dotar al motor del nivel transaccional y las llaves de matching maestras (`Order number`, `Nmero de factura`).
2. **Loader de "Fulfillment (CSV)":** Para cruzar `order_id` con el ciclo y mapear detalladamente la complejidad logística.
3. **Loader de "XML DTE":** Adaptar el lector XML para parsear las facturas de cobro emitidas por Ripley.
4. **Implementar Flujo de Matching:** Enlazar el flujo transaccional CSV con el facturado XML.

## 5. Impacto Esperado
* **Ciclos de Facturación:** Permitirá pasar de una "suma agregada" a un análisis "por pedido", destrabando el matching.
* **Fulfillment:** Dará visibilidad granular a las "fugas" de costos logísticos y discrepancias en sobreestadía (actualmente ciego en el modelo).
* **XML DTE:** Habilitará la Defensa Tributaria, verificando si lo que Ripley descontó por comisiones concuerda al centavo con lo declarado al SII.
