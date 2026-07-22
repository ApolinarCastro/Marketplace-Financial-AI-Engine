# Regression Guard

## Objetivo
Evitar cualquier degradación, pérdida de funcionalidad o inconsistencia financiera antes de autorizar un nuevo despliegue a producción.

## Ejecución Obligatoria
**ANTES DE CUALQUIER CAMBIO O DESPLIEGUE** se debe ejecutar el proceso de:
`Regression Certification`

## Validaciones Obligatorias

El Regression Certification debe validar de forma exhaustiva las siguientes igualdades:

1. **UI = API**: Los datos presentados en la interfaz de usuario deben coincidir exactamente con los expuestos en los endpoints de la API.
2. **API = SQL**: Los datos expuestos por la API deben coincidir exactamente con los resultados de las consultas en la base de datos subyacente.
3. **SQL = Ledger Clasificado**: Los datos transaccionales de SQL deben poder ser reconciliados perfectamente con la fuente oficial `marketplace_ledger_clasificado_v1`.
4. **XML = Document Match**: Los registros financieros deben tener correspondencia exacta (match) con la documentación fiscal emitida (XML).
5. **Alertas = Auditoría**: Todas las alertas generadas deben estar documentadas, justificadas y correspondidas por el modelo de auditoría.

## Políticas de Bloqueo
**SI FALLA ALGUNA DE LAS VALIDACIONES:**
* **BLOCK DEPLOY**: Queda estrictamente prohibido el despliegue a producción. El despliegue se cancela inmediatamente hasta que el incidente sea resuelto y el Regression Certification pase con éxito al 100%.
