# PARIS June 2026 — Ledger Date Certification

**Fecha:** 2026-06-11
**Auditoría:** FASE 1 de 6 — PARIS Forensic Reconciliation V2
**Fuente:** `marketplace_ledger_v1` (DuckDB, solo hechos demostrables)

---

## 1. Fechas con Registros en Ledger (PARIS, Junio 2026)

| Fecha | Filas | Ingresos | Devoluciones | Costos Op. | Monto Total |
|-------|-------|---------|-------------|------------|-------------|
| 2026-06-01 | 207 | $5,043,304 | -$103,288 | -$11,760 | **$4,928,256** |
| 2026-06-02 | 240 | $4,973,632 | -$104,952 | -$131,520 | **$4,737,160** |
| 2026-06-03 | 263 | $4,571,952 | -$52,064 | -$195,610 | **$4,324,278** |
| 2026-06-04 | 301 | $4,040,304 | -$180,056 | -$345,210 | **$3,515,038** |
| 2026-06-05 | 79 | $389,680 | -$86,496 | -$149,770 | **$153,414** |
| 2026-06-06 | 0 | — | — | — | **$0** |
| 2026-06-07 | 0 | — | — | — | **$0** |
| 2026-06-08 | 0 | — | — | — | **$0** |

## 2. Fechas Verificadas

- **Primera fecha**: 2026-06-01 ✅
- **Última fecha**: **2026-06-05** ✅
- **Junio 6, 7, 8**: **SIN REGISTROS** ❌

## 3. Respuesta

**¿Cuál es la última fecha real existente?**

**2026-06-05.** El ledger contiene exactamente 5 fechas (Jun 1-5). No existen registros para Jun 6, 7, ni 8 en `marketplace_ledger_v1`.

La fecha 2026-06-05 tiene solo 79 filas ($153,414), significativamente menos que los días anteriores (207-301 filas), indicando que el loader cargó solo una fracción de ese día.
