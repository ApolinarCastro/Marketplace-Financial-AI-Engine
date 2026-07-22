# PARIS XML ETL ROOT CAUSE

## FASE 1: ROOT CAUSE TÉCNICO

**Localización de Componentes**
*   **Parser XML actual:** `engine/v4/dte_indexer.py` (`DTEIndexer.parse_xml`)
*   **ETL XML actual:** `engine/v4/dte_indexer.py` (`DTEIndexer.run`)
*   **Proceso que alimenta dte_truth_v1:** Método `DatabaseV4.insert_df(..., "dte_truth_v1")` llamado desde `DTEIndexer.run()`

**¿Por qué los 62 XML nunca ingresaron?**
Los 62 archivos físicos estaban correctamente ubicados en `01_Raw/PARIS/Facturacion` y el parser tenía el soporte para extraer todos los campos requeridos (Folio, TipoDTE, RUTEmisor, RznSoc, FchEmis, RUTRecep, MntNeto, IVA/MntIVA, MntTotal). 
El problema fue que el ETL nunca se ejecutó para procesar la cola de la carpeta de PARIS. El orquestador principal omitió llamar a `DTEIndexer(marketplace='PARIS').run()`, provocando que la tabla `dte_truth_v1` quedara vacía para PARIS.

**Clasificación:**
* ETL nunca ejecutado
