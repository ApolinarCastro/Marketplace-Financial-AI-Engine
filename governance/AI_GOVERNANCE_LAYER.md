# AI Governance Layer

## Objetivo
Detectar y prevenir inconsistencias en la plataforma de manera proactiva, garantizando la integridad de los datos, la documentación y los procesos de negocio.

## Restricciones Fundamentales
* **Modo obligatorio:** `READ ONLY`
* **Operaciones Prohibidas:** Queda estrictamente prohibido que la capa de IA ejecute comandos de tipo `UPDATE`, `INSERT` o `DELETE`.

## Funciones y Validaciones
La capa de gobernanza de IA debe enfocarse en las siguientes áreas de detección automática y validación:

* **Regression Detection:** Detectar cualquier regresión funcional, financiera o de datos en un marketplace.
* **Documentary Validation:** Detectar la desaparición o alteraciones en archivos documentales (ej. desaparición de XML, cambios documentales).
* **Financial Validation:** Detectar cambios en la estructura financiera o la desaparición/modificación inesperada de comisiones.
* **UI/API Validation:** Asegurar y detectar diferencias entre los datos expuestos en la interfaz de usuario (UI) y los datos devueltos por la API.
* **API/SQL Validation:** Asegurar y detectar diferencias entre los datos de la API y los datos almacenados/calculados en las vistas o tablas SQL.
* **Taxonomy Validation:** Detectar cualquier modificación no autorizada o discrepancia en las taxonomías propias de cada marketplace.
