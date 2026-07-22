# ML_FULL_RULES_V1 — Certified Full Reconciliation Rules

**CERTIFICADO 008**
**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** ML_POSCOBRO_FORENSICS, MARKETPLACE_CHARGE_RECONCILIATION_CERTIFICATION

---

## Regla Fundamental de Full

```
Venta presente en Full
y ausente en Liquidaciones

NO implica inexistencia.
```

### Clasificación Correcta

```
VENTA_EXISTENTE       → La venta existe en el sistema
LIQUIDACION_PENDIENTE → La liquidación fiscal no se ha emitido aún

Asumir VENTA_EXISTENTE hasta demostrar lo contrario.
```

### Error Histórico a Evitar

```
❌ Venta en Full pero no en Liquidaciones = Venta no existe
✅ Venta en Full pero no en Liquidaciones = Timing difference
```

## Reglas de Full

| Regla | Descripción |
|-------|-------------|
| F1 | Full es logística operacional, NO fuente financiera. |
| F2 | No conciliar Full directamente contra revenue. |
| F3 | Full puede contener ventas no liquidadas aún fiscalmente. |
| F4 | La ausencia en Liquidaciones no invalida la existencia de la venta. |
| F5 | Full debe analizarse junto con Facturación ML y Todas las Transacciones. |

## Relación con Otras Fuentes

```
Full (Logística)
  │
  ├── ¿La venta aparece en Facturación ML?
  │     ├── SÍ → Venta existe, puede tener liquidación pendiente
  │     └── NO → Investigar: ¿error de carga? ¿timing?
  │
  ├── ¿La venta aparece en Todas las Transacciones?
  │     ├── SÍ → Venta existe, confirmada por source alternativo
  │     └── NO → Posible error en exportación Full
  │
  └── ¿Hay ajuste Poscobro asociado?
        ├── SÍ → La venta puede haber sido ajustada
        └── NO → Sin ajustes registrados
```

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/ML_POSCOBRO_FORENSICS.md` | Poscobro + Full analysis |
| `governance/MARKETPLACE_CHARGE_RECONCILIATION_CERTIFICATION.md` | Charge reconciliation |
| `governance/MARKETPLACE_WATERFALL_CERTIFICATION.md` | Waterfall completo |

## Aplicación a otros marketplaces

Full es específico de Mercado Libre (logística fulfillment). No aplica a RIPLEY, PARIS, FALABELLA o SHOPIFY.
