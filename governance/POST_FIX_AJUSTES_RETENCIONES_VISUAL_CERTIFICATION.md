# AJUSTES_RETENCIONES_VISUAL_CERTIFICATION

**Fecha:** 2026-06-06  
**DB:** `data/db/meli_financial_v4.db`  
**Registros:** EVENT_REGISTRY_V2, CASH_ROLE_REGISTRY_V1, FINANCIAL_STRUCTURE  
**Fix verificado:** `MECANISMOS_EXCLUIDOS` en `run_financial_closing()`  

---

## Validación 1: ¿Algún MECHANISM en el RN?

**NO.** Los 3 MECHANISMS de ML están excluidos del cierre por `MECANISMOS_EXCLUIDOS`:

| MECHANISM | Monto bruto | ¿En cierre? | Evidencia |
|---|---|---|---|
| Ajuste por Compra Protegida (BPP) | $100,298,430 | ❌ Excluido | `NOT IN (MECANISMOS_EXCLUIDOS)` |
| Ajuste Poscobro Conciliado | $46,120,093 | ❌ Excluido | `NOT IN (MECANISMOS_EXCLUIDOS)` |
| Ajuste Poscobro General | $3,941,267 | ❌ Excluido | `NOT IN (MECANISMOS_EXCLUIDOS)` |

**Total excluido: $150,359,790** — 0% en RN. PARIS, RIPLEY, FALABELLA no tienen MECHANISMS.

---

## Validación 2: ¿Algún concepto excluido suma al RN?

**NO.** El filtro `WHERE ... AND clasificacion_operativa NOT IN (...)` se aplica en la query SQL del cierre. Los $150.4M de MECANISMOS no aparecen en `total_ajustes` ni en `resultado_neto` de ninguna fila de `marketplace_cierre_financiero_v1`.

---

## Validación 3: ¿Cada concepto visible es ECONOMIC_EVENT / ROOT_EVENT?

**SÍ — 100% ROOT_EVENT.** Desglose por marketplace:

### ML — 11 ROOT_EVENTS visibles en Ajustes & Retenciones

| Concepto | Clasificación | Cash Role | Incluido en RN |
|---|---|---|---|
| Ajuste por Talla/Garantía | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Arrepentimiento | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Diferencia de Publicación | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Producto Dañado/Vacío | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Falla en Entrega | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Retraso en Entrega | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Disputa no Respondida | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Cambio de Dirección | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Ítem Faltante | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Ajuste por Falta de Stock | ROOT_EVENT | REAL_CASH | ✅ Sí |
| Abono manual | ROOT_EVENT | REAL_CASH | ✅ Sí |

Los 3 MECHANISMS (BPP $100.3M, Poscobro Conciliado $46.1M, Poscobro General $3.9M) están **EXCLUIDOS** de la UI.

### PARIS — 5 ROOT_EVENTS

| Concepto | Clasificación | Cash Role | Incluido en RN |
|---|---|---|---|
| Compensación logística | ROOT_EVENT | UNASSIGNED | ✅ Sí |
| Ajuste Inventario Activo | ROOT_EVENT | UNASSIGNED | ✅ Sí |
| Merma | ROOT_EVENT | UNASSIGNED | ✅ Sí |
| Cobro por campaña | ROOT_EVENT | UNASSIGNED | ✅ Sí |
| Abono manual | ROOT_EVENT | UNASSIGNED | ✅ Sí |

### RIPLEY — 2 ROOT_EVENTS

| Concepto | Clasificación | Cash Role | Incluido en RN |
|---|---|---|---|
| Descuento por cancelación | ROOT_EVENT | UNASSIGNED | ✅ Sí |
| Otros descuentos | ROOT_EVENT | UNASSIGNED | ✅ Sí |

### FALABELLA — 2 ROOT_EVENTS

| Concepto | Clasificación | Cash Role | Incluido en RN |
|---|---|---|---|
| Corrección de pago envio directo | ROOT_EVENT | UNASSIGNED | ✅ Sí |
| Corrección de cobro por envío directo | ROOT_EVENT | UNASSIGNED | ✅ Sí |

---

## Validación 4: Tabla de certificación final

### ML

| Concepto | Clasificación | Impacta Caja | Impacta RN | Impacta Disponible | Estado |
|---|---|---|---|---|---|
| Ajuste por Talla/Garantía | ROOT_EVENT | ✅ REAL_CASH (+$107.2M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Arrepentimiento | ROOT_EVENT | ✅ REAL_CASH (+$48.1M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Diferencia Publicación | ROOT_EVENT | ✅ REAL_CASH (+$9.2M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste Producto Dañado/Vacío | ROOT_EVENT | ✅ REAL_CASH (+$3.0M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Falla en Entrega | ROOT_EVENT | ✅ REAL_CASH (+$4.9M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Retraso en Entrega | ROOT_EVENT | ✅ REAL_CASH (+$2.3M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Disputa no Respondida | ROOT_EVENT | ✅ REAL_CASH (+$0.9M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Cambio de Dirección | ROOT_EVENT | ✅ REAL_CASH (+$0.7M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Ítem Faltante | ROOT_EVENT | ✅ REAL_CASH (+$0.2M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Falta de Stock | ROOT_EVENT | ✅ REAL_CASH (+$0.2M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Abono manual | ROOT_EVENT | ✅ REAL_CASH (-$0.4M) | ✅ Sí | ✅ Vía RN | CERTIFICADO |
| Ajuste por Compra Protegida (BPP)* | MECHANISM | ❌ MIRROR_ZERO | ❌ Excluido | ❌ NET=$0 | EXCLUIDO |
| Ajuste Poscobro Conciliado* | MECHANISM | ❌ MIRROR_ZERO | ❌ Excluido | ❌ NET=$0 | EXCLUIDO |
| Ajuste Poscobro General* | MECHANISM | ❌ MIRROR_ZERO | ❌ Excluido | ❌ NET=$0 | EXCLUIDO |

*\*No visibles en la UI — excluidos por MECANISMOS_EXCLUIDOS*

### PARIS

| Concepto | Clasificación | Impacta Caja | Impacta RN | Impacta Disponible | Estado |
|---|---|---|---|---|---|
| Compensación logística | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (+$1.6M) | ✅ Vía RN | CERTIFICADO |
| Ajuste Inventario Activo | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (+$0.6M) | ✅ Vía RN | CERTIFICADO |
| Merma | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (+$0.02M) | ✅ Vía RN | CERTIFICADO |
| Cobro por campaña | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (-$0.3M) | ✅ Vía RN | CERTIFICADO |
| Abono manual | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (-$0.6M) | ✅ Vía RN | CERTIFICADO |

### RIPLEY

| Concepto | Clasificación | Impacta Caja | Impacta RN | Impacta Disponible | Estado |
|---|---|---|---|---|---|
| Descuento por cancelación | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (-$28K) | ✅ Vía RN | CERTIFICADO |
| Otros descuentos | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (-$5K) | ✅ Vía RN | CERTIFICADO |

### FALABELLA

| Concepto | Clasificación | Impacta Caja | Impacta RN | Impacta Disponible | Estado |
|---|---|---|---|---|---|
| Corrección de pago envio directo | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (+$3K) | ✅ Vía RN | CERTIFICADO |
| Corrección de cobro por envío directo | ROOT_EVENT | 🟡 UNASSIGNED | ✅ Sí (-$4K) | ✅ Vía RN | CERTIFICADO |

---

## Evidencia de impacto

### Impacto en Caja (ML — certificado con Liberaciones)

Cash evidence: Liberaciones file (5,142 rows, $259.8M gross, $69.9M net). 3.9% delta vs DB. Mediación directa ($10.5M outflow) traced to root events.

- ML ROOT_EVENTs (ajustes): **$176.4M total** — todos REAL_CASH con evidencia de Liberaciones o Mediación
- ML MECHANISMs: **MIRROR_ZERO** — reserve_for_dispute NET=$0, paired con ROOT_EVENTs
- PARIS/RIPLEY/FALABELLA: **UNASSIGNED** — sin Liberaciones, default ACCRUAL

### Impacto en RN

Los $176.4M de ROOT_EVENTs en ML impactan el RN vía `total_ajustes` en el cierre:
- ML RN total: $712,045,128
- ML ajustes visibles (total_ajustes en cierre): $83,391,476 (incluye devoluciones + ROOT_EVENTs ajustes)
- Impacto neto de ROOT_EVENTs en RN: $176.4M (bruto ajustes) — antes del neteo con devoluciones

### Impacto en Disponible

Disponible = resultado_neto (por definición oficial `marketplace_cierre_financiero_v1`):
- ML Disponible: $712,045,128
- PARIS: $337,418,552
- RIPLEY: $206,946,843
- FALABELLA: $7,676,485

ROOT_EVENTs impactan Disponible indirectamente vía RN (son eventos económicos reales con impacto en caja o accrual).

---

## VEREDICTO: **PASS** ✅

1. **0 MECHANISMS en RN** — BPP/Poscobro excluidos por `MECANISMOS_EXCLUIDOS` ($150.4M)
2. **0 conceptos excluidos sumando** — Filtro `NOT IN` verificado en la query SQL
3. **100% ROOT_EVENT** — Todos los conceptos visibles en Ajustes & Retenciones son ECONOMIC_EVENT certificados
4. **Cash impact** — ML: 11/11 ROOT_EVENTs tienen REAL_CASH; PARIS/RIPLEY/FALABELLA: UNASSIGNED (default ACCRUAL)
5. **RN impact** — Todos los ROOT_EVENTs visibles impactan el RN certificado
6. **Disponible impact** — Vía RN, sin bypass

**La UI comunica correctamente:** Los conceptos en "Ajustes & Retenciones" son eventos económicos reales (ROOT_EVENTs). Los mecanismos contables (BPP/Poscobro) están fuera del RN y no son visibles en el resultado financiero.
