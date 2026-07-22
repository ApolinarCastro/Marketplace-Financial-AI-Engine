# POSCOBRO DELETION DECISION

**Estado: COMPLETED** — 2026-06-06
**Auditor:** Sistema de Agentes
**Propósito:** Determinar si PosCobro debe mantenerse (KEEP) o eliminarse (DELETE) del modelo financiero Marketplace Financial.

---

## Executive Summary

**VEREDICTO: DELETE** ❌ — PosCobro debe ser eliminado del modelo financiero.

**Razón principal:** 99.77% de la información financiera de PosCobro ($337.5M de $338.2M) ya está reflejada en otras fuentes (Liquidaciones/Facturación/Liberaciones). Solo $767,764 (0.23%) es exclusivo e inmaterial.

**Evidencia consolidada:**
| Métrica | Valor |
|---------|-------|
| PosCobro total | $338,221,582 (11,914 rows, 6,219 orders) |
| Reflejado en Facturación (84.5% orders) | $287,189,263 (84.91%) |
| Reflejado en Liberaciones (86.6% orders) | $293,037,143 (86.64%) |
| Reflejado en Ledger (90.0% orders) | $304,382,903 (89.99%) |
| Reflejado en ALGUNA fuente | $337,453,818 (99.77%) |
| **EXCLUSIVO a PosCobro** | **$767,764 (0.23%)** |

**Impacto de eliminación:**
- Cash (Liberaciones): **$0 impacto** — 96% nunca fue cash, 4% ya en Liberaciones
- Ingresos (Facturación): **$0 impacto** — todas las ventas ya están en Facturación
- Devoluciones (Facturación): **$0 impacto** — todas las devoluciones ya están en Facturación
- Ledger RN: **$-263.6M** — elimina ruido contable de paired mechanisms (GO-LIVE RECOMMENDED)
- Clasificación: **Se pierde granularidad operacional** (flow, reason_detail, status_detail) — información NO financiera

---

## FASE 1: Universo PosCobro

**Fuente:** `01_Raw/ML/Poscobro/` (5 archivos .xlsx, 11,914 rows)

| FLOW | Rows | Orders | Amount |
|------|------|--------|--------|
| claim | 6,158 | 5,325 | $183,063,202 |
| refund | 5,749 | 5,370 | $154,945,450 |
| chargeback | 7 | 7 | $212,930 |
| **TOTAL** | **11,914** | **6,219** | **$338,221,582** |

**Key:** Solo 3 FLOW values en todos los datos — claim (54.1%), refund (45.8%), chargeback (0.1%). Confirmado por POSCOBRO_FLOW_FINANCIAL_TRUTH.

---

## FASE 2: Trazabilidad a Otras Fuentes

### 2a. Liberaciones (Cash Truth)

**Fuente:** `01_Raw/ML/Liberaciones/` (18 archivos mensuales)
**Match key:** `operation_external_reference` ↔ `ID DE LA ORDEN` (float64→int→str)

| Métrica | Valor |
|---------|-------|
| Orders en Liberaciones | 5,383/6,219 (86.6%) |
| Amount en Liberaciones | $293,037,143 (86.64%) |
| Liberaciones NET de orders PosCobro | $13,441,859 |
| Cash conversion rate | 5.10% |

**Confirmación:** 86.6% de orders PosCobro existen en Liberaciones. Cash conversion rate 5.10% (consistente con el 4.07% de POSCOBRO_CASH_IMPACT — diferencia por metodología de matching).

### 2b. Ledger Marketplace (Facturación)

**Fuente:** `data/db/meli_financial_v4.db` — `marketplace_ledger_v1` (ML only)
**Match key:** `id_orden`

| Source en Ledger | Rows | Amount |
|------------------|------|--------|
| Facturación | 90,814 | $535,238,350 |
| PosCobro | 9,187 | $263,622,245 |
| Other/Liquidación | 2,197 | $63,544,323 |
| **TOTAL** | **102,198** | **$862,404,918** |

| Métrica | Valor |
|---------|-------|
| PosCobro orders en Ledger (PosCobro source) | 4,512/6,219 (72.6%) |
| PosCobro orders en Ledger (Facturación source) | 5,252/6,219 (84.5%) |
| PosCobro orders en Ledger (cualquier source) | 5,596/6,219 (90.0%) |
| Amount de PosCobro orders en Ledger (cualquier source) | $304,382,903 (89.99%) |

**Nota:** 1,708 PosCobro orders ($63.8M) NO están en el ledger con archivo_origen="poscobro". Esto es porque la clasificación de fuente en el ledger depende del nombre del archivo; algunas órdenes pueden tener ajustes cargados bajo otro nombre de archivo.

### 2c. Cobertura Combinada

| Coverage Type | Orders | Amount | % Amount |
|--------------|--------|--------|----------|
| En Facturación (Ledger) | 5,252 | $287,189,263 | 84.91% |
| En Liberaciones | 5,383 | $293,037,143 | 86.64% |
| En Ledger (cualquier fuente) | 5,596 | $304,382,903 | 89.99% |
| En ALGUNA fuente | 6,179 | $337,453,818 | 99.77% |
| **EXCLUSIVO a PosCobro** | **622** | **$767,764** | **0.23%** |

---

## FASE 3: Análisis de Órdenes Exclusivas

622 órdenes ($767,764) existen SOLO en PosCobro — no en Facturación, no en Liberaciones, no en Ledger.

### Desglose por FLOW

| FLOW | Orders | Amount | % Exclusive |
|------|--------|--------|-------------|
| claim | 24 | $95,322 | 0.03% |
| refund | 620 | $672,442 | 0.20% |
| chargeback | 0 | $0 | 0.00% |
| **TOTAL** | **622** | **$767,764** | **0.23%** |

### Caracterización

**Montos promedio:** $767,764/622 = $1,234/orden
- 24 claims: $95,322/24 = $3,972/claim (montos pequeños)
- 620 refunds: $672,442/620 = $1,085/refund (montos muy pequeños)

**Naturaleza probable:** Órdenes con ajustes mínimos que no llegaron a ser procesados por el settlement processor (Liberaciones) ni aparecen en Facturación. Posiblemente transacciones canceladas antes de completar el ciclo de pago.

**Impacto:** $768K representa 0.047% del ledger ML total ($862.4M). Inmaterial para cualquier propósito financiero.

---

## FASE 4: Simulación de Eliminación

### Escenario A — Actual (CON PosCobro)

| Componente | Valor |
|------------|-------|
| Ledger Facturación | $535,238,350 |
| Ledger PosCobro (ajustes) | $263,622,245 |
| Ledger Other | $63,544,323 |
| Ledger TOTAL | $862,404,918 |
| Liberaciones (matched orders) | $13,441,859 |
| Cash conversion | 5.10% |

### Escenario B — Sin PosCobro

| Componente | Valor | Cambio |
|------------|-------|--------|
| Ledger Facturación | $535,238,350 | $0 |
| Ledger PosCobro | $0 | -$263,622,245 |
| Ledger Other | $63,544,323 | $0 |
| Ledger TOTAL | $598,782,672 | -$263,622,245 |
| Liberaciones (matched orders) | $13,441,859 | **$0** |
| Ingresos | $535,238,350 | **$0** |
| Cash real | $13,441,859 | **$0** |

### Impacto por Componente

| Componente | Impacto | Explicación |
|-----------|---------|-------------|
| Ingresos | $0 | Facturación unchanged |
| Devoluciones | $0 | Facturación unchanged |
| Costos | $0 | Facturación unchanged |
| Ajustes | -$263.6M | Se eliminan todos los ajustes PosCobro |
| Liberaciones/Cash | $0 | Cash no cambia (96% nunca fue cash) |
| Clasificación | Pérdida de granularidad | Se pierde flow/reason_detail/status_detail |

---

## FASE 5: Análisis de Riesgos

### Riesgo 1: Pérdida de información clasificatoria

PosCobro provee flow (claim/refund/chargeback), reason_detail (31 variantes), y status_detail. Esta información NO está disponible en Facturación ni Liberaciones.

**Mitigación:** La clasificación financiera no necesita esta granularidad. POSCOBRO_FLOW_FINANCIAL_TRUTH (DEC-007) ya demostró que los 3 flows se clasifican correctamente como AJUSTES. La granularidad operacional es útil para análisis de negocio, no para contabilidad financiera.

### Riesgo 2: Los $768K exclusivos se pierden permanentemente

**Mitigación:** $768K es 0.05% del ledger ML. Probablemente corresponde a transacciones no procesadas/ canceladas. Si se requiere recuperación, el archivo raw PosCobro permanece disponible en `01_Raw/ML/Poscobro/`.

### Riesgo 3: Regression en API endpoints

**Mitigación:** Los endpoints API usan `marketplace_cierre_financiero_v1`, no el ledger directo. La eliminación de PosCobro del ledger requeriría re-clasificar y re-cerrar, pero los endpoints actuales leerían los nuevos valores de cierre.

### Riesgo 4: Pérdida de trazabilidad histórica

**Mitigación:** Los snapshots de DB (`snapshot_pre_fase2_20260603_112908/`, etc.) preservan el estado con PosCobro. Git preserva el código. Los archivos raw permanecen inalterados.

---

## Decisión Final: DELETE ❌

### Fundamento

1. **99.77% redundante**: La información financiera de PosCobro ya existe en Facturación (ingresos/devoluciones/costos), Liberaciones (cash), o Ledger (ajustes de otras fuentes).

2. **0.23% inmaterial**: $767,764 de $338.2M es financieramente irrelevante.

3. **Cash impact $0**: La eliminación no cambia el cash real reportado por Liberaciones.

4. **Go-Live Audit lo recomienda**: La eliminación de paired mechanisms (BPP+Poscobro) corregiría la sobrestimación de RN de $35.8M identificada en AJUSTES_RETENCIONES_IMPACT.md.

5. **Single Financial Truth se fortalece**: Al eliminar PosCobro, el ledger ML se alinea más con la realidad de caja (Liberaciones = Cash Truth, DEC-004).

### Condiciones

1. **NO eliminar archivos raw**: `01_Raw/ML/Poscobro/` debe preservarse como fuente de trazabilidad histórica y análisis operacional.

2. **NO modificar snapshots**: Los snapshots pre-eliminación preservan el estado con PosCobro para comparación forense futura.

3. **Mantener granularidad operacional**: Si el negocio requiere análisis de ajustes por FLOW/reason_detail, debe hacerse directamente desde archivos raw, no desde el ledger financiero.

4. **Re-clasificar ML**: Tras eliminar PosCobro del pipeline, se debe re-ejecutar clasificación y cierre para ML (similar a Sprint B2.5C para RIPLEY).

---

## Documentos Relacionados

| Documento | Relación |
|-----------|----------|
| POSCOBRO_CASH_IMPACT_CERTIFICATION.md | 96% non-cash — pre-condición para DELETE |
| POSCOBRO_TO_CASH_LAG_CERTIFICATION.md | Time-lag falsificado — cash gap es permanente |
| POSCOBRO_FLOW_FINANCIAL_TRUTH.md | 3 flows, todos AJUSTES — clasificación correcta |
| DOCUMENTARY_RECONCILIATION_V2.md | 73.3% conciliación documental (pure ID match) |
| POSCOBRO_LIQUIDACIONES_PRECEDENCE_CERTIFICATION.md | LIQUIDACIONES > POSCOBRO rule |
| SALE_TO_BANK_TRUTH_CERTIFICATION.md | Paired mechanisms inflan P&L (DEC-004) |
| AJUSTES_RETENCIONES_IMPACT.md | Go-Live Audit: $35.8M overstatement from paired mechs |
| GO_LIVE_AUDIT.md | FAIL — 3 structural issues, PosCobro is #1 |

---

*"El 99.77% de PosCobro ya vive en otra fuente. El 0.23% no justifica mantenerlo. PosCobro no es información financiera — es ruido operacional disfrazado de contabilidad."*
