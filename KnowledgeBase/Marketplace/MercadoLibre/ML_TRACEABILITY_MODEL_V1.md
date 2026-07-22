# ML_TRACEABILITY_MODEL_V1 — Certified Traceability Model

**CERTIFICADO 004**
**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** SEMANTIC_TRACEABILITY_MATRIX, MULTIPLE XML certifications

---

## Jerarquía Oficial de Llaves

```
1. numero_venta       → ID de la transacción original
2. numero_pago        → ID del pago asociado
3. numero_envio       → ID del envío
4. numero_paquete     → ID del paquete logístico
5. numero_cargo       → ID del cargo en facturación
6. cargo_que_bonifica → ID del cargo que este concepto bonifica/ajusta
```

## Reglas de Trazabilidad

### Prohibiciones

- **NO depender exclusivamente de `id_orden`**: Una orden puede tener múltiples pagos, cargos, envíos y ajustes.
- **NO depender exclusivamente de `id_paquete`**: Un paquete puede contener múltiples órdenes.
- **NO asumir que `numero_venta` = `numero_pago`**: Son dominios diferentes.

### Reglas

| Regla | Descripción |
|-------|-------------|
| T1 | Cada fila en el ledger debe poder rastrearse hasta su source file. |
| T2 | El source file debe tener un ID único estable entre exports. |
| T3 | La trazabilidad debe ser bidireccional: ledger → source y source → ledger. |
| T4 | `folio_xml` es la llave de trazabilidad fiscal (DTE). |
| T5 | `id_transaccion` es la llave de trazabilidad interna del ledger. |

## Niveles de Trazabilidad

```
NIVEL 1 (Ledger → Source)
  id_transaccion → archivo_origen + fila específica

NIVEL 2 (Ledger → XML)
  folio_xml → dte_truth_v1.folio

NIVEL 3 (Ledger → Cash)
  id_transaccion → Liberaciones (via reserve_for_dispute / Mediación)

NIVEL 4 (Ledger → Economic Event)
  id_orden + clasificacion_operativa → ROOT_EVENT vs MECHANISM
```

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/SEMANTIC_TRACEABILITY_MATRIX.md` | Trazabilidad semántica completa |
| `governance/XML_TRACEABILITY_CERTIFICATION.md` | Cobertura XML (30.2%) |
| `governance/MARKETPLACE_XML_LEDGER_COMPLETENESS_CERTIFICATION.md` | XML vs ledger ($12.6M gap) |
| `governance/XML_BUSINESS_SEMANTICS_CERTIFICATION.md` | Semántica de negocio XML |

## Aplicación a otros marketplaces

| Marketplace | Llave principal | Source ID | XML bridge |
|-------------|----------------|-----------|------------|
| RIPLEY | `id_orden` | Folio XLSX | NO (0/62,502 matched) |
| PARIS | `folio` | Folio comprobante | SÍ (48/54 XMLs) |
| FALABELLA | `id_orden` | Transaction ID | SÍ (100% folio traceable) |
| SHOPIFY | `ID de venta` (CSV) | Por determinar | Por determinar (110 XMLs) |
