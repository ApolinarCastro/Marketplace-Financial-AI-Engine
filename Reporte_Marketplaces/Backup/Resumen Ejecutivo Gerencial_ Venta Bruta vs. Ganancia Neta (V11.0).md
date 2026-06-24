
# Resumen Ejecutivo Gerencial: Venta Bruta vs. Ganancia Neta (V11.0)

Este resumen está diseñado para responder directamente a las preguntas gerenciales: **"¿Cuánto vendemos?"** y **"¿Cuánto nos queda?"**.

## 1. La Métrica Clave: Venta Neta (Ganancia Real)

La métrica más importante es la **Venta Neta**, que representa la ganancia real después de restar **TODOS** los costos (comisiones, envíos, publicidad, fullfilment, etc.) de la Venta Bruta.

| Métrica | Fórmula DAX | Interpretación Gerencial |
| :--- | :--- | :--- |
| **Venta Bruta (GMV)** | `Venta Bruta = CALCULATE(SUM('DATA_MAESTRA_360'[Monto]), 'DATA_MAESTRA_360'[ID_Tipo_Transaccion] = 1 || 'DATA_MAESTRA_360'[ID_Tipo_Transaccion] = 14)` | **"Cuánto vendemos en total"** (antes de costos). |
| **Ganancia Neta** | `Ganancia Neta = SUM('DATA_MAESTRA_360'[Monto])` | **"Cuánto dinero real va a la caja"** (después de todos los costos). |
| **Margen Neto (%)** | `Margen Neto % = DIVIDE([Ganancia Neta], [Venta Bruta])` | **"Por cada $100 que vendemos, cuánto nos queda"**. |

## 2. Presentación Gerencial (UX/UI Sugerida)

Para que la información sea "entendible por todos los usuarios", se recomienda un dashboard con la siguiente estructura:

### A. Vista de Alto Nivel (KPIs)

*   **KPI 1:** **Ganancia Neta** (Valor total en grande).
*   **KPI 2:** **Margen Neto %** (Valor total en grande).
*   **KPI 3:** **Venta Bruta** (Valor total en grande).

### B. Desglose por Marketplace

*   **Gráfico de Barras:** Muestra la **Ganancia Neta** por cada Marketplace (Mercado Libre, Ripley, París, Shopify).
*   **Segmentador de Datos:** Un botón grande para filtrar por **Marketplace** y otro para **Fecha**.

### C. Estado de Cuenta Detallado (Matriz)

*   **Tabla Matriz:** Replicando la imagen que enviaste, pero con una mejora:
    *   **Filas:** `Marketplace` (Nivel 1) > `Tipo_Transaccion` (Nivel 2).
    *   **Valores:** `[Ganancia Neta]` (Muestra el valor final de cada arista).

**Ejemplo de Interpretación:**

Si el gerente selecciona **Mercado Libre** y ve:
*   **Venta:** $100.000
*   **Comisión:** -$15.000
*   **Envío:** -$5.000
*   **Ganancia Neta:** $80.000

El mensaje es claro: **"Vendimos $100.000, pero después de costos, nos quedan $80.000."**

## 3. Lógica de Integración (Para el Equipo Técnico)

*   **Shopify:** Se incorpora como un nuevo Marketplace (ID 4). Las ventas se clasifican como **Venta Directa (ID 14)** para diferenciarla de las ventas de Marketplace (ID 1).
*   **París Fulfillment:** Se integra en las consultas de París (ID 3), asegurando que las ventas y comisiones de Fulfillment se sumen a las ventas y comisiones totales de París.
