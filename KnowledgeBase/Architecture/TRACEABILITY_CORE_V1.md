# TRACEABILITY_CORE_V1 — Abstract Traceability Framework

**Estado:** CERTIFICADO (versión abstracta)
**Fecha:** 2026-06-05
**Primer marketplace certificado:** Mercado Libre

---

## Definiciones Core

```
TRAZABILIDAD = capacidad de rastrear una transacción
desde su origen (source file) hasta su destino (Resultado Neto),
pasando por todas las capas de transformación.
```

## Niveles de Trazabilidad (Universal)

```
NIVEL 1 — Source Traceability
  ¿De qué archivo y fila proviene esta transacción?
  Requisito: archivo_origen + ID único en source

NIVEL 2 — Classification Traceability
  ¿Cómo se clasificó esta transacción?
  Requisito: clasificacion_operativa + confianza + origen

NIVEL 3 — Fiscal Traceability
  ¿Qué documento tributario soporta esta transacción?
  Requisito: folio_xml + dte_truth_v1

NIVEL 4 — Cash Traceability
  ¿Esta transacción corresponde a dinero real?
  Requisito: Liberaciones o cash source equivalente

NIVEL 5 — Economic Event Traceability
  ¿Es ROOT_EVENT o MECHANISM?
  Requisito: event_role + pair_id (si aplica)
```

## Llaves de Trazabilidad (Universal)

```
JERARQUÍA DE LLAVES (de más a menos específica):

1. transaction_id (único, estable entre exports)
2. order_id (agrupa transacciones de una misma orden)
3. fiscal_id (folio DTE, factura, nota crédito)
4. payment_id (id del pago asociado)
5. logistic_id (id de envío, paquete)

REGLAS:
  - Cada transacción debe tener AL MENOS transaction_id
  - transaction_id debe ser único entre exports
  - No depender exclusivamente de order_id
  - No depender exclusivamente de logistic_id
```

## Matriz de Trazabilidad por Marketplace

| Marketplace | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
|-------------|---------|---------|---------|---------|---------|
| **ML** | ✅ (XLSX + id_transaccion) | ✅ (clasificado_v1) | ⚠️ (30.2% folio_xml) | ✅ (Liberaciones) | ✅ (certificado) |
| RIPLEY | ✅ (XLSX + id_transaccion) | ✅ (clasificado_v1) | ❌ (0% folio) | ⚠️ (A pagar) | ❌ |
| PARIS | ✅ (XLSX + id_transaccion) | ✅ (clasificado_v1) | ⚠️ (51% XML) | ❌ | ❌ |
| FALABELLA | ✅ (XLSX + id_transaccion) | ✅ (clasificado_v1) | ✅ (100% folio) | ❌ | ❌ |
| SHOPIFY | ⚠️ (CSV, ID existe) | ❌ | ⚠️ (110 XMLs) | ❌ | ❌ |

## Reglas de Trazabilidad

| Regla | Descripción |
|-------|-------------|
| T1 | Toda fila en el ledger debe tener `archivo_origen` poblado. |
| T2 | Toda fila debe tener `id_transaccion` único generado por el loader. |
| T3 | `id_transaccion` debe ser determinista (mismo source → mismo ID). |
| T4 | `folio_xml` debe poblarse desde el source file o bridge. |
| T5 | Clasificación debe ser reproducible (mismo source → misma clasificación). |
| T6 | Trazabilidad debe ser bidireccional: ledger → source y source → ledger. |

## Certificaciones Core

| Documento | Relación |
|-----------|----------|
| `governance/SEMANTIC_TRACEABILITY_MATRIX.md` | Mapeo semántico completo |
| `governance/XML_TRACEABILITY_CERTIFICATION.md` | Cobertura XML |
| `governance/XML_BUSINESS_SEMANTICS_CERTIFICATION.md` | Semántica de negocio |
| `knowledge/marketplaces/mercadolibre/ML_TRACEABILITY_MODEL_V1.md` | ML certified implementation |
