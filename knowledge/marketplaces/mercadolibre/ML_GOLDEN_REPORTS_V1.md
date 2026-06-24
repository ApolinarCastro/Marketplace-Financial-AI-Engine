# ML_GOLDEN_REPORTS_V1 — Certified Golden Reports

**CERTIFICADO 001**
**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** Marketplace Financial (`data/db/meli_financial_v4.db`)

---

## Jerarquía Oficial de Fuentes

```
NIVEL A (Fuente Maestra Transaccional)
└── Facturación Mercado Libre (01_Raw/ML/ML_Facturacion/*.xlsx)

NIVEL B (Conciliación de Pagos)
└── Detalle de Pagos (01_Raw/ML/Detalle_Pagos/*.xlsx)

NIVEL C (Conciliación de Caja)
├── Liberaciones (01_Raw/ML/Liberaciones/*.xlsx)
├── Todas las Transacciones (01_Raw/ML/Todas_las_Transacciones/*.xlsx)
└── Estado de Cuenta (01_Raw/ML/Estado_de_Cuenta/*.xlsx)

NIVEL D (Logística)
└── Full (01_Raw/ML/Full/*.xlsx)
```

## Regla Fundamental

```
Facturación ML
    >  (es más confiable que)
Detalle de Pagos
    >
Liberaciones
    >
Caja
```

- **Facturación ML** es la fuente maestra transaccional. Contiene la verdad económica de cada operación.
- **Detalle de Pagos** es la conciliación de pagos (no reemplaza a facturación).
- **Liberaciones** es flujo de caja, NO fuente transaccional.
- **Full** es logística operacional, NO financiera.

## Prohibiciones

- Nunca usar Liberaciones como fuente maestra transaccional.
- Nunca conciliar Liberaciones contra Facturación directa (difieren en timing y propósito).
- Nunca usar Full como fuente de revenue.

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md` | Uso de Liberaciones para cash cross-check |
| `governance/G6_CASH_REALITY_CERTIFICATION.md` | Cash reality vía Liberaciones 2025-04 |
| `governance/SEMANTIC_TRACEABILITY_MATRIX.md` | Trazabilidad semántica entre fuentes |
| `governance/REVENUE_ENGINE_DECOMPOSITION.md` | Revenue drivers por fuente |

## Aplicación a otros marketplaces

| Marketplace | Nivel A | Nivel B | Nivel C | Nivel D |
|-------------|---------|---------|---------|---------|
| RIPLEY | Resumen financiero XLSX | N/A | N/A | N/A |
| PARIS | Transacciones XLSX | N/A | N/A | N/A |
| FALABELLA | Órdenes XLSX | N/A | N/A | N/A |
| SHOPIFY | Ventas totales CSV | N/A | XML DTE | N/A |
