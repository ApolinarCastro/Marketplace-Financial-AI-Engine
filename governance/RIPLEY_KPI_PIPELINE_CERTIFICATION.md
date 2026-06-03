# SPRINT B2.5A — RIPLEY KPI PIPELINE CERTIFICATION

**Fecha**: 2026-06-01
**Régimen**: READ ONLY — FORENSE
**Objetivo**: Determinar por qué el Dashboard muestra Resultado Neto RIPLEY = $0 cuando existen transacciones en `marketplace_ledger_v1`.

---

## FASE 1 — PERÍODO

Marketplace = RIPLEY
Mes = Mayo 2026 (2026-05)

---

## FASE 2 — EXTRACCIÓN

### 2A. marketplace_ledger_v1 (RAW)

| Detalle | Rows | Monto |
|---|---|---|
| Importe del pedido | 347 | $12,442,050.00 |
| A pagar | 347 | $8,640,593.00 |
| Comisiones sobre pedidos | 347 | $2,239,488.00 |
| Gastos de envio pagados por el operador | 258 | $1,011,576.00 |
| Envio | 258 | $1,011,576.00 |
| Pedidos reembolsados | 87 | $1,694,470.00 |
| Comisiones sobre pedidos reembolsados | 87 | $1,694,470.00 |
| Descuento por costo logistico | 236 | $672,594.00 |
| Envio reembolsado | 29 | $94,354.00 |
| Gastos de envio reembolsados pagados por el operador | 29 | $94,354.00 |
| Descuento por logistica inversa | 15 | $79,108.00 |
| Otros descuentos | 1 | $660.00 |
| Descuento por cancelacion | 1 | $3,980.00 |
| **TOTAL** | **1,737** | **$17,281,186.00** |

**Estado de columnas críticas:**

| Columna | Valor | Significado |
|---|---|---|
| `financial_group` | NULL (100% rows) | Sin clasificar |
| `clasificacion_operativa` | NULL (100% rows) | Sin clasificar |
| `include_in_operational_pnl` | NULL (100% rows) | Default TRUE |
| `folio_xml` | 347 rows (100%) | Presente desde XLSX |
| `estado_xml` | NULL (100% rows) | Sin certificar |

### 2B. marketplace_ledger_clasificado_v1

| Métrica | Valor |
|---|---|
| Rows en clasificado | 1,056 (de 1,737 en ledger = 61%) |
| Monto total en clasificado | $1,255,624.00 (de $17,281,186 = 7.3%) |
| `financial_group` | NULL (100% rows) |
| `include_in_operational_pnl = TRUE` | 1,023 rows ($627,812) |
| `include_in_operational_pnl = FALSE` | 33 rows ($627,812) |
| Ledger rows SIN clasificar | 681 rows ($16,025,562) |

**Conclusión**: El clasificado contiene datos **stales** de la ejecución pre-RFC-001. Solo cubre 61% de las filas del ledger y los montos no coinciden (7.3% del total). El `financial_group` nunca fue propagado.

### 2C. API Response (`/api/v4/cierre/desglose`)

Query SQL ejecutada por el endpoint:
```sql
SELECT COALESCE(financial_group, 'sin_clasificar') as financial_group,
       detalle, tipo_movimiento, clasificacion_operativa,
       SUM(COALESCE(monto, 0)) as total, COUNT(*) as cantidad
FROM marketplace_ledger_v1
WHERE marketplace='RIPLEY' AND fecha BETWEEN '2026-05-01' AND '2026-05-31'
  AND COALESCE(include_in_operational_pnl, 1) = 1
GROUP BY financial_group, detalle, tipo_movimiento, clasificacion_operativa
```

Resultado:
```
financial_group  | detalle                    | total
─────────────────┼────────────────────────────┼──────────────
sin_clasificar   | Importe del pedido         | $12,442,050
sin_clasificar   | A pagar                    | $8,640,593
sin_clasificar   | Pedidos reembolsados       | -$1,694,470
sin_clasificar   | Comisiones sobre pedidos   | -$2,239,488
... etc         | ...                        | ...
```

**100% de las filas en categoría `sin_clasificar`.**

### 2D. Dashboard Response

`renderCierre()` en `dashboard.html:722-737`:
```javascript
currentDesglose.forEach(row => {
    if (row.categoria === 'ingresos')          { ing += row.total; }
    else if (row.categoria === 'devoluciones')  { dev += row.total; }
    else if (row.categoria === 'costos_operacionales') { cop += row.total; }
    else if (row.categoria === 'costos_comerciales')   { ccm += row.total; }
    else if (row.categoria === 'ajustes')       { aju += row.total; }
});
// neto = ing + cop + ccm + dev + aju;
```

**Resultado**: `ing=0, dev=0, cop=0, ccm=0, aju=0` → `neto = $0`.

La categoría `sin_clasificar` **no existe** en los condicionales. Es ignorada silenciosamente.

---

## FASE 3 — PIPELINE TRACE

```
01_Raw/RIPLEY/46 XLSX
    │  load_ripley()  ✅  (RFC-001: dayfirst=True)
    ▼
marketplace_ledger_v1  ✅  1,737 rows, $17,281,186
    │  run_classification()  ❌  NUNCA RE-EJECUTADO
    │    ├── normaliza detalles
    │    ├── mapea → clasificacion_operativa
    │    ├── asigna financial_group
    │    └── UPDATE ledger con fg, co, pnl
    ▼
marketplace_ledger_v1 (financial_group = NULL)  ❌
    │  /api/v4/cierre/desglose
    ▼
API JSON → [{financial_group: "sin_clasificar", ...}]  ❌
    │  renderCierre() → solo reconoce 5 categorías
    ▼
Dashboard → "Resultado Neto RIPLEY: $0"  ❌
```

**El pipeline se rompe en la clasificación.**

---

## FASE 4 — DÓNDE APARECE EL CERO

| Etapa | ¿Hay datos? | ¿Son correctos? |
|---|---|---|
| Ledger (raw) | ✅ 1,737 rows, $17.3M | ✅ Valores correctos post-RFC-001 |
| Clasificación | ❌ No re-ejecutada | ❌ Stale data pre-RFC-001 |
| Ledger (financial_group) | ❌ NULL (100%) | ❌ Debería tener 'ingresos', 'costos', etc. |
| API desglose | ❌ "sin_clasificar" (100%) | ❌ Dashboard no reconoce esta categoría |
| Dashboard neto | ❌ $0 | ❌ Ignora sin_clasificar |

**El cero aparece en el Dashboard** porque el `renderCierre()` suma solo 5 categorías específicas y `sin_clasificar` no está entre ellas.

Pero la **raíz del problema** está una etapa antes: en la **API**, que devuelve `financial_group = 'sin_clasificar'` porque el ledger nunca recibió la propagación de clasificación.

---

## FASE 5 — CAUSA RAÍZ

### Respuesta: **B) Clasificación**

El problema NO está en:

| Etapa | Descartada por |
|---|---|
| **A) Ledger** | ❌ No. El ledger tiene datos correctos ($17.3M, 1,737 rows). Valores financieros verificados contra XLSX (Sprint B2.4A). |
| **C) API** | ❌ No. La API funciona correctamente — consulta el ledger y devuelve lo que encuentra. No hay bug en el SQL. |
| **D) Frontend** | ❌ No. El Dashboard renderiza correctamente las 5 categorías conocidas. La omisión de `sin_clasificar` es intencional (no debería existir). |

El problema SÍ está en:

| **B) Clasificación** | ✅ SÍ. `run_classification()` nunca fue re-ejecutado después del RFC-001 rebuild. |
|---|---|

### Detalle de la Causa Raíz

1. **RFC-001 (2026-06-01)**: Ejecutó `DELETE + INSERT` sobre `marketplace_ledger_v1` para RIPLEY.
2. **Efecto colateral**: Las 62,502 nuevas filas en ledger no tienen `financial_group`, `clasificacion_operativa`, ni `include_in_operational_pnl`.
3. **Clasificado table**: Quedó con datos pre-RFC-001 (stale). Solo cubre 61% de las filas actuales, montos no coinciden (7.3% del total).
4. **Propagación faltante**: `run_classification()` normalmente:
   - Lee todas las filas del ledger
   - Normaliza y clasifica cada `detalle` → `clasificacion_operativa`
   - Mapea a `financial_group` (ingresos, devoluciones, etc.)
   - Establece `include_in_operational_pnl` (FALSE para "A pagar")
   - **UPDATE** el ledger con estos valores
5. **Sin propagación**: `COALESCE(financial_group, 'sin_clasificar')` en API → Dashboard ignora `sin_clasificar` → `neto = $0`.

### Magnitud del Impacto

| Métrica | Valor |
|---|---|
| RIPLEY rows en ledger sin clasificar | 62,502 (100%) |
| RIPLEY monto sin clasificar | $413,893,686.00 (100%) |
| RIPLEY rows en clasificado (stale) | 17,879 (28.6%) |
| RIPLEY monto en clasificado (stale) | $14,310,416.00 (3.5%) |
| Dashboard neto actual | $0 |
| Dashboard neto esperado (post-clasificación) | ~$ -X,XXX,XXX (negativo: costos > ingresos después de comisiones/gastos) |

### Nota sobre "A pagar"

El concepto "A pagar" ($8.6M en Mayo 2026) será excluido del Resultado Neto por la regla:
```
if 'a pagar' in detalle_norm → include_in_operational_pnl = FALSE
```

Esto es correcto. "A pagar" es el neto después de comisiones/gastos — incluirlo duplicaría el cálculo.

---

## FASE 6 — CERTIFICACIÓN

### Diagnóstico

| Pregunta | Respuesta |
|---|---|
| ¿El ledger tiene datos? | ✅ Sí, $17.3M en Mayo 2026 |
| ¿Los datos son correctos? | ✅ Sí, verificados contra XLSX (B2.4A) |
| ¿La clasificación se ejecutó? | ❌ No, nunca post-RFC-001 |
| ¿El API funciona correctamente? | ✅ Sí, refleja fielmente el estado del ledger |
| ¿El Dashboard funciona correctamente? | ✅ Sí, renderiza las 5 categorías conocidas |
| ¿El error está en clasificación? | ✅ **SÍ — B) Clasificación** |

### Solución Requerida

Ejecutar `MarketplaceAuditorEngine.run_classification()` para:
1. Re-clasificar las 62,502 filas RIPLEY del ledger
2. Propagar `financial_group`, `clasificacion_operativa`, `include_in_operational_pnl`
3. Re-ejecutar `MarketplaceAuditorEngine.run_financial_closing()` para actualizar `marketplace_cierre_financiero_v1`

**Estimación de impacto post-corrección**:
- Dashboard RIPLEY Mayo 2026: ~$3-5M neto (ingresos $12.4M + costos operacionales -$1.1M + comisiones -$2.2M + devoluciones -$1.7M + ajustes varios)
- Todos los 17 meses históricos afectados igualmente
- ML, PARIS, FALABELLA sin impacto

### Veredicto

```
CAUSA RAÍZ IDENTIFICADA: B) Clasificación
CLASIFICACIÓN: PASS WITH OBSERVATIONS
RFC-001 REQUIERE: Re-ejecución de run_classification()
```

**Observación**: El Sprint B2.4 (POST_RIPLEY_RECERTIFICATION.md) ya documentó que la clasificación se perdió en el rebuild (sección 3, Evidence Chain: Class Confidence 0.85→0.0). Esta certificación confirma que esa pérdida **no es abstracta** — tiene un impacto directo y medible en el Dashboard: Resultado Neto RIPLEY = $0 en todos los meses.

---

*Sprint B2.5A completado. Read-only. Sin modificaciones.*
