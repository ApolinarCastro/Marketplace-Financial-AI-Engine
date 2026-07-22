# API REGRESSION REPORT (P32.2)

## Regresiones Detectadas

1. **Filtro de Marketplace Roto (Literal "ALL")**
   - **Impacto**: El Frontend fallaba al intentar visualizar "Todos los Marketplaces", ya que los endpoints `/api/v4/ledger`, `/api/v4/auditoria` y `/api/v4/cierre` inyectaban "ALL" como un valor literal en SQLite, retornando cero registros y rompiendo el flujo de estado de `loadDashboard()`.

2. **Ausencia de Parámetros Contextuales**
   - **Impacto**: `/api/v4/auditoria` ignoraba completamente el período, por lo que siempre retornaba la totalidad de alertas (límite duro), causando inconsistencia cuando el usuario cambiaba de mes en la interfaz.

3. **Contrato de Certificación Electrónica Roto**
   - **Impacto**: La función `openCertificationDrawer` en el Frontend recibía un diccionario con llaves como `marketplace`, `periodo` y `transaction_id`, mientras que esperaba los campos vitales `tipo_dte`, `folio`, el objeto anidado `pipeline` y `evidencia`.
   - **Origen**: En algún momento se cambió la implementación hacia el mockup `DocumentGapEngine()` que retornaba filas crudas sin serializar para el Drawer.

## Soluciones Implementadas

Las soluciones aplicadas en `api/api.py` cumplen con la restricción P32.2 de "No modificar la lógica de negocio":
- Se usó un condicional estándar para ignorar el filtro SQLite cuando `marketplace == "ALL"`.
- Se normalizó el consumo del `periodo` calculando `last_day` del mes seleccionado para las consultas temporales.
- Se reescribió `get_electronic_certification_status` mapeando directamente la base de datos `marketplace_ledger_v1` a la estructura del frontend (Pipeline / Evidencia).
