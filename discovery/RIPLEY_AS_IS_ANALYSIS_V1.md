# RIPLEY AS-IS ANALYSIS V1

**Scope:** `scope = RIPLEY`
**Estado:** ANÁLISIS DE IMPLEMENTACIÓN EXISTENTE

## 1. Executive Summary
El análisis de la base de código actual revela que RIPLEY ya cuenta con una implementación parcial y en estado primario dentro del ecosistema V4. El motor actualmente reconoce a RIPLEY como un *marketplace* válido, pero la ingesta de datos está severamente truncada: **sólo procesa los archivos XLSX (Seller)**. No existe integración logística, tributaria ni un motor de matching implementado para este dominio. Existen bugs diagnosticados relacionados con las clasificaciones financieras.

## 2. Current Architecture
* **Motor Base:** Funciona sobre la arquitectura `v4` (`database.duckdb`).
* **Ingesta:** `engine/v4/surgical_loader.py` (método `load_ripley`).
* **Clasificación:** `engine/v4/marketplace_auditor.py` (contiene el diccionario maestro de taxonomía para RIPLEY).
* **Cierre:** `engine/v4/financial_closing.py`.
* **Capa API:** `api/api.py` (FastAPI).

## 3. Current Data Flow
1. **RAW:** Sólo captura los archivos con extensión `*.xlsx` dentro de `01_Raw/RIPLEY/`.
2. **ETL (Loader):** Se aplica un proceso de pivot (melt) en `load_ripley` para transformar las columnas horizontales de los Excel en filas transaccionales, inyectándolas a `marketplace_ledger_v1`.
3. **Clasificación (Auditor):** El diccionario clasifica los rubros encontrados asignando un `financial_group` e insertando en `marketplace_ledger_clasificado_v1`.
4. **Cierre:** Se agrupa la información clasificada mensualmente en `marketplace_cierre_financiero_v1`.

## 4. Current Data Model
RIPLEY opera sobre las 3 tablas globales:
1. `marketplace_ledger_v1` (RAW Aplanado).
2. `marketplace_ledger_clasificado_v1` (Con taxonomía y atributos financieros).
3. `marketplace_cierre_financiero_v1` (Resumen P&L agregado).

## 5. Current Power Query Flow
* **Archivo:** `Reporte_Marketplaces/Reporte Gerencial 360 Marketplaces.xlsx`.
* **Conexión:** Se asume que Power Query consume directamente desde DuckDB o mediante endpoints API, dado que el reporte ya está centralizado y RIPLEY está habilitado en los scripts de cierre y APIs (ej: `/api/v4/cierre/desglose`).

## 6. Current Matching Flow
* **ESTADO:** INEXISTENTE.
* No existe código de cruce (`dte_matcher.py`, `xml_matcher.py` u otros) adaptado para buscar coincidencias transaccionales ni tributarias para RIPLEY.

## 7. Current Reconciliation Flow
* **ESTADO:** INEXISTENTE.
* No hay flujos que validen si los montos cobrados en Fulfillment, declarados en XML y liquidados en los Seller XLSX son matemáticamente idénticos. Sólo se realiza una agregación bruta (`GROUP BY`).

## 8. Current Dashboard Flow
La capa API permite consultar los cierres de RIPLEY (como se evidencia en `_debug_desglose.py` atacando `/api/v4/cierre/desglose?marketplace=RIPLEY&periodo=...`), lo que fluye hasta el Dashboard. Sin embargo, los datos reflejados son inherentemente incompletos.

## 9. Gaps Detectados
* **Gap Logístico:** Los archivos CSV de Fulfillment (`Resumen financiero/Fulfillment/`) son ignorados (`surgical_loader.py` sólo busca `.xlsx`).
* **Gap Operacional:** Los archivos CSV de "Ciclos de facturación" son ignorados.
* **Gap Tributario:** Los archivos XML (Facturas Tipo 33) en `Documentos Recepcionados` no se procesan para RIPLEY.
* **Gap de Transparencia:** La tabla RAW no contiene las llaves logísticas (`order_id`) requeridas para un matching futuro, ya que el archivo XLSX del Seller suele tener data agregada.

## 10. Bugs Evidentes
* **Scripts de Diagnóstico Activos:** Existen scripts de contingencia (`_diag_ripley.py`, `_fase3_validate.py`) intentando corregir o auditar problemas de campos `NULL` en RIPLEY.
* **Clasificación del Pago:** La marca de inclusión (`include_in_operational_pnl`) para las filas "A pagar" o "ajustes" presenta anomalías, generando que el balance final (`neto`) pueda estar distorsionado o fallar al generar el cierre P&L correcto.

## 11. Risks
* **Falsa Sensación de Completitud:** Al estar RIPLEY habilitado en la API y el Dashboard, los usuarios de negocio pueden ver un estado de P&L de RIPLEY asumiendo que es real, cuando en la práctica se está perdiendo toda la dimensión de cobros logísticos y cruces tributarios (faltan 3 de 4 fuentes).
* **Contaminación Global:** Las reglas de clasificación de RIPLEY están embebidas en `marketplace_auditor.py` (junto con las reglas de ML y PARIS), lo que viola la nueva política de aislamiento de dominios de gobernanza si se requieren modificaciones asimétricas.

## 12. Recommendations
Basado exclusivamente en la implementación existente y sin proponer rediseños no autorizados, la recomendación es:
1. **Apagar / Bloquear RIPLEY temporalmente del Dashboard/API** para evitar fugas de información inexacta a usuarios de negocio (dado que faltan fuentes críticas).
2. **Extraer y aislar el Pipeline:** La lógica del `load_ripley` en `surgical_loader.py` deberá ser migrada y ampliada para procesar los CSV y XML faltantes dentro de una estructura aislada, respetando la directiva actual.
