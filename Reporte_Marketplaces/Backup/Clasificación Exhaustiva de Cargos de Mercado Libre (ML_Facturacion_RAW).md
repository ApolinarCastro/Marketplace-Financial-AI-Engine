# Clasificación Exhaustiva de Cargos de Mercado Libre (ML_Facturacion_RAW)

El análisis de los valores únicos de la columna "Detalle" revela una complejidad mayor en los costos de Mercado Libre, especialmente en logística y servicios Full. A continuación, se presenta la clasificación de todos los cargos identificados y la lógica de filtrado para Power Query.

## 1. Clasificación de Cargos y Tipos de Transacción

Se requiere la creación de un nuevo tipo de transacción para agrupar los costos de Fullfilment y se debe ajustar la lógica de filtrado para los costos de envío y publicidad.

| Detalle (Valor en RAW) | Categoría | ID `Dim_Tipo_Transaccion` | Fact Table (Consulta) |
| :--- | :--- | :--- | :--- |
| **Venta y Comisión** | | | |
| `Cargo por venta` | Comisión Marketplace | 2 | `ML_Fact_Comisiones` |
| **Costos de Envío** | | | |
| `Cargo por Mercado Envíos` | Costo Envío | 3 | `ML_Fact_Envios` |
| `Cargo por envíos de Mercado Libre` | Costo Envío | 3 | `ML_Fact_Envios` |
| **Costos de Publicidad** | | | |
| `Campañas de publicidad - Brand Ads` | Publicidad | 7 | `ML_Fact_Publicidad` |
| `Campañas de publicidad - Display` | Publicidad | 7 | `ML_Fact_Publicidad` |
| `Campañas de publicidad - Product Ads` | Publicidad | 7 | `ML_Fact_Publicidad` |
| `Cargo por campaña de publicidad - Brand Ads` | Publicidad | 7 | `ML_Fact_Publicidad` |
| `Cargo por campaña de publicidad - Product Ads` | Publicidad | 7 | `ML_Fact_Publicidad` |
| **Costos de Devolución** | | | |
| `Cargo por devolución` | Devolución | 5 | `ML_Fact_Devoluciones` |
| **Costos de Asesoría** | | | |
| `Cargo por Asesoría Comercial` | Asesoría Comercial | 11 | `ML_Fact_Asesoria` |
| **NUEVO: Costos de Fullfilment** | | | |
| `Cargo por mantenimiento de Mi página` | Costo Fullfilment | **12** | `ML_Fact_Fullfilment` |
| `Cargo por retiro de stock Full` | Costo Fullfilment | **12** | `ML_Fact_Fullfilment` |
| `Cargo por servicio de almacenamiento Full` | Costo Fullfilment | **12** | `ML_Fact_Fullfilment` |
| `Cargo por stock antiguo en Full` | Costo Fullfilment | **12** | `ML_Fact_Fullfilment` |
| **Anulaciones y Bonificaciones** | | | |
| `Bonificación` | Bonificación | 9 | `ML_Fact_Bonificaciones` |
| `Anulación del cargo por venta` | Bonificación | 9 | `ML_Fact_Bonificaciones` |
| `Anulación del cargo por Mercado Envíos` | Bonificación | 9 | `ML_Fact_Bonificaciones` |
| `Anulación del cargo por envíos de Mercado Libre` | Bonificación | 9 | `ML_Fact_Bonificaciones` |
| `Anulación del cargo por devolución` | Bonificación | 9 | `ML_Fact_Bonificaciones` |
| **Otros** | | | |
| `Cargo` | Costo Fijo Operacional | 4 | `ML_Fact_Otros` |
| `Detalle` | (Ignorar) | - | - |
| `nan` | (Ignorar) | - | - |

## 2. Lógica de Filtrado y Transformación para Power Query

Se requiere:
1.  **Añadir ID 12** (`Costo Fullfilment`) a `Dim_Tipo_Transaccion`.
2.  **Crear nuevas consultas** `ML_Fact_Fullfilment` y `ML_Fact_Bonificaciones`.
3.  **Ajustar la lógica de filtrado** de las consultas existentes.

### A. Actualización de `Dim_Tipo_Transaccion`

Se añade el ID 12:

| ID | Tipo | Categoría | Signo Esperado |
| :--- | :--- | :--- | :--- |
| 12 | Costo Fullfilment | Costo | Negativo |

### B. Lógica de Filtrado por Consulta

| Consulta | ID Tipo Transacción | Lógica de Filtrado (Columna "Detalle") |
| :--- | :--- | :--- |
| `ML_Fact_Comisiones` | 2 | **Igual a** "Cargo por venta" |
| `ML_Fact_Envios` | 3 | **Comienza con** "Cargo por envío" **O** **Igual a** "Cargo por Mercado Envíos" |
| `ML_Fact_Publicidad` | 7 | **Contiene** "publicidad" **O** **Contiene** "Mercado Ads" |
| `ML_Fact_Asesoria` | 11 | **Igual a** "Cargo por Asesoría Comercial" |
| **`ML_Fact_Fullfilment`** | **12** | **Contiene** "Full" **O** **Igual a** "Cargo por mantenimiento de Mi página" |
| **`ML_Fact_Bonificaciones`** | **9** | **Igual a** "Bonificación" **O** **Comienza con** "Anulación del cargo por" |
| `ML_Fact_Devoluciones` | 5 | **Igual a** "Cargo por devolución" |
| `ML_Fact_Ventas` | 1 | **Filtrar por el campo "Detalle" de la Venta** (No se usa el campo "Detalle" de la Facturación para el GMV, sino el campo "Valor de la compra" en el registro de "Cargo por venta") |

**Nota sobre `ML_Fact_Ventas`:** El GMV (Venta) se extrae del campo `Valor de la compra` en las filas donde `Detalle` es "Cargo por venta". No se crea una consulta separada para la venta, sino que se utiliza la consulta `ML_Fact_Comisiones` (o una copia) para extraer el GMV.

## 3. Conclusión

La guía didáctica debe ser actualizada para reflejar esta nueva granularidad, incluyendo la creación de las consultas `ML_Fact_Fullfilment` y `ML_Fact_Bonificaciones`, y la adición del ID 12 a la dimensión de tipos de transacción.
