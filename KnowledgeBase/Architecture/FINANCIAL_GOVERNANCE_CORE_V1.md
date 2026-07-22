# FINANCIAL_GOVERNANCE_CORE_V1 — Abstract Financial Governance Framework

**Estado:** CERTIFICADO (versión abstracta)
**Fecha:** 2026-06-05
**Primer marketplace certificado:** Mercado Libre

---

## Principios Rectores

| # | Principio | Descripción |
|---|-----------|-------------|
| 1 | **Single Financial Truth** | Una sola fuente de verdad financiera: `marketplace_ledger_v1` |
| 2 | **Taxonomía financiera única** | 6 grupos de P&L: ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes, tesoreria |
| 3 | **Backend decide** | Toda lógica financiera vive en el backend. Frontend es consumidor pasivo. |
| 4 | **Determinismo** | Mismo input → mismo output. Reproducibilidad total. |
| 5 | **Auditabilidad** | Toda transacción debe ser rastreable desde origen hasta RN. |
| 6 | **Multi-marketplace** | Framework único para cualquier canal. |
| 7 | **Sin lógica financiera duplicada** | Cada regla existe exactamente una vez. |
| 8 | **Separation of Concerns** | Capas con responsabilidades únicas: Loader → Ledger → Classification → Event Model → Closing → API |

## Pipeline Universal

```
LOADER
  Responsabilidad: Ingesta de source file, generación de id_transaccion
  Restricción: Sin lógica de clasificación ni financiera
  Output: marketplace_ledger_v1

LEDGER
  Responsabilidad: Almacenamiento raw de transacciones
  Restricción: Inmutable después de carga
  Output: marketplace_ledger_v1 (persistido)

CLASSIFICATION
  Responsabilidad: Asignar clasificacion_operativa, financial_group, op_pnl
  Restricción: Sin lógica de agregación ni cierre
  Output: marketplace_ledger_clasificado_v1

EVENT MODEL (nueva capa)
  Responsabilidad: Asignar event_role (ROOT_EVENT vs MECHANISM)
  Restricción: Sin lógica de agregación
  Output: marketplace_ledger_clasificado_v1 (event_role poblado)

CLOSING
  Responsabilidad: Agregar por período, calcular RN
  Restricción: Sin lógica de clasificación ni event model
  Output: marketplace_cierre_financiero_v1

API
  Responsabilidad: Exponer datos certificados
  Restricción: Sin lógica financiera (PROHIBIDO FINANCIAL_STRUCTURE)
  Output: JSON responses
```

## Domain Separation

```
DOMAIN_OPERATIONAL    → Venta, Orden, Paquete, Devolución
DOMAIN_FISCAL         → Factura, Nota Crédito, DTE
DOMAIN_CASH           → Liberación, Cobro, Retiro, Settlement

PROHIBIDO mezclar dominios en una misma conciliación.
```

## Golden Source Hierarchy

```
NIVEL A (Fuente Maestra Transaccional)
  → La fuente más cercana al evento económico
  → Debe tener: ID único, fecha, monto, concepto

NIVEL B (Conciliación de Pagos)
  → Detalle de pagos, liquidaciones
  → NO reemplaza al Nivel A

NIVEL C (Caja)
  → Liberaciones, bank statements, settlement reports
  → NO es fuente transaccional

NIVEL D (Logística / Operaciones)
  → Datos operacionales complementarios
  → NO es fuente financiera
```

## Rule Location Pattern

Toda nueva regla financiera debe evaluarse contra:

```
¿Dónde debe vivir?

  Opción 1: LOADER
    → Solo si es transformación pura de source a ledger (signo, formato)
    → NO si requiere clasificación o contexto entre filas

  Opción 2: CLASSIFICATION
    → Solo si es row-level (qué es esta fila)
    → NO si requiere groupby (cross-row)

  Opción 3: EVENT MODEL
    → Si requiere groupby por id_orden
    → Si requiere detectar relaciones entre filas

  Opción 4: CLOSING
    → Solo si es agregación matemática pura
    → NO si requiere lógica de negocio

  Opción 5: API
    → NUNCA. Frontend es consumidor pasivo.
```

## Certification Requirements

```
Para certificar un marketplace en el Governance Framework:

  REQUIRED:
  ✓ Loader spec definido y probado
  ✓ Classification map completo (100% conceptos)
  ✓ Financial_group asignado por concepto
  ✓ Event_role asignado por concepto
  ✓ Cash reality cross-check (si cash source disponible)
  ✓ Closing produce RN correcto
  ✓ API expone datos sin lógica financiera
  ✓ 14/14 regression tests PASS

  RECOMMENDED:
  ✓ XML traceability (folio_xml poblado)
  ✓ Cash reality delta < 5%
  ✓ Event model certification (si hay MECHANISMS)
  ✓ Knowledge files creados
  ✓ Knowledge registry actualizado
```

## Certificaciones Core

| Documento | Relación |
|-----------|----------|
| `governance/SPRINT_A1_COMPLETION_REPORT.md` | Foundation of Trust |
| `governance/KPI_DEFINITIONS_V1.md` | KPI definitions |
| `governance/FINANCIAL_EVIDENCE_CHAIN_DESIGN.md` | F1-F7 framework |
| `governance/RFC_FINANCIAL_TRUTH_CONSOLIDATION.md` | Truth consolidation |
| `governance/DECISIONS_LOG.md` | Decision log (DEC-001) |
| `governance/C_HANGE_TEMPLATE.txt` | Change template |
| `governance/INCIDENT_PROTOCOL.txt` | Incident protocol |
| `governance/FREEZE_ACTIVO.txt` | V6 freeze rules |
| `governance/DB_PROTECTION_AUDIT.txt` | DB protection |
