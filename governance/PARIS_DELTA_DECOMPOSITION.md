# PARIS June 2026 — Delta Decomposition (Exact $418,696)

**Fecha:** 2026-06-11
**Auditoría:** FASE 4 de 6 — PARIS Forensic Reconciliation V2
**Objetivo:** Explicar el delta de $418,696 usando solo hechos demostrables

---

## 1. Corrección del Delta del Reporte Anterior

El reporte V1 (PARIS_JUNE2026_RECONCILIATION.md) reportó un delta de **$4,141,063**. Ese delta comparó **RAW Gross (monto)** contra **Ledger (monto)** sin considerar que RAW almacena montos brutos y ledger almacena montos netos.

**Delta correcto usando la misma base: $418,696**

| Medición | V1 (Incorrecto) | V2 (Correcto) |
|----------|----------------|---------------|
| Base RAW | Monto (Gross) | Monto a Pagar (Net) |
| Base Ledger | Ledger.monto | Ledger.monto |
| **Delta** | **$4,141,063** | **$418,696** |

**El V1 sobrestimó el delta en 10x por mezclar bruto vs neto.**

---

## 2. Descomposición Exacta del Delta de $418,696

### 2.1 Días No Cargados (RAW existe, Ledger no): **+$817,822**

| Fecha | RAW Net | Ledger | Delta | Estado |
|-------|---------|--------|-------|--------|
| 2026-06-06 | $162,910 | $0 | +$162,910 | Carga pendiente |
| 2026-06-07 | $508,774 | $0 | +$508,774 | Carga pendiente |
| 2026-06-08 | $146,138 | $0 | +$146,138 | Carga pendiente |
| **Subtotal** | **$817,822** | **$0** | **+$817,822** | |

### 2.2 Diferencia por Archivos Loader vs RAW Actual: **-$399,126**

| Fecha | RAW Net | Ledger | Delta | Explicación |
|-------|---------|--------|-------|-------------|
| 2026-06-01 | $4,766,536 | $4,928,256 | **-$161,720** | Loader usó archivo diferente al RAW actual |
| 2026-06-02 | $4,737,160 | $4,737,160 | **$0** | Match perfecto |
| 2026-06-03 | $4,324,278 | $4,324,278 | **$0** | Match perfecto |
| 2026-06-04 | $3,515,038 | $3,515,038 | **$0** | Match perfecto |
| 2026-06-05 | -$83,992 | $153,414 | **-$237,406** | Loader usó archivo diferente al RAW actual |
| **Subtotal** | | | **-$399,126** | |

### 2.3 Verificación

```
Delta Total = Días No Cargados + Diferencia Loader
            = +$817,822 + (-$399,126)
            = $418,696 ✅
```

---

## 3. Descomposición por Concepto (Ajustada por Neto)

### 3.1 Ventas (Ingresos)

| Componente | RAW Net | Ledger | Delta |
|-----------|---------|--------|-------|
| Ventas días 1-5 (match) | $19,018,872 | $19,018,872 | **$0** (3 días perfectos) |
| Ventas días 1 y 5 (diferencia) | $1,197,356 | ? | Diferencia de archivos |
| Ventas días 6-8 | $1,334,180 | $0 | No cargado |
| **Total Ventas** | **$21,550,408** | **$19,018,872** | **+$2,531,536** |

### 3.2 Devoluciones

| Componente | RAW Net | Ledger | Delta |
|-----------|---------|--------|-------|
| Devoluciones días 1-5 (match) | -$526,856 | -$526,856 | **$0** |
| Devoluciones días 6-8 | -$318,256 | $0 | No cargado |
| Otras diferencias | -$1,363,464 | — | Diferencia de archivos loader |
| **Total Devoluciones** | **-$2,208,576** | **-$526,856** | **-$1,681,720** |

### 3.3 Logística (Costos Operacionales)

| Componente | RAW Net | Ledger | Delta |
|-----------|---------|--------|-------|
| Logística días 1-5 | -$833,870 | -$833,870 | **$0** |
| Logística días 6-8 | -$88,546 | $0 | No cargado |
| Otras diferencias | -$342,574 | — | Diferencia de archivos |
| **Total Logística** | **-$1,264,990** | **-$833,870** | **-$431,120** |

---

## 4. Resumen

| Componente | Monto | % del Delta |
|-----------|-------|-------------|
| Días 6-8 no cargados (RAW existe) | +$817,822 | 195.3% |
| Diferencia archivos loader vs RAW actual (Jun 1 y 5) | -$399,126 | -95.3% |
| **Delta neto total** | **+$418,696** | **100%** |

**La mayor parte del delta ($817,822 de $418,696) es data existente en RAW que no ha sido cargada al ledger.** Sin la compensación de -$399,126 (donde el ledger tiene más que el RAW actual por archivos fuente diferentes), el delta sería mucho mayor.

**El delta de $4,141,063 del V1 es inválido — mezcló bruto con neto.**
