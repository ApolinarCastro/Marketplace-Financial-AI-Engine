# RIPLEY INTEGRATION BACKLOG V1

**Scope:** `scope = RIPLEY`
**Estado:** PRIORIZACIÓN DE COBERTURA

## 1. Resumen Ejecutivo
Basado en las brechas documentadas, este backlog detalla la estrategia de integración para las tres fuentes de RIPLEY actualmente ignoradas: **Ciclos CSV, Fulfillment CSV y XML DTE**. La integración de estos archivos desbloqueará la capacidad de realizar conciliación unitaria, control logístico granular y validación tributaria, pasando de un modelo "consolidado ciego" a uno de control transaccional E2E.

---

## 2. Fuente: Ciclos (Resumen Financiero / Ciclos de facturación)
* **Cantidad de archivos:** 48 CSVs.
* **Cantidad de columnas:** ~25 columnas.
* **Columnas nuevas (vs Seller):** `Nmero de factura`, `Estado del pedido`, `Subtotal de artculos (con/sin impuestos)`, `Impuestos sobre la comisin`, `Quantity`, `Producto`, `Product SKU`, `Offer SKU`, Detalles de dirección/Shipping.
* **Columnas ya existentes en Seller:** Análogos a Importe del pedido (`Precio total`), Gastos de envío (`Gastos de envo`), Comisiones (`Commission`), A pagar (`Amount transferred to tienda`).
* **Llaves de matching:** `Order number`, `Nmero de factura`.
* **Métricas financieras aportadas:** Desglose unitario (SKU, línea) del precio, impuestos detallados y comisión neta.
* **Métricas documentales aportadas:** Número de factura oficial para cruzar contra XML DTE.
* **Impacto `ledger_v1`:** Multiplicará masivamente el volumen de filas (granularidad por SKU/Pedido).
* **Impacto `clasificado_v1`:** Requerirá homologación del diccionario para los nombres de columnas de comisiones/impuestos en inglés/español.
* **Impacto `cierre_v1`:** Proveerá validación cruzada del importe agregado de venta y comisiones de la fuente Seller.

---

## 3. Fuente: Fulfillment (Resumen Financiero / Fulfillment)
* **Cantidad de archivos:** 62 CSVs (Standard y Abonos_Descuentos).
* **Cantidad de columnas:** ~17 core + >15 de descuentos = ~32 columnas.
* **Columnas nuevas (vs Seller):** `order_id`, `order_line_id`, `sku_pmm`, `shipping_type_code`, `date_created`. Múltiples descuentos específicos (Ej: `Descuento operacion VAS (FF)`, `Descuento por almacenamiento diario/prolongando (FF)`, `Descuento por Recogida (FF)`).
* **Columnas ya existentes en Seller:** Descuentos homologables (ej. `Descuento FF - sobreestadía`, `Descuento FF - pick and pack`), y montos bases como `commission_fee`, `transfer_amount`.
* **Llaves de matching:** `order_id` (Cruza con `Order number` en Ciclos y `Orden de compra` en Seller).
* **Métricas financieras aportadas:** Cargos y devoluciones logísticas unitarias al milímetro.
* **Métricas documentales aportadas:** Relación transaccional entre el pedido y el cargo operativo.
* **Impacto `ledger_v1`:** Creación de registros financieros de naturaleza puramente operativa/logística.
* **Impacto `clasificado_v1`:** Generación de la taxonomía más compleja de RIPLEY (más de 20 conceptos logísticos).
* **Impacto `cierre_v1`:** Justificará el margen neto operacional que se pierde en descuentos y logística.

---

## 4. Fuente: XML DTE (Documentos Recepcionados)
* **Cantidad de archivos:** 407 archivos XML (Tipo 33).
* **Cantidad de columnas (Etiquetas clave):** ~10 (`RutEmisor`, `RutReceptor`, `NroDTE`, `TpoDTE`, `FchEmis`, `MntNeto`, `IVA`, `MntTotal`).
* **Columnas nuevas:** Data oficial de validez ante el SII.
* **Columnas ya existentes:** Análogos a comisiones con IVA / montos de liquidación.
* **Llaves de matching:** `<NroDTE>` (Cruza con `Nmero de factura` en Ciclos).
* **Métricas financieras aportadas:** Montos netos, IVA y total de facturación de servicios Ripley.
* **Métricas documentales aportadas:** RUT, Folio del DTE, Fechas oficiales.
* **Impacto `ledger_v1`:** Nulo o paralelo (Usualmente alimenta tablas de impuestos como `marketplace_tax_v1` o similar, no el ledger transaccional per se, o se inyecta como "Factura de cobro").
* **Impacto `clasificado_v1`:** Validación de los impuestos retenidos vs facturados.
* **Impacto `cierre_v1`:** Generación de alarmas de discrepancia tributaria (Facturado vs Cobrado).

---

## 5. Matriz de Nuevos Campos (Top 5 Críticos por Fuente)
| Fuente | Campo Crítico | Razón |
| :--- | :--- | :--- |
| Ciclos | `Nmero de factura` | **Llave maestra** para el cruce tributario. |
| Ciclos | `Order number` | **Llave maestra** para el cruce transaccional. |
| Ciclos | `Product SKU` / `Quantity` | Permite Unit Economics reales y rentabilidad por producto. |
| FF | `order_id` / `order_line_id` | Enlace para imputar el costo logístico a una venta específica. |
| FF | `Descuentos varios (FF)` | Desagrega la caja negra de costos operacionales. |
| XML | `<NroDTE>` | Llave oficial frente al SII. |
| XML | `<MntTotal>` | Total facturado por comisiones/servicios. |

---

## 6. Matriz de Matching (El "Golden Path" de RIPLEY)
Para lograr un control punta a punta, el motor deberá ejecutar el siguiente flujo de enlace:
1. **Transaccional:** `Fulfillment CSV [order_id]` <==> `Ciclos CSV [Order number]` <==> `Seller XLSX [Orden de compra]`.
2. **Tributario:** `Ciclos CSV [Nmero de factura]` <==> `XML DTE [<NroDTE>]`.
3. **Liquidador:** `Seller XLSX [Número documento liquidación]` agrupa todas las órdenes del período.

---

## 7. Matriz de Impacto en Arquitectura V4
| Componente | Nivel de Modificación Requerida |
| :--- | :--- |
| `surgical_loader.py` | **ALTO.** Crear `load_ripley_ciclos`, `load_ripley_ff`. Parsear *encoding issues*. |
| `xml_matcher.py` | **MEDIO.** Incluir lógica de cruce de `NroDTE` vs `Nmero de factura`. |
| `marketplace_auditor.py` | **ALTO.** Añadir +30 reglas de taxonomía nuevas (especialmente para logística de FF). |
| Tablas DuckDB | **BAJO.** La estructura actual de las tablas V4 soporta inyección de atributos como JSON o en campos nativos (`id_transaccion`, `numero_documento`). |

---

## 8. Backlog Priorizado

### **P1 = Imprescindible (Fundamento de Trazabilidad)**
* **Tarea P1.1:** Ingesta y normalización (Loader) de **Ciclos CSV**.
  * *Retorno:* Obtener `Order number` y `Nmero de factura`, granularidad base.
* **Tarea P1.2:** Ingesta y normalización (Loader) de **Fulfillment CSV**.
  * *Retorno:* Obtener `order_id` y desglosar todos los cargos operativos y logísticos.

### **P2 = Alto Valor (Cruce y Certificación)**
* **Tarea P2.1:** Homologación y actualización del diccionario en `marketplace_auditor.py` para abarcar todas las nuevas columnas de Ciclos y Fulfillment (Evitar fugas de `financial_group = NULL`).
* **Tarea P2.2:** Creación de lógica de validación interna: `A pagar` (Seller) == SUMA(Ciclos + FF).

### **P3 = Complementario (Seguridad Tributaria)**
* **Tarea P3.1:** Ingesta de **XML DTE**.
* **Tarea P3.2:** Habilitación de Matching Tributario (`Nmero de factura` vs `NroDTE`).
  * *Retorno:* Asegurar que los cobros de comisiones declarados en CSV sean idénticos a las facturas electrónicas.
