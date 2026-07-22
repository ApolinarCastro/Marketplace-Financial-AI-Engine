# BASELINE_ESTABLE_V6 - STATS

Generated: 2026-05-29T10:59:29.140482
DB SHA256: e1e341ef44e0a61c4e846d34e05d14a4c291dcd904869f20fdf6e9a37fef1c29

## Global

| Metric | Value |
|---|---:|
| Total rows | 414,314 |
| Total SUM | $1,507,835,610 |

### Financial Groups

| Group | Rows | Total |
|---|---|---:|
| ingresos | 61,286 | $1,654,711,919 |
| ajustes | 78,203 | $307,950,395 |
| NULL | 8,413 | $142,448,680 |
| costos_operacionales | 148,704 | $-107,080,985 |
| costos_comerciales | 101,780 | $-210,279,697 |
| devoluciones | 15,928 | $-279,914,703 |

## ML

| Metric | Value |
|---|---:|
| Rows | 101,603 |
| SUM | $842,250,301 |
| NULL financial_group | 0 |
| NULL clasificacion_operativa | 0 |
| NO_CLASIFICADO | 0 |

### Financial Groups

| Group | Rows | Total |
|---|---|---:|
| ingresos | 31,103 | $875,869,354 |
| ajustes | 10,874 | $306,606,250 |
| costos_operacionales | 22,421 | $-71,705,336 |
| devoluciones | 2,995 | $-93,009,601 |
| costos_comerciales | 34,210 | $-175,510,367 |

### Transaction Types

| Detalle | Clasificación | FG | Rows | Total |
|---|---|---|---:|---:|
| Cargo por venta (Venta) | Cargo por venta (Venta) | ingresos | 31,091 | $875,809,123 |
| Cargo por venta (Comisión) | Cargo por venta (Comisión) | costos_comerciales | 31,091 | $-121,986,523 |
| bpp_refunded | Ajuste por Compra Protegida (BPP) | ajustes | 3,254 | $93,999,912 |
| Devolución de venta | Devolución de venta | devoluciones | 2,995 | $-93,009,601 |
| Cargo por envíos de Mercado Libre | Cargo por envíos de Mercado Libre | costos_operacionales | 16,077 | $-66,467,947 |
| bigger_than_expected_fashion | Ajuste por Talla/Garantía | ajustes | 1,758 | $55,271,088 |
| smaller_than_expected_fashion | Ajuste por Talla/Garantía | ajustes | 1,551 | $43,000,269 |
| reconciled | Ajuste Poscobro Conciliado | ajustes | 1,244 | $40,845,693 |
| Cargo por campaña de publicidad - Product Ads | Cargo por campaña de publicidad - Produc | costos_comerciales | 42 | $-21,681,625 |
| Campañas de publicidad - Display | Campañas de publicidad - Display | costos_comerciales | 15 | $-19,023,802 |
| Cargo por Asesoría Comercial | Cargo por Asesoría Comercial | costos_comerciales | 16 | $-16,462,046 |
| repentant_buyer | Ajuste por Arrepentimiento | ajustes | 537 | $15,508,764 |
| dont_want_it_another_cause_fashion | Ajuste por Arrepentimiento | ajustes | 472 | $14,665,088 |
| Anulación del cargo por venta | Anulación del cargo por venta | costos_comerciales | 2,995 | $12,595,193 |
| undelivered_repentant_buyer | Ajuste por Arrepentimiento | ajustes | 346 | $9,645,495 |
| Cargo por campaña de publicidad - Brand Ads | Cargo por campaña de publicidad - Brand  | costos_comerciales | 13 | $-7,066,148 |
| Cargo por Mercado Envíos | Cargo por Mercado Envíos | costos_operacionales | 1,432 | $-6,301,584 |
| Anulación del cargo por envíos de Mercado Libre | Anulación del cargo por envíos de Mercad | costos_operacionales | 1,506 | $6,239,445 |
| different_color_or_size_fashion | Ajuste por Diferencia de Publicación | ajustes | 169 | $5,280,371 |
| undelivered_other | Ajuste por Falla en Entrega | ajustes | 115 | $3,640,445 |
| compensated | Ajuste Poscobro Conciliado | ajustes | 104 | $3,545,575 |
| item_not_useful_fashion_different_change | Ajuste por Arrepentimiento | ajustes | 92 | $3,251,645 |
| Ajuste Poscobro | Ajuste Poscobro General | ajustes | 634 | $3,108,659 |
| not_match_size_guide_fashion | Ajuste por Talla/Garantía | ajustes | 89 | $2,829,810 |
| Cargo por servicio de almacenamiento Full | Cargo por servicio de almacenamiento Ful | costos_operacionales | 1,003 | $-2,570,731 |
| broken_item_fashion | Ajuste por Producto Dañado/Vacío | ajustes | 82 | $2,526,279 |
| Cargo por retiro de stock Full | Cargo por retiro de stock Full | costos_operacionales | 1,771 | $-2,200,469 |
| estimated_delivery_out_of_time | Ajuste por Retraso en Entrega | ajustes | 72 | $1,846,587 |
| different_color_or_size_fashion_change | Ajuste por Diferencia de Publicación | ajustes | 37 | $1,296,844 |
| different_than_published | Ajuste por Diferencia de Publicación | ajustes | 39 | $1,207,620 |
| Cargo por devolución | Cargo por devolución | costos_operacionales | 180 | $-1,145,720 |
| Campañas de publicidad - Product Ads | Campañas de publicidad - Product Ads | costos_comerciales | 1 | $-945,405 |
| bpp_covered | Ajuste por Compra Protegida (BPP) | ajustes | 37 | $921,722 |
| Anulación del cargo por Mercado Envíos | Anulación del cargo por Mercado Envíos | costos_operacionales | 188 | $799,471 |
| unauthorized_purchase | Ajuste por Disputa no Respondida | ajustes | 21 | $754,140 |
| delivered_but_not_receive_package | Ajuste por Falla en Entrega | ajustes | 23 | $616,130 |
| change_receiver_address | Ajuste por Cambio de Dirección | ajustes | 24 | $614,002 |
| different_item_other | Ajuste por Diferencia de Publicación | ajustes | 16 | $557,340 |
| Campañas de publicidad - Brand Ads	 | Campañas de publicidad - Brand Ads | costos_comerciales | 1 | $-536,145 |
| Cargo | Abono manual | ajustes | 85 | $-405,701 |
| Cargo por mantenimiento de Mi página | Cargo por mantenimiento de Mi página | costos_comerciales | 17 | $-288,830 |
| delivery_date_was_not_met | Ajuste por Retraso en Entrega | ajustes | 11 | $253,040 |
| different_color_or_size | Ajuste por Diferencia de Publicación | ajustes | 4 | $227,960 |
| out_of_stock | Ajuste por Falta de Stock | ajustes | 5 | $194,040 |
| partially_bpp_refunded | Ajuste por Compra Protegida (BPP) | ajustes | 4 | $187,940 |
| not_reconciled | Ajuste Poscobro General | ajustes | 5 | $176,950 |
| Anulación del cargo por devolución | Anulación del cargo por devolución | costos_operacionales | 26 | $170,740 |
| refund_account_money | Ajuste Poscobro General | ajustes | 5 | $169,467 |
| Cargo por stock antiguo en Full | Cargo por stock antiguo en Full | costos_operacionales | 216 | $-144,440 |
| missing_item | Ajuste por Ítem Faltante | ajustes | 7 | $130,930 |
| Cargo por campaña de publicidad - Display programático | Cargo por campaña de publicidad - Displa | costos_comerciales | 18 | $-119,586 |
| respondent_unanswered | Ajuste por Disputa no Respondida | ajustes | 6 | $112,150 |
| missing_accessories | Ajuste por Ítem Faltante | ajustes | 3 | $108,970 |
| ppv_covered_melienvio | Ajuste por Compra Protegida (BPP) | ajustes | 3 | $81,970 |
| missing_invoice | Ajuste Poscobro General | ajustes | 4 | $78,384 |
| Cargo por sobrepasar espacio Full | Cargo por sobrepasar espacio Full | costos_operacionales | 11 | $-73,000 |
| damaged_package_broken_item_fashion | Ajuste por Producto Dañado/Vacío | ajustes | 1 | $63,990 |
| Bonificación | Bonificación | ingresos | 12 | $60,231 |
| bought_by_mistake | Ajuste por Arrepentimiento | ajustes | 1 | $53,990 |
| empty_box | Ajuste por Producto Dañado/Vacío | ajustes | 3 | $48,970 |
| ppv_valid | Ajuste por Compra Protegida (BPP) | ajustes | 1 | $39,990 |
| INVALID_AUTHORIZATION | Ajuste Poscobro General | ajustes | 1 | $38,990 |
| buy_out_of_ml | Ajuste por Arrepentimiento | ajustes | 1 | $23,990 |
| CREDIT_NOT_PROCESSED | Ajuste Poscobro General | ajustes | 1 | $21,990 |
| different_item_other_change | Ajuste por Diferencia de Publicación | ajustes | 1 | $19,990 |
| item_not_useful_fashion_different | Ajuste por Arrepentimiento | ajustes | 1 | $18,990 |
| not_expected_quality_different | Ajuste por Diferencia de Publicación | ajustes | 1 | $17,490 |
| Cargo por diferencias en las medidas y el peso del paquete | Cargo por diferencias en las medidas y e | costos_operacionales | 11 | $-11,100 |
| by_admin | Ajuste Poscobro General | ajustes | 3 | $7,084 |
| Anulación del cargo por envíos de Mercado Libre | Campañas de publicidad - Display | costos_comerciales | 1 | $4,550 |
| refunded | Ajuste Poscobro General | ajustes | 1 | $1,208 |

## RIPLEY

| Metric | Value |
|---|---:|
| Rows | 269,216 |
| SUM | $284,897,360 |
| NULL financial_group | 8413 |
| NULL clasificacion_operativa | 0 |
| NO_CLASIFICADO | 0 |

### Financial Groups

| Group | Rows | Total |
|---|---|---:|
| ingresos | 8,413 | $240,979,600 |
| NULL | 8,413 | $142,448,680 |
| ajustes | 67,304 | $-30,372 |
| costos_operacionales | 109,369 | $-10,414,357 |
| costos_comerciales | 67,304 | $-34,027,680 |
| devoluciones | 8,413 | $-54,058,511 |

### Transaction Types

| Detalle | Clasificación | FG | Rows | Total |
|---|---|---|---:|---:|
| Importe del pedido | Importe del pedido | ingresos | 8,413 | $240,979,600 |
| A pagar | A pagar | NULL | 8,413 | $142,448,680 |
| Pedidos reembolsados | Pedidos reembolsados | devoluciones | 8,413 | $-54,058,511 |
| Comisiones sobre pedidos | Comisiones sobre pedidos | costos_comerciales | 8,413 | $-43,881,350 |
| Envío | Envío | costos_operacionales | 8,413 | $12,536,704 |
| Gastos de envío pagados por el operador | Gastos de envío pagados por el operador | costos_operacionales | 8,413 | $-12,536,704 |
| Comisiones sobre pedidos reembolsados | Comisiones sobre pedidos reembolsados | costos_comerciales | 8,413 | $9,853,670 |
| Descuento por costo logístico | Descuento por costo logístico | costos_operacionales | 8,413 | $-9,527,643 |
| Envío reembolsado | Envío reembolsado | costos_operacionales | 8,413 | $-1,125,187 |
| Gastos de envío reembolsados pagados por el operador | Gastos de envío reembolsados pagados por | costos_operacionales | 8,413 | $1,125,187 |
| Descuento por logistica inversa | Descuento por logística inversa | costos_operacionales | 8,413 | $-886,714 |
| Descuento por cancelación | Descuento por cancelación | ajustes | 8,413 | $-26,412 |
| Otros descuentos | Otros descuentos | ajustes | 8,413 | $-3,960 |
| Descuento FF - Otros | Descuento FF - Otros | costos_operacionales | 8,413 | $0 |
| Descuento por error de clase logistica | Descuento por error de clase logistica | costos_operacionales | 8,413 | $0 |
| Descuento oferta TC - OPEX | Descuento oferta TC - OPEX | costos_comerciales | 8,413 | $0 |
| Cobro despacho primera milla | Cobro despacho primera milla | costos_operacionales | 8,413 | $0 |
| Descuento FF - sobreestadía | Descuento FF - sobreestadía | costos_operacionales | 8,413 | $0 |
| Abono oferta TC - OPEX | Abono oferta TC - OPEX | costos_comerciales | 8,413 | $0 |
| Abonos soluciones comerciales | Abonos soluciones comerciales | costos_comerciales | 8,413 | $0 |
| Abono por error de comisión | Abono por error de comisión | ajustes | 8,413 | $0 |
| Descuento por compensación a cliente | Descuento por compensación a cliente | ajustes | 8,413 | $0 |
| Abonos por cupón promocional | Abonos por cupón promocional | costos_comerciales | 8,413 | $0 |
| Descuento por cupones de despacho | Descuento por cupones de despacho | costos_comerciales | 8,413 | $0 |
| Descuento por PDM | Descuento por PDM | costos_comerciales | 8,413 | $0 |
| Abono postventa | Abono postventa | ajustes | 8,413 | $0 |
| Descuento FF - pick and pack | Descuento FF - pick and pack | costos_operacionales | 8,413 | $0 |
| Abono por uso de flota propia | Abono por uso de flota propia | costos_operacionales | 8,413 | $0 |
| Otros abonos | Otros abonos | ajustes | 8,413 | $0 |
| Descuento operacional | Descuento operacional | costos_operacionales | 8,413 | $0 |
| Abono extraordinario - error de precio | Abono extraordinario - error de precio | ajustes | 8,413 | $0 |
| Abono por formalización a OPL | Abono por formalización a OPL | ajustes | 8,413 | $0 |

## PARIS

| Metric | Value |
|---|---:|
| Rows | 42,487 |
| SUM | $378,104,933 |
| NULL financial_group | 0 |
| NULL clasificacion_operativa | 0 |
| NO_CLASIFICADO | 0 |

### Financial Groups

| Group | Rows | Total |
|---|---|---:|
| ingresos | 21,645 | $533,201,155 |
| ajustes | 21 | $1,375,357 |
| costos_operacionales | 16,328 | $-24,578,542 |
| devoluciones | 4,493 | $-131,893,037 |

### Transaction Types

| Detalle | Clasificación | FG | Rows | Total |
|---|---|---|---:|---:|
| Venta | Venta | ingresos | 19,647 | $525,039,911 |
| Devolución | Devolución | devoluciones | 4,493 | $-131,893,037 |
| Cobro por despacho | Cobro por despacho | costos_operacionales | 15,165 | $-19,547,510 |
| Despacho | Despacho | ingresos | 1,996 | $7,888,014 |
| Logística inversa | Logística inversa | costos_operacionales | 1,147 | $-3,085,430 |
| Retiro stock bodega Paris | Retiro stock bodega Paris | costos_operacionales | 5 | $-1,630,800 |
| Compensación logística | Compensación logística | ajustes | 6 | $1,618,057 |
| Ajuste Inventario Activo | Ajuste Inventario Activo | ajustes | 8 | $647,108 |
| Cargo | Abono manual | ajustes | 5 | $-646,295 |
| Cobro stock antiguo | Cobro stock antiguo | costos_operacionales | 11 | $-314,802 |
| Rebate | Rebate | ingresos | 2 | $273,230 |
| Cobro por campaña | Cobro por campaña | ajustes | 1 | $-260,504 |
| Merma | Merma | ajustes | 1 | $16,991 |

## FALABELLA

| Metric | Value |
|---|---:|
| Rows | 1,008 |
| SUM | $2,583,016 |
| NULL financial_group | 0 |
| NULL clasificacion_operativa | 0 |
| NO_CLASIFICADO | 0 |

### Financial Groups

| Group | Rows | Total |
|---|---|---:|
| ingresos | 125 | $4,661,810 |
| ajustes | 4 | $-840 |
| costos_operacionales | 586 | $-382,750 |
| costos_comerciales | 266 | $-741,650 |
| devoluciones | 27 | $-953,554 |

### Transaction Types

| Detalle | Clasificación | FG | Rows | Total |
|---|---|---|---:|---:|
| Pago por precio del producto | Pago por precio del producto | ingresos | 125 | $4,661,810 |
| Descuento por devolución de producto | Descuento por devolución de producto | devoluciones | 27 | $-953,554 |
| Cobro por comisión por venta | Cobro por comisión por venta | costos_comerciales | 125 | $-932,359 |
| Cobro por cofinanciamiento logístico | Cobro por cofinanciamiento logístico | costos_operacionales | 103 | $-326,131 |
| Cobro Promo envío falabella.com | Cobro Promo envío falabella.com | costos_operacionales | 92 | $-298,494 |
| Reembolso por Promo envío falabella.com | Reembolso por Promo envío falabella.com | costos_operacionales | 92 | $298,494 |
| Reembolso por comisión por venta | Reembolso por comisión por venta | costos_comerciales | 27 | $190,709 |
| Pago de envío comprador | Pago de envío comprador | costos_operacionales | 125 | $140,892 |
| Reversa de pago de envío comprador | Reversa de pago de envío comprador | costos_operacionales | 125 | $-140,892 |
| Cobro por logística inversa | Cobro por logística inversa | costos_operacionales | 27 | $-65,859 |
| Pago por envío directo | Pago por envío directo | costos_operacionales | 22 | $9,240 |
| Corrección de cobro por envío directo | Corrección de cobro por envío directo | ajustes | 4 | $-840 |
| Pago de aporte promocionales a cliente (Promo) | Pago de aporte promocionales a cliente ( | costos_comerciales | 92 | $0 |
| Descuento por aportes promocionales a clientes (Promo) | Descuento por aportes promocionales a cl | costos_comerciales | 22 | $0 |
