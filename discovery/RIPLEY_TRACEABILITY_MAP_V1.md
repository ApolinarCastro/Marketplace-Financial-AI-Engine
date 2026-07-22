# RIPLEY TRACEABILITY MAP V1

**Scope:** `scope = RIPLEY`
**Estado:** RADIOGRAFÍA FINAL DE IMPLEMENTACIÓN (AS-IS)

---

## 1. Flujo E2E Actual
El flujo actual punta a punta (End-to-End) operativo para RIPLEY es extremadamente lineal y limitado, evadiendo cruces y validaciones complejas.

**Flujo Implementado:**
`01_Raw/RIPLEY/**/*.xlsx` 
→ `engine/v4/surgical_loader.py (load_ripley)` (Aplica `melt`)
→ Inyección a `marketplace_ledger_v1`
→ `_fase1_classify.py` llama a `engine/v4/marketplace_auditor.py` (Aplica Diccionario)
→ Inyección a `marketplace_ledger_clasificado_v1`
→ `_fase2_closing.py` llama a `engine/v4/financial_closing.py` (Agrupación simple)
→ Inyección a `marketplace_cierre_financiero_v1`
→ Exposición vía `api/api.py` (`/api/v4/cierre/desglose?marketplace=RIPLEY`)
→ Consumo en Power Query (`Reporte_Marketplaces/Reporte Gerencial 360 Marketplaces.xlsx`).

---

## 2. Mapa de Trazabilidad Completo por Fuente

### A. Resumen Financiero Seller (XLSX)
* **RAW:** `01_Raw/RIPLEY/Resumen financiero/*.xlsx`
* **Loader:** `surgical_loader.py` (`load_ripley`)
* **Parser:** (Embebido en el loader: `pd.melt` para normalizar columnas horizontales)
* **Tabla Base:** `marketplace_ledger_v1`
* **Clasificación:** `marketplace_auditor.py` -> `marketplace_ledger_clasificado_v1`
* **Cierre:** `financial_closing.py` -> `marketplace_cierre_financiero_v1`
* **API:** Soportado
* **Dashboard:** Mostrado en "Reporte Gerencial 360 Marketplaces"
* **Estado:** CONECTADO (Pero con problemas semánticos y nulos)

### B. Ciclos de Facturación (CSV)
* **RAW:** `01_Raw/RIPLEY/Resumen financiero/Ciclos de facturación/*.csv`
* **Loader -> Dashboard:** DESCONECTADO (Totalmente ignorado por el motor).

### C. Fulfillment (CSV)
* **RAW:** `01_Raw/RIPLEY/Resumen financiero/Fulfillment/*.csv`
* **Loader -> Dashboard:** DESCONECTADO (Totalmente ignorado por el motor).

### D. Documentos Tributarios (XML)
* **RAW:** `01_Raw/RIPLEY/Documentos Recepcionados/*.xml`
* **Loader -> Dashboard:** DESCONECTADO (El parser DTE actual no captura facturas recibidas de Ripley).

---

## 3. Inventario de Componentes (RIPLEY)

### Scripts de Motor (Core)
* `engine/v4/surgical_loader.py` (Contiene `load_ripley`)
* `engine/v4/marketplace_auditor.py` (Contiene taxonomía Ripley)
* `engine/v4/financial_closing.py` (Cierre genérico que soporta Ripley)
* `engine/v4/run_initial_audit.py` (Script de reconstrucción que incluye a Ripley)
* `engine/v4/reset_and_close.py` (Script de wipe y rebuild)

### API & Reportes
* `api/api.py` (Endpoints de cierre y desglose funcionales para `?marketplace=RIPLEY`)
* `Reporte Gerencial 360 Marketplaces.xlsx` (Power Query / Dashboard)

### Tablas (DuckDB)
* `marketplace_ledger_v1`
* `marketplace_ledger_clasificado_v1`
* `marketplace_cierre_financiero_v1`
*(No se detectan vistas específicas)*

### Scripts Auxiliares y de Diagnóstico Activos
* `_diag_ripley.py`: Evalúa valores `NULL` o comportamientos inesperados de `include_in_operational_pnl` para las filas "A pagar" en Ripley.
* `_fase3_validate.py`: Ejecuta 4 validaciones específicas codificadas para `RIPLEY`.
* `_surgical_review.py`: Contiene bloque `RIPLEY DEEP DIVE`.
* `_fase1_classify.py`, `_fase2_closing.py`, `_reclassify_all.py`, `_killcritic_validate.py`: Orquestadores que incluyen Ripley en su array de iteración `['ML', 'RIPLEY', 'PARIS', 'FALABELLA']`.

---

## 4. Matriz de Cobertura
| Componente | Nivel de Cobertura | Detalle |
| :--- | :--- | :--- |
| **Ingesta de Archivos** | **25%** | 1 de 4 fuentes (Sólo Seller XLSX). |
| **Volumen de Datos** | **Parcial** | Se pierde toda la granularidad logística y transaccional. |
| **Matching Tributario** | **0%** | Sin cruce de folios contra XML. |
| **Matching Operacional** | **0%** | Sin cruce de `Order number` vs `order_id`. |
| **Reportabilidad Dashboard** | **Aparente (100%)** | Pasa la data al Dashboard, pero la data subyacente está incompleta. |

---

## 5. Matriz de Dependencias
* **Dependencia de Origen:** El Dashboard depende estrictamente de `marketplace_cierre_financiero_v1`.
* **Dependencia Transaccional:** `marketplace_cierre_financiero_v1` depende estrictamente de que `marketplace_ledger_clasificado_v1` no contenga `financial_group = NULL` (problema diagnosticado en `_diag_ripley.py`).
* **Dependencia de Aislamiento:** Actualmente Ripley DEPENDE de los mismos módulos que ML y PARIS (`surgical_loader.py` y `marketplace_auditor.py`). Cualquier cambio global lo impacta.

---

## 6. Matriz de Fuentes No Integradas
| Fuente | Tipo | ¿Qué se ignora? | Consecuencia en el Modelo Actual |
| :--- | :--- | :--- | :--- |
| **Ciclos de Facturación** | CSV | Ventas unitarias, impuestos detallados. | Falta de trazabilidad por `Order number`. No se pueden defender diferencias de precio. |
| **Fulfillment** | CSV | Sobrecargos logísticos y `order_id`. | Imposibilidad de imputar mermas logísticas a envíos específicos. |
| **DTE (XML)** | XML | Folio Oficial y validación SII. | Riesgo de incongruencia contable-tributaria. |

---

## 7. Matriz de Componentes Muertos / Rotos
| Componente / Concepto | Estado | Observación |
| :--- | :--- | :--- |
| **Matching Engine** (`dte_matcher.py` / `xml_matcher.py`) | Muerto para Ripley | Carece de llaves e instrucciones para procesar Ripley. |
| **Clasificación Financiera Ripley** | Roto / Parcial | `_diag_ripley.py` evidencia conflictos con "A pagar" (`include_in_operational_pnl`). |
| **Descuentos Operacionales (CSV)** | Muerto | Reglas de taxonomía para FF no tienen data sobre la que operar. |

---

## 8. Lista Exacta de Archivos Faltantes por Integrar
* Todos los archivos en: `01_Raw/RIPLEY/Resumen financiero/Ciclos de facturación/*.csv` (Aprox. 48)
* Todos los archivos en: `01_Raw/RIPLEY/Resumen financiero/Fulfillment/*.csv` (Aprox. 62)
* Todos los archivos en: `01_Raw/RIPLEY/Documentos Recepcionados/*.xml` (Aprox. 407)

---

## 9. Lista Exacta de Tablas Afectadas
*(Tablas que deberán absorber el impacto de las nuevas integraciones)*
1. `marketplace_ledger_v1` (Absorberá Ciclos y Fulfillment).
2. `marketplace_ledger_clasificado_v1` (Absorberá la taxonomía de las nuevas columnas).
3. `marketplace_cierre_financiero_v1` (Variará sus totales al integrar verdaderos descuentos FF y evitar nulos).

---

## 10. Lista Exacta de Procesos Afectados
*(Procesos que requerirán codificación/refactor para lograr la cobertura)*
1. `engine/v4/surgical_loader.py` (Agregar ingesta CSV).
2. `engine/v4/xml_matcher.py` o módulo de DTE (Agregar parsing XML Ripley).
3. `engine/v4/marketplace_auditor.py` (Expansión de diccionario Ripley para CSVs).
4. `engine/v4/reconciliation.py` / `dte_matcher.py` (Construcción del Matching Engine `order_id` vs `Order number` vs `<NroDTE>`).
