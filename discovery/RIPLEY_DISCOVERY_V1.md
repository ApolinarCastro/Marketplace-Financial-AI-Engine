# RIPLEY DISCOVERY V1

**Scope:** `scope = RIPLEY`
**Estado:** PENDIENTE DE EVIDENCIA

Este documento es el repositorio central para recibir y catalogar las evidencias de Ripley durante la fase de descubrimiento (Discovery). Se adhiere estrictamente a la política **Evidence First** y no contiene ni contendrá lógica inferida, heurística o reutilizada de ML/PARIS.

---

## 1. Inventario de Fuentes
Listado de los orígenes de datos oficiales identificados y disponibles para RIPLEY.

| Tipo Fuente | Descripción / Sistema | Estado de Recepción |
| :--- | :--- | :--- |
| **RAW** | (Portal, Seller Center, etc.) | *Pendiente de evidencia* |
| **APIs** | (Endpoints, Documentación oficial) | *Pendiente de evidencia* |
| **XML** | (Facturación, SII, Documentos Tributarios) | *Pendiente de evidencia* |
| **Reportes** | (Liquidaciones, Cobros, Conciliación manual) | *Pendiente de evidencia* |

---

## 2. Inventario de Archivos
Registro detallado de los archivos de muestra que se han recibido.

| Nombre del Archivo | Origen | Frecuencia | Formato (CSV/XLSX/JSON) |
| :--- | :--- | :--- | :--- |
| *[A la espera]* | *[A la espera]* | *[A la espera]* | *[A la espera]* |

---

## 3. Inventario de Campos
Diccionario en construcción basado estrictamente en la definición oficial proporcionada por Ripley o deducida directamente de su documentación técnica.

| Columna RAW/API | Descripción oficial | Estado de validación |
| :--- | :--- | :--- |
| *[A la espera]* | *[A la espera]* | *Pendiente de evidencia* |

---

## 4. Flujo Económico Observado
*(Pendiente de evidencia)*
> No se documentará ningún flujo hasta recibir ejemplos reales de transacciones completas (desde la venta hasta el abono en cuenta).

---

## 5. Taxonomía Candidata
*(Pendiente de evidencia)*
> La clasificación contable y financiera (taxes, fees, gross_sales, net_sales, etc.) será definida únicamente cuando se disponga del Inventario de Campos validado.

---

## 6. Riesgos Detectados
*(Pendiente de evidencia)*
> Se listarán discrepancias, faltantes de información o potenciales escenarios donde la RAW no cruce con el XML o API, basados estrictamente en los ejemplos proporcionados.

---

## 7. Próximas Acciones
1. Recibir y catalogar el primer set de archivos RAW y documentos de API en este repositorio.
2. Actualizar el **Inventario de Archivos** y **Fuentes**.
3. Requerir definiciones para rellenar el **Inventario de Campos**.
4. Detener cualquier avance hacia código (ETL/SQL/API) hasta que el flujo económico esté 100% clarificado en este documento.
