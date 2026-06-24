# G6.1 — Resultado Neto: EVENTOS vs REGISTROS

**Fecha**: 2026-06-05
**Auditor**: Forensic Pipeline G6.1
**DB**: `data/db/meli_financial_v4.db`
**Scope**: ML — Abril 2025, Octubre 2025, All-time

---

## Hallazgo Central: FAIL

**El cierre calcula REGISTROS y existe INFLACION DOCUMENTAL confirmada.**

`marketplace_cierre_financiero_v1.resultado_neto` se calcula como `SUM(monto)` sobre cada fila de `marketplace_ledger_clasificado_v1` sin ningún mecanismo de deduplicación, neteo causal, o consolidación por evento económico.

---

## 1. Mecanismo Exacto de Cálculo

**Archivo**: `engine/v4/marketplace_auditor.py:514-557`

```
resultado_neto = total_ingresos + total_devoluciones + total_costos_operacionales 
               + total_costos_comerciales + total_ajustes
```

Donde cada componente es:
```sql
SUM(CASE WHEN clasificacion_operativa IN (<lista de conceptos>) THEN monto ELSE 0 END)
FROM marketplace_ledger_clasificado_v1
WHERE marketplace = ? AND fecha BETWEEN ? AND ?
```

No existe ningún mecanismo de:
- `GROUP BY id_orden`
- `GROUP BY id_transaccion` (sin sufijo)
- `GROUP BY payment_id`
- Deduplicación por causalidad
- Neteo de pares documentales
- Filtro `include_in_operational_pnl`

---

## 2. Pares Documentales Confirmados

### Abril 2025

| Métrica | Valor |
|---------|-------|
| Registros en `ajustes` | 680 filas, $22,993,874 |
| Órdenes con 2+ conceptos | 225 |
| Pares exactos (mismo monto) | 237 filas, $8,559,160 |
| Órdenes con pares exactos | 222 |
| **Inflación documental en ajustes** | **50.94%** |
| Pares con ambos `op_pnl=1` (afectan P&L) | 7 orders, $259,180 |
| **Inflación directa en Resultado Neto** | **$259,180 (0.39%)** |

### Octubre 2025

| Métrica | Valor |
|---------|-------|
| Registros en `ajustes` | 849 filas, $24,106,487 |
| Órdenes con 2+ conceptos | 302 |
| Pares exactos (mismo monto) | 336 filas, $9,905,876 |
| Órdenes con pares exactos | 300 |
| **Inflación documental en ajustes** | **~41%** |
| Pares con ambos `op_pnl=1` (afectan P&L) | 5 orders, $283,878 |
| **Inflación directa en Resultado Neto** | **$283,878 (0.40%)** |

### All-time ML

| Métrica | Valor |
|---------|-------|
| Pares exactos totales (cualquier op_pnl) | 520 entries, $15,512,381, 480 órdenes |
| % del total de `ajustes` ML | 5.06% |
| Pares exactos con ambos `op_pnl=1` | 65 entries, $2,202,507, 61 órdenes |
| % del Resultado Neto ML total | 0.26% |
| Pares Arre+Posc con ambos `op_pnl=1` | 36 entries, $1,300,129, 36 órdenes |

---

## 3. Mapeo de los 8 Conceptos Solicitados

| Concepto solicitado | `clasificacion_operativa` real | Apr 2025 rows | Apr 2025 total |
|---|---|---|---|
| `different_color_or_size_fashion` | Ajuste por Talla/Garantía | 227 | $7,530,873 |
| `bigger_than_expected` | Ajuste por Talla/Garantía | 227 | $7,530,873 |
| `smaller_than_expected` | Ajuste por Talla/Garantía | 227 | $7,530,873 |
| `not_match_size_guide` | Ajuste por Talla/Garantía | 227 | $7,530,873 |
| `undelivered_repentant_buyer` | Ajuste por Arrepentimiento | 71 | $2,623,903 |
| `bpp_refunded` | Ajuste por Compra Protegida (BPP) | 198 | $6,495,870 |
| `reconciled` | Ajuste Poscobro Conciliado | 109 | $4,429,841 |
| `compensated` | Ajuste Poscobro Conciliado | 109 | $4,429,841 |

Los 4 primeros (`different_color_or_size_fashion`, `bigger_than_expected`, `smaller_than_expected`, `not_match_size_guide`) confluyen en el mismo concepto real: **Ajuste por Talla/Garantía**.

---

## 4. Relación Causal: Evento Raíz → Mecanismo de Ejecución

### Pareja 1: Talla/Garantía + Compra Protegida (BPP)

```
Evento Raíz:      Talla/Garantía (95 órdenes en abril)
                    ↓
Mecanismo:        Compra Protegida BPP (mismo monto, 99% exactos)
                    ↓
Ambos op_pnl=0:   NO afectan Resultado Neto (0/0 en 117/121 órdenes)
Conclusión:       Inflación documental en ajustes pero NO en P&L
```

### Pareja 2: Arrepentimiento + Poscobro Conciliado

```
Evento Raíz:      Arrepentimiento (23 órdenes en abril)
                    ↓
Mecanismo:        Poscobro Conciliado (mismo monto, misma fecha en 14/23)
                    ↓
op_pnl:           INCONSISTENTE — 6 órdenes con ambos op_pnl=1
                    20 órdenes con Raíz=1, Mecanismo=0
Conclusión:       AFECTA Resultado Neto cuando ambos op_pnl=1
```

| Configuración | Abril 2025 | Impacto RN |
|---|---|---|
| Raíz op_pnl=1 + Mecanismo op_pnl=1 | 6 orders | **INFLACION DIRECTA** |
| Raíz op_pnl=1 + Mecanismo op_pnl=0 | 20 orders | Sin inflación (mecanismo excluido) |
| Raíz op_pnl=0 + Mecanismo op_pnl=0 | 117 orders | Sin inflación (ambos excluidos) |

---

## 5. Evidencia SQL Exacta

### Query: Pares exactos (mismo monto, misma fecha)
```sql
SELECT COUNT(*) as pairs_cnt,
       ROUND(SUM(a.monto), 2) as total_amount,
       COUNT(DISTINCT a.id_orden) as unique_orders
FROM marketplace_ledger_v1 a
JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden 
    AND a.monto = b.monto 
    AND a.id_transaccion <> b.id_transaccion
    AND a.fecha = b.fecha
WHERE a.marketplace = 'ML' AND b.marketplace = 'ML'
  AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
  AND a.clasificacion_operativa < b.clasificacion_operativa
  AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
```

### Query: Parejas Arre+Posc en P&L
```sql
SELECT COUNT(*) as pairs_cnt,
       ROUND(SUM(a.monto), 2) as total_amount,
       COUNT(DISTINCT a.id_orden) as unique_orders
FROM marketplace_ledger_v1 a
JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden 
    AND a.monto = b.monto 
    AND a.id_transaccion <> b.id_transaccion
    AND a.fecha = b.fecha
WHERE a.marketplace = 'ML' AND b.marketplace = 'ML'
  AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
  AND a.clasificacion_operativa LIKE '%Arrepentimiento%'
  AND b.clasificacion_operativa LIKE '%Poscobro%'
  AND a.include_in_operational_pnl = 1 AND b.include_in_operational_pnl = 1
```

### Resultados de estas consultas:

| Consulta | Entradas | Monto | Órdenes |
|----------|----------|-------|---------|
| Pares exactos ambos op_pnl=1 (all-time) | 65 | $2,202,507 | 61 |
| Arre+Posc ambos op_pnl=1 (all-time) | 36 | $1,300,129 | 36 |
| Pares exactos totales (all-time) | 520 | $15,512,381 | 480 |

---

## 6. Verificación por Período

| Período | RN Actual | Inflación Documental | RN Económico | Delta % |
|---------|-----------|---------------------|--------------|---------|
| Abril 2025 | $67,247,555 | $259,180 | $66,988,375 | 0.39% |
| Octubre 2025 | $70,641,011 | $283,878 | $70,357,133 | 0.40% |
| All-time | $842,250,301 | $2,202,507 | $840,047,794 | 0.26% |

---

## Dictamen Final

### PREGUNTA:
**¿Resultado Neto calcula EVENTOS ECONÓMICOS o REGISTROS DEL LEDGER?**

### RESPUESTA: **REGISTROS DEL LEDGER.**

### FAIL: Existe inflación documental confirmada.

**Base legal (SQL):**
```
SELECT SUM(monto) FROM marketplace_ledger_clasificado_v1 
WHERE marketplace=? AND fecha BETWEEN ? AND ?
```
— no hay `GROUP BY id_orden`, no hay deduplicación, no hay neteo causal.

**Base forense:**
- 520 pares exactos ($15.5M) representan el MISMO evento económico registrado bajo 2 conceptos distintos
- 65 de esos pares ($2.2M) tienen ambos `include_in_operational_pnl=1`, afectando directamente al Resultado Neto
- El diseño del `include_in_operational_pnl` es INCONSISTENTE (pares con Mixed op_pnl en 84/121 órdenes en abril)
- No existe trazabilidad desde evento raíz → mecanismo de ejecución → cierre financiero

**Magnitud de la inflación sobre Resultado Neto:**
- Abril 2025: $259,180 (0.39% del RN) — 7 órdenes afectadas
- Octubre 2025: $283,878 (0.40% del RN) — 5 órdenes afectadas
- All-time ML: $2,202,507 (0.26% del RN) — 61 órdenes afectadas

**Conclusiones:**

1. **Estructuralmente, el cierre procesa REGISTROS** — cada fila del ledger contribuye independientemente al resultado sin importar si representa un evento económico único o duplicado.

2. **La inflación actual es acotada** (0.26-0.40% del RN) porque el campo `include_in_operational_pnl` excluye la mayoría de los pares. Sin embargo, este campo no fue diseñado para este propósito — es un subproducto de la clasificación, no un mecanismo de deduplicación.

3. **El riesgo es la INCONSISTENCIA**: el `op_pnl` tiene configuraciones mixtas para el mismo tipo de par (ej: Arre+Posc aparece como 1+1, 1+0, y 0+0). Cualquier cambio futuro en la clasificación podría duplicar la inflación sin que el closing lo detecte.

4. **No existe barrera técnica contra la inflación documental**: el closing no tiene validaciones de unicidad por order_id, ni advertencias cuando un mismo order_id aparece en múltiples conceptos de `ajustes`.

---

*Investigación forense completa. Sin recomendaciones. Sin propuestas de cambio.*
