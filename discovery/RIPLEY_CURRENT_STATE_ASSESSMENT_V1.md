# RIPLEY CURRENT STATE ASSESSMENT V1

## 1. Executive Summary
Esta evaluación presenta el estado actual del ecosistema de datos crudos (RAW) disponibles para RIPLEY. Basado en la evidencia encontrada en `01_Raw/RIPLEY/`, Ripley cuenta con un volumen considerable de información histórica estructurada en reportes CSV, XLSX y documentos tributarios XML. 

Existen 3 grandes vertientes de datos financieros ("Ciclos de facturación", "Seller" y "Fulfillment"), lo que indica una operación madura pero con una alta complejidad en la estructura de cobros y descuentos operacionales. Actualmente, no hay evidencia de integración vía API.

## 2. Mapa de Fuentes
| Fuente | Tipo | Estado | Ubicación |
| :--- | :--- | :--- | :--- |
| **Portal / Seller Center** | Reportes (CSV, XLSX) | **Disponible** | `01_Raw/RIPLEY/Resumen financiero/` |
| **SII / Facturación** | XML (DTE Tipo 33) | **Disponible** | `01_Raw/RIPLEY/Documentos Recepcionados/` |
| **API** | Endpoints JSON | **Faltante** | No hay evidencia en carpeta RAW. |

## 3. Mapa de Archivos (Inventario)

**Total de archivos analizados:** 564 archivos.

| Directorio | Tipo | Cant. | Patrón de Nombre | Ejemplo de Campos Clave |
| :--- | :--- | :--- | :--- | :--- |
| `Documentos Recepcionados` | XML | 407 | `dteproveedor_*.xml` | `RutEmisor`, `RutReceptor`, `TpoDTE` (33), `NroDTE` |
| `Ciclos de facturación` | CSV | 48 | `dd-mm-yyyy - dd-mm-yyyy.csv` | `Número de factura`, `Order number`, `Precio total`, `Commission`, `Amount transferred to tienda` |
| `Fulfillment` | CSV | 62 | `*_ff_*.csv`, `abonos_descuentos_*` | `order_id`, `commission_fee`, `transfer_amount`, `Descuento FF - pick and pack` |
| `Seller` | XLSX | 47 | `*-2815.xlsx` | `Orden de compra`, `Número documento liquidación`, `Comisiones sobre pedidos`, `A pagar` |

## 4. Mapa de Relaciones (Aparentes)
A la espera de validación estricta, las siguientes entidades muestran potencial cruce transaccional (Matching):
* **Cruce Transaccional:** El campo `Order number` (Ciclos) cruza aparentemente con `order_id` (Fulfillment) y `Orden de compra` (Seller).
* **Cruce Tributario:** El campo `Número de factura` (Ciclos) debería cruzar lógicamente con el `NroDTE` de los XMLs (Documentos Recepcionados).
* **Cruce de Liquidación:** El `Número documento liquidación` (Seller) podría ser la llave primaria de la remesa.

## 5. Mapa de Cobertura
* **Cobertura Documental:** **ALTA**. 407 XMLs proveen la base tributaria oficial (Facturas electrónicas emitidas/recibidas).
* **Cobertura Financiera:** **ALTA**. Cobertura extensa a nivel de ciclos y liquidaciones (`A pagar`, `Amount transferred to tienda`).
* **Cobertura Operacional / Logística:** **MEDIA-ALTA**. Existe detalle granular en el Fulfillment (costos de sobreestadía, pick and pack, logística inversa).
* **Cobertura Tributaria:** **MEDIA**. Los XMLs están, pero falta mapear cómo los impuestos se desglosan en los CSVs (`Impuestos sobre la comisión`, etc.).

## 6. Gaps Detectados y Riesgos de Información
1. **Falta de APIs:** Todo el proceso actual parece depender de exportaciones manuales o reportes estáticos.
2. **Encoding Issues:** Se observaron problemas de codificación de caracteres en los encabezados (ej. `Nmero de factura`, `artculos`), lo cual es un riesgo para el Parser.
3. **Complejidad de Descuentos (FF):** El modelo de Fulfillment de Ripley contiene decenas de columnas de descuentos muy específicos (`Descuento FF - Otros`, `Descuento oferta TC - OPEX`, `Descuento por PDM`). Esto requerirá una taxonomía compleja.
4. **Significado Económico No Validado:** No se puede asumir si `A pagar` es neto o bruto de impuestos sin una liquidación real explicada.

## 7. Recomendación de Prioridades
Para continuar con la integración controlada (Scope = RIPLEY) y mantener la regla **Evidence First**:

1. **Prioridad 1 (Parser & Normalización):** Construir el `parser` de RIPLEY enfocado primero en solucionar los problemas de encoding de los CSVs y extraer de forma segura los XMLs.
2. **Prioridad 2 (Diccionario de Datos):** Solicitar al negocio la confirmación explícita del significado de las columnas de descuentos de Fulfillment y Seller.
3. **Prioridad 3 (Taxonomía):** Solo después de resolver la Prioridad 2, iniciar la construcción del módulo `taxonomy` de Ripley aislando completamente su lógica de ML/PARIS.
4. **Prioridad 4 (Matching Preliminar):** Intentar el cruce `Order number` vs `XML NroDTE` para validar si existe un Delta Financiero inicial.
