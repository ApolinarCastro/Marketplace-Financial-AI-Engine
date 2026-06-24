# ML_FACTURATION_MODEL_V1 — Certified Facturation Model

**Estado:** CERTIFICADO
**Fecha:** 2026-06-05
**Fuente oficial:** RAW_TO_CLASSIFICATION_MAP, SEMANTIC_TRACEABILITY_MATRIX, MARKETPLACE_CONCEPT_MASTER_CERTIFICATION

---

## Estructura de Facturación ML

Facturación ML es el Nivel A (Fuente Maestra Transaccional). Contiene:

- **Ventas**: Cargo por venta (Venta) — positive, `financial_group=ingresos`
- **Comisiones**: Cargo por venta (Comisión) — negative, `financial_group=costos_comerciales`
- **Envíos**: Cargo por Mercado Envíos / Cargo por envíos de Mercado Libre — `costos_operacionales`
- **Full**: Almacenamiento, retiro, stock antiguo, sobrepasar espacio — `costos_operacionales`
- **Devoluciones**: Devolución de venta — `devoluciones`
- **Publicidad**: Product Ads, Brand Ads, Display — `costos_comerciales`
- **Servicios**: Asesoría Comercial, Mantenimiento Mi página — `costos_comerciales`
- **Bonificaciones**: Bonificación — `ingresos`
- **Ajustes**: Mediación, Cancelación de la mediación, cashback — `ajustes`

## Mapeo a Classification

El mapa oficial `RAW_TO_CLASSIFICATION_MAP` contiene **~85 entries principales** para ML, más **~40 códigos técnicos de Poscobro** en inglés.

### Reglas de Mapeo

| Regla | Descripción |
|-------|-------------|
| M1 | Cada raw detail único debe mapearse a EXACTAMENTE UNA clasificación canónica. |
| M2 | Variantes de encoding (tildes, caracteres especiales) deben normalizarse antes del mapeo. |
| M3 | Códigos técnicos en inglés deben mapearse a conceptos canónicos en español. |
| M4 | Conceptos nuevos sin mapeo → `NO_CLASIFICADO` (confianza=0) hasta certificación. |
| M5 | El mapa es inmutable una vez certificado. Cambios requieren RFC. |

### Ejemplos de Normalización

| Raw detail (source) | Canonical | Grupo |
|---------------------|-----------|-------|
| `"Cargo por venta (Venta)"` | `"Cargo por venta (Venta)"` | ingresos |
| `"Cargo por venta (Comisión)"` | `"Cargo por venta (Comisión)"` | costos_comerciales |
| `"Devolucin de dinero\nEnvo"` | `"Devolución de dinero\nEnvío"` | devoluciones |
| `"smaller_than_expected_fashion"` | `"Ajuste por Talla/Garantía"` | ajustes |
| `"bpp_refunded"` | `"Ajuste por Compra Protegida (BPP)"` | ajustes |
| `"nan"` | `"Ajuste Poscobro General"` | ajustes |

## Loader Spec

| Parámetro | Valor |
|-----------|-------|
| Formato | XLSX (Excel) |
| Frecuencia | Mensual |
| Patrón archivo | `YYYY_MM.xlsx` |
| Date column | Fecha de cargo |
| ID generation | `id_transaccion = tipo + order_id + file + idx` |
| Sign convention | Ingresos = +, Costos = -, Ajustes = según corresponda |
| Folio extraction | Extraído de columna Folio en source |

## Certificaciones Asociadas

| Documento | Relación |
|-----------|----------|
| `governance/MARKETPLACE_CONCEPT_MASTER_CERTIFICATION.md` | Concept master (100% identificados) |
| `governance/SEMANTIC_TRACEABILITY_MATRIX.md` | Trazabilidad semántica |
| `governance/FINANCIAL_EXPLAINABILITY_CERTIFICATION.md` | Explainability de 7 conceptos críticos |
| `governance/REVENUE_ENGINE_DECOMPOSITION.md` | Revenue drivers ML |

## Aplicación a otros marketplaces

Cada marketplace requiere su propio mapa de clasificación. El patrón RAW_TO_CLASSIFICATION_MAP es universal, pero los conceptos son específicos.
