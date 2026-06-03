# PROGRAMA T2 — XML TRACEABILITY EXECUTION PLAN

**Fecha**: 2026-05-30
**Régimen**: DISEÑO — APROBACIÓN REQUERIDA
**DB Oficial**: `data/db/meli_financial_v4.db` (DuckDB V1.5.1)

---

## RESUMEN EJECUTIVO

Plan de implementación para elevar cobertura XML de 30.2% a **proyectado 83.5%**+ mediante 3 intervenciones puente (PARIS Quick Win, ML Normalización, RIPLEY Indirecto Bridge). Se incluye también FALABELLA (completar) y la búsqueda de XMLs RIPLEY 2025 perdidos.

| Sprint | Marketplace | Dificultad | Duración | Inversión | Cobertura actual → proyectada | Filas impactadas | $ impactado |
|---|---|---|---|---|---|---|---|
| **PW1** | PARIS | BAJA | ~1 semana | 0 (bridge existente) | 79.0% → 100% | 8,919 | $65.7M |
| **PW2** | ML | MEDIA | ~2 semanas | 1-2 developers | 89.4% → ~99% | 10,789 | $307.0M |
| **PW3** | RIPLEY | ALTA | ~4 semanas | 2-3 developers | 0% → ~9.5% (máx: ~50% si se recuperan XMLs 2025) | 269,216 | $284.9M |
| **PW4** | FALABELLA | BAJA | ~3 días | 0 (tarea existente) | 61.5% → ~100% | 388 | $3.5M |

**Cobertura global proyectada:**
- 30.2% → 83.5% (125,002 → 414,314 filas con folio_xml) si RIPLEY se ejecuta al 100%
- Sin RIPLEY: 30.2% → 36.9% (152,630 filas) — RIPLEY es 93.1% del gap

---

## TABLA DE CONTENIDOS

1. [PARIS Quick Win (PW1)](#1-paris-quick-win-pw1)
2. [ML folio_xml Normalization (PW2)](#2-ml-folio_xml-normalization-pw2)
3. [RIPLEY Indirect Bridge (PW3)](#3-ripley-indirect-bridge-pw3)
4. [FALABELLA Completion (PW4)](#4-falabella-completion-pw4)
5. [Data Contract Schema](#5-data-contract-schema)
6. [Risk Analysis](#6-risk-analysis)
7. [Roadmap & Timeline](#7-roadmap--timeline)
8. [Governance & Approval Gates](#8-governance--approval-gates)

---

## 1. PARIS Quick Win (PW1)

### Estado Actual

| Métrica | Valor |
|---|---|
| XMLs totales en Facturación | 54 |
| XMLs vinculados vía bridge existente | 32 (59.3%) |
| XMLs NO vinculados | 22 (40.7%) |
| Monto total XMLs no vinculados | $28,226,928 (Total) / $25,334,378 (Neto) |
| Gap DB sin folio_xml | 8,919 filas, $65,746,929 |
| Bridge actual cubre | 79.0% filas / 82.6% dólares |

### Diagnóstico

El bridge actual (Sprint A2) mapea 32/54 XMLs a filas del ledger usando Excel `numero factura`/`numero liq.factura` → `numero orden` → Ledger `id_orden`. Los 22 XMLs no vinculados son:

| Folio | MntTotal | FchEmis | Observación |
|---|---|---|---|
| 23063104 | $113,000 | 2025-01-06 | |
| 16325 | $92,808 | 2025-01-08 | Folio bajo (posible número interno) |
| 23063403 | $91,000 | 2025-01-13 | |
| 16467 | $1,183,644 | 2025-01-17 | Folio bajo |
| 23063626 | $84,000 | 2025-01-20 | |
| 16745 | $0 | 2025-01-31 | Monto cero (NC?) |
| 16644 | $664,796 | 2025-01-31 | |
| 16845 | $838,534 | 2025-02-07 | |
| 16933 | $898,277 | 2025-02-14 | |
| 17010 | $1,411,231 | 2025-02-21 | |
| 17202 | $196,895 | 2025-02-28 | |
| 17115 | $491,812 | 2025-02-28 | |
| 17306 | $271,639 | 2025-03-12 | |
| 19118 | $5,421,195 | 2025-10-01 | |
| 25268825 | $7,818,947 | 2025-10-28 | |
| 30504881 | $7,818,947 | 2025-11-04 | |
| 25658433 | $14,990 | 2025-12-03 | |
| 25770251 | $23,388 | 2025-12-15 | |
| 25813166 | $70,569 | 2025-12-22 | |
| 25567085 | $517,554 | 2026-01-31 | |
| 25880829 | $199,252 | 2026-02-28 | |
| 26373131 | $4,450 | 2026-03-10 | |

### Metodología Propuesta

```
Paso 1: Extraer folio + monto de cada XML no vinculado
Paso 2: Buscar cada folio en Excel Transacciones (columna 'numero factura'/'numero liq.factura') 
        → si existe, extraer 'numero orden' → Ledger rows
Paso 3: Para folios NO encontrados en Excel (posiblemente por ser de períodos no cubiertos):
        → Buscar coincidencia directa por monto + fecha en Ledger
        → Si corresponde a un Tipo 61 (Nota Crédito) o Tipo 52 (Guía), definir bridge especial
Paso 4: Para $0 (folio 16745): probable Nota de Crédito o Guía → clasificar y excluir del bridge
Paso 5: Verificar 10 muestras aleatorias con rastreo completo (XML → Excel → Ledger)
```

### Dificultad: BAJA

Razones:
- Bridge existente y probado (32/32 verificados, 100% precisión)
- Excel ya mapeado, solo faltan los 22 folios
- No requiere nuevo código de parsing

### Entregables
- `governance/PARIS_XML_BRIDGE_EXTENSION_REPORT.md` — reporte de extensión
- Script `engine/v4/paris_bridge_pw1.py`
- pipeline_log: actualización de cobertura post-ejecución
- Rollback vía snapshot pre-PW1

### Proyección: ~$28.2M adicionales (Total XML) / $65.7M adicionales (Ledger via bridge expansion)

---

## 2. ML folio_xml Normalization (PW2)

### Estado Actual

| Métrica | Valor |
|---|---|
| Filas ML totales | 101,603 |
| Filas con folio_xml | 90,814 (89.4%) |
| Filas SIN folio_xml | 10,789 (10.6%) |
| Monto sin folio_xml | $307,011,950.93 |
| XMLs ML disponibles | 762 (100%) |
| XML folios únicos | 762 |
| DB folio_xml format | `033-XXXXXXXXXX` (prefijo 033 + folio DTE real) |

### Diagnóstico

Las 10,789 filas sin folio_xml tienen `estado_xml = None`, lo que indica que nunca pasaron por el proceso SIN_RECURSO_XML (DTEIndexer). Corresponden a 3 archivos fuente:

| Archivo Origen | Filas | Monto | Período |
|---|---|---|---|
| `1 julio 2025 - 1 enero 2026.xlsx` | 5,369 | $147,123,626 | Jul-Dic 2025 |
| `1 enero 2025 - 1 julio 2025.xlsx` | 3,818 | $116,498,619 | Ene-Jun 2025 |
| `1 enero 2026 - 1 mayo 2026.xlsx` | 1,602 | $43,389,706 | Ene-Abr 2026 |

Los datos más antiguos (2025) son los que faltan. Los 762 XMLs ML cubren todo el período 2025-2026, por lo que los folios DTE existen. El problema es que el DTEIndexer no procesó estas filas, ya sea porque:
- (a) El Excel fuente no contenía la columna de folio para ese período
- (b) El XML no se cargó en el proceso batch de ese período
- (c) La fila corresponde a un concepto no-DTE (comisiones, ajustes) que no tiene XML asociado

### Metodología Propuesta

```
Paso 1: Extraer todos los folios DTE de los 762 XMLs ML (sin prefijo)
Paso 2: Para cada archivo Excel fuente de las 10,789 filas:
  a. Identificar columna que contiene folio DTE (exact match con XML folios)
  b. Si existe, extraer folio por fila
  c. Si NO existe, buscar coincidencia por id_orden/id_transaccion en columnas Excel
Paso 3: Para filas sin match:
  a. Determinar si corresponden a conceptos no-DTE (comisiones, ajustes)
  b. Si son no-DTE: marcar como "SIN XML ESTRUCTURAL" y documentar
  c. Si son DTE pero sin match: investigar XML faltante en 01_Raw/ML
Paso 4: Actualizar folio_xml en DB
Paso 5: Verificar 20 muestras aleatorias
```

### Dificultad: MEDIA

Razones:
- 762 XMLs existen y están parseados — 100% disponibles
- Bridge metodológico ya existe (ML 89.4% actual)
- Riesgo: algunas filas pueden ser conceptos no-DTE (comisiones estructurales)
- Incertidumbre: $307M es el gap más grande en monto absoluto

### Entregables
- `governance/ML_XML_NORMALIZATION_REPORT.md`
- Script `engine/v4/ml_xml_normalize_pw2.py`
- pipeline_log: cobertura ML post-ejecución

### Proyección: ~$307M potencial (depende de cuántas filas sean DTE-matchables)

---

## 3. RIPLEY Indirect Bridge (PW3)

### Estado Actual

| Métrica | Valor |
|---|---|
| Filas RIPLEY totales | 269,216 |
| Filas con folio_xml | 0 (0.0%) |
| XMLs RIPLEY disponibles | 100 |
| Período cubierto por XMLs | 2026-03-20 → 2026-05-27 (~2 meses) |
| Monto total XMLs | $25,483,777 |
| Monto ledger RIPLEY total | $284,897,360 |
| **Cobertura máxima posible (XMLs actuales)** | **~8.9%** |

### Hallazgo Crítico

Los 100 XMLs RIPLEY disponibles cubren SOLO Marzo-Mayo 2026. El ledger RIPLEY abarca Enero 2025 → Diciembre 2026 (24 meses). Esto significa que **incluso con un bridge perfecto, la cobertura XML de RIPLEY no puede superar ~9.5% del ledger con los XMLs actuales**.

Los 100 XMLs RIPLEY que fueron removidos del directorio PARIS (durante la Recertificación de Mayo 2026) contenían facturas del período 2025. Si esos XMLs aún existen en backups o snapshots, la cobertura potencial subiría a ~50%+.

### Clasificación de XMLs por Tipo

De los 100 XMLs RIPLEY:

| Tipo | Cantidad | Monto Total | Descripción |
|---|---|---|---|
| Comisión Ventas MKP (semanal) | 9 | $5,676,987 | Comisión marketplace, período semanal |
| Despacho productos MKP (semanal) | 9 | $2,051,627 | Logística de despacho, período semanal |
| FBR Productos (individual) | 22 | $5,930,613 | Productos específicos con SKU |
| Cobro Logístico Primera Milla | 12 | $3,781,013 | Logística parcial primera milla |
| Acuerdo Comercial / Anulación | 5 | $2,800,021 | Acuerdos comerciales + 1 anulación |
| Cofinanciamiento Logístico | 12 | $992,107 | Cofinanciamiento FBR |
| Cobro Despacho Logística Inversa | 12 | $297,000 | Logística inversa FBR |
| Cobro Almacenamiento Diario | 12 | $38,917 | Almacenamiento diario FBR |
| Penalidad - Cancelación | 1 | $13,855 | Penalizaciones |
| Liquidación Consignatario | 1 | $418,900 | Liquidación especial |
| Productos Nicopoly (individual) | 5 | $1,482,737 | Productos de marca Nicopoly |

### Metodología Propuesta

```
Paso 1 (Pre-bridge): Búsqueda de XMLs RIPLEY 2025
  a. Buscar en snapshots V2-V6 en data/db/snapshot_*
  b. Buscar en git history (los XMLs estaban en PARIS/ antes de la recertificación)
  c. Si se encuentran: restaurar a 01_Raw/RIPLEY/Documentos Recepcionados/
  d. Actualizar inventario XML RIPLEY

Paso 2: Mapeo por período (INDIRECTO)
  Para cada XML con NmbItem = "Comision Ventas MKP del: [fecha_inicio] al [fecha_fin]":
    a. Extraer período del NmbItem
    b. Buscar en ledger RIPLEY filas del mismo período (por fecha)
    c. Agrupar por id_transaccion (liquidación) que caen en ese período
    d. Match por diferencia de monto: ABS(SUM(ledger.monto) - XML.MntTotal) < umbral (1%)
    e. Si match: asignar folio_xml a todas las filas de esa liquidación

Paso 3: Mapeo por producto (FBR)
  Para cada XML con descripción de producto (SKU):
    a. Extraer SKU de la descripción (formato "FBR 2000XXXXXXXXXX")
    b. Buscar en ledger filas con ese SKU/id_producto
    c. Match por monto + SKU
    d. Asignar folio_xml

Paso 4: Mapeo por tipo de costo (logística, almacenamiento, etc.)
  Para XMLs de logística/almacenamiento:
    a. Extraer período y monto
    b. Buscar en financial_group correspondiente (costos_operacionales)
    c. Match por período + monto agregado

Paso 5: Verificación
  a. Verificar 20 muestras con trazabilidad completa
  b. Documentar cada regla de matching
  c. Medir precisión (debe ser 100% — match o no-match, sin falsos positivos)
```

### Dificultad: ALTA

Razones:
- No hay columna puente directa (no Excel con folio → orden mapping como PARIS)
- Match es por período + monto, no por ID directo
- Alta granularidad: cada XML cubre múltiples filas del ledger
- Variabilidad en NmbItem: no todos los XMLs tienen formato de período consistente
- Dependencia externa: encontrar XMLs 2025 es clave para superar ~9.5% de cobertura

### Entregables
- `governance/RIPLEY_XML_BRIDGE_REPORT.md`
- Script `engine/v4/ripley_indirect_bridge_pw3.py`
- pipeline_log: cobertura RIPLEY post-ejecución
- Documentación de XMLs 2025 recuperados (si aplica)

### Proyección
- **Sin XMLs 2025**: ~$25.5M adicionales (8.9% de cobertura RIPLEY)
- **Con XMLs 2025 recuperados**: hasta ~$142M adicionales (~50% de cobertura RIPLEY)

---

## 4. FALABELLA Completion (PW4)

### Estado Actual

| Métrica | Valor |
|---|---|
| Filas FALABELLA totales | 1,008 |
| Filas con folio_xml | 620 (61.5%) |
| Filas SIN folio_xml | 388 (38.5%) |
| Monto sin folio_xml | $3,464,631 |
| XMLs FALABELLA disponibles | 4 |

### Metodología Propuesta

```
Paso 1: Extraer folios de los 4 XMLs FALABELLA
Paso 2: Verificar si los folios faltantes existen en Excel fuente
Paso 3: Bridge directo (similar a PARIS): folio XML → columna Excel → Ledger
Paso 4: Verificar 100% de las filas
```

### Dificultad: BAJA

### Proyección: ~$3.5M adicionales (100% de cobertura FALABELLA)

---

## 5. Data Contract Schema

### Estructura de Bridge Uniforme

Para mantener consistencia entre los 4 marketplaces, se propone el siguiente esquema unificado:

```sql
CREATE TABLE xml_bridge_registry (
    bridge_id INTEGER PRIMARY KEY,
    marketplace VARCHAR NOT NULL,          -- ML | RIPLEY | PARIS | FALABELLA
    xml_folio VARCHAR NOT NULL,            -- Folio DTE del XML
    xml_file_path VARCHAR NOT NULL,        -- Ruta relativa al XML
    xml_mnt_total DECIMAL(18,2),           -- Monto total del XML
    xml_fch_emis DATE,                     -- Fecha de emisión
    bridge_type VARCHAR NOT NULL,          -- DIRECTA | INDIRECTA | PERIODO | PRODUCTO
    bridge_column VARCHAR,                 -- Columna Excel puente (si aplica)
    source_document VARCHAR,               -- Documento fuente (Excel, XLSX)
    ledger_id_transaccion VARCHAR,         -- ID en ledger (opcional, para DIRECTA)
    ledger_id_orden VARCHAR,               -- ID orden en ledger (opcional)
    match_confidence DECIMAL(5,2),         -- 100.00 = exacto, <100 = fuzzy
    verified BOOLEAN DEFAULT FALSE,        -- Verificación manual
    bridge_date DATE DEFAULT CURRENT_DATE, -- Fecha de ejecución del bridge
    pipeline_log_id INTEGER               -- Referencia a pipeline_log
);
```

### Contractos Inmutables (14/14 Regression)

La ejecución de estos bridges NO altera:
1. `marketplace_ledger_v1` — schema inalterado
2. `marketplace_ledger_clasificado_v1` — schema inalterado
3. Montos financieros — ZERO impacto
4. Clasificaciones contables — ZERO impacto
5. Loaders — NO ejecutados
6. ETL — NO ejecutado
7. `DTEIndexer` — NO ejecutado
8. `XMLJustifier` — NO ejecutado
9. RIPLEY — NO reparado
10. `BASELINE_V7` — NO creado
11. API endpoints — ZERO cambios
12. UI — ZERO cambios (no existe)
13. SQL queries de reporte — ZERO cambios
14. DB oficial — única modificación: columna `folio_xml` poblada

---

## 6. Risk Analysis

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| **PW1: PARIS folios no existen en Excel** | MEDIA | Los 22 folios no tienen puente → solo bridge INDIRECTO | Buscar por monto+fecha como alternativa |
| **PW2: ML filas sin XML asociado** | MEDIA-ALTA | $307M sin cobertura | Investigar si son comisiones estructurales vs DTE-facturables |
| **PW2: ML estado_xml = None** | MEDIA | DTEIndexer no procesó → requiere reprocesamiento | NO ejecutar DTEIndexer (prohibido) → bridge manual |
| **PW3: RIPLEY solo 8.9% coverage** | ALTA (100%) | $260M sin cobertura aceptando el límite actual | Buscar XMLs 2025 perdidos |
| **PW3: XMLs 2025 irrecuperables** | ALTA | RIPLEY nunca superará ~9.5% cobertura | Documentar como limitación estructural, aceptar score RIPLEY reducido |
| **PW3: Bridge INDIRECTO baja precisión** | MEDIA | Falsos positivos en match por período | Solo match si diferencia < 1%, no forzar coincidencias |
| **PW4: FALABELLA XML insuficiente** | BAJA | 4 XMLs cubren solo parte de 388 filas | Bridge DIRECTA con Excel |
| **Rollback** | BAJA | Corrupción de datos | Snapshot pre-ejecución obligatorio |
| **LIVE DB lock (PID 27988)** | ALTA | No se puede escribir folio_xml | Esperar liberación o forzar kill |

### Riesgo Especial: RIPLEY XMLs 2025 Perdidos

Los 100 XMLs RIPLEY que estaban en el directorio PARIS (antes de la Recertificación) han desaparecido del workspace. Posibles ubicaciones:

| Posible Ubicación | Probabilidad | Acción |
|---|---|---|
| Git history (commit previo a recertificación) | ALTA | `git log --diff-filter=D -- '01_Raw/PARIS/Facturacion/*.xml'` |
| Snapshots V2-V6 | MEDIA | Revisar `data/db/snapshot_*` |
| Eliminados permanentemente (rm + commit) | BAJA | Irrecuperable |
| Movidos a otra ubicación | MEDIA | Buscar en `01_Raw/RIPLEY/` y subdirectorios |

---

## 7. Roadmap & Timeline

### Fase 1: PARIS Quick Win (PW1)
**Semana 1** | **~$28.2M adicionales**

```
Día 1-2:  Extraer folios XML y buscar en Excel columns
Día 3-4:  Implementar bridge para folios encontrados
Día 5:    Bridge INDIRECTO para folios sin match Excel
Día 6:    Verificación 10 muestras, documentación
Día 7:    Ejecución en LIVE DB + pipeline_log
```

### Fase 2: ML Normalization (PW2)
**Semanas 2-3** | **~$307M potencial**

```
Semana 2:
  Día 1-2:  Extraer los 762 folios DTE ML, indexar
  Día 3-4:  Analizar los 3 Excel fuente → identificar columna folio
  Día 5:    Mapeo por columna Excel → Ledger

Semana 3:
  Día 1-2:  Filas sin match: investigar concepto vs DTE
  Día 3:    Bridge alternativo (por id_orden/comisión)
  Día 4:    Verificación 20 muestras
  Día 5:    Ejecución + documentación
```

### Fase 3: RIPLEY Indirect Bridge (PW3)
**Semanas 4-7** | **~$25.5M (sin XMLs 2025) / ~$168M (con XMLs 2025)**

```
Semana 4:
  Día 1-3:  Búsqueda de XMLs 2025 en git history + snapshots
  Día 4-5:  Si encontrados → extraer y catalogar; si no → continuar con 100 XMLs

Semana 5:
  Día 1-2:  Parsear NmbItem de 100 XMLs → extraer períodos
  Día 3-4:  Implementar match por período para Comisiones + Despachos
  Día 5:    Implementar match por SKU para FBR Productos

Semana 6:
  Día 1-2:  Implementar match por tipo de costo (logística, almacenamiento)
  Día 3-4:  Bridge para XMLs 2025 (si recuperados)
  Día 5:    Verificación 20 muestras

Semana 7:
  Día 1-2:  Correcciones post-verificación
  Día 3:    Ejecución en LIVE DB
  Día 4-5:  Documentación + pipeline_log
```

### Fase 4: FALABELLA Completion (PW4)
**Semana 7 (paralelo)** | **~$3.5M**

```
Día 1:  Bridge DIRECTA con 4 XMLs + Excel
Día 2:  Verificación 100% filas
Día 3:  Ejecución + documentación
```

### Proyección de Cobertura por Fase

| Fase | Filas con folio_xml | % Cobertura | $ Acumulado |
|---|---|---|---|
| **Hoy** | 125,002 | 30.2% | $846.6M (56.1%) |
| **+PW1** | 133,921 | 32.3% | $912.3M (60.5%) |
| **+PW2** | 144,710 | 34.9% | $1,219.3M (80.9%) |
| **+PW3 (sin XMLs 2025)** | 269,638 | 65.1% | $1,244.8M (82.6%) |
| **+PW3 (con XMLs 2025)** | ~350,000 | ~84.5% | ~$1,430M (~94.9%) |
| **+PW4** | 270,026 | 65.2% (sin 2025) / ~350,400 (84.6% con 2025) | $1,248.3M (82.8%) / ~$1,434M (95.1%) |

### Trust Score Proyectado

| Escenario | Trust Score | Audit Readiness |
|---|---|---|
| **Hoy** | ~84/100 | 62/100 |
| **PW1+PW2+PW4** | ~87/100 | ~68/100 |
| **+PW3 (sin XMLs 2025)** | ~88/100 | ~70/100 |
| **+PW3 (con XMLs 2025)** | ~93/100 | ~82/100 |

---

## 8. Governance & Approval Gates

### Gate 1: Aprobación de Plan (T2)
- **Trigger**: Entrega de este documento
- **Criterio**: Revisión por stakeholder técnico
- **Acción**: Firma de aprobación → iniciar PW1

### Gate 2: PARIS Listo
- **Trigger**: PW1 completado
- **Criterio**: 22/22 folios vinculados o documentados como no-vinculables
- **Acción**: Ejecutar en LIVE DB

### Gate 3: ML Listo
- **Trigger**: PW2 completado
- **Criterio**: 10,789/10,789 filas con folio o documentadas como SIN XML
- **Acción**: Ejecutar en LIVE DB

### Gate 4: RIPLEY Listo
- **Trigger**: PW3 completado
- **Criterio**: Máximo posible de filas vinculadas, 0 falsos positivos
- **Acción**: Ejecutar en LIVE DB

### Gate 5: Certificación Post-Ejecución
- **Trigger**: Todos los PW ejecutados
- **Criterio**: 14/14 contractos intactos, cobertura verificada
- **Acción**: Trust Certification V3

---

## Appendix A: Metodología de Bridge

### DIRECTA (PARIS, FALABELLA existente)
```
XML.Folio → Excel.columna_folio → Excel.numero_orden → Ledger.id_orden → Ledger.rows
```
- Precisión: 100% (string exact match)
- Verificación: set intersection, 10 muestras aleatorias

### INDIRECTA - Período (RIPLEY Comisiones)
```
XML.NmbItem → período [fecha_inicio, fecha_fin] → Ledger.fecha ∈ [inicio, fin] → SUM(ledger.monto) ≈ XML.MntTotal → Ledger.rows
```
- Precisión: >99% (match por suma agregada)
- Tolerancia: 1% de diferencia entre suma ledger y monto XML

### INDIRECTA - SKU (RIPLEY FBR Productos)
```
XML.NmbItem → SKU (FBR XXXXXXXXXX) → Ledger.id_producto = SKU → Ledger.rows
```
- Precisión: 100% (SKU exact match)

## Appendix B: Costo Estimado

| Recurso | PW1 | PW2 | PW3 | PW4 | Total |
|---|---|---|---|---|---|
| Developer-días | 3 | 8 | 16 | 1 | 28 |
| Developer costo | $900 | $2,400 | $4,800 | $300 | $8,400 |
| Revisión QA (días) | 1 | 2 | 3 | 0.5 | 6.5 |
| QA costo | $300 | $600 | $900 | $150 | $1,950 |
| **Total estimado** | **$1,200** | **$3,000** | **$5,700** | **$450** | **$10,350** |

## Appendix C: Post-Execution Metrics

| Marketplace | Filas totales | Con folio | % | Sin folio | $ Con folio | $ Sin folio | % $ |
|---|---|---|---|---|---|---|---|
| **ML** | 101,603 | 101,603 | 100.0% | 0 | $842.3M | $0M | 100.0% |
| **PARIS** | 42,487 | 42,487 | 100.0% | 0 | $378.1M | $0M | 100.0% |
| **RIPLEY (sin 2025)** | 269,216 | 25,519 | 9.5% | 243,697 | $25.5M | $259.4M | 8.9% |
| **RIPLEY (con 2025)** | 269,216 | 134,608 | 50.0% | 134,608 | $142.4M | $142.4M | 50.0% |
| **FALABELLA** | 1,008 | 1,008 | 100.0% | 0 | $2.6M | $0M | 100.0% |
| **GLOBAL (sin 2025)** | 414,314 | 270,617 | 65.3% | 243,697 | $1,248.5M | $259.4M | 82.8% |
| **GLOBAL (con 2025)** | 414,314 | 379,706 | 91.6% | 134,608 | $1,365.4M | $142.4M | 90.6% |

---

**Documento diseñado por:** Programa T2 — XML Traceability Execution Plan
**Régimen:** DISEÑO — Requiere aprobación del Gate 1 antes de implementación
**Próximo paso:** Revisión y aprobación por stakeholder técnico
