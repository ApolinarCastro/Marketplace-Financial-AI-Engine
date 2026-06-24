# G3.1 — Marketplace Economic Dictionary

**Date:** 2026-06-03  
**Scope:** Formal economic definition of every charge concept across ML, RIPLEY, PARIS, FALABELLA  
**Criterion:** Each charge must answer: What is it? Why does it exist? Who charges? Where backed? P&L impact?

---

## Structure

Each entry follows this format:

```
## {Concept Name}
- **Naturaleza económica:** 
- **Razón de existencia:**
- **Quién cobra → Quién paga:**
- **Respaldo documental:**
- **Cobertura XML:**
- **Impacto P&L:**
- **Clasificación auditor:**
- **Clasificación 360:**
```

---

## 1. VENTA (Ingreso Bruto)

### 1a. Importe del pedido (RIPLEY) / Cargo por venta — Venta (ML) / Venta (PARIS) / Pago por precio del producto (FALABELLA)

- **Naturaleza económica:** Ingreso bruto por venta de bienes. Es el dinero que el comprador paga por el producto, que el marketplace recauda y debe transferir al vendedor (neto de comisiones y gastos).
- **Razón de existencia:** Es la transacción económica fundamental del marketplace: un comprador adquiere un producto de un vendedor. El marketplace actúa como intermediario de pago.
- **Quién cobra → Quién paga:** El marketplace recauda del comprador (por cuenta del vendedor) y lo refleja como ingreso del vendedor en la liquidación.
- **Respaldo documental:** Liquidación XLSX (columna "Importe del pedido" / "Cargo por venta (Venta)" / "Venta" / "Pago por precio del producto"). XML DTE: **NO aplica** — los DTEs cubren cargos del marketplace al vendedor, no el pago del comprador.
- **Cobertura XML:** 0% en todos los marketplaces. Los DTEs no documentan el ingreso bruto del vendedor.
- **Impacto P&L:** **+Ingreso.** Es la línea superior del P&L. Aumenta Ganancia Bruta.
- **Clasificación auditor:** `financial_group = ingresos`, `include_in_operational_pnl = True`
- **Clasificación 360:** `ID_Tipo_Transaccion = 1 (Venta)`

**Ejemplo:** RIPLEY, Importe del pedido = $15,990, orden 24628430501-A. El comprador pagó $15,990 por un producto. RIPLEY retiene ese monto en la liquidación, deduce comisiones y gastos, y paga el neto al vendedor.

---

## 2. COMISIÓN

### 2a. Comisiones sobre pedidos (RIPLEY) / Cargo por venta — Comisión (ML) / Cobro por comisión por venta (FALABELLA)

- **Naturaleza económica:** Cobro del marketplace al vendedor por usar la plataforma de venta. Es la tarifa por intermediación comercial. Generalmente un porcentaje del valor de venta.
- **Razón de existencia:** El marketplace provee infraestructura de venta (plataforma, tráfico, procesamiento de pagos, atención al cliente). La comisión es su ingreso principal.
- **Quién cobra → Quién paga:** El marketplace cobra al vendedor. Se deduce automáticamente del importe del pedido antes de calcular el neto a pagar.
- **Respaldo documental:** 
  - Liquidación XLSX: columna "Comisiones sobre pedidos" (RIPLEY), "Cargo por venta (Comisión)" (ML)
  - XML DTE 33 (Factura): "MKP COMISIÓN COSTO FIJO MKP", "Comision Ventas MKP del: {period}" (RIPLEY), "COMISIONES" (FALABELLA)
- **Cobertura XML:** RIPLEY 87% ($41.8M de $49.1M), FALABELLA 89.7% ($0.83M de $0.74M), PARIS 0% (no existe como línea separada en ledger), ML 0% (XMLs no contienen detalle de comisiones).
- **Impacto P&L:** **-Costo.** Disminuye la Ganancia Bruta. Es un gasto para el vendedor, ingreso para el marketplace.
- **Clasificación auditor:** `financial_group = costos_comerciales`, `include_in_operational_pnl = True`
- **Clasificación 360:** `ID_Tipo_Transaccion = 2 (Comisión)`

**RIPLEY específico:** La comisión RIPLEY tiene 2 subcomponentes:
1. **Costo Fijo MKP** — tarifa fija por transacción (NmbItem: "MKP COMISIÓN COSTO FIJO MKP")
2. **Comisión Periódica** — porcentaje sobre ventas del período (NmbItem: "Comision Ventas MKP del: 28/12/2024 al 13/01/2025")

**PARIS específico:** Paris NO desglosa la comisión como concepto separado en el ledger. La comisión está implícita en el spread entre `Venta` y `Cobro por despacho - Devolución`. La 360 Pipeline la calcula mediante fórmula: `COMISIÓN = Venta * TASA - Acuerdo Comercial`.

---

## 3. LOGÍSTICA — DESPACHO

### 3a. Gastos de envío pagados por el operador (RIPLEY) / Cargo por envíos de Mercado Libre (ML) / Cobro por despacho (PARIS) / Cofinanciamiento logístico (FALABELLA)

- **Naturaleza económica:** Cobro al vendedor por el costo de despacho de productos al comprador. El marketplace contrata y paga al operador logístico, y luego pasa el costo al vendedor.
- **Razón de existencia:** El marketplace ofrece logística integrada. El vendedor no necesita contratar transporte por separado.
- **Quién cobra → Quién paga:** El marketplace cobra al vendedor (deducción en liquidación). El marketplace paga al operador logístico (por separado, no visible en ledger del vendedor).
- **Respaldo documental:**
  - Liquidación XLSX: columna "Gastos de envío pagados por el operador" (RIPLEY), "Cargo por envíos de Mercado Libre" (ML)
  - XML DTE 33/52 (RIPLEY): "MKP Cobro logistico despacho", "DESPACHO DE PRODUCTOS MKP"
  - XML DTE (FALABELLA): "ENVIO: A CARGO DEL CLIENTE"
- **Cobertura XML:** RIPLEY 163% ($31.5M XML vs $19.3M ledger — XML incluye despachos que ledger no desglosa), FALABELLA 278% ($0.88M XML vs $0.32M ledger), PARIS 42% ($8.1M XML vs $19.5M ledger — solo Fulfillment), ML 0%.
- **Impacto P&L:** **-Costo operacional.** Gasto del vendedor.
- **Clasificación auditor:** `financial_group = costos_operacionales`
- **Clasificación 360:** `ID_Tipo_Transaccion = 3 (Costo Envío)`

**RIPLEY estructura logística:**
```
Envío (passthrough): +$18.4M (ingreso que pasa al vendedor, etiqueta de envío pagada por comprador)
Gastos de envío pagados por operador: -$18.4M (costo real del envío, cobrado al vendedor)
Descuento por costo logístico: -$12.8M (descuento/adjuste adicional por logística)
Neto logístico: -$12.8M (costo neto de logística para el vendedor)
```

---

## 4. LOGÍSTICA — INVERSA

### 4a. Descuento por logística inversa (RIPLEY) / Logística inversa (PARIS) / Cargo por logística inversa (FALABELLA) / Cargo por devolución + retiro stock (ML)

- **Naturaleza económica:** Cobro al vendedor por la gestión logística de productos devueltos (transporte de vuelta, recepción, revisión, reposición).
- **Razón de existencia:** Cuando un comprador devuelve un producto, el marketplace gestiona la logística inversa. El costo se traslada al vendedor.
- **Quién cobra → Quién paga:** Marketplace cobra al vendedor.
- **Respaldo documental:** XLSX + XML (RIPLEY DTE: "MKP Cobro despacho logistica inversa" = $3.1M, FALABELLA DTE: "LOGISTICA INVERSA (DEVOLUCIONES)" = $48.7K)
- **Impacto P&L:** **-Costo operacional.**
- **Clasificación auditor:** `costos_operacionales`

---

## 5. ALMACENAMIENTO / FULFILLMENT

### 5a. Cargo por servicio de almacenamiento Full (ML) / Cargo por retiro de stock Full (ML) / Cobro stock antiguo (PARIS)

- **Naturaleza económica:** Cobro al vendedor por almacenar productos en bodegas del marketplace (Full/FF). Incluye almacenamiento, picking, packing, y gestión de inventario.
- **Razón de existencia:** El marketplace ofrece fulfillment (almacenar + despachar). El vendedor paga por el espacio y servicio.
- **Quién cobra → Quién paga:** Marketplace cobra al vendedor.
- **Respaldo documental:** EXCLUSIVAMENTE en liquidaciones XLSX. **No hay XML DTE** que describa estos conceptos como línea separada.
- **Impacto P&L:** **-Costo operacional.**

---

## 6. PUBLICIDAD

### 6a. Cargo por campaña de publicidad — Product Ads / Brand Ads / Display (ML) / Cobro por campaña (PARIS)

- **Naturaleza económica:** Cobro al vendedor por servicios de publicidad dentro del marketplace. El vendedor paga por visibilidad adicional (anuncios en búsqueda, display, marcas).
- **Razón de existencia:** Los vendedores pueden pagar por mayor visibilidad. Es un servicio opcional de valor añadido.
- **Quién cobra → Quién paga:** Marketplace cobra al vendedor.
- **Respaldo documental:** EXCLUSIVAMENTE en liquidaciones XLSX (columnas de Poscobro ML, columna "Cobro por campaña" PARIS). **No hay XML DTE.**
- **Impacto P&L:** **-Costo comercial.**
- **Clasificación auditor:** `costos_comerciales`
- **Clasificación 360:** `ID_Tipo_Transaccion = 4 (Publicidad)`

---

## 7. ACUERDO COMERCIAL

### 7a. MKP Acuerdo comercial (RIPLEY) / Cargo por Asesoría Comercial (ML)

- **Naturaleza económica:** Cargos fijos o periódicos acordados contractualmente entre el marketplace y el vendedor. Incluye suscripciones, espacios preferenciales, tarifas planas.
- **Razón de existencia:** Acuerdos comerciales bilaterales. El vendedor accede a beneficios (categoría premium, volumen, espacios) a cambio de un pago fijo.
- **Quién cobra → Quién paga:** Marketplace cobra al vendedor según contrato.
- **Respaldo documental:** RIPLEY: XML DTE 33 "MKP Acuerdo comercial" = $18.4M. ML: Liquidación (columna "Cargo por Asesoría Comercial" = -$16.5M).
- **Cobertura XML:** RIPLEY 100% ($18.4M en XML, $0 como concepto separado en ledger — absorbido en comisiones+logística). ML 0% (XMLs no contienen). PARIS 0%.
- **Impacto P&L:** **-Costo comercial.**

**Gap económico:** RIPLEY tiene $18.4M en XML como "Acuerdo Comercial" que las liquidaciones ABSORBEN dentro de "Comisiones sobre pedidos" y "Descuento por costo logístico". El vendedor paga el total correcto, pero no ve "Acuerdo Comercial" como línea separada en su liquidación. **$0 pérdida, pero pérdida de transparencia para el vendedor.**

---

## 8. DEVOLUCIÓN / REEMBOLSO

### 8a. Pedidos reembolsados (RIPLEY) / Devolución de venta (ML) / Devolución (PARIS) / Descuento por devolución de producto (FALABELLA)

- **Naturaleza económica:** Reversión de una venta cuando el comprador devuelve el producto o solicita reembolso. El vendedor "pierde" esa venta.
- **Razón de existencia:** Derecho del comprador a devolver productos (garantía legal, satisfacción, defectos).
- **Quién cobra → Quién paga:** El vendedor "paga" (deducción en liquidación) porque la venta se revierte. El marketplace procesa la devolución.
- **Respaldo documental:** Liquidación XLSX + XML (PARIS: "Devoluciones MKP" = $58.6M, 44% del total de devoluciones ledger = $131.9M).
- **Cobertura XML:** 44% PARIS, 0% otros.
- **Impacto P&L:** **-Devolución.** Reduce ingresos brutos para obtener ventas netas.
- **Clasificación auditor:** `financial_group = devoluciones`
- **Clasificación 360:** `ID_Tipo_Transaccion = 6 (Devolución)`

### 8b. Comisiones sobre pedidos reembolsados (RIPLEY) / Reembolso por comisión por venta (FALABELLA)

- **Naturaleza económica:** Devolución de la comisión cuando un pedido es reembolsado. El marketplace no cobra comisión por ventas que no se concretan.
- **Razón de existencia:** Consistencia económica: si la venta se revierte, la comisión también.
- **Impacto P&L:** **+Ingreso (reversión de costo).** Compensa la comisión original.

---

## 9. PROMOCIÓN

### 9a. Cobro Promo envío falabella.com (FALABELLA) / Descuento por aportes promocionales (FALABELLA)

- **Naturaleza económica:** Cobro al vendedor por participar en promociones de envío gratis o descuentos financiados por el marketplace.
- **Razón de existencia:** El marketplace ofrece promociones para atraer compradores. El vendedor puede optar por participar cofinanciando la promoción.
- **Quién cobra → Quién paga:** Marketplace cobra al vendedor (deducción). El marketplace paga al operador logístico o descuenta al comprador.
- **Respaldo documental:** EXCLUSIVAMENTE en liquidaciones XLSX.
- **Impacto P&L:** **-Costo operacional.**

---

## 10. PENALIDAD

### 10a. Descuento por cancelación (RIPLEY) / Otros descuentos (RIPLEY)

- **Naturaleza económica:** Multa o descuento aplicado al vendedor por cancelación de pedidos, incumplimiento de SLA, o mal servicio.
- **Razón de existencia:** Incentivar al vendedor a cumplir estándares de servicio (tiempo de despacho, calidad, disponibilidad).
- **Quién cobra → Quién paga:** Marketplace cobra al vendedor.
- **Respaldo documental:** RIPLEY XML: "MKP Penalidad - Cancelacion" = $42,054. Ledger: "Descuento por cancelación" = -$28,490 + "Otros descuentos" = -$4,950. Delta XML vs Ledger: $8,614 (26%) por reversiones/post-liquidación.
- **Impacto P&L:** **-Costo (ajuste).**
- **Clasificación auditor:** `financial_group = ajustes`

---

## 11. SETTLEMENT (A pagar / Tesorería)

### 11a. A pagar (RIPLEY)

- **Naturaleza económica:** Monto neto que el marketplace transfiere al vendedor después de aplicar todos los cargos, descuentos, devoluciones y ajustes. Es el resultado final de la liquidación.
- **Razón de existencia:** Es el propósito del sistema de liquidación — calcular cuánto debe pagar el marketplace al vendedor por las ventas del período.
- **Quién cobra → Quién paga:** El vendedor recibe del marketplace (tesorería).
- **Respaldo documental:** Liquidación XLSX, columna "A pagar". **No tiene respaldo XML — no es un cargo, es el neto.**
- **Impacto P&L:** **NO impacta P&L operacional.** Es tesorería (movimiento de caja). `include_in_operational_pnl = False`.
- **Clasificación auditor:** `financial_group = NULL` (diseñado — no es ingreso ni gasto, es la resultante).

---

## Summary Statistics

| Concept Family | ML | RIPLEY | PARIS | FALABELLA | Total Amount | P&L |
|---|---|---|---|---|---|---|
| VENTA | 1 concept | 1 concept | 3 concepts | 1 concept | $1,766.8M | +Ingreso |
| COMISIÓN | 1 concept | 2 concepts | 0 (implícita) | 2 concepts | $186.8M | -Costo |
| LOGÍSTICA DESPACHO | 2 concepts | 3 concepts | 1 concept | 3 concepts | $103.6M | -Costo |
| LOGÍSTICA INVERSA | 2 concepts | 1 concept | 2 concepts | 1 concept | $10.8M | -Costo |
| ALMACENAMIENTO | 4 concepts | 0 (XML only) | 1 concept | 0 | $5.1M | -Costo |
| PUBLICIDAD | 4 concepts | 0 | 1 concept | 0 | $49.6M | -Costo |
| ACUERDO COMERCIAL | 1 concept | 1 concept (XML) | 0 | 0 | $34.9M | -Costo |
| DEVOLUCIÓN | 2 concepts | 2 concepts | 1 concept | 1 concept | $308.8M | -Devolución |
| PROMOCIÓN | 0 | 0 | 0 | 3 concepts | $0.6M | -Costo |
| PENALIDAD | 0 | 2 concepts | 0 | 0 | $0.03M | -Ajuste |
| SETTLEMENT | 0 | 1 concept | 0 | 0 | $206.9M | NO P&L |

**Total concepts defined: 42** (all economically significant charges across 4 marketplaces)

---

*Economic definitions based on analysis of: 845 XML DTEs, 150+ XLSX liquidations, marketplace_ledger_v1 (207,600 rows), and marketplace_ledger_clasificado_v1 classification rules.*
