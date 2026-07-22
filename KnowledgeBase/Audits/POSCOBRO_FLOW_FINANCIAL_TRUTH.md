# POSCOBRO_FLOW_FINANCIAL_TRUTH

**Base**: 11,914 rows, 5 archivos Poscobro. Campo FLOW como clasificador primario.

---

## FASE 1 — Inventario de FLOW

Solo existen **3 valores únicos** de FLOW en todo el universo Poscobro:

| Flow | Rows | Monto | %Rows | %Monto |
|---|---|---|---|---|
| `claim` | 6,158 | $183,063,202 | 51.7% | 54.1% |
| `refund` | 5,749 | $154,945,450 | 48.3% | 45.8% |
| `chargeback` | 7 | $212,930 | 0.1% | 0.1% |
| **Total** | **11,914** | **$338,221,582** | **100%** | **100%** |

No hay otros valores. No hay nulos. No hay variantes.

---

## FASE 2 — Naturaleza económica por FLOW

### `flow='claim'` (54.1% del monto)

| Atributo | Valor |
|---|---|
| **Signo monto** | 100% positivo |
| **Operation status** | 83.3% refunded, 14.1% approved, 2.0% rejected |
| **status_detail** | **VACÍO** (0 valores) |
| **reason_detail** | 31 variantes (ej: bigger_than_expected_fashion, repentant_buyer) |
| **resolution** | 80% "complainant" (comprador gana) |

**Naturaleza**: **RECLAMO / DISPUTA**. El comprador inicia un reclamo contra el vendedor. ML resuelve a favor del comprador y cobra al vendedor el monto del reembolso. Es una **RECUPERACIÓN** — ML recupera del vendedor el costo de la devolución.

### `flow='refund'` (45.8% del monto)

| Atributo | Valor |
|---|---|
| **Signo monto** | 100% positivo |
| **Operation status** | 99.9% refunded |
| **status_detail** | 9 valores: bpp_refunded (63%), reconciled (23%), compensated (2%) |
| **reason_detail** | **VACÍO** (0 valores) |

**Naturaleza**: **LIQUIDACIÓN / SETTLEMENT**. Poscobro procesa automáticamente la compensación al comprador (BPP) o la conciliación con la liquidación del vendedor. No es un reclamo — es el mecanismo operacional de Poscobro para cuadrar cuentas.

### `flow='chargeback'` (0.1% del monto)

| Atributo | Valor |
|---|---|
| **Signo monto** | 100% positivo |
| **Operation status** | 71% charged_back, 29% refunded |
| **status_detail** | ppv_covered_melienvio (5), ppv_valid (2) |

**Naturaleza**: **CONTRA CARGO**. El banco emisor revierte la transacción. ML pasa el costo al vendedor. Es residual (0.1%).

---

## FASE 3 — Trazabilidad Poscobro → Ledger

Todos los FLOW confluyen en el mismo financial_group:

| Flow | Ledger FG | Rows | Orders | Monto |
|---|---|---|---|---|
| `claim` | **ajustes** | 10,440 | 5,301 | $317,707,707 |
| `refund` | **ajustes** | 9,786 | 4,749 | $299,046,429 |
| `chargeback` | **ajustes** | 11 | 7 | $336,890 |

**Las mismas órdenes tienen entradas en otros grupos** (pero esas entradas vienen de otras fuentes — Facturación, no Poscobro):

| Flow | Órdenes con Devolución | Órdenes sin Devolución |
|---|---|---|
| `claim` | 2,692 (50.6%) | 2,633 (49.4%) |
| `refund` | 2,882 (53.7%) | 2,488 (46.3%) |
| `chargeback` | 1 (14.3%) | 6 (85.7%) |

**Conclusión**: La trazabilidad demuestra que el FLOW determina UNIFORMEMENTE el financial_group en el ledger. No hay variación dentro del mismo FLOW. El 100% de las filas Poscobro terminan en `ajustes`, independientemente del valor de `reason_detail`.

---

## FASE 4 — Matriz de clasificación correcta

| FLOW | Evento económico | Clasificación correcta | Fundamento |
|---|---|---|---|
| `claim` | ML cobra al vendedor por reclamo resuelto a favor del comprador | **AJUSTES** (Recuperación) | Es un recovery del seller, no un refund (el refund ya se registró como devolución). ML recupera el costo del vendedor. |
| `refund` | Poscobro procesa liquidación automática (BPP, conciliación) | **AJUSTES** (Settlement) | Es el mecanismo contable entre Poscobro y la liquidación del seller. No es ingreso ni devolución. |
| `chargeback` | ML pasa al vendedor el costo del contra cargo bancario | **AJUSTES** (Pase a costo) | Es residual. ML transfiere la pérdida bancaria al vendedor. |

**La clasificación actual del ledger (financial_group='ajustes') es CORRECTA para los 3 FLOWs.** No requiere cambio.

---

## FASE 5 — Dictamen: FLOW vs reason_detail

### ¿Debe la clasificación partir de FLOW o de reason_detail?

**Respuesta**: **FLOW**.

**Evidencia documental**:

1. **FLOW determina el evento económico**: `claim` = reclamo, `refund` = liquidación, `chargeback` = contra cargo. Cada uno representa un tipo de transacción diferente.

2. **reason_detail es solo la causa dentro del mismo FLOW**: Las 31 variantes de `reason_detail` dentro de `flow='claim'` (bigger_than_expected, repentant_buyer, broken_item, etc.) NO cambian la naturaleza económica. Todas son reclamos. Todas terminan en `ajustes` en el ledger.

3. **FLOW tiene 3 valores. reason_detail tiene 31+.** La clasificación por FLOW es más simple, estable y auditable.

4. **status_detail solo aparece en flow='refund'**: Es un estado operacional del settlement, no una clasificación financiera independiente.

5. **Trazabilidad unívoca**: 100% de filas con mismo FLOW → mismo financial_group. Cero excepciones.

### Regla de clasificación

```
FLOW
  ├─ claim     → AJUSTES (Recuperación de reclamo)
  ├─ refund    → AJUSTES (Liquidación/settlement)  
  └─ chargeback → AJUSTES (Contra cargo)
```

`reason_detail` solo explica **por qué** ocurrió el reclamo, no **qué** es financieramente.

### Impacto en certificaciones previas

| Certificación anterior | Veredicto previo | Veredicto corregido |
|---|---|---|
| AJUSTES_RETENCIONES_DOCUMENTARY_TRUTH | 54% mal clasificado | **CLASIFICACIÓN CORRECTA** — Los 3 FLOWs están en AJUSTES por diseño |
| POSCOBRO_LIQUIDACIONES_PRECEDENCE | LIQUIDACIONES > POSCOBRO | **CONFIRMADO** — FLOW no cambia la precedencia |
| DOCUMENTARY_RECONCILIATION_V2 | 73.3% conciliado | **CONFIRMADO** — FLOW no afecta la conciliación documental |

---

**Archivo**: `governance/POSCOBRO_FLOW_FINANCIAL_TRUTH.md`
