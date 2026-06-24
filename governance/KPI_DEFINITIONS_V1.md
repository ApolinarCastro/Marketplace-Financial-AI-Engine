# KPI Definitions v1.0

*Certified 2026-06-05 per RFC Financial Truth Consolidation (DEC-001)*

---

## Ventas

| Propiedad | Definición |
|-----------|-----------|
| **Source** | `marketplace_ledger_v1` |
| **Filtro** | `financial_group = 'ingresos'` |
| **Incluye** | Comisiones por venta, fees de marketplace cobrados a Eccsa |
| **Excluye** | GMV (valor de venta al consumidor), devoluciones, ajustes, costos operacionales |
| **Fórmula** | `SUM(monto) WHERE financial_group = 'ingresos'` |
| **Signo** | Positivo |
| **Dashboard** | KPI card "Ventas" en UX1.1 (borde azul) |
| **API** | `/api/v4/exec/summary` → `total_ventas` |

**Nota**: Representa el ingreso por servicios de marketplace, NO el valor bruto de las ventas a consumidores.

---

## Devoluciones

| Propiedad | Definición |
|-----------|-----------|
| **Source** | `marketplace_ledger_v1` |
| **Filtro** | `financial_group = 'devoluciones'` |
| **Incluye** | Devoluciones de productos clasificadas vía pipeline ETL |
| **Excluye** | Chargebacks de Poscobro no clasificados como devolución pura, claims, ajustes por BPP |
| **Fórmula** | `SUM(monto) WHERE financial_group = 'devoluciones'` |
| **Signo** | Negativo (reduce Ventas) |
| **Dashboard** | KPI card "Devoluciones" en UX1.1 (borde rojo) |
| **API** | `/api/v4/exec/summary` → `total_devoluciones` |

---

## Disponible

| Propiedad | Definición |
|-----------|-----------|
| **Source** | `marketplace_cierre_financiero_v1` |
| **Filtro** | `periodo_inicio` = primer día del período |
| **Incluye** | Ingresos + Costos Operacionales + Costos Comerciales + Ajustes (incl. recoveries) |
| **Excluye** | N/A — es el resultado integral del período |
| **Fórmula** | `resultado_neto` = `total_ingresos + total_costos_operacionales + total_costos_comerciales + total_ajustes` |
| **Signo** | Positivo |
| **Dashboard** | KPI card "Disponible" en UX1.1 (borde verde, mayor tamaño) |
| **API** | `/api/v4/exec/summary` → `total_disponible` |

**Nota**: Es el resultado neto certificado del período. Incluye todos los ajustes (BPP, arrepentimiento, garantías, conciliados, etc.)

---

## Cobros

| Propiedad | Definición |
|-----------|-----------|
| **Source** | Computado desde `marketplace_cierre_financiero_v1` + `marketplace_ledger_v1` |
| **Filtro** | Mismo período |
| **Incluye** | Comisiones, Logística, Publicidad, Fulfillment, Acuerdos Comerciales, Bonificaciones, Otros |
| **Excluye** | Ventas, Devoluciones, Disponible (son los otros 3 KPIs) |
| **Fórmula** | `Ventas + Devoluciones - Disponible` |
| **Signo** | Convención: display como valor absoluto (es neto de costos) |
| **Dashboard** | KPI card "Cobros" en UX1.1 (borde naranja) + desglose por componente en matriz |
| **API** | `/api/v4/cierre/desglose` → breakdown por concepto |

**Nota**: Cobros NO es un concepto contable directo sino la diferencia económica entre Ventas, Devoluciones y Disponible. Su desglose por componente (comisiones, logística, publicidad, etc.) se obtiene de `marketplace_cierre_financiero_v1` y `marketplace_ledger_clasificado_v1`.

---

## Validación

| Check | Resultado |
|-------|-----------|
| **Consistencia** | Ventas - Devoluciones - Cobros = Disponible |
| **Trazabilidad** | RAW → ETL → Ledger → Cierre → API → Dashboard |
| **Regression** | 14/14 tests PASS |
| **Certificación** | B2.2 (Dashboard vs DB, $0 delta), G5.6 (Revenue Engine, 4 PASS) |
