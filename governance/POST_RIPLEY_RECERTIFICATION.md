# SPRINT B2.4 — POST-RIPLEY RECERTIFICATION

**Fecha**: 2026-06-01
**Régimen**: READ ONLY — CERTIFICACIÓN GLOBAL POST RFC-001
**DB Oficial**: `data/db/meli_financial_v4.db` (DuckDB V1.5.1)
**Pre-fix snapshot**: `data/db/snapshot_pre_ripley_rebuild_20260601_172043/`
**Tags**: `PRE_RIPLEY_DATEFIX` → `POST_RIPLEY_DATEFIX`
**RFC-001**: RIPLEY Temporal Reconstruction — `dayfirst=True` en `surgical_loader.py:382,400`

---

## CAMBIOS INCORPORADOS

| Cambio | Detalle |
|---|---|
| **RFC-001 dayfirst=True** | 2 líneas modificadas en `surgical_loader.py` (382, 400) |
| **DELETE + INSERT Ripley** | 46 XLSX recargados con fecha corregida |
| **Snapshot pre-fix** | `snapshot_pre_ripley_rebuild_20260601_172043/` (131 MB, SHA256 `88082bbc`) |
| **Tags git** | `PRE_RIPLEY_DATEFIX` + `POST_RIPLEY_DATEFIX` |
| **14/14 regression tests** | PASS (sin cambios en ML/PARIS/FALABELLA) |

---

## 1. TRUST SCORE GLOBAL (V2 — 5-Component Model)

### 1.1 Trust Score por Marketplace

#### ML — 94/100 (SIN CAMBIOS)

| Componente | Peso | Score | Evidencia |
|---|---|---|---|
| Documental | 25% | 25/25 | 20/20 source files verificados |
| Operacional | 25% | 25/25 | 101,603 rows, 31,281 órdenes trazables |
| Financiero | 20% | 17/20 | 86.9% CERTIFICADO vía XML |
| XML Traceability | 15% | 13/15 | 89.4% con folio_xml, 17 folios únicos |
| Actualidad | 15% | 14/15 | Data hasta 2026-12-04 |
| **Total** | **100%** | **94/100** | |

#### RIPLEY — 87/100 (ANTES: 72/100 — MEJORA DE +15 PTS)

| Componente | Peso | Score Antes | Score Después | Cambio | Evidencia |
|---|---|---|---|---|---|
| Documental | 25% | 25/25 | 25/25 | = | 46/46 XLSX files verificados en disco |
| Operacional | 25% | 25/25 | 25/25 | = | 62,502 rows trazables a 46 archivos |
| Financiero | 20% | 12/20 | **18/20** | **+6** | Importe $353.2M = 100% match XLSX. 0 NaT. $0 residual. |
| XML Traceability | 15% | 0/15 | **8/15** | **+8** | 100% folio_xml (46 folios) desde XLSX Folio column. 0% certificado. |
| Actualidad | 15% | 10/15 | **14/15** | **+4** | 46/46 archivos cargados. Data hasta 2026-05. 584269 AUSENTE. |
| **Total** | **100%** | **72/100** | **87/100** | **+15** | |

**Mejora vs V2**: +15 pts. Driver principal: corrección date parsing.
**Riesgo residual**: 0% XML certificado. $413.9M sin clasificar. 584269 AUSENTE.

#### FALABELLA — 71/100 (SIN CAMBIOS)

| Componente | Peso | Score | Evidencia |
|---|---|---|---|
| Documental | 25% | 25/25 | 2/2 source files verificados |
| Operacional | 25% | 25/25 | 125 transacciones, 1,008 rows trazables |
| Financiero | 20% | 8/20 | 0% CERTIFICADO |
| XML Traceability | 15% | 6/15 | 61.5% folio_xml. 0% certificado. |
| Actualidad | 15% | 7/15 | Data hasta 2026-04-30 |
| **Total** | **100%** | **71/100** | |

#### PARIS — 70/100 (SIN CAMBIOS)

| Componente | Peso | Score | Evidencia |
|---|---|---|---|
| Documental | 25% | 25/25 | 18/18 source files |
| Operacional | 25% | 25/25 | 42,487 rows trazables |
| Financiero | 20% | 10/20 | ~51% coverage post-XML recert |
| XML Traceability | 15% | 5/15 | 79% folio_xml pero 0 matched con XMLs actuales |
| Actualidad | 15% | 5/15 | XMLs reemplazados (154→54) |
| **Total** | **100%** | **70/100** | |

### 1.2 Trust Score Global Ponderado

| Marketplace | % Ledger | Score | Contribución |
|---|---|---|---|
| ML | 51.5% ($842.3M) | 94 | 48.4 |
| RIPLEY | 25.3% ($413.9M) | 87 | 22.0 |
| PARIS | 23.1% ($378.1M) | 70 | 16.2 |
| FALABELLA | 0.2% ($2.6M) | 71 | 0.1 |
| **Global (ponderado)** | | | **86.7/100** |
| **Global (promedio simple)** | | | **80.5/100** |

**Cambio**: 83.8 → 86.7/100 (+2.9 pts). RIPLEY contribution mejora de 13.6→22.0.

---

## 2. MARKETPLACE RISK RANKING

| Ranking | Marketplace | Trust Score | Monto | Riesgo Antes | Riesgo Después |
|---|---|---|---|---|---|
| **1** | **ML** | **94/100** | $842.3M (51.5%) | Bajo | **Bajo** |
| **2** | **RIPLEY** | **87/100** | $413.9M (25.3%) | Medio | **Medio-Bajo** |
| **3** | **FALABELLA** | **71/100** | $2.6M (0.2%) | Medio-Alto | **Medio-Alto** |
| **4** | **PARIS** | **70/100** | $378.1M (23.1%) | Medio | **Medio** |

**RIPLEY ya NO es el mayor riesgo.** Con 87/100 supera a PARIS (70) y FALABELLA (71). El riesgo principal del sistema sigue siendo la **XML traceability general** (PARIS + RIPLEY sin certificación).

**PARIS se convierte en el marketplace más riesgoso** por la combinación de:
- Trust Score más bajo (70/100)
- Monto alto ($378.1M = 23.1%)
- 0% XML certificado post-recertificación
- Folios en DB referencian XMLs eliminados

---

## 3. EVIDENCE CHAIN RECALCULATION

### 3.1 Confidence Levels por Marketplace

| Marketplace | Source | XML | Class | Aggregation | **Overall** | Cambio |
|---|---|---|---|---|---|---|
| **ML** | 1.0 | 0.90 | 0.95 | 1.0 | **0.96** | = |
| **RIPLEY** | 1.0 | 0.25 | 0.0 | 1.0 | **0.48** | **-0.23** |
| **PARIS** | 1.0 | 0.75 | 0.90 | 1.0 | **0.91** | = |
| **FALABELLA** | 1.0 | 0.50 | 0.80 | 1.0 | **0.83** | = |

**RIPLEY XML Confidence**: 0.0 → 0.25 (mejora: folio_xml ahora 100%, pero sin DTEIndexer ni certificación)
**RIPLEY Class Confidence**: 0.85 → 0.0 (empeora: antes $142M clasificado, ahora $0 — DELETE del rebuild eliminó datos de clasificación)
**RIPLEY Overall**: 0.71 → 0.48 (disminuye por pérdida de clasificación)

**Nota crítica**: La clasificación de RIPLEY se perdió en el rebuild (DELETE de ledger rows también eliminó referencias). Esto es un efecto colateral de RFC-001 no anticipado.

### 3.2 Explainability Contract (6 Preguntas)

**PREGUNTA**: ¿Puede cada KPI responder las 6 preguntas (Qué, Cuánto, De dónde, Por qué, Dónde impacta, Qué evidencia)?

| Marketplace | 6-Question Score | Estado |
|---|---|---|
| ML | 6/6 | COMPLETO |
| RIPLEY | 4/6 | PARCIAL — Sin clasificación (Por qué, Dónde impacta) |
| PARIS | 5/6 | PARCIAL — XML no matchea |
| FALABELLA | 5/6 | PARCIAL — Sin certificación |

---

## 4. KPI VALIDATION

### 4.1 KPIs que CAMBIARON (RIPLEY)

| KPI | Antes | Después | Delta | Driver |
|---|---|---|---|---|
| **RIPLEY Importe Total (Ledger)** | $284,897,360 | $413,893,686 | +$128,996,326 | Date fix + full 46 file load |
| **RIPLEY Importe del pedido** | $240,979,600 | $353,160,324 | +$112,180,724 | Date fix: NaT rows now parsed |
| **RIPLEY Apr 2026 Importe** | $1,500,432 | $16,460,180 | +$14,959,748 | Date fix: swapped dates corrected |
| **RIPLEY A pagar** | $142,448,680 | $206,946,843 | +$64,498,163 | Proportional increase |
| **RIPLEY Ledger rows** | 269,216 | 62,502 | -206,714 | Now only non-zero concepts |
| **RIPLEY Ventas marketplace rows** | 10,647 | 10,578 | -69 | Dedup effect |
| **RIPLEY Importe del pedido rows** | 8,413 | 10,555 | +2,142 | NaT rows now included |
| **RIPLEY Financial concepts** | 32 | 13 | -19 | No more zero-value concepts |
| **RIPLEY Folio XML rows** | 0 (0%) | 62,502 (100%) | +62,502 | From XLSX Folio column |
| **RIPLEY Clasificado rows** | 40 | 0 | -40 | Classification lost in rebuild |
| **RIPLEY 6 archivos sin cargar** | 6 files ($18.6M) | 0 files ($0) | -6 files | All 46 XLSX loaded |
| **Global ledger total** | $1,507,835,610 | $1,636,831,936 | +$128,996,326 | Ripley increase |

### 4.2 KPIs que NO CAMBIARON

| KPI | Antes | Después | Delta |
|---|---|---|---|
| **ML total** | $842,250,301 | $842,250,301 | $0 |
| **ML rows** | 101,603 | 101,603 | 0 |
| **PARIS total** | $378,104,933 | $378,104,933 | $0 |
| **PARIS rows** | 42,487 | 42,487 | 0 |
| **FALABELLA total** | $2,583,016 | $2,583,016 | $0 |
| **FALABELLA rows** | 1,008 | 1,008 | 0 |
| **ML folio_xml %** | 89.4% | 89.4% | 0% |
| **PARIS folio_xml %** | 79.0% | 79.0% | 0% |
| **FALABELLA folio_xml %** | 61.5% | 61.5% | 0% |
| **14/14 regression tests** | PASS | PASS | 0 |

### 4.3 SQL = API = UI Contract

Los 14 tests de regresión (SQL/API contract) pasan 14/14:
- `test_api_rejects_invalid_param_subgroup` — PASS
- `test_desglose_endpoint_no_heuristics` — PASS
- `test_insert_update_delete_blocked` — PASS
- `test_ledger_endpoint_no_heuristics` — PASS
- `test_falabella_cofinanciamiento` — PASS
- `test_falabella_comision` — PASS
- `test_ml_ajuste_arrepentimiento` — PASS
- `test_ml_cargo_venta` — PASS
- `test_paris_devolucion` — PASS
- `test_paris_venta` — PASS
- `test_ripley_importe_pedido` — PASS (con nuevo valor $353.2M)
- `test_ripley_pedidos_reembolsados` — PASS (con nuevo valor $-82.9M)
- `test_api_file_no_contains_startswith` — PASS
- `test_dashboard_no_catmap` — PASS

---

## 5. DASHBOARD CONSISTENCY

La certificación B2.2 (Dashboard vs Database) comparó 5 KPIs con delta $0. Post-RFC-001:

Los KPIs de **ML, PARIS, FALABELLA** mantienen delta $0 (sin cambios en DB).

Los KPIs de **RIPLEY** cambian en DB (ver sección 4.1). La UI/Dashboard reflejará automáticamente los nuevos valores porque la API consulta la DB oficial en tiempo real. **No requiere cambios de código.**

**Recomendación**: Re-ejecutar B2.2 Dashboard Certification con los nuevos valores RIPLEY para confirmar delta $0 en UI.

---

## 6. COVERAGE CERTIFICATION

### 6.1 Financial Coverage por Marketplace

| Marketplace | Source files | Files en DB | Coverage | Status |
|---|---|---|---|---|
| **ML** | 20 CSV | 20 | 100% | COMPLETO |
| **RIPLEY** | 46 XLSX | 46 | **100%** | **MEJORADO** (antes: 40/46 = 87%) |
| **PARIS** | 18 XLSX | 18 | 100% | COMPLETO |
| **FALABELLA** | 2 XLSX | 2 | 100% | COMPLETO |

### 6.2 RIPLEY Coverage Detail

| Dimensión | Antes | Después |
|---|---|---|
| XLSX files on disk | 46 | 46 |
| XLSX loaded in DB | 40 (87%) | **46 (100%)** |
| Source rows in XLSX | 10,755 | 10,755 |
| Ventas rows loaded | 10,647 | 10,578 |
| Ledger Importe del pedido | $240,979,600 | **$353,160,324** |
| A pagar coverage | 86.7% | **100%** (0 NaT, 0 gap) |
| 584269 AUSENTE | Still missing | **Still missing** |

### 6.3 XML Coverage Post-RFC-001

| Marketplace | folio_xml % | CERTIFICADO % | estado_xml | Cambio |
|---|---|---|---|---|
| ML | 89.4% | 86.9% | CERTIFICADO | = |
| RIPLEY | **100%** | 0% | None | **+100pp folio** |
| PARIS | 79.0% | 0% | PENDIENTE | = |
| FALABELLA | 61.5% | 0% | None | = |

**RIPLEY folio_xml ahora 100%** pero 0% certificado. Los 46 folios provienen de la columna "Folio" en XLSX — son referencias a DTEs no verificados por DTEIndexer.

---

## 7. CONCLUSIONES ANTERIORES INVALIDADAS

Las siguientes conclusiones de `TRUST_CERTIFICATION_V2.md` quedan **INVALIDADAS** por RFC-001:

| # | Conclusión Anterior | Invalidad Por | Nueva Realidad |
|---|---|---|---|
| 1 | RIPLEY Trust Score = 72/100 | Date fix +15 pts | **87/100** |
| 2 | RIPLEY: 0% folio_xml | XLSX Folio column ahora cargada | **100% folio_xml** |
| 3 | RIPLEY: 6 archivos sin cargar ($18.6M) | Rebuild cargó todos los 46 XLSX | **0 archivos sin cargar** |
| 4 | RIPLEY: 269,216 rows en ledger | Solo non-zero concepts post-fix | **62,502 rows** |
| 5 | RIPLEY Importe: $240.9M | Date correction | **$353.2M** |
| 6 | RIPLEY Ledger total: $284.9M | Full 46 files loaded | **$413.9M** |
| 7 | RIPLEY: $142M sin clasificar | Total increased | **$413.9M sin clasificar** |
| 8 | Global ledger: $1,507.8M | RIPLEY increase | **$1,636.8M** |
| 9 | RIPLEY: 18.9% of global ledger | Ripley value increase | **25.3%** |
| 10 | RIPLEY ranking #2 a 72/100 | Now 87/100, still #2 | **87/100, risk reduced** |
| 11 | RIPLEY gap $21.8M en filas sin liquidación | No más NaT | **$0 gap** |
| 12 | Trust Score Global: 83.8/100 | RIPLEY improvement | **86.7/100** |

### Conclusiones que SIGUEN VÁLIDAS

| # | Conclusión | Status |
|---|---|---|
| 1 | RIPLEY: 0% XML certificado | VÁLIDA (estado_xml = None for all) |
| 2 | RIPLEY: Sin DTEIndexer | VÁLIDA (no ejecutado) |
| 3 | RIPLEY: $50.5M facturas no cargadas (INVALIDADO PARCIALMENTE) | VÁLIDA: 584269 AUSENTE |
| 4 | ML: 94/100 — Líder absoluto | VÁLIDA |
| 5 | PARIS: 79% folio pero 0% certificado | VÁLIDA |
| 6 | FALABELLA: 61.5% folio, 0% certificado | VÁLIDA |
| 7 | PARIS XML set reemplazado (154→54) | VÁLIDA |
| 8 | $0 permanent financial loss from date bug | VÁLIDA (confirmado) |
| 9 | 14/14 regression contract | VÁLIDA (confirmado) |

---

## 8. NUEVA HOJA DE RUTA

### Prioridad 1 — CRÍTICO: RIPLEY Classification Recovery

| Item | Impacto | Effort | Ratio |
|---|---|---|---|
| **Recuperar clasificación RIPLEY** | Trust: +5 pts. Audit: +10 pts. | Medio | **ALTA** |
| **Re-ejecutar clasificador en RIPLEY** | 62,502 rows financieras sin clasificar | Bajo (read from XLSX → classify) | **ALTA** |

La clasificación se perdió en el RFC-001 rebuild. Necesita re-ejecución del proceso de clasificación. $413.9M sin financial_group.

### Prioridad 2 — ALTA: XML Certification (RIPLEY + PARIS)

| Item | Impacto | Effort | Ratio |
|---|---|---|---|
| **DTEIndexer para RIPLEY** | XML Trust: +5 pts | Alto (46 folios → buscar XMLs) | **MEDIA** |
| **PARIS XML recert bridge** | PARIS Trust: +15 pts | Alto (54 XMLs → re-match) | **MEDIA** |

### Prioridad 3 — MEDIA: FALABELLA Certification

| Item | Impacto | Effort | Ratio |
|---|---|---|---|
| **XML certification FALABELLA** | Trust: +10 pts | Bajo (solo 5 folios, 620 rows) | **MEDIA** |

### Prioridad 4 — MEDIA: Governance Hardening

| Item | Impacto | Effort |
|---|---|---|
| **Config/database.yaml** | Audit readiness: +5 pts | Bajo |
| **Pipeline log estandarizado** | Observabilidad | Bajo |
| **Trust Score V3 implementation** | Metodología mejorada | Medio |

### Roadmap Timeline

```
Sprint           Focus                    Trust Impact
──────────────────────────────────────────────────────────
SPRINT B2.5      RIPLEY Classification    +5 pts (87→92)
SPRINT A4        PARIS residual XML       +3 pts (70→73)
SPRINT A5        DTEIndexer RIPLEY        +5 pts (92→97)
SPRINT A6        FALABELLA cert           +2 pts (71→73)
SPRINT C1        Governance               +3 pts global
──────────────────────────────────────────────────────────
PROYECCIÓN       Trust Score Global       ~92-95/100
```

---

## 9. RESPUESTAS

### ¿Cuál es el nuevo Trust Score?
**86.7/100 ponderado** (antes: 83.8/100). RIPLEY subió de 72→87/100 (+15 pts).

### ¿Cuál es el marketplace más riesgoso?
**PARIS** (70/100, $378.1M) — destronó a RIPLEY. Combinación de Trust Score más bajo y monto alto lo convierte en el riesgo sistémico #1.

### ¿Qué KPIs cambiaron?
12 KPIs de RIPLEY cambiaron (ver tabla 4.1). Los más relevantes:
- Importe del pedido: $241M → $353M (+46.6%)
- Apr 2026: $1.5M → $16.5M (×11)
- Ledger rows: 269K → 62.5K (-77%)
- Folio XML: 0% → 100%
- Archivos sin cargar: 6 → 0

### ¿Qué cobertura cambió?
- **RIPLEY XLSX coverage**: 87% (40/46) → **100%** (46/46)
- **RIPLEY folio_xml**: 0% → **100%** (46 folios from XLSX)
- **RIPLEY clasificación**: 0.06% → **0%** (lost in rebuild)
- **RIPLEY gap rows sin liquidación**: $21.8M → **$0**

### ¿Qué conclusiones anteriores quedan invalidadas?
12 conclusiones de TRUST_CERTIFICATION_V2.md (ver sección 7). Las principales:
- RIPLEY Trust Score 72→87 ya no es válido
- RIPLEY 0% folio_xml ya no es cierto (ahora 100%)
- RIPLEY 6 archivos sin cargar ya no existe
- Global ledger $1,507.8M ahora es $1,636.8M

### ¿Cuál es la nueva hoja de ruta?
1. **CRÍTICO**: Recuperar clasificación RIPLEY ($413.9M perdidos en rebuild)
2. **ALTA**: DTEIndexer RIPLEY + PARIS XML recert
3. **MEDIA**: FALABELLA cert + Governance hardening
4. **PROYECCIÓN**: Trust Score Global → ~92-95/100

---

*Sprint B2.4 completado. Read-only. Sin modificaciones al sistema.*
*Próximo: Sprint B2.5 — RIPLEY Classification Recovery.*
