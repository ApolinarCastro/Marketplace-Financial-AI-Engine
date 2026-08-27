# Clasificación Exhaustiva de Cargos de Marketplaces (360°)

Este documento consolida la lógica de filtrado y clasificación de todos los cargos e ingresos de Mercado Libre, Ripley y París, tal como se implementa en la Guía Definitiva PRO (Versión 7.0).

El objetivo es estandarizar todas las transacciones bajo las columnas: `ID_Transaccion`, `Fecha`, `SKU`, `Monto`, `Tipo_Transaccion` y `Marketplace`.

---

## 1. Mercado Libre (ML)

**Fuente RAW:** `ML_Facturacion_RAW` (para la mayoría de cargos) y `ML_Poscobro_RAW` (para devoluciones).

| Tipo de Transacción | Fuente RAW | Columna de Filtrado | Criterio de Filtrado (Lógica de Power Query) | Signo Final (Monto) |
| :--- | :--- | :--- | :--- | :--- |
| **Venta** | `ML_Facturacion_RAW` | `Detalle` | Es igual a `"Cargo por venta"` | Positivo (+) |
| **Comisión** | `ML_Facturacion_RAW` | `Detalle` | Es igual a `"Cargo por venta"` | Negativo (-) |
| **Costo Envío** | `ML_Facturacion_RAW` | `Detalle` | Contiene `"Mercado Envíos"` o `"envíos de Mercado Libre"` | Negativo (-) |
| **Publicidad** | `ML_Facturacion_RAW` | `Detalle` | Contiene `"publicidad"`, `"Ads"` o es igual a `"Cargo por publicación"` | Negativo (-) |
| **Asesoría Comercial** | `ML_Facturacion_RAW` | `Detalle` | Es igual a `"Cargo por Asesoría Comercial"` | Negativo (-) |
| **Costo Fullfilment** | `ML_Facturacion_RAW` | `Detalle` | Contiene `"Full"` | Negativo (-) |
| **Bonificación** | `ML_Facturacion_RAW` | `Detalle` | Contiene `"Bonificación"` o `"Anulación"` | Positivo (+) |
| **Devolución** | `ML_Poscobro_RAW` | N/A | Usar columna `"MONTO_DEVOLUCION"` | Negativo (-) |

---

## 2. Ripley

**Fuente RAW:** `Ripley_Finanzas_RAW` (El archivo de Historial Financiero consolida todos los movimientos).

| Tipo de Transacción | Fuente RAW | Columna de Filtrado | Criterio de Filtrado (Lógica de Power Query) | Signo Final (Monto) |
| :--- | :--- | :--- | :--- | :--- |
| **Venta** | `Ripley_Finanzas_RAW` | `Tipo` | Es igual a `"Importe del pedido"` | Positivo (+) |
| **Comisión** | `Ripley_Finanzas_RAW` | `Tipo` | Es igual a `"Comisiones"` | Negativo (-) |
| **Costo Envío** | `Ripley_Finanzas_RAW` | `Tipo` | Contiene `"Gastos de envío (RIPLEY)"` | Negativo (-) |
| **Impuesto** | `Ripley_Finanzas_RAW` | `Tipo` | Es igual a `"Impuesto sobre la comisión (IVA 0,00%)"` | Negativo (-) |
| **Reembolso** | `Ripley_Finanzas_RAW` | `Tipo` | Es igual a `"Importe de reembolso"` | Negativo (-) |

---

## 3. París

**Fuente RAW:** `Paris_Finanzas_RAW` (El archivo de Transacciones consolida todos los movimientos).

| Tipo de Transacción | Fuente RAW | Columna de Filtrado | Criterio de Filtrado (Lógica de Power Query) | Signo Final (Monto) |
| :--- | :--- | :--- | :--- | :--- |
| **Venta** | `Paris_Finanzas_RAW` | `TIPO` | Es igual a `"Venta"` | Positivo (+) |
| **Comisión** | `Paris_Finanzas_RAW` | `TIPO` | Es igual a `"Venta"` (Se calcula: `[MONTO] * [COMISIÓN] / 100`) | Negativo (-) |
| **Descuento Comercial** | `Paris_Finanzas_RAW` | `TIPO` | Es igual a `"Venta"` (Usar columna `DESCUENTO COMERCIAL` si es > 0) | Negativo (-) |
| **Logística** | `Paris_Finanzas_RAW` | `TIPO` | Es igual a `"Despacho"`, `"Cobro por despacho"`, `"Logística inversa"` o `"Compensación logística"` | Condicional (Negativo, excepto `"Compensación logística"`) |
| **Otros Cargos** | `Paris_Finanzas_RAW` | `TIPO` | Es igual a `"Cargo"`, `"Cobro por campaña"` o `"Rebate"` | Condicional (Negativo, excepto `"Rebate"`) |

---

**Nota sobre Signos:**

*   **Positivo (+):** Representa un **Ingreso** (Venta, Bonificación, Compensación).
*   **Negativo (-):** Representa un **Costo** (Comisión, Envío, Impuesto, Reembolso, Descuento).

La suma de la columna `Monto` de la tabla maestra consolidada (`DATA_MAESTRA_360`) representa la **Venta Neta Real** después de aplicar todos estos cargos.
