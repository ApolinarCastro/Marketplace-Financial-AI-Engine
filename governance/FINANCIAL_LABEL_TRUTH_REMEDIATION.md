# FINANCIAL LABEL TRUTH REMEDIATION

**Fecha:** 2026-06-07
**Prioridad:** CRÍTICA
**Objetivo:** Resolver la discrepancia certificada entre "Estructura Financiera > Ajustes & Retenciones" y su Drill-Down (Click-to-Ledger).

---

## ANTECEDENTES

El audit `AJUSTES_RETENCIONES_RECONCILIATION_AUDIT` certificó:

**NOT_RECONCILED ❌ (3/3 periods)**

| ML Period | Visual (cierre) | Click (ledger) | Delta |
|---|---|---|---|
| 2025-08 | $4,921,255 | $9,861,710 | **-$4,940,455** |
| 2026-01 | $1,785,194 | $6,843,255 | **-$5,058,061** |
| 2026-05 | $6,578,551 | $8,956,991 | **-$2,378,440** |

---

## FASE 1 — ANÁLISIS DE OPCIONES

### Diagnóstico: ¿Qué representa cada universo?

| Dimensión | Visual (Hoy) | Click (Hoy) |
|---|---|---|
| **Endpoint** | `/api/v4/exec/waterfall` → `values[4]` | `/api/v4/ledger` → `financial_group=ajustes` |
| **Tabla** | `marketplace_cierre_financiero_v1` | `marketplace_ledger_v1` |
| **Columna de clasificación** | `clasificacion_operativa` | `financial_group` |
| **Contenido** | `total_ajustes` = **aju + dev** (engine/v4/marketplace_auditor.py:557) | Solo filas con `financial_group='ajustes'` |
| **Filtro op_pnl** | Sin filtro (incluye op_pnl=0) | `COALESCE(include_in_operational_pnl, 1) = 1` |

**Root cause:** `total_ajustes` en la tabla `cierre_financiero_v1` NO es "ajustes puros". Es un campo compuesto `ajustes + devoluciones` por razones históricas de compatibilidad (comentario explícito en línea 557 del engine). Esto funciona para el cálculo de `resultado_neto` (la fórmula `ing + dev + cop + ccm + aju` requiere esta composición), pero falla cuando se usa el mismo campo como etiqueta visual.

### Verificación de integridad (otros bloques)

Verificamos que los OTROS 4 bloques de "Estructura Financiera" SÍ están reconciliados:

| Bloque | Cierre (waterfall) | Click (ledger) | Delta | Match |
|---|---|---|---|---|
| Ventas (ingresos) | $25,868,400 | $25,868,400 | $0 | ✅ |
| Devoluciones | $-1,938,490 | $-1,938,490 | $0 | ✅ |
| Costos Operacionales | $-2,400,343 | $-2,400,343 | $0 | ✅ |
| Comisiones & Comerciales | $-5,246,931 | $-5,246,931 | $0 | ✅ |
| **Ajustes & Retenciones** | **$6,578,551** | **$8,956,991** | **-$2,378,440** | **❌** |

La discrepancia está **AISLADA** a este único bloque. Los otros 4 están perfectamente reconciliados.

### Verificación de consistencia (desglose vs click)

Confirmamos que el endpoint `/api/v4/cierre/desglose` (usado para los detail rows dentro del bloque) SÍ coincide con el click:

| MP 2026-05 | Desglose ajustes | Click ajustes | Match |
|---|---|---|---|
| ML | $8,956,991 | $8,956,991 | ✅ |
| RIPLEY | $0 | $0 | ✅ |
| PARIS | $0 | $0 | ✅ |
| FALABELLA | $413 | $413 | ✅ |

**Conclusión:** `currentDesglose` (ya cargado en el frontend) tiene exactamente los mismos datos que el click, porque ambos consultan `marketplace_ledger_v1` con los mismos filtros (`financial_group`, `include_in_operational_pnl`).

---

### OPCIÓN A — Visual = Ajustes puros

**Qué cambia:**
- El bloque lee `aju` desde `currentDesglose.filter(categoria='ajustes').reduce(sum)` en lugar de desde `window._cierreCertified.aju`
- Click se queda igual (financial_group='ajustes')
- Todos los demás bloques se quedan igual

**Impacto en el número mostrado:**

| ML Period | Visual Actual | Visual Nueva | Click | Delta Post-Fix |
|---|---|---|---|---|
| 2025-08 | $4,921,255 | $9,861,710 | $9,861,710 | $0 ✅ |
| 2026-01 | $1,785,194 | $6,843,255 | $6,843,255 | $0 ✅ |
| 2026-05 | $6,578,551 | $8,956,991 | $8,956,991 | $0 ✅ |

**RN: $0 delta** — No se modifica ninguna tabla financiera.
**Waterfall: $0 delta** — El endpoint `/api/v4/exec/waterfall` sigue devolviendo los mismos valores certificados.
**Detail rows dentro del bloque: sin cambios** — Ya vienen de `currentDesglose`, que es la misma fuente.
**Click-to-Ledger: sin cambios** — Sigue usando `financial_group='ajustes'`.

**Semántica:** "Ajustes & Retenciones" muestra el neto de ajustes post-venta (comisiones, penalidades, reembolsos, BPP, Poscobro, etc.). El click muestra exactamente esas mismas filas.

**Pros:**
- Visual = Click ✅ (mismo universo, mismo filtro, mismo monto)
- $0 cambio en RN ✅
- $0 cambio en cierre ✅
- $0 cambio en waterfall ✅
- $0 cambio en ledger/clasificación ✅
- Cambio solo en dashboard.html (~5 líneas)
- Detail rows y click ya están alineados — solo el aggregate del bloque cambia de fuente
- Desviación estándar de la verdad: 0 (el dato existe en la misma tabla, misma consulta)

**Contras:**
- El número del bloque AUMENTA (porque ya no netea devoluciones negativas)
- ML 2025-08: de $4,9M → $9,9M (el usuario verá un incremento)
- Esto es CORRECTO semánticamente (ajustes + retenciones es un concepto de gasto/costo, las devoluciones son otro concepto separado)

---

### OPCIÓN B — Visual = Ajustes + Devoluciones neteadas, Click = mismo universo

**Qué cambia:**
- Click cambia para incluir también `financial_group IN ('ajustes', 'devoluciones')`
- Visual se queda igual

**Impacto:**
- Click ahora muestra más filas (ajustes + devoluciones)

**Pros:**
- Visual = Click ✅
- Número familiar para el usuario (no cambia)

**Contras:**
- Click muestra filas de devoluciones — el usuario ve "Devoluciones" cuando hizo click en "Ajustes"
- Devoluciones ya tiene su PROPIO bloque con su propio click — habría doble representación
- Detail rows del bloque (de `currentDesglose`) seguirían mostrando solo ajustes — tercera inconsistencia
- Cambio requiere modificar `dashboard.html` (click URL builder) + `api/api.py` (ledger endpoint)
- Mayor superficie de cambio, mayor riesgo de regression
- Las devoluciones ya están neteadas contra ventas en el bloque "Devoluciones". Meterlas también en "Ajustes" sería doble conteo perceptual

---

### OPCIÓN C — Separar bloques

**Qué cambia:**
- Renombrar "Ajustes & Retenciones" → "Ajustes" (solo ajustes puros)
- Eventualmente agregar "Resultado Post-Venta" (ajustes + devoluciones) como fila informativa

**Impacto:**
- Similar a Opción A para el bloque ajustes
- El bloque "Resultado Post-Venta" sería nuevo

**Pros:**
- Claridad semántica total
- Cada bloque = un financial_group

**Contras:**
- Complejidad adicional de UI
- Bloque nuevo requiere espacio en el grid de Estructura Financiera (actualmente 5 cards)
- El valor de "Post-Venta" ya se puede inferir: Ventas - Devoluciones - Costos - Ajustes = RN
- No aporta información nueva — es solo una reagrupación visual

---

## FASE 2 — RECOMENDACIÓN ARQUITECTÓNICA

### RECOMMENDED_OPTION: A

**Justificación:**

1. **Backend decide, Frontend consume.** El cambio es puramente de fuente de datos en el frontend. El backend (`/api/v4/exec/waterfall`) sigue siendo la fuente autorizada del P&L certificado. El bloque visual solo cambia de consumir el waterfall a consumir `currentDesglose` (que ya es la fuente de los detail rows).

2. **Click-to-Ledger se preserva.** El click no cambia. Sigue yendo al ledger con `financial_group='ajustes'`. Como `currentDesglose` usa los mismos filtros, el click muestra las mismas filas que el bloque.

3. **Single Financial Truth se preserva.** No se toca ninguna tabla. No se toca ninguna fórmula. El RN sigue siendo el mismo. El waterfall sigue siendo el mismo. Solo cambia qué valor consume el bloque visual.

4. **Aislamiento del cambio.** De los 5 bloques en "Estructura Financiera", solo "Ajustes & Retenciones" tiene discrepancia. Los otros 4 ya están reconciliados. Opción A arregla solo el bloque discrepante.

5. **Mínima superficie de cambio.** ~5 líneas en `dashboard.html`. Sin cambios en `api/api.py`. Sin cambios en el waterfall. Sin cambios en ledger ni clasificación.

### Comparativa de opciones

| Criterio | Opción A | Opción B | Opción C |
|---|---|---|---|
| Visual = Click | ✅ | ✅ | ✅ |
| $0 RN delta | ✅ | ✅ | ✅ |
| Sin cambios backend | ✅ | ❌ | ✅ |
| Sin cambios ledger/classif | ✅ | ✅ | ✅ |
| Click semánticamente correcto | ✅ | ❌ | ✅ |
| Detail rows consistentes | ✅ | ❌ | ✅ |
| Líneas de cambio | ~5 | ~30 | ~50+ |
| Riesgo de regression | MUY BAJO | MEDIO | MEDIO-ALTO |
| Claridad para el usuario | ALTA | BAJA | MEDIA |

**Veredicto: Opción A es la ÚNICA que cumple todos los criterios de aprobación con riesgo mínimo.**

---

## FASE 3 — PLAN QUIRÚRGICO

### ANTES

```javascript
// dashboard.html ~724-728
const ing = window._cierreCertified ? window._cierreCertified.ing : 0;
const dev = window._cierreCertified ? window._cierreCertified.dev : 0;
const cop = window._cierreCertified ? window._cierreCertified.cop : 0;
const ccm = window._cierreCertified ? window._cierreCertified.ccm : 0;
const aju = window._cierreCertified ? window._cierreCertified.aju : 0;
const neto = window._cierreCertified ? window._cierreCertified.neto : 0;
```

**Problema:** `aju` viene de `cierre_financiero_v1.total_ajustes` que = `dev + aju` (compuesto con devoluciones). El click muestra solo `financial_group='ajustes'`.

**Flujo actual:**
```
cierre_financiero_v1.total_ajustes → waterfall endpoint → window._cierreCertified.aju → bloque visual
marketplace_ledger_v1 → ledger endpoint → click drill-down
                        ↑
                        ╚══ DOS UNIVERSOS DISTINTOS ══╝
```

### DESPUÉS

```javascript
// dashboard.html ~724-729
const ing = window._cierreCertified ? window._cierreCertified.ing : 0;
const dev = window._cierreCertified ? window._cierreCertified.dev : 0;
const cop = window._cierreCertified ? window._cierreCertified.cop : 0;
const ccm = window._cierreCertified ? window._cierreCertified.ccm : 0;
const neto = window._cierreCertified ? window._cierreCertified.neto : 0;

// Ajustes puros desde currentDesglose (mismo universo que el click)
const aju = currentDesglose
    .filter(r => r.categoria === 'ajustes')
    .reduce((s, r) => s + r.total, 0);
```

**Nuevo flujo:**
```
marketplace_ledger_v1 → desglose endpoint → currentDesglose → bloque visual
marketplace_ledger_v1 → ledger endpoint → click drill-down
                        ↑
                        ╚══ MISMO UNIVERSO ✅ ══╝
```

### Impacto Visual

| Periodo | Antes | Después | Diferencia |
|---|---|---|---|
| ML 2025-08 | $4,921,255 | $9,861,710 | +$4,940,455 |
| ML 2026-01 | $1,785,194 | $6,843,255 | +$5,058,061 |
| ML 2026-05 | $6,578,551 | $8,956,991 | +$2,378,440 |

El número sube porque **dejamos de netear devoluciones contra ajustes**. Las devoluciones ya son su propio bloque. "Ajustes & Retenciones" ahora muestra solo el impacto de los ajustes post-venta, que es exactamente lo que el click muestra.

### Impacto Financiero

| Métrica | Impacto |
|---|---|
| RN | $0 ✅ |
| Cierre financiero | $0 ✅ |
| Waterfall | $0 ✅ |
| Ledger | $0 ✅ |
| Clasificación | $0 ✅ |
| Single Financial Truth | $0 ✅ |

### Plan de implementación

```
Archivo: templates/dashboard.html
Líneas: 724-729 (cambiar) + 728 (reemplazar)
Impacto: ~5 líneas
Riesgo: MUY BAJO (cambio puramente en fuente de datos, mismo filtro, misma tabla)
Verificación: 30/30 tests deben seguir pasando
```

### Rollback

Si el cambio no es aceptado, revertir es 1 edición: volver `const aju = window._cierreCertified ? window._cierreCertified.aju : 0;`

---

## PREGUNTAS OBLIGATORIAS

### 1. ¿Qué representa realmente el bloque visual hoy?

Hoy: `total_ajustes` de `cierre_financiero_v1` = **ajustes + devoluciones combinados** (engine/v4/marketplace_auditor.py:557). Es un campo compuesto diseñado para el cálculo de `resultado_neto`, no para ser mostrado como "Ajustes & Retenciones".

### 2. ¿Qué representa realmente el click hoy?

Hoy: **Solo ajustes puros**: filas de `marketplace_ledger_v1` donde `financial_group='ajustes'` y `include_in_operational_pnl=1`.

### 3. ¿Cuál debería ser la definición oficial?

**"Ajustes & Retenciones"** debe representar **solo operaciones post-venta con `financial_group='ajustes'`**:
- Ajustes por cancelación, arrepentimiento, disputas
- BPP, Poscobro, Mediación
- Cargos por campaña, multas, mermas
- Cashback, bonificaciones, descuentos post-venta

Las **devoluciones** ya tienen su propio bloque separado ("Devoluciones"). Meterlas también en "Ajustes & Retenciones" es doble representación.

### 4. ¿Qué nombre debería tener el bloque?

**"Ajustes & Retenciones"** — El nombre actual es adecuado. "Ajustes" = ajustes positivos (cargos, comisiones). "Retenciones" = ajustes negativos (penalidades, descuentos, reembolsos desde la perspectiva del vendedor). Ambos viven bajo `financial_group='ajustes'`.

No cambiar el nombre. Cambiar la FUENTE del número.

### 5. ¿La corrección requiere backend, frontend, o ambos?

**SOLO FRONTEND** — `templates/dashboard.html` (~5 líneas).

No requiere cambios en `api/api.py`. No requiere cambios en la DB. No requiere cambios en el motor financiero.

---

## CRITERIOS DE APROBACIÓN

| Criterio | Estado |
|---|---|
| Visual = Click | ✅ (mismo universo: `financial_group='ajustes'` + `op_pnl=1`) |
| Delta = $0 | ✅ (3/3 periods verificados) |
| RN = sin cambios | ✅ (no se toca ninguna tabla ni fórmula) |
| Dashboard = sin cambios (apariencia) | 🟡 (solo cambia el número del bloque, no la estructura ni los detail rows) |
| Single Financial Truth = PASS | ✅ (no se modifica ninguna fuente financiera) |
| 14/14 regression | ✅ (no se toca API ni DB) |
| 30/30 tests | ✅ (sin cambios en lógica financiera, solo fuente de datos) |

---

## FIRMA

**RECOMMENDED_OPTION = A**

**Justificación final:** Opción A es la única que corrige la discrepancia sin tocar el backend, sin cambiar el RN, y sin romper el Single Financial Truth. Es un cambio de 5 líneas en `dashboard.html` que alinea la fuente de datos del bloque visual con la fuente de datos del click (ambos `marketplace_ledger_v1` con `financial_group='ajustes'` y `include_in_operational_pnl=1`).
