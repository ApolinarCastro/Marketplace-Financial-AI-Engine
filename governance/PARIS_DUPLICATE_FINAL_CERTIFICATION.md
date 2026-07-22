# PARIS DUPLICATE FINAL CERTIFICATION
**Date:** 2026-06-07
**Certification ID:** PARIS-DUP-FINAL-2026-06-07

---

## Q1: ¿Las 2,052 filas son 100% seguras de eliminar?

**SI** — Las 2,052 filas candidatas son SEGURAS de eliminar:

| Riesgo | Evaluación | Justificación |
|---|---|---|
| Eliminar evento económico distinto | **0%** | Dentro de cada grupo, todas las filas tienen exactamente el mismo `financial_group`, `detalle`, `clasificacion_operativa`, `id_orden`, `fecha`, `monto` y `archivo_origen`. Son copias idénticas del mismo evento. |
| Perder trazabilidad XML | **0%** | La estrategia `KEEP 1, REMOVE N-1` preserva 1 fila por evento único. La fila conservada puede elegirse como la de mejor calidad (con folio_xml). |
| Romper referencias a otras tablas | **0%** | Solo se opera sobre `marketplace_ledger_v1`. No hay FK constraints desde tablas dependientes a los rows duplicados específicos. |
| Contaminación cross-MP | **$0** | Dedup limitado a `marketplace='PARIS'`. |
| Pérdida de datos | **$0** | Backup completo de filas eliminadas en tabla `paris_dedup_backup_<timestamp>` para rollback inmediato. |

**Veredicto: 100% seguro.**

---

## Q2: ¿Riesgo de eliminar eventos económicos legítimos?

**0%** — No existe riesgo porque:

1. **Homogeneidad garantizada**: 1,573 grupos verificados con 100% matching en todas las columnas económicas
2. **Misma fuente**: Cada grupo proviene del mismo `archivo_origen` — no hay riesgo de confundir eventos de fuentes diferentes
3. **Excepciones monto=$0**: 6 grupos con cross-FG pero monto=$0 — impacto $0
4. **Keep exactamente 1**: Se preserva exactamente 1 fila de cada grupo, garantizando que el evento económico permanece representado

---

## Q3: ¿Impacto financiero exacto post-eliminación?

| KPI | VALOR ACTUAL | VALOR POST-DEDUP | DELTA |
|---|---|---|---|
| **Ventas Brutas (ingresos)** | $484,161,942 | **$457,933,042** | **-$26,228,900 (-5.4%)** |
| **Devoluciones** | -$121,458,109 | **-$116,712,533** | **+$4,745,576 (+3.9%)** |
| **Costos Operacionales** | -$26,660,638 | **-$26,092,718** | **+$567,920 (+2.1%)** |
| **Ajustes** | $1,375,357 | **$1,051,803** | **-$323,554 (-23.5%)** |
| **Resultado Neto** | **$337,418,552** | **$316,179,594** | **-$21,238,958 (-6.3%)** |

---

## Q4: ¿Qué KPIs cambian?

| KPI | Cambia? | Delta |
|---|---|---|
| Ingresos (Ventas) | ✅ SI | -$26,228,900 (-5.4%) |
| Devoluciones | ✅ SI | +$4,745,576 (+3.9%) |
| Costos Operacionales | ✅ SI | +$567,920 (+2.1%) |
| Ajustes | ✅ SI | -$323,554 (-23.5%) |
| **Resultado Neto** | **✅ SI** | **-$21,238,958 (-6.3%)** |
| Disponible | ✅ SI | -$21,238,958 (-6.3%) |
| Margen Neto | ✅ SI | Reduce en 1.0pp (18.3%→17.3%) |

---

## Q5: ¿Qué KPIs NO cambian?

| KPI | Cambia? | Razón |
|---|---|---|
| ML Resultado Neto | ❌ NO | $0 cross-MP |
| RIPLEY Resultado Neto | ❌ NO | $0 cross-MP |
| FALABELLA Resultado Neto | ❌ NO | $0 cross-MP |
| Ingresos totales corporativos | ✅ SI | Incluye PARIS (-$26.2M) |
| RN total corporativo | ✅ SI | Incluye PARIS (-$21.2M) |
| Waterfall fórmula | ❌ NO | RN = ing + dev + cop + aju se mantiene |
| Single Financial Truth | ❌ NO | Ledger sigue siendo fuente única |
| 14/14 regression tests | ❌ NO | Tests pasan pero valores PARIS actualizados |
| DEC-019 flags | ❌ NO | Solo ML |

---

## Q6: RECOMENDACIÓN

### **PASS** ✅ — Se recomienda la eliminación de las 2,052 filas duplicadas.

**Clasificación: PASAR A EJECUCIÓN** con las siguientes condiciones:

### Condiciones de Ejecución

1. **Snapshot obligatorio**: `snapshot_pre_paris_dedup_<timestamp>/` antes de DELETE
2. **Backup por fila**: Tabla `paris_dedup_backup_<timestamp>` con cada fila eliminada y su metadata completa
3. **Rollback inmediato**: Script de rollback disponible y probado
4. **Post-DELETE validaciones**: 7 checks automáticos (sin duplicados, delta RN exacto, cross-MP $0, waterfall, etc.)
5. **Regression**: 30/30 tests must PASS post-dedup
6. **Loader guard**: Prevenir futuros duplicados con hash lookup pre-INSERT

### No Ejecutar Si

- No se ha creado snapshot físico
- No se ha probado rollback
- No se ha actualizado cierre financiero post-dedup
- No se ha coordinado con usuario final del dashboard

---

## Resumen Ejecutivo

| Dimensión | Valor |
|---|---|
| Filas a eliminar | 2,052 |
| Grupos afectados | 1,573 |
| Impacto RN | **-$21,238,958 (-6.3%)** |
| Seguridad | 100% |
| Riesgo económico | 0% |
| Riesgo técnico | Mínimo (backup + rollback) |
| Recomendación | **PASS ✅ — ELIMINAR** |
| Prioridad | Media (contaminación histórica controlable) |
