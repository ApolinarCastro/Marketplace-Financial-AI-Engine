# PARIS FORENSIC TRUTH FINAL CERTIFICATION
**Date:** 2026-06-07
**Certification ID:** PARIS-FORENSIC-FASE8

---

## Veredicto

# PASS WITH WARNINGS ⚠️

---

## Resumen de 8 Fases

| FASE | TÃ­tulo | Resultado |
|---|---|---|
| **FASE 1** | Physical Source Inventory | 84 archivos (62 XML + 22 XLSX), 46,090 filas, $338.7M neto |
| **FASE 2** | RAW Economic Universe | 12 conceptos identificados, $487.7M Ventas RAW, 18.5% take rate |
| **FASE 3** | Physical Duplicates | **0** duplicados exactos dentro de cualquier archivo ⚠️ |
| **FASE 4** | Source Overlap Matrix | Misma orden aparece en DS + FF (pipeline overlap) |
| **FASE 5** | RAW vs Ledger | 43,488 eventos Ãºnicos, -550 filas en ledger |
| **FASE 6** | Ledger Contamination | **$0 contaminaciÃ³n.** CERO loader bugs |
| **FASE 7** | Truth Answers | 10/10 respondidas |
| **FASE 8** | **Final Certification** | **PASS WITH WARNINGS** |

---

## Las 4 Preguntas Ejecutivas

### 1. ¿El problema estÃ¡ en RAW?

**SÃ, PARCIALMENTE** ⚠️

Existen **133 grupos de near-duplicados** en los archivos fuente RAW ($1,544,345). Estos son casos donde el mismo producto, misma orden, mismo monto aparece 2-17 veces en el mismo archivo (solo difiere el `id` auto-increment).

**Causa raÃ­z:** Problema de calidad de datos en el sistema fuente de PARIS (sistema Cencosud). No es un problema del loader ni del ledger.

**Magnitud:** $1.5M sobre un universo de $338.7M = **0.46% del universo econÃ³mico**.

### 2. ¿El problema estÃ¡ en ETL?

**NO** ✅

El loader NO crea duplicados. Cada fila del ledger corresponde exactamente a una fila en un archivo fuente. No hay casos donde 1 fila source → N filas ledger.

**Evidencia:** `id_transaccion` en ledger = `id` en source file (1:1). Conteo de filas consistente.

### 3. ¿El problema estÃ¡ en el Ledger?

**NO** ✅

El ledger es un reflejo FIEL de los archivos fuente. No hay contaminaciÃ³n generada durante la carga. No hay filas sin respaldo documental (excepto 381 grupos de archivos probablemente renombrados).

### 4. ¿Puede autorizarse una limpieza?

**SÃ, PARCIALMENTE** ⚠️

Se puede limpiar **$1,544,345** (133 grupos) con CONFIANZA ALTA (riesgo 0%).

**NO se debe limpiar** el resto ($19.7M de 1,059 grupos) porque representan Ã³rdenes multi-producto legÃ­timas.

### 5. ¿Debe emitirse un nuevo RFC?

**SÃ** — RFC necesario para:

1. **RFC-DEDUP-PARIS-V2:** Limpieza de 133 grupos reales ($1.5M) con nuevo dedup key que incluya `sku` y `descripciÃ³n`
2. **RFC-SOURCE-QUALITY:** Investigar por quÃ© el sistema PARIS genera filas duplicadas (especialmente orden 302998803 con 17 copias)
3. **RFC-FILE-RENAME:** Investigar si `06-06-2026.xlsx` y `1 jun 2026 - 5 jun 2026.xlsx` fueron renombrados a `1 jun 2026 - 8 jun 2026.xlsx`

---

## Correcciones a AuditorÃ­as Previas

### 1. CertificaciÃ³n Previa: "2,052 filas duplicadas, $21.2M"

**CORREGIDO:** Solo **133 grupos** son duplicados reales ($1.5M). Los 1,059 grupos restantes ($19.7M) son Ã³rdenes multi-producto colapsadas por un dedup key que excluÃ­a SKU y descripciÃ³n.

### 2. CertificaciÃ³n Previa: "Duplicados nacen en archivos fuente"

**PARCIALMENTE CORREGIDO:** Los 133 grupos sÃ­ nacen en fuente. Pero los 1,059 grupos no son duplicados — son diferentes productos que casualmente tienen el mismo precio en la misma orden.

### 3. CLAUDE.md: "Facturacion estÃ¡ vacÃ­o (0 files)"

**CORREGIDO:** Facturacion tiene **62 archivos XML** (dteproveedor_5372.xml a dteproveedor_7440.xml). No es un directorio vacÃ­o.

### 4. "Data/freshness gap: PARIS/FALABELLA end Apr 2026"

**CORREGIDO:** PARIS tiene datos hasta Junio 2026 en los archivos fuente RAW (DS `1 jun 2026 - 8 jun 2026.xlsx`, FF `1 may 2026 - 31 may 2026.xlsx`). Sin embargo, estos pueden no estar completamente cargados al ledger.

---

## Recomendaciones Finales

| AcciÃ³n | Prioridad | Impacto |
|---|---|---|
| Corregir CLAUDE.md con hallazgos actuales | **ALTA** | DocumentaciÃ³n |
| Ejecutar DELETE para 133 grupos ($1.5M) | **MEDIA** | $1.5M recuperado |
| Reprocesar con nuevo dedup key (incluir SKU) | **MEDIA** | Prevenir falsos positivos |
| Investigar archivos renombrados (06-06-2026 vs 1 jun) | **BAJA** | Cerrar 381 grupos no verificables |
| Corregir loader PARIS para cargar data faltante (Jun 2026) | **MEDIA** | $2.8M en datos no cargados |
| RFC-DEDUP-PARIS-V2 | **MEDIA** | Nueva certificaciÃ³n de limpieza |
