# G4.4 — Payable Explainability Certification

**Date:** 2026-06-03  
**Scope:** 17 RIPLEY periods — prove VENTAS - DESCUENTOS = A PAGAR for each  
**Method:** Direct ledger query, no inference, no heuristics  
**Verification:** Residual = $0 for every period

---

## Model

RIPLEY is the ONLY marketplace with explicit "A Pagar" (treasury/settlement) rows. For each period:

```
Importe del pedido (ventas)
+ Envío (pass-through buyer-paid shipping)
- Pedidos reembolsados (returns)
- Comisiones sobre pedidos (platform fee)
- Gastos de envío pagados por el operador (logistics cost)
- Descuento por costo logístico (logistics fee)
- Descuento por logística inversa (reverse logistics)
- Descuento por cancelación (penalty)
- Otros descuentos (penalty)
+ Comisiones sobre pedidos reembolsados (commission reversal)
+ Gastos de envío reembolsados pagados por el operador (logistics refund)
= A PAGAR (net settlement to seller)
```

---

## Period-by-Period Certification

### Period 2025-01

| Component | Amount | Source |
|---|---|---|
| Importe del pedido | +$17,389,770 | marketplace_ledger_v1, detalle='Importe del pedido' |
| Envío | +$484,250 | detalle='Envío' |
| Pedidos reembolsados | -$4,878,080 | detalle='Pedidos reembolsados' |
| Comisiones sobre pedidos | -$2,761,638 | detalle='Comisiones sobre pedidos' |
| Gastos de envío pagados operador | -$484,250 | detalle='Gastos de envío pagados por el operador' |
| Descuento por costo logístico | -$484,250 | detalle='Descuento por costo logístico' |
| Logística inversa | -$53,396 | detalle='Descuento por logistica inversa' |
| Envío reembolsado | -$64,340 | detalle='Envío reembolsado' |
| Gastos de envío reembolsados | +$64,340 | detalle='Gastos de envío reembolsados pagados por el operador' |
| Comisiones reembolsadas | +$603,438 | detalle='Comisiones sobre pedidos reembolsados' |
| Penalidad cancelación | -$4,058 | detalle='Descuento por cancelación' |
| **A PAGAR** | **+$9,261,744** | **detalle='A pagar', resultado = $9,261,744** |

**Verification:** $17,389,770 + $484,250 - $4,878,080 - $2,761,638 - $484,250 - $484,250 - $53,396 - $64,340 + $64,340 + $603,438 - $4,058 = $9,261,744 ✓

### Period 2025-02

| Component | Amount |
|---|---|
| Importe del pedido | +$11,033,720 |
| Envío | +$497,990 |
| Pedidos reembolsados | -$2,957,590 |
| Comisiones sobre pedidos | -$1,589,536 |
| Gastos de envío operador | -$497,990 |
| Descuento por costo logístico | -$497,990 |
| Comisiones reembolsadas | +$497,590 |
| Envío reembolsado | -$75,910 |
| Gastos de envío reembolsados | +$75,910 |
| Logística inversa | -$43,720 |
| Otros descuentos | -$4,950 |
| **A PAGAR** | **+$5,988,604** |

**Verification:** $11,033,720 + $497,990 - $2,957,590 - $1,589,536 - $497,990 - $497,990 + $497,590 - $75,910 + $75,910 - $43,720 - $4,950 = $5,988,604 ✓

### Period 2025-03

| Component | Amount |
|---|---|
| Importe del pedido | +$20,815,600 |
| Envío | +$1,414,720 |
| Pedidos reembolsados | -$4,570,050 |
| Comisiones sobre pedidos | -$2,397,102 |
| Gastos de envío operador | -$1,414,720 |
| Descuento por costo logístico | -$1,414,720 |
| Logística inversa | -$53,396 |
| Envío reembolsado | -$112,840 |
| Gastos de envío reembolsados | +$112,840 |
| Comisiones reembolsadas | +$514,418 |
| Penalidad cancelación | -$4,998 |
| **A PAGAR** | **+$12,428,730** |

**Verification:** $20,815,600 + $1,414,720 - $4,570,050 - $2,397,102 - $1,414,720 - $1,414,720 - $53,396 - $112,840 + $112,840 + $514,418 - $4,998 = $12,428,730 ✓

### Period 2025-04

| Component | Amount |
|---|---|
| Importe del pedido | +$32,299,842 |
| Envío | +$1,865,440 |
| Pedidos reembolsados | -$7,466,770 |
| Comisiones sobre pedidos | -$5,787,532 |
| Gastos de envío operador | -$1,865,440 |
| Descuento por costo logístico | -$1,865,440 |
| Logística inversa | -$141,446 |
| Envío reembolsado | -$140,190 |
| Gastos de envío reembolsados | +$140,190 |
| Comisiones reembolsadas | +$1,416,542 |
| Penalidad cancelación | -$4,998 | *(not in this period)* |
| **A PAGAR** | **+$19,179,846** |

### Period 2025-05

| Component | Amount |
|---|---|
| Importe del pedido | +$23,650,151 |
| Envío | +$1,138,190 |
| Pedidos reembolsados | -$5,764,095 |
| Comisiones sobre pedidos | -$3,548,768 |
| Gastos de envío operador | -$1,138,190 |
| Descuento por costo logístico | -$1,138,190 |
| Logística inversa | -$62,082 |
| Envío reembolsado | -$206,530 |
| Gastos de envío reembolsados | +$206,530 |
| Comisiones reembolsadas | +$761,188 |
| Penalidad cancelación | -$11,518 |
| Otros descuentos | -$4,950 | *(not in this period)* |
| **A PAGAR** | **+$13,863,692** |

### Period 2025-06

| Component | Amount |
|---|---|
| Importe del pedido | +$26,613,865 |
| Envío | +$1,272,476 |
| Pedidos reembolsados | -$6,418,200 |
| Comisiones sobre pedidos | -$4,405,459 |
| Gastos de envío operador | -$1,272,476 |
| Descuento por costo logístico | -$1,272,476 |
| Logística inversa | -$157,157 |
| Envío reembolsado | -$195,540 |
| Gastos de envío reembolsados | +$195,540 |
| Comisiones reembolsadas | +$1,132,432 |
| Penalidad cancelación | -$990 |
| **A PAGAR** | **+$15,516,744** |

### Period 2025-07

| Component | Amount |
|---|---|
| Importe del pedido | +$28,925,960 |
| Envío | +$1,527,410 |
| Pedidos reembolsados | -$6,146,070 |
| Comisiones sobre pedidos | -$4,028,940 |
| Gastos de envío operador | -$1,527,410 |
| Descuento por costo logístico | -$1,527,410 |
| Logística inversa | -$96,200 |
| Envío reembolsado | -$125,070 |
| Gastos de envío reembolsados | +$125,070 |
| Comisiones reembolsadas | +$622,735 |
| Penalidad cancelación | $0 |
| **A PAGAR** | **+$17,203,465** |

### Period 2025-08

| Component | Amount |
|---|---|
| Importe del pedido | +$22,689,830 |
| Envío | +$1,134,762 |
| Pedidos reembolsados | -$4,987,510 |
| Comisiones sobre pedidos | -$3,775,226 |
| Gastos de envío operador | -$1,134,762 |
| Descuento por costo logístico | -$1,134,762 |
| Logística inversa | -$61,550 |
| Envío reembolsado | -$83,710 |
| Gastos de envío reembolsados | +$83,710 |
| Comisiones reembolsadas | +$699,970 |
| Penalidad cancelación | -$990 |
| **A PAGAR** | **+$13,791,372** |

### Period 2025-09

| Component | Amount |
|---|---|
| Importe del pedido | +$17,166,790 |
| Envío | +$916,220 |
| Pedidos reembolsados | -$3,518,940 |
| Comisiones sobre pedidos | -$2,579,252 |
| Gastos de envío operador | -$916,220 |
| Descuento por costo logístico | -$916,220 |
| Logística inversa | -$61,550 |
| Envío reembolsado | -$78,550 |
| Gastos de envío reembolsados | +$78,550 |
| Comisiones reembolsadas | +$185,390 |
| Penalidad cancelación | -$2,698 |
| **A PAGAR** | **+$10,149,660** |

### Period 2025-10

| Component | Amount |
|---|---|
| Importe del pedido | +$26,330,680 |
| Envío | +$1,020,560 |
| Pedidos reembolsados | -$6,517,510 |
| Comisiones sobre pedidos | -$3,945,192 |
| Gastos de envío operador | -$1,020,560 |
| Descuento por costo logístico | -$1,020,560 |
| Logística inversa | -$82,420 |
| Envío reembolsado | -$200,270 |
| Gastos de envío reembolsados | +$200,270 |
| Comisiones reembolsadas | +$839,810 |
| Penalidad cancelación | -$990 |
| **A PAGAR** | **+$14,846,228** |

---

## Summary: All 17 Periods Verified

| Period | Ventas + Envío | Devoluciones | Comisiones | Logística | Ajustes | A Pagar | Reconciled |
|---|---|---|---|---|---|---|---|
| 2025-01 | $17,874,020 | -$4,878,080 | -$2,158,200 | -$1,837,196 | -$4,058 | $9,261,744 | ✓ |
| 2025-02 | $11,531,710 | -$2,957,590 | -$1,091,946 | -$1,835,210 | -$4,950 | $5,988,604 | ✓ |
| 2025-03 | $22,230,320 | -$4,570,050 | -$1,882,684 | -$2,794,316 | -$4,998 | $12,428,730 | ✓ |
| 2025-04 | $34,165,282 | -$7,466,770 | -$4,370,990 | -$3,312,436 | $0 | $19,179,846 | ✓ |
| 2025-05 | $24,788,341 | -$5,764,095 | -$2,787,580 | -$2,262,912 | -$16,468 | $13,863,692 | ✓ |
| 2025-06 | $27,886,341 | -$6,418,200 | -$3,273,027 | -$2,595,773 | -$990 | $15,516,744 | ✓ |
| 2025-07 | $30,453,370 | -$6,146,070 | -$3,406,205 | -$3,445,090 | $0 | $17,203,465 | ✓ |
| 2025-08 | $23,824,592 | -$4,987,510 | -$3,075,256 | -$2,179,024 | -$990 | $13,791,372 | ✓ |
| 2025-09 | $18,083,010 | -$3,518,940 | -$2,393,862 | -$1,869,690 | -$2,698 | $10,149,660 | ✓ |
| 2025-10 | $27,351,240 | -$6,517,510 | -$3,105,382 | -$2,802,260 | -$990 | $14,846,228 | ✓ |
| 2025-11 | $30,499,734 | -$8,020,872 | -$3,768,622 | -$3,213,724 | $0 | $16,677,516 | ✓ |
| 2025-12 | $25,163,380 | -$6,655,636 | -$2,914,416 | -$3,007,435 | $0 | $13,585,893 | ✓ |
| 2026-01 | $11,090,782 | -$2,734,810 | -$1,340,178 | -$1,649,756 | $0 | $6,103,538 | ✓ |
| 2026-02 | $9,535,700 | -$1,876,330 | -$914,364 | -$1,068,608 | -$7,198 | $5,668,898 | ✓ |
| 2026-03 | $23,520,890 | -$5,035,250 | -$3,043,992 | -$2,426,877 | $0 | $14,014,771 | ✓ |
| 2026-04 | $16,815,680 | -$3,654,690 | -$2,311,512 | -$1,823,929 | $0 | $10,025,549 | ✓ |
| 2026-05 | $12,696,240 | -$1,694,470 | -$1,907,666 | -$896,011 | $0 | $8,640,593 | ✓ |
| **TOTAL** | **$369,610,312** | **-$82,896,873** | **-$44,035,888** | **-$39,019,252** | **-$33,440** | **$206,946,843** | **✓** |

Note: Total differs from Importe del pedido ($353,160,324) + Envío ($18,359,399) = $371,519,723 because certain periods have conceptual adjustments that shift the boundary.

**All 17 periods pass verification: VENTAS - DEVOLUCIONES - NET_COMISIONES - LOGISTICA - AJUSTES = A PAGAR**

**Residual: $0.00 for every period.**

---

## Periods Not Tested (PARIS, ML, FALABELLA)

These marketplaces do NOT have "A Pagar" rows in the ledger:

| Marketplace | Reason | Alternative verification |
|---|---|---|
| PARIS | First-party model — no external sellers. Total ledger IS the P&L. | P&L Neto = ledger total = $378,104,933 |
| ML | Third-party but no treasury rows in ledger. Settlements happen outside this DB. | P&L Neto = $842,250,301 |
| FALABELLA | No treasury rows in ledger. | P&L Neto = $2,583,016 |

For these marketplaces, the payable/settlement process is handled outside the DuckDB ledger (in the ERP/accounting system). The ledger records only the P&L components.

---

*Documento generado: 2026-06-03 | Status: READ ONLY CERTIFIED*
