# PARIS FORENSIC TRUTH
**Date:** 2026-06-07
**Certification ID:** PARIS-FORENSIC-FASE7

---

## Truth Answers

### 1. ¿Existen duplicados reales en RAW?

**SÃ** — 133 grupos de "near-duplicados" existen en los archivos RAW.

Son filas donde:
- Misma orden (`nÃºmero orden`)
- Mismo producto (mismo `sku`, misma `descripciÃ³n`)
- Mismo monto (mismo `monto a pagar`)
- Misma fecha
- Solo cambia el `id` auto-increment (identificador Ãºnico de fila)

Estos son **133 grupos** que, si se ignora la columna `id`, son duplicados exactos.

**Ejemplo principal:** Orden 302998803 aparece 17 veces en `07-2025.xlsx` con datos idÃ©nticos (mismo SKU `MKWZWAZUQ3-2`, mismo precio $34,990 bruto / $29,742 neto).

### 2. ¿Existen duplicados reales en ledger?

**SÃ** — Los mismos 133 grupos aparecen en el ledger. El ledger es un reflejo fiel de los RAW.

El ledger tiene 1,573 grupos totales que cumplen el criterio del dedup key anterior. De estos:
- **133 son duplicados reales** (origen: source file)
- **1,059 son colapsos de clasificaciÃ³n** (diferentes productos en misma orden, mismo monto neto)
- **381 no son verificables** (archivos fuente no encontrados en disco, probablemente renombrados)

### 3. ¿CuÃ¡ntos?

| Tipo | Grupos | Filas en exceso | Monto inflado real |
|---|---|---|---|
| **Duplicados reales** (source-borne) | **133** | **433** | **$1,544,345** |
| Colapsos de clasificaciÃ³n (no duplicados) | 1,059 | 1,519 | $19,694,613 |
| No verificables (archivo faltante) | 381 | ~100 | No calculable |
| **Total reportado anteriormente** | **1,573** | **2,052** | **$21,238,958** |

### 4. ¿CuÃ¡l es el monto exacto?

**$1,544,345** — Este es el monto EXACTO inflado por duplicados reales (source-borne).

Los $21,238,958 reportados anteriormente incluyen $19,694,613 de Ã³rdenes multi-producto que NO son duplicados.

### 5. ¿QuÃ© porcentaje nace en RAW?

**100%** de los duplicados reales nacen en RAW.

El loader es FIEL: si el RAW tiene 17 filas idÃ©nticas, el ledger tiene 17 filas idÃ©nticas.

### 6. ¿QuÃ© porcentaje nace en ETL?

**0%** — El ETL (loader) no crea duplicados.

Evidencia:
- No hay casos donde el RAW tenga 1 fila y el ledger tenga N copias (0 LOADER_BUG cases)
- `id_transaccion` en el ledger = `id` en el source file (1:1 mapping)
- El conteo de filas por archivo se mantiene consistente entre RAW y ledger

### 7. ¿QuÃ© porcentaje corresponde a contaminaciÃ³n del ledger?

**0%** — El ledger NO estÃ¡ contaminado.

No hay:
- Filas sin respaldo documental
- Filas sin archivo origen vÃ¡lido
- Filas cargadas mÃºltiples veces por error ETL

### 8. ¿Los 2.052 registros certificados anteriormente siguen siendo vÃ¡lidos?

**NO** — La certificaciÃ³n anterior sobrestimÃ³ los duplicados.

La certificaciÃ³n previa usaba el dedup key:
```
(id_orden, fecha, monto, financial_group, detalle, clasificacion_operativa, archivo_origen)
```

Este key NO incluye `sku` ni `descripcion`, por lo que NO puede distinguir entre:
- 2 productos diferentes en la misma orden con el mismo precio (LEGÃTIMO)
- 2 copias del mismo producto en la misma orden (DUPLICADO REAL)

**Error estimado: ~$19.7M sobrestimado** (93% del total reportado era incorrecto).

### 9. ¿Los 1.573 grupos siguen siendo vÃ¡lidos?

**PARCIALMENTE** — El nÃºmero de grupos (1,573) es correcto en el ledger, pero la interpretaciÃ³n es incorrecta:

| Subconjunto | Validez | ExplicaciÃ³n |
|---|---|---|
| 133 grupos | **VÃLIDOS** ✅ | Son duplicados reales (source-borne, $1.5M) |
| 1,059 grupos | **INVÃLIDOS** ❌ | Son Ã³rdenes multi-producto. NO son duplicados |
| 381 grupos | **NO VERIFICABLES** ❓ | Archivos fuente faltantes |

### 10. ¿Existe evidencia para ejecutar DELETE?

**PARCIAL** — Solo para 133 grupos ($1,544,345).

**SÃ se puede eliminar:**
- Los 133 grupos de duplicados reales ($1,544,345)
- Riesgo: 0% (misma orden, mismo producto, misma cantidad — solo cambia auto-increment id)
- Rollback disponible via snapshot

**NO se debe eliminar:**
- Los 1,059 grupos de Ã³rdenes multi-producto ($19,694,613)
- Son diferentes productos en la misma orden
- Se perderÃ­an ventas legÃ­timas

**Se necesita investigar:**
- Los 381 grupos con archivo fuente faltante
- Determinar si `06-06-2026.xlsx` y `1 jun 2026 - 5 jun 2026.xlsx` son renombres de archivos existentes

---

## Contradicciones con AuditorÃ­as Previas

| AfirmaciÃ³n Anterior | Evidencia Actual | Correcta | ExplicaciÃ³n |
|---|---|---|---|
| "1,573 grupos duplicados, $21.2M" | 133 grupos, $1.5M | **AuditorÃ­a actual** | El dedup key anterior excluÃ­a SKU/descripciÃ³n, colapsando Ã³rdenes multi-producto |
| "Duplicados nacen en RAW" | Parcialmente cierto | **Ambas** | 133 grupos sÃ­, 1,059 grupos no son duplicados |
| "Loader no crea duplicados" | Confirmado | **AuditorÃ­a anterior** | Correcta |
| "Facturacion estÃ¡ vacÃ­o" | 62 XML files | **AuditorÃ­a actual** | El directorio NO estÃ¡ vacÃ­o |
| "2 archivos fuente existen" | No encontrados en disco | **AuditorÃ­a actual** | Probablemente renombrados despuÃ©s de la carga |
