# PARIS June 2026 — File Inventory

**Fecha:** 2026-06-11
**Auditoría:** FASE 1 de 7 — PARIS June 2026 Data Completeness Certification
**Método:** Revisión física de `01_Raw/PARIS/Transacciones/Dropshipping/` y `01_Raw/PARIS/Transacciones/Fulfillment/`

---

## 1. Dropshipping — Archivos Existentes

| Archivo | Tamaño | Modificado | Período | Filas |
|---------|--------|-----------|---------|-------|
| `01-2025.xlsx` | 177 KB | 2026-05-30 | Ene 2025 | ~1,318 |
| `02-2025.xlsx` | 143 KB | 2026-05-30 | Feb 2025 | ~1,061 |
| `03-2025.xlsx` | 90 KB | 2026-05-30 | Mar 2025 | ~643 |
| `04-2025.xlsx` | 258 KB | 2026-05-30 | Abr 2025 | ~1,405 |
| `05-2025.xlsx` | 112 KB | 2026-05-30 | May 2025 | ~795 |
| `06-2025.xlsx` | 271 KB | 2026-05-30 | Jun 2025 | ~2,056 |
| `07-2025.xlsx` | 265 KB | 2026-05-30 | Jul 2025 | ~2,033 |
| `08-2025.xlsx` | 264 KB | 2026-05-30 | Ago 2025 | ~2,019 |
| `09-2025.xlsx` | 198 KB | 2026-05-30 | Sep 2025 | ~1,461 |
| `10-2025.xlsx` | 400 KB | 2026-05-30 | Oct 2025 | ~3,042 |
| `11-2025.xlsx` | 247 KB | 2026-05-30 | Nov 2025 | ~1,848 |
| `12-2025.xlsx` | 422 KB | 2026-05-30 | Dic 2025 | ~3,222 |
| `01-2026.xlsx` | 197 KB | 2026-05-30 | Ene 2026 | ~1,436 |
| `02-2026.xlsx` | 132 KB | 2026-05-30 | Feb 2026 | ~940 |
| `03-2026.xlsx` | 198 KB | 2026-05-30 | Mar 2026 | ~1,477 |
| `04-2026.xlsx` | 330 KB | 2026-05-30 | Abr 2026 | ~1,876 |
| `05-2026.xlsx` | 185 KB | 2026-06-05 | May 2026 | ~1,277 |
| **`1 jun 2026 - 8 jun 2026.xlsx`** | **187 KB** | **2026-06-09** | **1-8 Jun 2026** | **1,329** |

## 2. Fulfillment — Archivos Existentes

| Archivo | Tamaño | Modificado | Período | Filas |
|---------|--------|-----------|---------|-------|
| `1 ene 2025 - 31 dic 2025.xlsx` | 1,836 KB | 2026-05-30 | Ene-Dic 2025 | ~14,740 |
| `1 ene 2026 - 30 abr 2026.xlsx` | 232 KB | 2026-05-30 | Ene-Abr 2026 | ~1,768 |
| `1 may 2026 - 31 may 2026.xlsx` | 39 KB | 2026-06-05 | May 2026 | ~235 |
| **`1 jun 2026 - 8 jun 2026.xlsx`** | **21 KB** | **2026-06-09** | **1-8 Jun 2026** | **109** |

## 3. Archivos Cargados al Ledger vs Archivos Reales

El ledger fue cargado desde:
- `06-06-2026.xlsx` → **NO EXISTE en disco** (renombrado a `1 jun 2026 - 8 jun 2026.xlsx`)
- `1 jun 2026 - 5 jun 2026.xlsx` → **NO EXISTE en disco** (fusionado en `1 jun 2026 - 8 jun 2026.xlsx`)

## 4. Hallazgos

- **Solo 2 archivos** cubren Junio 2026: Dropshipping (1,329 filas) + Fulfillment (109 filas) = 1,438 filas total
- **Período: SOLO 1 al 8 de Junio** (8 de 30 días = 27% del mes)
- **No existe archivo** para Junio 9-30 (22 días sin datos)
- **Archivos originales del loader** (`06-06-2026.xlsx`, `1 jun 2026 - 5 jun 2026.xlsx`) renombrados/fusionados — inconsistencia de trazabilidad
- **Patrón histórico**: Todos los meses anteriores tienen archivos completos de mes completo. Junio rompe el patrón.
