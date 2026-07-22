# BACKLOG

## Persistencia de capa_origen en BD
- **Objetivo:** Eliminar inferencias por prefijo de `id_transaccion` (ej. `RIP_TH_`, `RIP_FF_`, `RIP_CSV_`).
- **Descripción:** Actualmente, la identificación de la capa de origen (Operacional, Liquidación, Tesorería) se hace mediante inferencia de prefijos del `id_transaccion` o del `archivo_origen` como mecanismo transitorio. Esto es frágil. Se requiere modificar el esquema de la base de datos para agregar y persistir una columna `capa_origen` en `marketplace_ledger_v1`, y actualizar el pipeline ETL para poblarla correctamente desde el origen.
- **Prioridad:** Alta (Deuda Técnica).
