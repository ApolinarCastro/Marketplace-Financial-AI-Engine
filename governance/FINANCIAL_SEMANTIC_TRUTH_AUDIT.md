# FINANCIAL SEMANTIC TRUTH AUDIT
**Priority:** BLOQUEANTE
**Objective:** Auditoría semántica de conceptos en Marketplace Auditor v3.5 y Reporte Gerencial UX1.2.
**Período:** 2025-01-01 hasta la fecha actual
**Marketplaces:** ML, RIPLEY, PARIS, FALABELLA

**Regla de Oro (DEC-019 / P&L Truth):**
*Si un concepto no altera ingresos, costos, margen, resultado neto o caja, NO puede vivir en el P&L. Debe migrar a Inteligencia Operacional.*

---

## 1. TABLA DE AUDITORÍA SEMÁNTICA (CROSS-MARKETPLACE)

| Concepto | Origen Raw | Marketplace | Monto Total (Ref) | Rows (Ref) | Tipo | Justificación de Riesgo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Venta / Order Revenue | Facturación / Sales | ML, Falabella, Paris, Ripley | $$$ | 100k+ | **FINANCIAL_EVENT** | Impacta directamente los Ingresos Brutos (GMV). |
| Comisión por Venta | Facturación / Billed | ML, Falabella, Paris, Ripley | $$$ | 100k+ | **FINANCIAL_EVENT** | Costo directo sobre la venta (COGS). |
| Costo de Envío | Facturación / Shipping | ML, Falabella, Paris, Ripley | $$$ | 85k+ | **FINANCIAL_EVENT** | Gasto logístico operativo. |
| Costo de Almacenaje / Fulfillment | Liquidación / Invoices | ML (Full), Falabella (FBY) | $$$ | 15k+ | **FINANCIAL_EVENT** | OPEX Marketplace. |
| Gastos de Publicidad / Ads | Facturación / Marketing | ML (Product Ads), Paris | $$ | 12k+ | **FINANCIAL_EVENT** | Inversión comercial. |
| Cancelación de Compra | Poscobro / Orders | ML, Falabella, Paris, Ripley | -$$$ | 8k+ | **FINANCIAL_EVENT** | Reversión total de la venta e impuestos. |
| Reembolso por Extravío | Liberaciones / Adjustments | ML, Ripley, Falabella | $$ | 2k+ | **FINANCIAL_EVENT** | Adición a caja / Recuperación de Opex. |
| Talla o Color Incorrecto | Poscobro / Claims | ML, Paris, Falabella | $0 | 3k+ | **OPERATIONAL_REASON** | El impacto P&L es la *Devolución*. El *motivo* es puramente operacional. |
| Producto Dañado en Tránsito | Poscobro / Claims | ML, Ripley | $0 | 1k+ | **OPERATIONAL_REASON** | Explica la causa de un siniestro, no es un cargo financiero _per se_. |
| Arrepentimiento de Compra | Poscobro / Claims | ML, Falabella | $0 | 4k+ | **OPERATIONAL_REASON** | Comportamiento del consumidor. Debe ir a Inteligencia Operacional. |
| Retraso en la Entrega (Delay) | Poscobro / Claims | Falabella, Paris | $0 | 1.5k+ | **OPERATIONAL_REASON** | Indicador de SLA, no deduce dinero directamente de la caja. |
| Chargeback (Contracargo) | Poscobro / Reserve | ML, Ripley | -$$ | 500+ | **MIXED** | Tiene impacto en caja (pérdida de fraude), pero trae inteligencia operativa (riesgo). |
| Retenciones Temporales | Liberaciones / Reserve | ML | $0 (en P&L) | 800+ | **MIXED** | Afecta el Flujo de Caja (Disponible), pero NO el Resultado Neto (P&L). |
| Mediación / Claims Administrativos | Poscobro | ML, Paris | -$$ / $$ | 1.2k+ | **MIXED** | Requiere separar la resolución financiera (abono/descuento) del reclamo. |

---

## 2. RIESGO DE RECLASIFICACIÓN DE LOS SISTEMAS ACTUALES

El análisis revela el riesgo sistémico de mantener mezclados estos conceptos bajo etiquetas ambiguas como "Ajustes & Retenciones" en el sistema actual v3.5.

*   **Riesgo ALTO:** Combinar _Retenciones Temporales_ con _Gastos de Publicidad_ o _Ajustes por Fraude_. Genera un P&L falso que subestima la caja.
*   **Riesgo MEDIO:** Poner motivos de devolución (ej. _Talla Incorrecta_) en el P&L. Dificulta la lectura financiera cruzada entre Falabella y ML porque cada uno usa descripciones de errores distintas.
*   **Riesgo BAJO:** Mantener los _Reembolsos Logísticos_ dentro de Costos en lugar de Ingresos Extraordinarios (solo afecta el gross margin, no el RN final).

---

## SALIDA FINAL

```yaml
P&L_CORE:
  - Ingresos Brutos (Ventas Marketplace)
  - Devoluciones y Cancelaciones Monetarias
  - Comisiones por Venta
  - Costos de Logística y Fulfillment
  - Publicidad y Marketing Ads
  - Recuperaciones y Compensaciones Monetarias (Abonos)

OPERATIONAL_LAYER:
  - Talla o Color Incorrecto
  - Arrepentimiento de Compra
  - Producto Dañado / Empaque Dañado
  - Falla en la Entrega / Retraso Logístico
  - Cambio de Dirección del Cliente
  - Diferencia de Publicación (Not as described)
  - Tasa de Contactabilidad (SLA)

MIXED_CONCEPTS:
  - Chargebacks (Requiere partición: Gasto Financiero al P&L, Registro de Fraude a Operacional)
  - Retenciones / Reservas Temporales (Requiere partición: Resta a Caja Disponible, No Toca P&L)
  - Mediaciones (Requiere partición: Indemnización Monetaria al P&L, Motivo de disputa a Operacional)

RIESGO_DE_RECLASIFICACION:
  - ALTO (Contaminar el P&L con metadatos de reclamos distorsiona el margen operativo transversal)

RECOMMENDED_FINAL_STRUCTURE:
  - VISTA_FINANCIERA (P&L): GMV -> Net Revenue -> Marketplace COGS -> Opex -> Resultado Neto. (Exclusivo para conceptos FINANCIAL_EVENT).
  - VISTA_CAJA (Cashflow): Disponible + Liberaciones - Retenciones - Transferencias. (Exclusivo para movimientos de Fideicomiso/Liquidez).
  - VISTA_OPERACIONAL (Intelligence): Pareto de motivos de devolución, SLAs, Claims. (Exclusivo para conceptos OPERATIONAL_REASON).
```
