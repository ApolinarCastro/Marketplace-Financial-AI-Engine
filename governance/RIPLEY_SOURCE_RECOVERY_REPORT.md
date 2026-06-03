# RIPLEY SOURCE RECOVERY REPORT — SPRINT A5.1

**Date:** 2026-05-30
**Mode:** FORENSE (READ ONLY)
**Status:** COMPLETED

---

## Executive Summary

**Veredicto: NO EXISTE EVIDENCIA de archivos XLSX históricos con formato de 37 columnas financieras.**

Los archivos XLSX que originaron las 269,216 filas / $284.9M de RIPLEY en la DB no existen en ningún disco accesible. Se encontraron archivos XLSX de RIPLEY en `Conciliación\`, pero corresponden a un esquema de conciliación (16 columnas) y NO al formato de 37 columnas financieras que espera el ETL.

---

## FASE 1 — Búsqueda Ampliada

| Location | RIPLEY XLSX (37-col)? | RIPLEY XLSX (other)? | Files Found |
|---|---|---|---|
| `Marketplace_Conciliacion\` | ❌ Ruta no existe | ❌ | 0 |
| `Conciliación\Ripley 2024\` | ❌ | ✅ 12 reconciliación (16-col), 10 MB total | 22 |
| `Conciliación\Ripley 2025\` | ❌ | ✅ 10 reconciliación (16-col) + Base Pagos, 105 MB total | 85 |
| `01_Raw/RIPLEY/` | ❌ Solo CSV + XML | ❌ | 0 |
| `RIPLEY.zip` | ❌ Solo CSV + XML dentro | ❌ | 0 |
| `data/raw/ripley/` | ❌ Directorio vacío | ❌ | 0 |
| `Desktop\` | ❌ No encontrado | ❌ | 0 |
| `Backup Apps\Marketplace Financial AI Engine - Backup\` | ❌ | ❌ | 0 |
| `Proyectos\Conciliacion_Meli_RTU\01_Raw\` | ❌ Solo ML/PARIS | ❌ | 0 |

### Archivos XLSX Encontrados (RIPLEY — Formato Reconciliación 16-columnas)

**2024** (12 mensuales + 1 Resumen):
```
Conciliación\Año 2024\Ripley 2024\{Mes}\Ripley {Mes} 2024.xlsx
  Columnas: Fecha Ripley, Numero de Orden, Numero de factura, Tipo Ripley,
            Valor Ripley, Fecha Sap, Orden de Venta, Numerador, Prefijo,
            Tipo Sap, Valor SAP, Total Sin Despacho, Despacho,
            Saldo Pendiente, Saldo Conciliación, Detalle Conciliación
```

**2025** (10 mensuales + 2 Resumen + Base Pagos):
```
  Ripley {Mes} 2025.xlsx          (mismas 16 columnas de conciliación)
  Base Pagos Efectuados Ripley.xlsx  (SAP payments — 19 cols)
  Base Pagos Recibidos Ripley.xlsx   (SAP receipts — 19 cols)
  Conciliación.xlsx / Ripley Resumen.xlsx  (12 MB - consolidated)
```

**Conclusión FASE 1:** Los archivos XLSX de 37 columnas que espera el ETL **NO EXISTEN** en ninguna de las ubicaciones inspeccionadas.

---

## FASE 2 — Búsqueda por Firma (37 Columnas Financieras)

### Firma Buscada (de `surgical_loader.py` y `FORENSE_RIPLEY_MATRIZ.md`):
```
- NÚMERO DOCUMENTO LIQUIDACIÓN / NUMERO DOCUMENTO LIQUIDACION
- ORDEN DE COMPRA
- FECHA OC
- Shop ID
- Tienda
- A pagar, Comisión, Logística, Descuento, Comisión IVA, etc. (~29 columnas de montos)
```

### Resultado: NO ENCONTRADO

Ningún archivo XLSX en `C:\Users\ASUS Zenbook\Documents\` contiene estas columnas. Se inspeccionaron >1000 archivos XLSX en todo el árbol de Documents.

**Conclusión FASE 2:** Los archivos con firma de 37 columnas no existen en disco.

---

## FASE 3 — Power Query Trace

| File Type | Search Result |
|---|---|
| `*.pbix` | ❌ No encontrado en todo `C:\Users\ASUS Zenbook\Documents\` |
| `*.pbit` | ❌ No encontrado |
| `*.pq` | ❌ No encontrado |
| `*.m` | ❌ No encontrado (solo archivos Python que generan código M) |

**Nota:** Existen 7 generadores de código M en Python en `Reporte_Marketplaces\Backup\`, incluyendo `generate_m_code_final_ripley_fix.py`. Estos generan código Power Query para procesar CSVs de Mirakl, pero **nunca se implementaron en el pipeline activo**. No hay evidencia de que este código M se haya ejecutado alguna vez.

**Conclusión FASE 3:** No existen archivos nativos de Power Query (.pbix, .pq, .m). La ruta Power Query fue diseñada pero no implementada.

---

## FASE 4 — ETL Evidence (CSV → XLSX Transform)

### Ruta de Transformación Conocida

```
Mirakl Platform (web)
    → CSV exports (47 files, 43 cols, order-level)
    → ??? (transformación desconocida)
    → XLSX files (37 cols, financial-period-level)  ← LOST
    → surgical_loader.py (pandas.melt)
    → marketplace_ledger_v1 (DB)
```

### ¿Existe algún artefacto que explique CSV → XLSX?

| Evidence | Status | Classification |
|---|---|---|
| Script Python de transformación | ❌ NO ENCONTRADO | No existe |
| Script PowerShell/BAT | ❌ NO ENCONTRADO | No existe |
| Configuración de Power Query | ✅ Diseñado pero no implementado | PROBABLE (intención documentada) |
| Macro de Excel | ❌ NO ENCONTRADO | No existe |
| Documentación del proceso | ✅ `Especificación del Proceso ETL...md` describe la arquitectura (no el detalle) | PROBABLE (concepto documentado) |
| `_transform.py` en Backup Apps | ❌ Archivo ausente / vacío | No existe |
| `ripley_scraper.py` | ❌ Scraper web, no transformador | No existe |
| Proceso manual en Excel | ❌ No hay evidencia directa | PROBABLE (más plausible) |

### Conclusión FASE 4 — Clasificación

| Categoría | Artefactos |
|---|---|
| **DEMOSTRADO** | Melt algorithm (`surgical_loader.py:388`), 29 column names inventory (`FORENSE_RIPLEY_MATRIZ.md`), Power Query M code generator (`generate_m_code_final_ripley_fix.py`), ETL spec (`Especificación del Proceso ETL...md`) |
| **PROBABLE** | CSV → XLSX fue un proceso manual en Excel (copy-paste desde Mirakl CSVs a plantilla xlsx con 37 columnas). El M code documenta la intención de automatizar esto en Power Query. |
| **NO ENCONTRADO** | Los XLSX originales de 37 columnas, el script/fórmula que los genera, archivos .pbix/.pq/.m ejecutables |

---

## FASE 5 — Recoverability

### ¿Los XLSX históricos existen?

| Respuesta | Confianza |
|---|---|
| **NO EXISTE EVIDENCIA** | 95% |

### Análisis de Confianza

| Factor | Peso | Assessment |
|---|---|---|
| Búsqueda en disco (Documents, Desktop) | Alta | Cero hits para 37-col signature |
| Búsqueda en git (baseline_v6) | Alta | Cero xlsx en historial |
| Ruta `Marketplace_Conciliacion\` | Alta | Ruta no existe |
| Legacy loaders ref path | Alta | `data_loader_v3.py/v4.py` ref `Marketplace_Conciliacion/01_Raw/RIPLEY/Ripley/` — no existe |
| ZIP (`RIPLEY.zip`, 2MB) | Media | Solo CSV+XML dentro |
| `data/raw/ripley/` | Media | Directorio vacío |
| Backups externos (Backup Apps) | Media | Sin evidencia |
| Posibilidad de otro disco/USB | Baja | No evaluable — no hay evidencia |

### ¿Por qué no existen?

La hipótesis más probable:

1. Los XLSX (37-columnas) fueron creados **manualmente en Excel** desde los CSVs exportados de Mirakl
2. Estos XLSX residían en `C:\Users\ASUS Zenbook\Documents\Marketplace_Conciliacion\01_Raw\RIPLEY\Ripley\`
3. El proyecto `Marketplace_Conciliacion` fue **eliminado o movido** (posiblemente renombrado a la carpeta `Conciliación\` que existe hoy)
4. Al renombrar/mover, los XLSX financieros (37-col) fueron **reemplazados** por los de conciliación (16-col) que existen actualmente
5. La DB DuckDB (`meli_financial_v4.db`) conserva los datos transformados originales, pero la fuente XLSX se perdió en el proceso

### Recuperabilidad

| Activo | Estado |
|---|---|
| Datos DB (269,216 rows, $284.9M) | ✅ INTACTO en `meli_financial_v4.db` y snapshots V6 |
| Algoritmo ETL (melt) | ✅ Recuperado de `surgical_loader.py:351-418` |
| Columnas originales (nombres) | ✅ Documentado en `FORENSE_RIPLEY_MATRIZ.md` |
| XLSX fuente (37-col per-period) | ❌ PERDIDO — no existe en disco |
| CSV raw (47 files, 43-col order-level) | ✅ EXISTE en `01_Raw/RIPLEY/Archivos de pedido/` |
| XML DTE (100 files) | ✅ EXISTE en `01_Raw/RIPLEY/Documentos Recepcionados/` |
| Transformación CSV → XLSX (script) | ❌ PERDIDO — nunca existió como script |
| Power Query M code (automatización) | ✅ DISEÑADO pero no implementado |

---

## Recomendación

Para restaurar la capacidad de reproducir RIPLEY:

1. **Aceptar pérdida**: Los XLSX de 37 columnas no se recuperarán del disco actual
2. **Construir nuevo ETL** que procese los 47 CSVs (Mirakl order-level) directamente, implementando el diseño Power Query documentado en `generate_m_code_final_ripley_fix.py`
3. **Alternativa**: Extraer datos directamente de la API de Mirakl para evitar el paso CSV intermedio

---

*Fin del reporte. SPRINT A5.1 COMPLETED — NO EXISTE EVIDENCIA.*
