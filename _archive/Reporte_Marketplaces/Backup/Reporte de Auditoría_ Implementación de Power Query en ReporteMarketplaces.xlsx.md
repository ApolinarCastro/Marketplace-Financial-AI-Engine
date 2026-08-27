# Reporte de Auditoría: Implementación de Power Query en ReporteMarketplaces.xlsx

**Objetivo:** Analizar la estructura y lógica de las consultas implementadas en el archivo `ReporteMarketplaces.xlsx` para identificar discrepancias con la Guía Definitiva PRO (V7.0) y proponer mejoras significativas sin alterar la lógica central.

## 1. Hallazgos de la Auditoría (Discrepancias)

La implementación del usuario utiliza una estructura de datos más avanzada (Star Schema) que la estructura plana de 6 columnas sugerida en la Guía V7.0. Sin embargo, existen inconsistencias en la estandarización de columnas y en la lógica de Ripley.

| ID | Consulta | Discrepancia Encontrada | Propuesta de Corrección (Lógica) |
| :--- | :--- | :--- | :--- |
| **D1** | Todas las Consultas | Uso de `ID_Marketplace` y `ID_Tipo_Transaccion` (IDs numéricos) en lugar de `Marketplace` y `Tipo_Transaccion` (texto descriptivo). | **Mantener la estructura de IDs** (es una buena práctica de modelado de datos - Star Schema). La Guía Maestra Final debe reflejar esta estructura y añadir una tabla de dimensiones. |
| **D2** | ML_Fact_Publicidad, ML_Fact_Asesoria | Falta la columna `SKU` en la salida. | **Corregir el Código M** para incluir la columna `SKU` con un valor nulo (`null`) o un valor por defecto (`"N/A"`) cuando no aplique, para mantener la uniformidad de la tabla de hechos. |
| **D3** | ML_Fact_Bonificaciones | El orden de las columnas es inconsistente (`SKU` al final). | **Corregir el Código M** para estandarizar el orden de las columnas en todas las consultas. |
| **D4** | Ripley Queries | El usuario sigue utilizando `Ripley_Fact_Ajustes` y `Ripley_Pedidos_RAW` (Worksheets 16 y 19), a pesar de que la Guía V7.0 determinó que solo el Historial Financiero (`Ripley_Ajustes_RAW` / `Ripley_Finanzas_RAW`) era necesario. | **Corregir el Código M** de Ripley para basarse únicamente en el archivo de Historial Financiero, eliminando la dependencia del archivo de pedidos. |
| **D5** | Ripley Queries | El usuario tiene 3 consultas de Ripley, mientras que la Guía V7.0 propuso 5 consultas (Ventas, Comisiones, Envíos, Impuestos, Reembolsos). | **Corregir el Código M** para implementar las 5 consultas de Ripley, asegurando la exhaustividad de las aristas. |

## 2. Propuestas de Mejoras Significativas (Sin Cambiar la Lógica Central)

La principal mejora es formalizar la estructura de datos que el usuario ya está utilizando (Star Schema) y optimizar la carga de datos.

| Mejora | Descripción | Impacto |
| :--- | :--- | :--- |
| **M1** | **Creación de Tablas de Dimensiones** | Formalizar las consultas `Dim_Marketplace` y `Dim_Tipo_Transaccion` para mapear los IDs numéricos a los nombres descriptivos. Esto permite al usuario usar los nombres en la Tabla Dinámica sin perder la eficiencia de los IDs. | **Modelado de Datos** (Mejora la usabilidad del reporte final). |
| **M2** | **Optimización de Carga de Datos RAW** | En lugar de usar "Combinar y Transformar" para cada carpeta, usar la función `Folder.Contents` y luego filtrar por el nombre del archivo. Esto reduce el número de consultas RAW a solo una por Marketplace (ej. `ML_RAW`). | **Rendimiento** (Simplifica el mantenimiento y acelera la actualización de datos). |
| **M3** | **Estandarización de Columnas** | Implementar una función M (`fn_EstandarizarColumnas`) para asegurar que todas las consultas de hechos tengan exactamente el mismo nombre y orden de columnas, resolviendo las discrepancias D2 y D3. | **Robustez** (Evita errores de anexado en el futuro). |

## 3. Consolidación de la Guía Maestra Final

La Guía Maestra Final (V8.0) debe incorporar estas correcciones y mejoras, manteniendo el flujo continuo y el detalle exhaustivo de las versiones anteriores. El anexo de Código M será completamente reescrito para reflejar la estructura de IDs y las 5 consultas de Ripley.

---
*(Este reporte sirve como base para la Fase 3: Consolidación de la Guía Maestra Final.)*
