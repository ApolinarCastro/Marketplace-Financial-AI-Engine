# P32R10 — EXEC SUMMARY PROFILE

## Pre-Fix (2026-06-19)

`/api/v4/exec/summary` ejecutaba en **16–23 segundos** para cualquier marketplace/período.

## Root Cause

### 1. `DocumentGapEngine.get_risk_summary()` — 19.5s (99.9% del tiempo)

El método `get_risk_summary()` llamaba a `self.get_document_gaps(marketplace, periodo, limit=1000)`, el cual:

1. Ejecutaba **1 consulta SQL** → rápida (~5ms)
2. Leía **todos los archivos Excel de FALABELLA** (`01_Raw/Falabella/Órdenes y Transacciones/*.xlsx`) mediante `glob` + `pd.read_excel`
3. Leía **todos los archivos Excel de RIPLEY SELLER** (`01_Raw/Ripley/SELLER/*.xlsx`)
4. Leía **todos los archivos CSV de RIPLEY CICLOS** (`01_Raw/Ripley/Ciclos/*.csv`)

Esto ocurría en **CADA** llamada a `exec/summary`, sin caché ni optimización.

### 2. Per-MP Loop en `get_executive_breakdown()` — ~40ms

El loop sobre 4 marketplaces ejecutaba **8 consultas SQL** (2 por MP) donde **1 consulta GROUP BY** era suficiente.

### 3. Path de Taxonomía Incorrecto

`_build_signal_filter()` y `query_ledger()` buscaban archivos JSON en `knowledge/taxonomy/` (ruta inexistente), causando que el filtrado SIGNAL/NOISE de RIPLEY estuviera **silenciosamente deshabilitado** desde Phase 13.

### 4. Duplicación de Certificaciones

`get_coverage_summary()` para ALL llamaba `get_all_certifications()` (4 queries SQL).
`get_risk_summary()` también llamaba `get_all_certifications()` (4 queries SQL duplicadas).

## Fixes Aplicados

| Fix | Archivo | Impacto |
|-----|---------|---------|
| Reemplazar file I/O con SQL-only en `get_risk_summary()` | `document_gap_engine.py` | **19.5s → 27ms** |
| Reemplazar per-MP loop con GROUP BY | `financial_engine.py` | 40ms → 5ms |
| Cachear JSON de taxonomía | `financial_engine.py` | 5+ lecturas → 1 lectura |
| Eliminar certificaciones duplicadas | `api.py` | 8 queries → 0 queries |
| Corregir path de taxonomías | `financial_engine.py` | Restaura signal filtering |

## Post-Fix

`/api/v4/exec/summary` ejecuta en **~24ms** — **99.9% de mejora**.
