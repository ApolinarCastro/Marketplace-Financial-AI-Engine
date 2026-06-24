# RFC_FINANCIAL_STRUCTURE_REDESIGN

**Fecha**: 2026-06-05
**DB**: `data/db/meli_financial_v4.db`
**READ ONLY**: Sin implementación, sin cambios, sin código.

---

## DICTAMEN CENTRAL: FAIL

**La estructura financiera actual NO representa la realidad económica.**

**Certificación Shopify: FAIL condicional — imposible en estado actual.**

---

## FASE 1 — INVENTARIO Y CLASIFICACIÓN

### Estructura Actual (37 conceptos activos en ML)

| Grupo | Conceptos | % del total |
|---|---|---|
| **ingresos** | Cargo por venta (Venta), Bonificación | 100% eventos reales |
| **devoluciones** | Devolución de venta | 100% evento real |
| **costos_operacionales** | Envíos, Fulfillment, Almacenamiento | 100% eventos reales |
| **costos_comerciales** | Comisiones, Publicidad, Honorarios | 100% eventos reales |
| **ajustes** | 14 conceptos* | **MEZCLA eventos reales + mecanismos** |
| **tesoreria** | Retiro de dinero | Treasury |

*\* Incluye Talla/Garantía (evento), Arrepentimiento (evento), BPP (mecanismo), Poscobro (mecanismo), y otros.*

### Clasificación Económica por Concepto

| Concepto | Clasificación | P&L | Auditoría |
|---|---|---|---|
| **Cargo por venta (Venta)** | A) Evento Económico — Ingreso directo | SI | NO |
| **Bonificación** | A) Evento Económico — Rebate comercial | SI | NO |
| **Devolución de venta** | A) Evento Económico — Contraparte del ingreso | SI | NO |
| **Cargo por envíos/ML Envíos** | A) Evento Económico — Logística | SI | NO |
| **Cargo por devolución** | A) Evento Económico — Logística revertida | SI | NO |
| **Cargo por venta (Comisión)** | A) Evento Económico — Comisión ML | SI | NO |
| **Anulación del cargo por venta** | A) Evento Económico — Reverso de comisión | SI | NO |
| **Cargo por publicidad (Product/Brand/Display)** | A) Evento Económico — Gasto en ads | SI | NO |
| **Cargo por Asesoría Comercial** | A) Evento Económico — Honorarios fijos | SI | NO |
| **Cargo por mantenimiento** | A) Evento Económico — Suscripción | SI | NO |
| **Cargo por Full (retiro/almacenaje/exceso)** | A) Evento Económico — Fulfillment | SI | NO |
| **Ajuste por Talla/Garantía** | **A) Evento Económico Raíz (Postventa)** | **SI** | SI |
| **Ajuste por Arrepentimiento** | **A) Evento Económico Raíz (Postventa)** | **SI** | SI |
| **Ajuste por Falla en Entrega** | A) Evento Económico Postventa | SI | SI |
| **Ajuste por Retraso en Entrega** | A) Evento Económico Postventa | SI | SI |
| **Ajuste por Producto Dañado** | A) Evento Económico Postventa | SI | SI |
| **Ajuste por Cambio de Dirección** | A) Evento Económico Postventa | SI | SI |
| **Ajuste por Ítem Faltante** | A) Evento Económico Postventa | SI | SI |
| **Ajuste por Diferencia de Publicación** | E) Mixto — Casuístico | SI | SI |
| **Ajuste por Disputa no Respondida** | E) Mixto — Depende del caso | SI | SI |
| **Ajuste por Falta de Stock** | E) Mixto — Penalización | SI | SI |
| **Abono manual** | E) Mixto — Correcciones manuales | SI | SI |
| **Ajuste por Compra Protegida (BPP)** | **B) Mecanismo de Ejecución** | **NO** | **SI** |
| **Ajuste Poscobro Conciliado** | **B) Mecanismo de Ejecución** | **NO** | **SI** |
| **Ajuste Poscobro General** | **B) Mecanismo de Ejecución** | **NO** | **SI** |

---

## FASE 2 — MODELO ACTUAL vs MODELO ECONÓMICO

### Abril 2025

| Métrica | Modelo Actual | Modelo Económico | Delta |
|---|---|---|---|
| Resultado Neto | $67,247,555 | $64,315,098 | **$2,932,457 (4.36%)** |

### Octubre 2025

| Métrica | Modelo Actual | Modelo Económico | Delta |
|---|---|---|---|
| Resultado Neto | $70,641,011 | $65,941,333 | **$4,699,678 (6.65%)** |

### All-time ML

| Métrica | Modelo Actual | Modelo Económico | Delta |
|---|---|---|---|
| Resultado Neto | $842,250,301 | $758,077,921 | **$84,172,380 (9.99%)** |

### Descomposición del Ajuste (All-time)

| Componente | Monto | % del RN |
|---|---|---|
| Mecanismos pareados eliminados (BPP+Poscobro) | -$92,991,861 | -11.04% |
| Mecanismos standalone preservados | +$8,819,481 | +1.05% |
| **Ajuste neto al RN** | **-$84,172,380** | **-9.99%** |

---

## FASE 3 — ESTRUCTURA vs DRILL DOWN vs AUDITORÍA

### Nivel 1: Financial Structure (P&L Oficial)
Solo eventos económicos reales. Refleja la realidad económica del negocio.

```
FINANCIAL STRUCTURE:
├── Ingresos (Ventas netas)
│   ├── Cargo por venta (Venta)
│   └── Bonificación
├── Devoluciones
│   └── Devolución de venta
├── Costos Operacionales
│   ├── Envíos (Cargo por envíos ML / Mercado Envíos)
│   └── Devoluciones (Cargo por devolución)
├── Costos Comerciales
│   ├── Comisiones (Cargo por venta (Comisión))
│   ├── Publicidad (Product Ads / Brand Ads / Display)
│   ├── Servicios (Asesoría, Mantenimiento)
│   └── Fulfillment (Retiro, Almacenaje, Exceso, Stock antiguo)
├── Eventos Postventa
│   ├── Talla/Garantía (cash real confirmado)
│   ├── Arrepentimiento (cash real confirmado)
│   ├── Falla en Entrega
│   ├── Retraso en Entrega
│   ├── Producto Dañado
│   ├── Cambio de Dirección
│   └── Ítem Faltante
└── Resultado Neto
```

### Nivel 2: Drill Down (Desglose de Postventa)
Desglose detallado de eventos postventa y ajustes. Separa eventos de mecanismos.

```
DRILL DOWN — EVENTOS POSTVENTA:
├── Por tamaño (Talla/Garantía): $101.1M
│   ├── bigger_than_expected
│   ├── smaller_than_expected
│   ├── not_match_size_guide
│   └── different_color_or_size_fashion
├── Por arrepentimiento: $43.2M
│   └── undelivered_repentant_buyer
├── Por logística ML: $7.0M (Falla, Retraso, Cambio, Dañado, Faltante)
└── Mixtos: $9.3M (Diferencia, Disputa, Stock, Manual)
```

### Nivel 3: Auditoría (Trazabilidad Completa)
Trazabilidad completa incluyendo mecanismos. Vincula con archivos fuente de ML.

```
AUDITORÍA — TRAZABILIDAD:
├── Eventos Postventa (los mismos del Nivel 2)
│   └── Trazables a: Liberaciones (Mediación)
└── Mecanismos de Ejecución (SOLO AQUÍ)
    ├── BPP ($95.2M) — Reserva contable pareada con Talla/Garantía (82.9%)
    │   └── Trazable a: Liberaciones (reserve_for_dispute, NETO CERO)
    ├── Poscobro Conciliado ($44.4M) — Intento de cobro pareado con Talla (26.4%)
    │   └── Trazable a: Liberaciones (reserve_for_dispute, NETO CERO)
    └── Poscobro General ($3.6M) — Intento de cobro general
```

---

## FASE 4 — PROPUESTA CONCEPTUAL

### Estructura Financiera Propuesta

```
GRUPOS (5 → 6):
                                                 Incluye
┌─ Ingresos                    (sin cambio)      Venta, Bonificación
├─ Devoluciones                (sin cambio)      Devolución de venta
├─ Costos Operacionales        (sin cambio)      Envíos, Devolución logística
├─ Costos Comerciales          (sin cambio)      Comisiones, Publicidad, Servicios, Full
├─ Eventos Postventa           (NUEVO)           Talla, Arrepentimiento, Falla, Retraso, Dañado
└─ Resultado Neto              (sin cambio)      Suma de todos los grupos
```

### Reglas de Clasificación

| Si el concepto es... | Entonces... |
|---|---|
| Un ingreso por venta de producto | → `ingresos` |
| Una devolución de producto | → `devoluciones` |
| Un costo de logística/operación | → `costos_operacionales` |
| Una comisión, publicidad, o servicio | → `costos_comerciales` |
| Un evento postventa CON cash outflow real | → `eventos_postventa` |
| Un mecanismo de ejecución de ML SIN cash | → **NO en estructura** (solo auditoría) |

### Mecanismos Excluidos (solo auditoría)

```
BPP:              Mecanismo de reserva. Excluir del P&L.
                  Trazable a: reserve_for_dispute en Liberaciones (NETO CERO).
                  Información preservada vía Talla/Garantía (82.9% overlap).

Poscobro:         Mecanismo de cobro. Excluir del P&L.
                  Trazable a: reserve_for_dispute en Liberaciones (NETO CERO).
                  Información preservada vía Talla/Garantía (26.4%) o Arrepentimiento (27.4%).
```

---

## FASE 5 — IMPACTO FINANCIERO

### Por Período

| Período | RN Actual | Mecanismos | RN Económico | Delta $ | Delta % |
|---|---|---|---|---|---|
| 2025-01 | $23,328,848 | -$3,672,901 | $19,655,947 | -$3,672,901 | -15.7% |
| 2025-02 | $21,338,230 | -$2,894,511 | $18,443,719 | -$2,894,511 | -13.6% |
| 2025-03 | $55,466,167 | -$5,671,890 | $49,794,277 | -$5,671,890 | -10.2% |
| 2025-04 | $67,247,555 | -$2,932,457 | $64,315,098 | -$2,932,457 | -4.4% |
| 2025-05 | $83,423,022 | -$10,812,390 | $72,610,632 | -$10,812,390 | -13.0% |
| 2025-06 | $70,590,065 | -$8,738,990 | $61,851,075 | -$8,738,990 | -12.4% |
| 2025-07 | $57,079,564 | -$8,131,040 | $48,948,524 | -$8,131,040 | -14.2% |
| 2025-08 | $41,704,099 | -$6,045,360 | $35,658,739 | -$6,045,360 | -14.5% |
| 2025-09 | $44,139,775 | -$5,878,410 | $38,261,365 | -$5,878,410 | -13.3% |
| 2025-10 | $70,641,011 | -$4,699,678 | $65,941,333 | -$4,699,678 | -6.7% |
| 2025-11 | $86,810,046 | -$11,783,911 | $75,026,135 | -$11,783,911 | -13.6% |
| 2025-12 | $83,809,802 | -$11,782,540 | $72,027,262 | -$11,782,540 | -14.1% |
| **Total** | **$842,250,301** | **-$84,172,380** | **$758,077,921** | **-$84,172,380** | **-10.0%** |

### Descomposición del Delta (All-time)

| Componente | Monto |
|---|---|
| Paired BPP eliminado (Talla+BPP) | -$63,329,912 |
| Paired Poscobro eliminado (Poscobro+Arre/Talla) | -$29,661,949 |
| Standalone BPP preservado | +$4,112,345 |
| Standalone Poscobro preservado | +$4,707,136 |
| **Ajuste neto** | **-$84,172,380** |

---

## MATRIZ DE CLASIFICACIÓN (Extendida)

| Concepto | Evento | Mecanismo | P&L | Auditoría | Notas |
|---|---|---|---|---|---|
| Cargo por venta (Venta) | SI | - | SI | - | Ingreso directo |
| Bonificación | SI | - | SI | - | Rebate |
| Devolución de venta | SI | - | SI | - | Contraparte |
| Cargo por envíos ML | SI | - | SI | - | Logística real |
| Cargo por devolución | SI | - | SI | - | Logística revertida |
| Cargo por venta (Comisión) | SI | - | SI | - | Comisión ML |
| Anulación cargo venta | SI | - | SI | - | Reverso comisión |
| Carga publicidad | SI | - | SI | - | Gasto real |
| Cargo Asesoría/Mant. | SI | - | SI | - | Servicio fijo |
| Cargo Full (todos) | SI | - | SI | - | Fulfillment real |
| **Talla/Garantía** | **SI*** | **NO** | **SI** | **SI** | **Evento raíz postventa** |
| **Arrepentimiento** | **SI*** | **NO** | **SI** | **SI** | **Evento raíz postventa** |
| Falla en Entrega | SI | - | SI | SI | Evento postventa |
| Retraso en Entrega | SI | - | SI | SI | Evento postventa |
| Producto Dañado | SI | - | SI | SI | Evento postventa |
| Cambio de Dirección | SI | - | SI | SI | Evento postventa |
| Ítem Faltante | SI | - | SI | SI | Evento postventa |
| Diferencia Publicación | E) Mixto | - | SI | SI | Casuístico |
| Disputa no Respondida | E) Mixto | - | SI | SI | Casuístico |
| Falta de Stock | E) Mixto | - | SI | SI | Penalización |
| Abono manual | E) Mixto | - | SI | SI | Corrección |
| **BPP** | **NO** | **SI** | **NO** | **SI** | **Reserva contable, neto cero** |
| **Poscobro Conciliado** | **NO** | **SI** | **NO** | **SI** | **Cobro, neto cero** |
| **Poscobro General** | **NO** | **SI** | **NO** | **SI** | **Cobro, neto cero** |

*\* Evento raíz confirmado por RFC_POSCOBRO_CAUSALITY_FINAL*

---

## DICTAMEN FINAL

### Pregunta 1: ¿La estructura financiera actual representa la realidad económica?

### FAIL

**Razones:**

1. **Mezcla de eventos y mecanismos**: La categoría `ajustes` contiene tanto eventos económicos reales (Talla/Garantía, Arrepentimiento) como mecanismos de ejecución de ML (BPP, Poscobro) que representan el MISMO evento económico bajo distinto nombre.

2. **Inflación documental**: 46.71% del total de ajustes ($143.2M de $306.6M) corresponde a mecanismos de ejecución (BPP + Poscobro) que no representan eventos económicos independientes.

3. **Ausencia de separación postventa**: No existe una categoría `eventos_postventa` que aísle los eventos posteriores a la venta del core P&L, mezclándolos con ajustes misceláneos.

4. **Riesgo de doble conteo**: El 9.99% del Resultado Neto all-time ($84.2M) corresponde a mecanismos que duplican eventos ya registrados.

### Pregunta 2: ¿Puede certificarse para Shopify?

### FAIL condicional — NO en estado actual.

**Barreras para Shopify:**

| Requisito Shopify | Estado | Detalle |
|---|---|---|
| Single Source of Truth | **NO** | BPP/Poscobro crean doble representación |
| Trail balance sin inflación | **NO** | $84.2M de inflación documental all-time |
| Cada transacción = 1 evento económico | **NO** | 82.9% de BPP duplica Talla/Garantía |
| GAAP/IFRS compatible | **NO** | Mezcla reservas contables con P&L real |

**Lo que se requiere para certificar:**

1. **Separar** `ajustes` en dos: `eventos_postventa` (económicos) + `mecanismos_ejecucion` (trazabilidad)
2. **Mover** BPP y Poscobro a tabla de trazabilidad exclusivamente (Nivel 3)
3. **Crear** la categoría `eventos_postventa` en el P&L visible
4. **Recalcular** Resultado Neto sin mecanismos de ejecución pareados
5. **Preservar** mecanismos standalone como eventos económicos (representan pérdida real cuando no hay evento raíz)

**Después de estas correcciones, el modelo SÍ sería certificable.** La data subyacente es correcta — el problema es exclusivamente de clasificación y agregación, no de integridad de datos.

---

## Evidencia SQL Reproductible

```sql
-- Query 1: TOTAL de mecanismos en ajustes (all-time ML)
SELECT SUM(monto) as total_mecanismos
FROM marketplace_ledger_v1
WHERE marketplace = 'ML' AND financial_group = 'ajustes'
  AND clasificacion_operativa IN (
      'Ajuste por Compra Protegida (BPP)',
      'Ajuste Poscobro Conciliado',
      'Ajuste Poscobro General'
  );
-- Result: $143,225,533.93 (46.71% de ajustes)

-- Query 2: Pares BPP+Talla con montos exactos
SELECT COUNT(*) as pairs, ROUND(SUM(a.monto),2) as total
FROM marketplace_ledger_v1 a
JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden
    AND a.monto = b.monto
WHERE a.clasificacion_operativa = 'Ajuste por Talla/Garantía'
  AND b.clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)'
  AND a.marketplace = 'ML';
-- Result: 2,818 pairs, $63,329,912.40

-- Query 3: Mecanismos standalone (sin evento raíz)
SELECT clasificacion_operativa, COUNT(*) as standalone_orders,
       ROUND(SUM(monto),2) as total
FROM marketplace_ledger_v1
WHERE marketplace = 'ML' AND financial_group = 'ajustes'
  AND (clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)'
       OR clasificacion_operativa LIKE '%Poscobro%')
  AND id_orden IN (
      SELECT id_orden FROM marketplace_ledger_v1
      WHERE marketplace = 'ML' AND financial_group = 'ajustes'
      GROUP BY id_orden HAVING COUNT(DISTINCT clasificacion_operativa) = 1
  )
GROUP BY clasificacion_operativa;
-- BPP standalone: 39 orders, $4.1M
-- Poscobro standalone: ~36 orders, $4.7M

-- Query 4: Resultado Neto Económico (propuesta)
WITH paired_mechanisms AS (
    SELECT DISTINCT a.id_transaccion
    FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden
    WHERE a.marketplace = 'ML' AND b.marketplace = 'ML'
      AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
      AND (
          (a.clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)'
           AND b.clasificacion_operativa = 'Ajuste por Talla/Garantía')
          OR
          (a.clasificacion_operativa LIKE '%Poscobro%'
           AND (b.clasificacion_operativa = 'Ajuste por Arrepentimiento'
                OR b.clasificacion_operativa = 'Ajuste por Talla/Garantía'))
      )
)
SELECT ROUND(SUM(monto), 2) as economic_rn
FROM marketplace_ledger_v1
WHERE marketplace = 'ML'
  AND id_transaccion NOT IN (SELECT id_transaccion FROM paired_mechanisms);
-- All-time ML Economic RN: $758,077,920.72
```
