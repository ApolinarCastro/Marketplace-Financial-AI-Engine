# PARIS DUPLICATE INVARIANTS
**Date:** 2026-06-07
**Certification ID:** PARIS-DUP-INV-2026-06-07

---

## Q1: ¿Los duplicados están actualmente inflando el resultado financiero?

**SI** — Los duplicados INFLAN el resultado financiero de PARIS en **$21,238,958**.

| Componente | Inflación |
|---|---|
| Ingresos | +$26,228,900 (Ventas duplicadas) |
| Devoluciones | -$4,745,576 (Devoluciones duplicadas, efecto neto reductor) |
| Costos operacionales | +$567,920 (Costos duplicados, efecto neto reductor) |
| Ajustes | +$323,554 (Ajustes duplicados) |
| **Resultado Neto** | **+$21,238,958** |

---

## Q2: ¿Los duplicados afectan Disponible?

**SI** — Disponible (definido como `resultado_neto` en `cierre_financiero_v1`) se reduce en **$21,238,958**.

Disponible actual PARIS: $337,418,552
Disponible post-dedup: $316,179,594
**Delta: -$21,238,958**

---

## Q3: ¿Los duplicados afectan Resultado Neto?

**SI** — Monto exacto: **-$21,238,958** (reducción post-eliminación).

---

## Invariants Verification

### 1. Delta Sum Consistency
```
Ing_delta + Dev_delta + Cop_delta + Aju_delta = RN_delta
(-26,228,900) + (+4,745,576) + (+567,920) + (-323,554) = -21,238,958 ✅
```

### 2. Cross-FG Consistency
6 grupos excepcionales con mismo `(id_orden, fecha, monto=$0, archivo_origen)` pero DISTINTO `financial_group`. Estos NO son eliminados por el dedup (diferente FG = diferente grupo). Impacto financiero: **$0**.

### 3. Cross-MP Contamination
**$0** — El dedup solo afecta filas con `marketplace='PARIS'`. ML, RIPLEY, FALABELLA permanecen intactos.

### 4. Single Financial Truth Consistency
La dedup NO rompe la Single Financial Truth porque:
- Solo opera sobre `marketplace_ledger_v1` (fuente única)
- No modifica `financial_group`, `detalle`, ni ninguna clasificación
- Preserva exactamente 1 fila por evento económico único
- Todos los conceptos financieros mantienen su signo natural

### 5. DEC-019 Compatibility
DEC-019 afecta solo a ML (Paired PosCobro mechanisms). PARIS no tiene DEC-019 flags. **Compatible.**

### 6. Waterfall Formula Integrity
RN = ing + dev + cop + ccm + aju → Se mantiene post-dedup. PARIS no tiene `costos_comerciales` (siempre $0 para PARIS).

---

## Invariant Table

| Invariant | Status | Value |
|---|---|---|
| Delta Sum | ✅ | -$21,238,958 = ing(-26,228,900) + dev(+4,745,576) + cop(+567,920) + aju(-323,554) |
| Cross-FG | ✅ | 0 eventos afectados con monto ≠ $0 |
| Cross-MP | ✅ | $0 contaminación |
| SFT | ✅ | Fuente única ledger preservada |
| DEC-019 | ✅ | No aplica a PARIS |
| Waterfall | ✅ | RN = ing + dev + cop + aju (ccm=0) |
| Periodicidad | ✅ | Todos los 18 meses tienen delta negativo consistente |
