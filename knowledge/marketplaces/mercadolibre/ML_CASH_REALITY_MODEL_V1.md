# ML_CASH_REALITY_MODEL_V1 — Certified Cash Reality Model

**CERTIFICADO 005**
**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** G6_CASH_REALITY_CERTIFICATION, RFC_CASH_CERTIFICATION_BPP_POSCOBRO, ML_POSCOBRO_FORENSICS

---

## Verdades Fundamentales

| Verdad | Fuente | Propósito |
|--------|--------|-----------|
| **Verdad Transaccional** | Facturación ML | Qué se vendió, a qué precio, qué comisiones |
| **Verdad Fiscal** | Factura + Nota Crédito (XML DTE) | Documentos tributarios que soportan la operación |
| **Verdad Caja** | Liberaciones + Movimientos MP | Cuándo y cuánto dinero realmente se movió |

## Reglas de Cash Reality

### Regla 1: Movimiento de dinero ≠ Evento económico

```
Liberación = flujo de caja
Venta = evento económico

Una venta puede liberarse en múltiples pagos.
Un pago puede contener múltiples ventas.
NO son equivalentes.
```

### Regla 2: Liberación ≠ Venta

```
El monto liberado en un período NO equivale
a las ventas del mismo período.

Diferencias esperadas:
- Timing (ventas de marzo se liberan en abril)
- Retenciones (impuestos, comisiones, reservas)
- Ajustes (devoluciones, reclamos)
```

### Regla 3: Cobro ≠ Venta

```
Cobro es CASH.
Venta es ACCRUAL.

El cobro ocurre después de la venta.
Puede incluir ajustes, descuentos, comisiones.
```

## ML Cash Reality (Certified 2025-04)

| Métrica | Valor | Fuente |
|---------|-------|--------|
| DB resultado_neto | $67,207,965 | marketplace_cierre_financiero_v1 |
| Liberaciones neto | $69,879,948 | Abril 2025 Liberaciones |
| Delta | $2,671,983 (3.9%) | Esperado por timing + retenciones |
| Paired orders in cash | 197 (97.5%) | Trazadas a Liberaciones |
| Net cash impact (paired) | -$40,599 ≈ $0 | Doble conteo = ~$0 |

## BPP + Poscobro Cash (Certified ALL-TIME)

| Métrica | Valor |
|---------|-------|
| reserve_for_dispute NET | $45,447 (~$0) |
| Mediación cash OUTFLOW | $10,491,578 (root events) |
| Paired mechanisms (all-time) | $134,402,513 (93.8%) |
| Standalone mechanisms | $8,819,481 (6.2%) |
| **Total mechanisms** | **$143,225,534** |
| **Of which ZERO cash impact** | **$134,402,513 (93.8%)** |

## Cash Proxy por Concepto

| Concepto | Cash Proxy | NET | Confianza |
|----------|-----------|-----|-----------|
| Talla/Garantía | Mediación (Liberaciones) | $10.5M outflow | ALTA |
| Arrepentimiento | Mediación (Liberaciones) | (incluido en Mediación) | ALTA |
| BPP (pareado) | reserve_for_dispute | $0 | ALTA |
| BPP (standalone) | REAL_CASH | $2.8M | ALTA |
| Poscobro Conciliado (pareado) | reserve_for_dispute | $0 | ALTA |
| Poscobro Conciliado (standalone) | REAL_CASH | $3.5M | ALTA |
| reserve_for_dispute | Liberaciones DEBIT vs CREDIT | $45K | ALTA |

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/G6_CASH_REALITY_CERTIFICATION.md` | Cash reality ML 2025-04 |
| `governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md` | BPP+Poscobro cash (PASS CONDITIONAL) |
| `governance/ML_POSCOBRO_FORENSICS.md` | Poscobro forensics |
| `governance/MARKETPLACE_MONEY_FLOW_TRUTH.md` | Money flow por MP |

## Aplicación a otros marketplaces

| Marketplace | Cash source | Status |
|-------------|-------------|--------|
| RIPLEY | A pagar (settlement) | PENDIENTE |
| PARIS | N/A | NO |
| FALABELLA | N/A | NO |
| SHOPIFY | N/A | PENDIENTE |
