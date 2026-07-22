# EVENT_MODEL_CORE_V1 — Abstract Financial Event Model

**Estado:** CERTIFICADO (versión abstracta, no marketplace-specific)
**Fecha:** 2026-06-05
**Primer marketplace certificado:** Mercado Libre

---

## Definiciones Core

```
ROOT_EVENT
    Evento económico real con impacto en caja.
    → Participa en Resultado Neto
    → Se preserva en auditoría

EXECUTION_MECHANISM
    Ejecución operacional que refleja un ROOT_EVENT existente.
    → Se excluye de Resultado Neto cuando está pareado
    → Se preserva en auditoría
    → Se preserva en Resultado Neto cuando es STANDALONE

STANDALONE
    MECHANISM sin ROOT_EVENT en la misma orden.
    → Representa cash real (no es mirror)
    → Se preserva en Resultado Neto
```

## Regla Universal

```
Por cada orden (id_orden):
  Si tiene SOLO UN concepto → participa en Resultado Neto
  Si tiene ROOT_EVENT + MECHANISM pareados:
    → ROOT_EVENT participa en Resultado Neto
    → MECHANISM se excluye de Resultado Neto
    → Ambos se preservan en auditoría
  Si tiene MECHANISM STANDALONE:
    → Se preserva en Resultado Neto
```

## Aplicación por Marketplace

| Marketplace | ROOT_EVENTS | MECHANISMS | Estado |
|-------------|-------------|------------|--------|
| Mercado Libre | 14 concepts | 3 (BPP, Poscobro Conciliado, Poscobro General) | **CERTIFICADO** |
| RIPLEY | All concepts | None identified | PENDIENTE |
| PARIS | All concepts | None identified | PENDIENTE |
| FALABELLA | All concepts | None identified | PENDIENTE |
| SHOPIFY | All concepts (hypothesis) | None identified | PENDIENTE |

## Cómo detectar MECHANISMS

```
Para cada marketplace nuevo:
  1. Agrupar transacciones por id_orden
  2. Identificar órdenes con MÚLTIPLES conceptos
  3. Buscar pares donde:
     a) Dos conceptos tienen el mismo monto (exacto o aproximado)
     b) Un concepto es "causa" (evento) y el otro es "efecto" (ajuste)
     c) El "efecto" tiene cash NET ≈ $0
  4. Si se encuentra el patrón → aplicar modelo ML
  5. Si NO se encuentra → todos los conceptos = ROOT_EVENT
```

## Validación Requerida

```
Para certificar event model en un marketplace:
  ✓ Análisis de pares por id_orden
  ✓ Cash cross-check (Liberaciones o equivalente)
  ✓ reserve_for_dispute NET ≈ $0 (si aplica)
  ✓ Concept typology (standalone %)
  ✓ Regresión 14/14
```

## Arquitectura

La regla debe implementarse en una **nueva capa entre clasificación y cierre**:

```
Loader → Ledger → Clasificación → Clasificado → EVENT_MODEL → Cierre → API
                                                    │
                                              Nueva capa:
                                              - Groupby id_orden
                                              - Asignar event_role
                                              - Marcar parejas
                                              - Preservar standalone
```

## Certificaciones Core

| Documento | Relación |
|-----------|----------|
| `governance/RFC_EVENT_MODEL_CERTIFICATION.md` | PASS — rule is deterministic |
| `governance/RFC_CASH_CERTIFICATION_BPP_POSCOBRO.md` | PASS CONDITIONAL — cash evidence |
| `governance/RFC_EVENT_RULE_LOCATION.md` | Opción D (nueva capa) |
| `governance/G6_1_RESULTADO_NETO_EVENTS_VS_RECORDS.md` | FAIL — records ≠ events |
| `knowledge/marketplaces/mercadolibre/ML_FINANCIAL_EVENT_MODEL_V1.md` | ML certified implementation |
