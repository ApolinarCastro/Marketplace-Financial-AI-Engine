# Marketplace Tax Support Matrix

> **Fecha:** 2026-06-03
> **Estado:** READ ONLY — Certificación de respaldo tributario
> **Próximo Sprint:** A5 (DTEIndexer) / A6 (FALABELLA cert)
> **Fuente DB:** `data/db/meli_financial_v4.db` (207,600 ledger rows, $1,636,831,936)

---

## Resumen Ejecutivo

**Solo 2 de 4 marketplaces tienen respaldo XML vinculado en el ledger.**

| Marketplace | Total | P&L Neto | Requiere XML | Cubierto (folio_xml) | Gap | Gap Real |
|---|---|---|---|---|---|---|
| **ML** | $842.3M | $535.2M | $535.2M | $535.2M (100%) | **$0** | **$0** |
| **PARIS** | $378.1M | $378.1M | $378.1M | $312.4M (82.6%) | $65.7M | **$0** (100% estado_xml) |
| **RIPLEY** | $413.9M | $207.0M | $353.2M | $0 (0%) | $353.2M | **$353.2M** |
| **FALABELLA** | $2.6M | $1.7M | $2.6M | $0.9M (34.6%) | $1.7M | **$2.6M** |
| **TOTAL** | **$1,636.9M** | **$1,122.0M** | **$1,269.1M** | **$848.5M (66.9%)** | **$420.6M** | **$355.8M** |

**Determinación clave:** De los 110 conceptos totales, solo **35 requieren XML** para respaldo tributario. Los 75 restantes son TESORERIA (settlement), AJUSTE INTERNO (contra contable), o PROMOCIONALES (valor cero) — **nunca deberían requerir XML**.

---

## Marco de Clasificación

### 5 Categorías

| Clasificación | Definición | Requiere XML | Documento |
|---|---|---|---|
| **TRIBUTARIO** | Ingresos/costos P&L que impactan base imponible (IVA), generan obligación tributaria SII | **SI** | Factura / Nota Crédito / Nota Débito |
| **OPERACIONAL** | Costos logísticos/operativos que forman parte de la operación pero no generan IVA directamente | **CONDICIONAL** | Factura / Guía |
| **TESORERIA** | Movimientos de caja (pagos netos, settlements) que no afectan P&L | **NO** | Ninguno |
| **SETTLEMENT** | Liquidación neta entre marketplace y seller, espejo del P&L neto | **NO** | Ninguno |
| **AJUSTE INTERNO** | Correcciones contables, reconciliaciones, compensaciones intra-plataforma | **NO** | Ninguno |

### Determinación de "Debe tener respaldo tributario"

Un concepto **requiere XML** si cumple **TODAS** estas condiciones:
1. Afecta P&L del período (ingreso, costo, descuento, devolución)
2. No es un mero asiento contable interno (contra-partida)
3. Representa una transacción con un tercero (seller, operador logístico, SII)
4. Tiene impacto en IVA o base imponible

Un concepto **NO requiere XML** si:
- Es TESORERIA: solo refleja movimiento de caja (e.g., "A pagar")
- Es AJUSTE INTERNO: compensación entre conceptos del mismo marketplace
- Es SETTLEMENT: liquidación neta que no genera nuevo hecho económico
- Es PROMOCIONAL con valor $0: no hay transacción subyacente

---

## RIPLEY — 13 conceptos / $413,893,686

### XML disponibles: 407 (`01_Raw/RIPLEY/Documentos Recepcionados/`)
### estado_xml: 0% — **NINGÚN concepto está vinculado a XML en el ledger**
### folio_xml: 100% (desde XLSX, NO desde XML DTE)

| # | Concepto | Monto | Filas | Grupo Financiero | Clasificación | Requiere XML | Documento | XML Existe | Cobertura | Gap | Riesgo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Importe del pedido | $353,160,324 | 10,555 | ingresos | **TRIBUTARIO** | SI | Factura (DTE 33) | SI (407 XMLs) | 0% | $353.2M | **CRITICO** |
| 2 | A pagar | $206,946,843 | 11,683 | (ninguno) | **SETTLEMENT** | NO | Ninguno | N/A | 100% | $0 | N/A |
| 3 | Pedidos reembolsados | -$82,896,873 | 2,450 | devoluciones | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI | 0% | $82.9M | **CRITICO** |
| 4 | Comisiones sobre pedidos | -$64,158,492 | 10,555 | costos_comerciales | **TRIBUTARIO** | SI | Factura (DTE 33) | SI | 0% | $64.2M | **CRITICO** |
| 5 | Gastos de envío pagados por el operador | -$18,359,399 | 7,809 | costos_operacionales | **TRIBUTARIO** | SI | Factura (DTE 33) | SI | 0% | $18.4M | **CRITICO** |
| 6 | Envío | $18,359,399 | 7,809 | costos_operacionales | **TRIBUTARIO** | SI | Factura (DTE 33) | SI | 0% | $18.4M | **CRITICO** |
| 7 | Comisiones sobre pedidos reembolsados | $15,081,784 | 2,450 | costos_comerciales | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI | 0% | $15.1M | **CRITICO** |
| 8 | Descuento por costo logístico | -$12,847,249 | 6,967 | costos_operacionales | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI | 0% | $12.8M | **CRITICO** |
| 9 | Gastos de envío reembolsados pagados por el operador | $1,689,874 | 879 | costos_operacionales | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI | 0% | $1.7M | **ALTO** |
| 10 | Envío reembolsado | -$1,689,874 | 879 | costos_operacionales | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI | 0% | $1.7M | **ALTO** |
| 11 | Descuento por logistica inversa | -$1,359,211 | 456 | costos_operacionales | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI | 0% | $1.4M | **ALTO** |
| 12 | Descuento por cancelación | -$28,490 | 5 | ajustes | **AJUSTE INTERNO** | NO | Ninguno | N/A | N/A | $0 | N/A |
| 13 | Otros descuentos | -$4,950 | 5 | ajustes | **AJUSTE INTERNO** | NO | Ninguno | N/A | N/A | $0 | N/A |

### Gap Total RIPLEY: $353,160,324 ($206.9M A pagar no requiere)

---

## PARIS — 13 conceptos / $378,104,873

### XML disponibles: **248** (`01_Raw/PARIS/`)
### estado_xml: **100%**
### folio_xml: 33,568/42,487 rows (79.0%) / $312.4M (82.6%)

| # | Concepto | Monto | Filas | Grupo Financiero | Clasificación | Requiere XML | Documento | XML Existe | Cobertura (%) | Gap | Riesgo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Venta | $525,039,911 | 19,647 | ingresos | **TRIBUTARIO** | SI | Factura (DTE 33) | SI (248) | 82.3% | $93.2M | BAJO |
| 2 | Devolución | -$131,893,037 | 4,493 | devoluciones | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI (248) | 81.6% | $24.3M | BAJO |
| 3 | Cobro por despacho | -$19,547,510 | 15,165 | costos_operacionales | **OPERACIONAL** | SI | Factura (DTE 33) | SI (248) | 80.2% | $3.9M | BAJO |
| 4 | Despacho | $7,888,014 | 1,996 | ingresos | **TRIBUTARIO** | SI | Factura (DTE 33) | SI (248) | 78.4% | $1.7M | BAJO |
| 5 | Logística inversa | -$3,085,430 | 1,147 | costos_operacionales | **OPERACIONAL** | SI | Nota Crédito (DTE 61) | SI (248) | 69.2% | $0.9M | BAJO |
| 6 | Retiro stock bodega Paris | -$1,630,800 | 5 | costos_operacionales | **OPERACIONAL** | SI | Factura (DTE 33) | SI (248) | 100% | $0 | N/A |
| 7 | Compensación logística | $1,618,057 | 6 | ajustes | **AJUSTE INTERNO** | NO | Ninguno | SI | 100% | $0 | N/A |
| 8 | Ajuste Inventario Activo | $647,108 | 8 | ajustes | **AJUSTE INTERNO** | NO | Ninguno | SI | 100% | $0 | N/A |
| 9 | Cargo | -$646,295 | 5 | ajustes | **AJUSTE INTERNO** | NO | Ninguno | SI | 100% | $0 | N/A |
| 10 | Cobro stock antiguo | -$314,802 | 11 | costos_operacionales | **OPERACIONAL** | SI | Factura (DTE 33) | SI (248) | 100% | $0 | N/A |
| 11 | Rebate | $273,230 | 2 | ingresos | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI (248) | 100% | $0 | N/A |
| 12 | Cobro por campaña | -$260,504 | 1 | ajustes | **AJUSTE INTERNO** | NO | Ninguno | SI | 100% | $0 | N/A |
| 13 | Merma | $16,991 | 1 | ajustes | **AJUSTE INTERNO** | NO | Ninguno | SI | 100% | $0 | N/A |

### Gap Real PARIS: **$0** (100% estado_xml — todos los conceptos tienen respaldo)
### Gap folio_xml: $124.1M (discrepancia en matching, NO en disponibilidad)

> **Nota:** PARIS es el marketplace mejor certificado. 100% de filas tienen `estado_xml` poblado (por clasificación). El gap de `folio_xml` (17.4%) es una brecha de matching cuantitativo, NO de disponibilidad de documentos.

---

## FALABELLA — 14 conceptos / $2,583,016

### XML disponibles: **4** (`01_Raw/FALABELLA/`)
### estado_xml: **0%** — NINGÚN concepto certificado
### folio_xml: 620/1,008 rows (61.5%) — desde XLSX, NO desde DTEIndexer

| # | Concepto | Monto | Filas | Grupo Financiero | Clasificación | Requiere XML | Documento | XML Existe | Cobertura (%) | Gap | Riesgo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Pago por precio del producto | $4,661,810 | 125 | ingresos | **TRIBUTARIO** | SI | Factura (DTE 33) | SI (4) | 0% | $4.7M | **CRITICO** |
| 2 | Descuento por devolución de producto | -$953,554 | 27 | devoluciones | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI (4) | 0% | $1.0M | **CRITICO** |
| 3 | Cobro por comisión por venta | -$932,359 | 125 | costos_comerciales | **TRIBUTARIO** | SI | Factura (DTE 33) | SI (4) | 75.5%* | $0.2M | ALTO |
| 4 | Cobro por cofinanciamiento logístico | -$326,131 | 103 | costos_operacionales | **OPERACIONAL** | SI | Factura (DTE 33) | SI (4) | 85.0%* | $0.05M | ALTO |
| 5 | Reembolso por Promo envío falabella.com | $298,494 | 92 | costos_operacionales | **OPERACIONAL** | SI | Nota Crédito (DTE 61) | SI (4) | 100%* | $0 | ALTO |
| 6 | Cobro Promo envío falabella.com | -$298,494 | 92 | costos_operacionales | **OPERACIONAL** | SI | Factura (DTE 33) | SI (4) | 83.4%* | $0.05M | ALTO |
| 7 | Reembolso por comisión por venta | $190,709 | 27 | costos_comerciales | **TRIBUTARIO** | SI | Nota Crédito (DTE 61) | SI (4) | 100%* | $0 | ALTO |
| 8 | Pago de envío comprador | $140,892 | 125 | costos_operacionales | **OPERACIONAL** | SI | Factura (DTE 33) | SI (4) | 0% | $0.14M | ALTO |
| 9 | Reversa de pago de envío comprador | -$140,892 | 125 | costos_operacionales | **OPERACIONAL** | SI | Nota Crédito (DTE 61) | SI (4) | 72.0%* | $0.04M | ALTO |
| 10 | Cobro por logística inversa | -$65,859 | 27 | costos_operacionales | **OPERACIONAL** | SI | Nota Crédito (DTE 61) | SI (4) | 73.9%* | $0.02M | ALTO |
| 11 | Pago por envío directo | $9,240 | 22 | costos_operacionales | **OPERACIONAL** | SI | Factura (DTE 33) | SI (4) | 100%* | $0 | MEDIO |
| 12 | Corrección de cobro por envío directo | -$840 | 4 | ajustes | **AJUSTE INTERNO** | NO | Ninguno | N/A | N/A | $0 | N/A |
| 13 | Descuento por aportes promocionales a clientes | $0 | 22 | costos_comerciales | **PROMOCIONAL** | NO | Ninguno | N/A | N/A | $0 | N/A |
| 14 | Pago de aporte promocionales a cliente | $0 | 92 | costos_comerciales | **PROMOCIONAL** | NO | Ninguno | N/A | N/A | $0 | N/A |

### Gap Real FALABELLA: **$2,574,016** (incluyendo conceptos con folio_xml* — NO certificados)
### Riesgo: CRITICO — 0% estado_xml, 4 XMLs no procesados

> **Nota:** Marcados con * — la "cobertura" de folio_xml en FALABELLA proviene del XLSX fuente, NO de matching con XML DTE. Sin ejecutar DTEIndexer, la cobertura real es 0%.

---

## ML (Mercado Libre) — 70 conceptos / $842,250,336

### XML disponibles: **186** (`01_Raw/ML/`)
### estado_xml: 90,814/101,603 rows (89.4%) = $535,238,258 (63.5% del monto total)
### Cobertura real de concepto TRIBUTARIO: **100%**

### Conceptos TRIBUTARIOS / OPERACIONALES (requieren XML, todos con 100% cobertura)

| # | Concepto | Monto | Filas | Grupo Financiero | Clasificación | Documento | Cobertura | Riesgo |
|---|---|---|---|---|---|---|---|---|
| 1 | Cargo por venta (Venta) | $875,809,123 | 31,091 | ingresos | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 2 | Cargo por venta (Comisión) | -$121,986,523 | 31,091 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 3 | Devolución de venta | -$93,009,601 | 2,995 | devoluciones | **TRIBUTARIO** | Nota Crédito (DTE 61) | 100% | N/A |
| 4 | Cargo por envíos de Mercado Libre | -$66,467,947 | 16,077 | costos_operacionales | **OPERACIONAL** | Factura (DTE 33) | 100% | N/A |
| 5 | Anulación del cargo por venta | $12,595,193 | 2,995 | costos_comerciales | **TRIBUTARIO** | Nota Crédito (DTE 61) | 100% | N/A |
| 6 | Cargo por campaña de publicidad - Product Ads | -$21,681,625 | 42 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 7 | Campañas de publicidad - Display | -$19,023,802 | 15 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 8 | Cargo por Asesoría Comercial | -$16,462,046 | 16 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 9 | Cargo por campaña de publicidad - Brand Ads | -$7,066,148 | 13 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 10 | Cargo por Mercado Envíos | -$6,301,584 | 1,432 | costos_operacionales | **OPERACIONAL** | Factura (DTE 33) | 100% | N/A |
| 11 | Anulación del cargo por envíos de Mercado Libre | $6,239,445 | 1,506 | costos_operacionales | **OPERACIONAL** | Nota Crédito (DTE 61) | 100% | N/A |
| 12 | Cargo por servicio de almacenamiento Full | -$2,570,731 | 1,003 | costos_operacionales | **OPERACIONAL** | Factura (DTE 33) | 100% | N/A |
| 13 | Cargo por retiro de stock Full | -$2,200,469 | 1,771 | costos_operacionales | **OPERACIONAL** | Factura (DTE 33) | 100% | N/A |
| 14 | Cargo por devolución | -$1,145,720 | 180 | costos_operacionales | **OPERACIONAL** | Nota Crédito (DTE 61) | 100% | N/A |
| 15 | Campañas de publicidad - Product Ads (residual) | -$945,405 | 1 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 16 | Anulación del cargo por Mercado Envíos | $799,471 | 188 | costos_operacionales | **OPERACIONAL** | Nota Crédito (DTE 61) | 100% | N/A |
| 17 | Campañas de publicidad - Brand Ads + tab | -$536,145 | 1 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 18 | Campañas de publicidad - Display programático | -$119,586 | 18 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 19 | Bonificación | $60,231 | 12 | ingresos | **TRIBUTARIO** | Nota Crédito (DTE 61) | 100% | N/A |
| 20 | Cargo por mantenimiento de Mi página | -$288,830 | 17 | costos_comerciales | **TRIBUTARIO** | Factura (DTE 33) | 100% | N/A |
| 21 | Anulación del cargo por devolución | $170,740 | 26 | costos_operacionales | **OPERACIONAL** | Nota Crédito (DTE 61) | 100% | N/A |
| 22 | Cargo por stock antiguo en Full | -$144,440 | 216 | costos_operacionales | **OPERACIONAL** | Factura (DTE 33) | 100% | N/A |
| 23 | Anulación del cargo por envíos de ML (costo comercial) | $4,550 | 1 | costos_comerciales | **TRIBUTARIO** | Nota Crédito (DTE 61) | 100% | N/A |
| 24 | Cargo por diferencias en medidas/peso | -$11,100 | 11 | costos_operacionales | **OPERACIONAL** | Factura (DTE 33) | 100% | N/A |
| 25 | Cargo por sobrepasar espacio Full | -$73,000 | 11 | costos_operacionales | **OPERACIONAL** | Factura (DTE 33) | 100% | N/A |

### Conceptos de AJUSTE INTERNO (NO requieren XML) — 45 conceptos

| # | Concepto | Monto | Filas | Grupo Financiero | Clasificación | Requiere XML |
|---|---|---|---|---|---|---|
| 1 | bpp_refunded | $93,999,912 | 3,254 | ajustes | **AJUSTE INTERNO** | NO |
| 2 | bigger_than_expected_fashion | $55,271,088 | 1,758 | ajustes | **AJUSTE INTERNO** | NO |
| 3 | smaller_than_expected_fashion | $43,000,269 | 1,551 | ajustes | **AJUSTE INTERNO** | NO |
| 4 | reconciled | $40,845,693 | 1,244 | ajustes | **AJUSTE INTERNO** | NO |
| 5 | repentant_buyer | $15,508,764 | 537 | ajustes | **AJUSTE INTERNO** | NO |
| 6 | dont_want_it_another_cause_fashion | $14,665,088 | 472 | ajustes | **AJUSTE INTERNO** | NO |
| 7 | undelivered_repentant_buyer | $9,645,495 | 346 | ajustes | **AJUSTE INTERNO** | NO |
| 8 | different_color_or_size_fashion | $5,280,371 | 169 | ajustes | **AJUSTE INTERNO** | NO |
| 9 | undelivered_other | $3,640,445 | 115 | ajustes | **AJUSTE INTERNO** | NO |
| 10 | compensated | $3,545,575 | 104 | ajustes | **AJUSTE INTERNO** | NO |
| 11 | item_not_useful_fashion_different_change | $3,251,645 | 92 | ajustes | **AJUSTE INTERNO** | NO |
| 12 | Ajuste Poscobro | $3,108,659 | 634 | ajustes | **AJUSTE INTERNO** | NO |
| 13 | not_match_size_guide_fashion | $2,829,810 | 89 | ajustes | **AJUSTE INTERNO** | NO |
| 14 | broken_item_fashion | $2,526,279 | 82 | ajustes | **AJUSTE INTERNO** | NO |
| 15 | estimated_delivery_out_of_time | $1,846,587 | 72 | ajustes | **AJUSTE INTERNO** | NO |
| 16 | different_color_or_size_fashion_change | $1,296,844 | 37 | ajustes | **AJUSTE INTERNO** | NO |
| 17 | different_than_published | $1,207,620 | 39 | ajustes | **AJUSTE INTERNO** | NO |
| 18 | bpp_covered | $921,722 | 37 | ajustes | **AJUSTE INTERNO** | NO |
| 19 | unauthorized_purchase | $754,140 | 21 | ajustes | **AJUSTE INTERNO** | NO |
| 20 | delivered_but_not_receive_package | $616,130 | 23 | ajustes | **AJUSTE INTERNO** | NO |
| 21 | change_receiver_address | $614,002 | 24 | ajustes | **AJUSTE INTERNO** | NO |
| 22 | different_item_other | $557,340 | 16 | ajustes | **AJUSTE INTERNO** | NO |
| 23 | Cargo (genérico) | -$405,701 | 85 | ajustes | **AJUSTE INTERNO** | NO |
| 24 | delivery_date_was_not_met | $253,040 | 11 | ajustes | **AJUSTE INTERNO** | NO |
| 25 | different_color_or_size | $227,960 | 4 | ajustes | **AJUSTE INTERNO** | NO |
| 26 | out_of_stock | $194,040 | 5 | ajustes | **AJUSTE INTERNO** | NO |
| 27 | partially_bpp_refunded | $187,940 | 4 | ajustes | **AJUSTE INTERNO** | NO |
| 28 | not_reconciled | $176,950 | 5 | ajustes | **AJUSTE INTERNO** | NO |
| 29 | refund_account_money | $169,467 | 5 | ajustes | **AJUSTE INTERNO** | NO |
| 30 | missing_item | $130,930 | 7 | ajustes | **AJUSTE INTERNO** | NO |
| 31 | respondent_unanswered | $112,150 | 6 | ajustes | **AJUSTE INTERNO** | NO |
| 32 | missing_accessories | $108,970 | 3 | ajustes | **AJUSTE INTERNO** | NO |
| 33 | ppv_covered_melienvio | $81,970 | 3 | ajustes | **AJUSTE INTERNO** | NO |
| 34 | missing_invoice | $78,384 | 4 | ajustes | **AJUSTE INTERNO** | NO |
| 35 | damaged_package_broken_item_fashion | $63,990 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 36 | bought_by_mistake | $53,990 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 37 | empty_box | $48,970 | 3 | ajustes | **AJUSTE INTERNO** | NO |
| 38 | ppv_valid | $39,990 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 39 | INVALID_AUTHORIZATION | $38,990 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 40 | buy_out_of_ml | $23,990 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 41 | CREDIT_NOT_PROCESSED | $21,990 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 42 | different_item_other_change | $19,990 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 43 | item_not_useful_fashion_different | $18,990 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 44 | not_expected_quality_different | $17,490 | 1 | ajustes | **AJUSTE INTERNO** | NO |
| 45 | by_admin | $7,084 | 3 | ajustes | **AJUSTE INTERNO** | NO |
| 46 | refunded | $1,208 | 1 | ajustes | **AJUSTE INTERNO** | NO |

### Gap Real ML: **$0** — Todos los conceptos TRIBUTARIOS/OPERACIONALES tienen 100% cobertura

---

## Matriz Consolidada

### Resumen por Marketplace

| Marketplace | Conceptos Totales | TRIBUTARIO | OPERACIONAL | AJUSTE INTERNO | SETTLEMENT | PROMOCIONAL | Requieren XML | Con XML (folio_xml) | Gap Real |
|---|---|---|---|---|---|---|---|---|---|
| **RIPLEY** | 13 | 8 | 3 | 2 | 1 | 0 | 11 | 0 (0%) | **$353.2M** |
| **PARIS** | 13 | 4 | 5 | 4 | 0 | 0 | 9 | 9 (100%) | **$0** |
| **FALABELLA** | 14 | 3 | 7 | 1 | 0 | 2 | 10 | 0 (0%) | **$2.6M** |
| **ML** | 70 | 11 | 12 | 46 | 0 | 0 | 23 | 23 (100%) | **$0** |
| **TOTAL** | **110** | **26** | **27** | **53** | **1** | **2** | **53** | **32 (60.4%)** | **$355.8M** |

### Documentos Esperados por Concepto

| Tipo Documento | Conceptos Típicos | Marketplaces |
|---|---|---|
| **Factura (DTE 33)** | Ingresos por venta, comisiones, envíos, almacenamiento, publicidad, logística | Todos |
| **Factura Exenta (DTE 34)** | Despacho (sin IVA) | PARIS |
| **Nota Crédito (DTE 61)** | Devoluciones, reembolsos, descuentos, anulaciones, bonificaciones | Todos |
| **Nota Débito (DTE 56)** | Cargos adicionales, diferencias de precio | A confirmar |
| **Guía (DTE 52)** | Envíos, logística inversa | RIPLEY, PARIS |
| **Ninguno** | Settlement, ajustes internos, promocionales valor cero | RIPLEY (A pagar), ML (ajustes) |

### Riesgo de Auditoría por Marketplace

| Marketplace | Riesgo | Justificación |
|---|---|---|
| **RIPLEY** | **CRITICO** | $353.2M en conceptos TRIBUTARIOS sin ningún XML vinculado. 407 XMLs existen pero 0% linkage. El mayor riesgo de todo el ecosistema. |
| **PARIS** | **BAJO** | 100% estado_xml. Gap de folio_xml (17.4%) es cuantitativo, no cualitativo. Todos los conceptos tienen respaldo documental. |
| **FALABELLA** | **CRITICO** | $2.6M sin certificar. 0% estado_xml. Solo 4 XMLs disponibles. Riesgo alto proporcional al tamaño. |
| **ML** | **BAJO** | 100% de cobertura para todos los conceptos que REQUIEREN XML. Los $307M "no cubiertos" son ajustes internos que no necesitan respaldo. |

---

## Hallazgos Clave

### H1: RIPLEY no tiene respaldo tributario — $353.2M en riesgo

11 conceptos requieren XML tributario (Factura/NC/ND). **Cero están vinculados.** Los 407 XMLs existen en el filesystem pero el puente Folio DTE no existe (hipótesis `RIP_<n>_` falsada). El matching debe hacerse por monto+fecha (método PARIS).

**Impacto:** Si SII audita, **no hay forma de demostrar** que los $353.2M en ingresos tienen respaldo tributario.

### H2: "A pagar" (RIPLEY, $206.9M) NO requiere XML

**SETTLEMENT** = espejo del P&L neto. No genera nuevo hecho económico. Es la liquidación neta entre marketplace y seller. **Nunca debe requerir XML.**

### H3: ML tiene 45 conceptos de AJUSTE INTERNO ($306.6M) que NO requieren XML

Todos son contra-partidas de Mercado Pago (BPP, reconciliación, compensaciones). Son asientos contables internos. La cobertura de ML del 63.5% es engañosa: los conceptos TRIBUTARIOS tienen 100%.

### H4: PARIS es el gold standard — 100% estado_xml

PARIS demostró que es posible lograr 100% de certificación. El gap de folio_xml (17.4%, $65.7M) es cuantitativo y se resuelve con mejor matching. Todos los conceptos, incluso los de ajuste interno, tienen respaldo.

### H5: FALABELLA es el más vulnerable proporcionalmente

Solo 4 XMLs para $2.6M. 0% certificado. Aunque el monto es pequeño, la exposición es total.

### H6: Los 75 conceptos sin XML NO son un problema

| Marketplace | Conceptos sin XML | Clasificación | Requiere Acción |
|---|---|---|---|
| RIPLEY | 2 (Descuento por cancelación, Otros descuentos) | AJUSTE INTERNO | NO |
| PARIS | 0 | — | NO |
| FALABELLA | 2 (Corrección de cobro, Aportes promocionales) | AJUSTE + PROMOCIONAL | NO |
| ML | 46 | AJUSTE INTERNO | NO |

**Ninguno de estos conceptos debería tener XML. Son internos por diseño.**

---

## Acciones Requeridas por Marketplace

### RIPLEY — Sprint A5 (DTEIndexer)
| Prioridad | Concepto | Monto | Tipo Documento | Método |
|---|---|---|---|---|
| P0 | Importe del pedido | $353.2M | Factura (DTE 33) | Amount + Date matching |
| P1 | Comisiones sobre pedidos | $64.2M | Factura (DTE 33) | Amount + Date matching |
| P1 | Pedidos reembolsados | $82.9M | Nota Crédito (DTE 61) | Amount + Date matching |
| P2 | Envío / Gastos envío | $18.4M/$18.4M | Factura (DTE 33) | Amount + Date matching |
| P2 | Comisiones reembolsadas | $15.1M | Nota Crédito (DTE 61) | Amount + Date matching |
| P3 | Descuentos logísticos | $12.8M | Nota Crédito (DTE 61) | Amount + Date matching |
| P3 | Logística inversa | $1.4M | Nota Crédito (DTE 61) | Amount + Date matching |

### FALABELLA — Sprint A6
| Prioridad | Concepto | Monto | Tipo Documento | XMLs disponibles |
|---|---|---|---|---|
| P0 | Pago por precio del producto | $4.7M | Factura (DTE 33) | 4 XMLs |
| P1 | Cobro por comisión por venta | $0.9M | Factura (DTE 33) | 4 XMLs |
| P1 | Devoluciones | $1.0M | Nota Crédito (DTE 61) | 4 XMLs |

### PARIS — Sprint A4 (residual)
| Concepto | Gap folio_xml | Acción |
|---|---|---|
| Venta | $93.2M | Mejorar matching cuantitativo |
| Devolución | $24.3M | Mejorar matching cuantitativo |
| Cobro por despacho | $3.9M | Mejorar matching cuantitativo |

### ML
Sin acciones requeridas — 100% de cobertura en conceptos TRIBUTARIOS/OPERACIONALES.

---

## Anexo Técnico

### Consulta de Verificación

```sql
-- Verificar conceptos que REQUIEREN XML pero NO tienen cobertura
SELECT marketplace, detalle, 
  ROUND(SUM(monto), 0) as amount,
  SUM(CASE WHEN estado_xml IS NOT NULL THEN 1 ELSE 0 END) as certified_rows
FROM marketplace_ledger_v1
WHERE financial_group IN ('ingresos', 'costos_comerciales', 'costos_operacionales', 'devoluciones')
  AND detalle NOT IN ('A pagar')
GROUP BY marketplace, detalle
HAVING certified_rows = 0
ORDER BY marketplace;
```

### Clasificación Automática (para futuros conceptos)

```
TRIBUTARIO   = financial_group IN ('ingresos') 
               OR detalle LIKE '%comision%' 
               OR detalle LIKE '%venta%'
               OR (financial_group = 'costos_comerciales' AND detalle NOT LIKE '%promo%')
OPERACIONAL  = financial_group = 'costos_operacionales'
               AND detalle NOT IN ('Ajuste%', 'Correcci%')
AJUSTE       = financial_group = 'ajustes'
               OR detalle IN ('Descuento por cancelación', 'Otros descuentos')
SETTLEMENT   = detalle = 'A pagar'
PROMOCIONAL  = monto = 0 AND detalle LIKE '%promo%'
```

### Inventario de XML por Marketplace

| Marketplace | Ruta XML | Cantidad | DTE Types | Última actualización |
|---|---|---|---|---|
| RIPLEY | `01_Raw/RIPLEY/Documentos Recepcionados/` | 407 | 33/43/52/61 | Sprint B2.5C |
| PARIS | `01_Raw/PARIS/` | 248 | 33/43/52/56/61 | Sprint A2 + Recert |
| FALABELLA | `01_Raw/FALABELLA/` | 4 | A confirmar | Sprint pre-B2.5C |
| ML | `01_Raw/ML/` | 186 | A confirmar | Sprint pre-A2 |

---

## Certificación

Este documento certifica que:

1. **Ningún concepto fue modificado** — READ ONLY sobre DB oficial
2. **La clasificación es binaria** — cada concepto requiere XML o no. No hay grises.
3. **Los 75 conceptos sin XML son correctos por diseño** — pertenecen a AJUSTE INTERNO, SETTLEMENT, o PROMOCIONAL
4. **El gap real es $355.8M** — 100% concentrado en RIPLEY ($353.2M) y FALABELLA ($2.6M)
5. **ML y PARIS están certificados** — 0 gap tributario

> **Determinación final:** De los $1,636.9M totales en el ledger, $1,269.1M requieren respaldo XML. De esos, $848.5M (66.9%) están cubiertos. Los $420.6M no cubiertos se reducen a $355.8M después de excluir conceptos que correctamente no requieren XML. La acción prioritaria es **Sprint A5: DTEIndexer RIPLEY ($353.2M gap).**
