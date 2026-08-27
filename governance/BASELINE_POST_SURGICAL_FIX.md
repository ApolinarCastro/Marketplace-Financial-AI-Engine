---
id: BASELINE_POST_SURGICAL_FIX
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Lead Financial Engineer & Chief Architect
ultima_revision: 2026-07-27
dependencias: [EXECUTION_PLAN_PHASE_0_FOUNDATION_V3, AGENTS.md]
relacionado_con: [SURGICAL_FIX_REGISTRY, TECHNICAL_DEBT_REGISTRY_V1, PMO_REGISTRY_V1]
---

# LÍNEA BASE Y CONGELAMIENTO POST FIX QUIRÚRGICO

## Resumen de Congelamiento Operativo
Se establece el estado congelado e inmutable de la línea base técnica y financiera del **Marketplace Financial AI Engine**. Queda prohibida la modificación de la base de datos oficial, motor financiero, esquemas de cálculo y endpoints hasta la habilitación formal de las fases subsecuentes.

---

## Parámetros de la Línea Base Oficial

| Parámetro | Valor Certificado | Estado |
| :--- | :--- | :--- |
| **Rama Git Oficial** | `phase5/production-readiness` | CONGELADA |
| **Commit SHA** | `2d51f52` (`F5-05: Add idempotency regression tests for recovery mechanism`) | VERIFICADO |
| **Base de Datos Oficial** | `data/db/meli_financial_v4.db` | CONGELADA (READ-ONLY) |
| **Motor DB** | DuckDB V1.5.1 | OFICIAL |
| **Hash SHA-256 DB** | `311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9` | INMUTABLE |
| **Estado de Pruebas** | 646 PASS, 184 FAIL (Suites Legacy/Golden en TD-001) | REGISTRADO EN DEUDA |
| **Fixes Quirúrgicos Cerrados** | `POST_F5_08_CLP_FORMAT_PARITY_FIX`<br>`POST_F5_08_DTE_COVERAGE_STATUS_RENDER_FIX` | CERRADO Y VERIFICADO |

---

## Artefactos Financieros Certificados Inmutables

1. **Marketplace Ledger V1**: `marketplace_ledger_v1` (69/69 períodos conciliados con $0 delta en Ingresos y Devoluciones).
2. **Cierre Financiero V1**: `marketplace_cierre_financiero_v1` (Resultado Neto oficial: Paris $0 delta, Ripley $0 delta, Falabella $12K delta controlado).
3. **Economic Dictionary V1**: Definiciones de 96 conceptos financieros canónicos mapeados en 4 marketplaces (Mercado Libre, Paris, Ripley, Falabella).
4. **Single Source of Truth**: `Marketplace Financial` como única fuente de verdad financiera corporativa. `Reporte_Gerencial_Marketplaces` catalogado como LEGACY.

---

## Fixes Quirúrgicos Incluidos en esta Línea Base

### Fix 1: `POST_F5_08_CLP_FORMAT_PARITY_FIX`
- **Componente**: `templates/dashboard.html`, `templates/executive_dashboard.html`
- **Descripción**: Normalización de la representación monetaria CLP sin decimales espurios y paridad exacta en tooltips explicativos de KPI cards.
- **Resultado**: Verificado $0 divergencia visual.

### Fix 2: `POST_F5_08_DTE_COVERAGE_STATUS_RENDER_FIX`
- **Componente**: `templates/dashboard.html`, `api/api.py`
- **Descripción**: Corrección en el renderizado del indicador de cobertura DTE/XML garantizando fallback seguro en UI ante folios no mapeados.
- **Resultado**: Verificado 100% de render sin excepciones JS/Python.

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:BASELINE_POST_SURGICAL_FIX` (Tipo: `Linea_Base_Certificada`)
- `Node:DB_MELI_FINANCIAL_V4` (Tipo: `Base_Datos_Oficial`, SHA: `311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9`)
- `Node:COMMIT_2D51F52` (Tipo: `Commit_Git`)

### Execution Graph Nodes
- `ExecNode:VERIFY_DB_HASH` (Process: Computar `sha256(data/db/meli_financial_v4.db)` y comparar contra `311c78e...`)
- `ExecNode:RUN_REGRESSION_BASELINE` (Process: Ejecución de la suite `tests/` registrando 646 PASS)

---

## Relaciones y Trazabilidad
- **CERTIFICA**: Estado inmutable post-Fix Quirúrgico Fase 5.
- **ORIGINA**: [SURGICAL_FIX_REGISTRY](file:///c:/Users/ASUS%20Zenbook/Documents/Marketplace%20Financial%20AI%20Engine/governance/SURGICAL_FIX_REGISTRY.md)
- **BLOQUEA**: Cualquier modificación a `data/db/meli_financial_v4.db` o `engine/` sin RFC formal.

---

## Compatibilidad Obsidian
- Enlace Obsidian: [[BASELINE_POST_SURGICAL_FIX]]
- Mapeo de navegación: `KnowledgeOS/02_Governance/BASELINE_POST_SURGICAL_FIX.md`
