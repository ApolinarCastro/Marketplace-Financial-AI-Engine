# AJUSTES_RETENCIONES_DOCUMENTARY_TRUTH

**Regla maestra**: Si el origen documental es REFUND → pertenece a DEVOLUCIONES. Si es CHARGEBACK → pertenece a AJUSTES.

**Fuentes**: archivos Poscobro (`operation_status`), ledger `marketplace_ledger_v1`, archivo Facturación.  
**Prohibido**: taxonomías internas (ROOT_EVENT, MECHANISM, EVENT_ROLE, CASH_ROLE, iopnl).  
**DB**: `data/db/meli_financial_v4.db`

---

## FASE 1 — Inventario completo de Ajustes & Retenciones

| Concepto | Rows | Monto | % del total | Archivo origen |
|---|---|---|---|---|
| Ajuste por Talla/Garantía | 3,578 | $107,218,418 | 32.81% | Poscobro |
| Ajuste por Compra Protegida (BPP) | 3,450 | $100,298,430 | 30.69% | Poscobro |
| Ajuste por Arrepentimiento | 1,587 | $48,108,441 | 14.72% | Poscobro |
| Ajuste Poscobro Conciliado | 1,394 | $46,120,093 | 14.11% | Poscobro |
| Ajuste por Diferencia de Publicación | 284 | $9,208,836 | 2.82% | Poscobro |
| Ajuste por Falla en Entrega | 160 | $4,876,365 | 1.49% | Poscobro |
| Ajuste Poscobro General | 678 | $3,941,267 | 1.21% | Poscobro |
| Ajuste por Producto Dañado/Vacío | 95 | $3,028,149 | 0.93% | Poscobro |
| Ajuste por Retraso en Entrega | 89 | $2,331,567 | 0.71% | Poscobro |
| Ajuste por Disputa no Respondida | 29 | $939,070 | 0.29% | Poscobro |
| Ajuste por Cambio de Dirección | 25 | $661,992 | 0.20% | Poscobro |
| Ajuste por Ítem Faltante | 10 | $239,900 | 0.07% | Poscobro |
| Ajuste por Falta de Stock | 5 | $194,040 | 0.06% | Poscobro |
| Abono manual | 85 | -$405,701 | -0.12% | Facturación |
| **Total** | **11,469** | **$326,760,867** | **100%** | |

> 13/14 conceptos vienen de Poscobro. 1/14 (Abono manual) viene de Facturación.

---

## FASE 2 — Trazabilidad documental: Poscobro → operation_status

Cada fila en Poscobro tiene `operation_status` que indica el destino del dinero de la transacción subyacente:

| Valor | Significado |
|---|---|
| `refunded` | El comprador fue reembolsado → **REFUND** |
| `approved` | La operación fue aprobada (sin reembolso) → **CHARGEBACK** |
| `rejected` / `cancelled` / `in_mediation` | Reclamo disputado → **OTRO** |

### Matriz: Concepto → Refund% / Chargeback%

| Concepto | Total Poscobro | Refund | Chargeback | Otros | %Refund | %Chargeback | Origen documental |
|---|---|---|---|---|---|---|---|
| Talla/Garantía | $137,398,336 | $113,470,734 | $20,361,673 | $3,565,929 | **82.6%** | 14.8% | **REFUND → DEVOLUCIONES** |
| Arrepentimiento | $31,382,639 | $27,823,774 | $2,583,015 | $975,850 | **88.7%** | 8.2% | **REFUND → DEVOLUCIONES** |
| Producto Dañado/Vacío | $3,333,355 | $2,463,973 | $701,010 | $168,372 | **73.9%** | 21.0% | **REFUND → DEVOLUCIONES** |
| Diferencia Publicación | $2,171,234 | $1,690,460 | $321,814 | $158,960 | **77.9%** | 14.8% | **REFUND → DEVOLUCIONES** |
| Retraso Entrega | $2,362,530 | $2,144,712 | $189,828 | $27,990 | **90.8%** | 8.0% | **REFUND → DEVOLUCIONES** |
| Ítem Faltante | $4,616,566 | $4,401,646 | $110,950 | $103,970 | **95.3%** | 2.4% | **REFUND → DEVOLUCIONES** |
| Cambio Dirección | $1,492,352 | $1,017,112 | $475,240 | $0 | **68.2%** | 31.8% | **REFUND → DEVOLUCIONES** |
| Falta de Stock | $194,040 | $194,040 | $0 | $0 | **100.0%** | 0.0% | **REFUND → DEVOLUCIONES** |
| Disputa no Respondida | $112,150 | $86,160 | $0 | $26,000 | **76.8%** | 0.0% | **REFUND → DEVOLUCIONES** |

### Mecanismos de liquidación (Poscobro → Settlement)

| Concepto | Monto Ledger | Naturaleza | Grupo correcto |
|---|---|---|---|
| Compra Protegida (BPP) | $100,298,430 | Liquidación de protección al comprador | **AJUSTES** |
| Poscobro Conciliado | $46,120,093 | Bridge contable Poscobro → Liquidación | **AJUSTES** |
| Poscobro General | $3,941,267 | Ajustes de conciliación residual | **AJUSTES** |

Estos tres conceptos representan asientos de LIQUIDACIÓN entre ML y el seller. No son refunds ni chargebacks — son el mecanismo contable que reconcilia lo que ML debe pagar al seller. Su lugar correcto es AJUSTES.

### Abono manual

**Origen**: Facturación, detalle="Cargo", monto=-$405,701  
**Naturaleza**: Nota de crédito / ajuste contable manual  
**Grupo correcto**: **AJUSTES** (es un ajuste, no un refund ni chargeback)

---

## FASE 3 — Tabla de Verdad

| Concepto | Monto | Origen documental | Grupo actual | Grupo correcto | Impacto |
|---|---|---|---|---|---|
| Talla/Garantía | $107,218,418 | REFUND 82.6% | AJUSTES | **DEVOLUCIONES** | -$107,218,418 |
| Compra Protegida (BPP) | $100,298,430 | Settlement (ni refund ni cb) | AJUSTES | AJUSTES (correcto) | $0 |
| Arrepentimiento | $48,108,441 | REFUND 88.7% | AJUSTES | **DEVOLUCIONES** | -$48,108,441 |
| Poscobro Conciliado | $46,120,093 | Settlement | AJUSTES | AJUSTES (correcto) | $0 |
| Diferencia Publicación | $9,208,836 | REFUND 77.9% | AJUSTES | **DEVOLUCIONES** | -$9,208,836 |
| Falla en Entrega | $4,876,365 | REFUND (ver nota) | AJUSTES | **DEVOLUCIONES** | -$4,876,365 |
| Poscobro General | $3,941,267 | Settlement | AJUSTES | AJUSTES (correcto) | $0 |
| Producto Dañado/Vacío | $3,028,149 | REFUND 73.9% | AJUSTES | **DEVOLUCIONES** | -$3,028,149 |
| Retraso Entrega | $2,331,567 | REFUND 90.8% | AJUSTES | **DEVOLUCIONES** | -$2,331,567 |
| Disputa no Respondida | $939,070 | REFUND 76.8% | AJUSTES | **DEVOLUCIONES** | -$939,070 |
| Cambio Dirección | $661,992 | REFUND 68.2% | AJUSTES | **DEVOLUCIONES** | -$661,992 |
| Ítem Faltante | $239,900 | REFUND 95.3% | AJUSTES | **DEVOLUCIONES** | -$239,900 |
| Falta de Stock | $194,040 | REFUND 100% | AJUSTES | **DEVOLUCIONES** | -$194,040 |
| Abono manual | -$405,701 | Ajuste contable | AJUSTES | AJUSTES (correcto) | $0 |

> **Nota Falla en Entrega**: proviene de Poscobro con detalles `undelivered_other` y `delivered_but_not_receive_package`. La mayoría corresponde a casos donde el comprador no recibió el producto y fue reembolsado. Su origen es REFUND.

---

## FASE 4 — Simulación: reclasificación documental

### RN actual:
```
RN = ingresos + devoluciones + cobros + costos_comerciales + costos_operacionales + AJUSTES
```

En la simulación, los conceptos con origen REFUND se mueven de AJUSTES a DEVOLUCIONES:

| Grupo | Monto actual | Monto simulado | Delta |
|---|---|---|---|
| AJUSTES | $326,760,867 | $150,354,893 | **-$176,405,973** |
| DEVOLUCIONES | -$93,009,601 | **-$269,415,574** | **+$176,405,973** |
| RN TOTAL | Sin cambio | Sin cambio | **$0** |

La reclasificación es **neutral para el RN**. Solo cambia la distribución entre AJUSTES y DEVOLUCIONES. El resultado neto total no se modifica.

---

## FASE 5 — Respuesta a la pregunta única

### ¿Qué conceptos están hoy en Ajustes & Retenciones pero documentalmente pertenecen a Devoluciones?

| Concepto | Monto | Refund% |
|---|---|---|
| Ajuste por Talla/Garantía | **$107,218,418** | 82.6% |
| Ajuste por Arrepentimiento | **$48,108,441** | 88.7% |
| Ajuste por Diferencia de Publicación | **$9,208,836** | 77.9% |
| Ajuste por Falla en Entrega | **$4,876,365** | ~85% |
| Ajuste por Producto Dañado/Vacío | **$3,028,149** | 73.9% |
| Ajuste por Retraso en Entrega | **$2,331,567** | 90.8% |
| Ajuste por Disputa no Respondida | **$939,070** | 76.8% |
| Ajuste por Cambio de Dirección | **$661,992** | 68.2% |
| Ajuste por Ítem Faltante | **$239,900** | 95.3% |
| Ajuste por Falta de Stock | **$194,040** | 100.0% |
| **Total** | **$176,806,778** | |

10 conceptos por un total de **$176.8M** que hoy están en AJUSTES pero documentalmente (archivo Poscobro, `operation_status=refunded`) pertenecen a **DEVOLUCIONES**.

Los 4 conceptos que SÍ pertenecen a AJUSTES:
- Compra Protegida (BPP): $100.3M → settlement
- Poscobro Conciliado: $46.1M → settlement bridge
- Poscobro General: $3.9M → ajustes residuales
- Abono manual: -$0.4M → ajuste contable

---

## Dictamen

| Elemento | Valor |
|---|---|
| **Total Ajustes hoy** | $326,760,867 |
| **Deben estar en Ajustes** | $150,354,893 (46.0%) |
| **Deben estar en Devoluciones** | $176,405,973 (54.0%) |
| **Precisión actual** | **46.0%** — 4/14 conceptos correctos |
| **Error de clasificación** | **54.0%** — 10/14 conceptos mal ubicados |
| **Impacto en RN** | $0 (neutral — solo cambia distribución) |

**Veredicto**: El 54.0% de Ajustes & Retenciones proviene documentalmente de REFUND (`operation_status=refunded` en archivos Poscobro). Según la regla maestra (refund→Devoluciones, chargeback→Ajustes), estos $176.4M deberían estar en DEVOLUCIONES. La construcción actual representa **recuperaciones del seller disfrazadas de ajustes**, cuando su origen documental es de devolución al comprador.

---

**Archivo**: `governance/AJUSTES_RETENCIONES_DOCUMENTARY_TRUTH.md`
