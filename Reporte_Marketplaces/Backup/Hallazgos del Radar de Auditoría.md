### Hallazgos del Radar de Auditoría

El análisis de los archivos RAW ha revelado los siguientes conceptos no clasificados:

**París:**
*   El radar no encontró nuevos conceptos en el archivo de París. Nuestra lógica actual parece ser completa.

**Ripley:**
El archivo de Ripley (`Historial_Nov2025.csv`) contiene múltiples conceptos que son variaciones de los que ya mapeamos. La mejor práctica es incluirlos en la `Tabla_Mapeo` para asegurar que todos los movimientos se clasifiquen correctamente.

| Concepto_Desconocido | Clasificación Propuesta (ID) | Tipo_Transaccion |
| :--- | :--- | :--- |
| Importe del envío del pedido | 3 | Costo Envío |
| Gastos de envío pagados por el operador | 3 | Costo Envío |
| Impuesto sobre las comisiones | 7 | Impuesto |
| Importe del pedido reembolsado | 8 | Reembolso |
| Importe del envío del pedido reembolsado | 8 | Reembolso |
| Gastos de envío reembolsados pagados por el operador | 8 | Reembolso |
| Comisión de reembolso | 2 | Comisión |
| Impuesto sobre la comisión de reembolso | 7 | Impuesto |
| Impuesto de la factura manual | 7 | Impuesto |
| Pago | 13 | Otros Cargos (Ajuste) |
| Impuesto sobre el abono manual | 7 | Impuesto |

### Propuesta de Actualización de la `Tabla_Mapeo`

Para que el motor dinámico clasifique estos nuevos conceptos, debes agregar las siguientes filas a tu tabla `Tabla_Mapeo` en Excel:

| Marketplace_Nombre | Termino_Busqueda | ID_Tipo_Transaccion |
| :--- | :--- | :--- |
| Ripley | Importe del envío del pedido | 3 |
| Ripley | Gastos de envío pagados por el operador | 3 |
| Ripley | Impuesto sobre las comisiones | 7 |
| Ripley | Importe del pedido reembolsado | 8 |
| Ripley | Importe del envío del pedido reembolsado | 8 |
| Ripley | Gastos de envío reembolsados pagados por el operador | 8 |
| Ripley | Comisión de reembolso | 2 |
| Ripley | Impuesto sobre la comisión de reembolso | 7 |
| Ripley | Impuesto de la factura manual | 7 |
| Ripley | Pago | 13 |
| Ripley | Impuesto sobre el abono manual | 7 |

### Siguiente Paso

Una vez que actualices tu `Tabla_Mapeo` en Excel con estas nuevas filas, el sistema de mapeo dinámico las clasificará automáticamente. No es necesario modificar el código M.

Procederé a actualizar la **Guía Maestra Definitiva (V16.0)** para incluir esta tabla de hallazgos y la lógica de auditoría como el estándar final.
