# P40R2 GAP ANALYSIS — ¿Qué eslabones existen? ¿Cuáles faltan? (CORREGIDO)

## Pregunta central

> ¿Qué información falta exactamente para certificar una transacción desde el RAW hasta el dinero recibido?

Este documento responde con evidencia verificable, sin opiniones ni estimaciones.

> **Corrección P40R2B**: El Orchestrator solo usa métodos públicos de FinancialEngine, LedgerEngine, ReconciliationEngine, CertificationEngine. CopilotEngine queda como consumidor (presentación), no como proveedor.

## Contrato público que expone cada gap (P40R2B)

| Gap | Engine propietario | Método público disponible | Accesible desde Orchestrator |
|-----|-------------------|--------------------------|------------------------------|
| G1 CashTrace | FinancialEngine | `query_cierre()` — solo RN, no cash real | ✅ Parcial |
| G2 Liberaciones no en DB | FinancialEngine | `query_ledger(detalle='Retiro de dinero')` — única fila | ✅ |
| G3 Sin fuente cash 3 MPs | FinancialEngine | `query_ledger(financial_group=NULL)` — "A pagar" RIPLEY | ✅ |
| G4 Sin integración bancaria | ReconciliationEngine | `validate_marketplace_consistency().level4` | ✅ |
| G5 RIPLEY folio≠SII | FinancialEngine | `query_ledger()` — folio_xml en ledger | ✅ Parcial (no DTE info) |
| G6 PARIS heuristic fails | FinancialEngine | `query_ledger()` — folio_xml en ledger | ✅ Parcial |
| G7 FALABELLA folio_xml=0% | FinancialEngine | `query_ledger()` — 0% folio_xml | ✅ |
| G8 Sin Referencia tag | ❌ GAP-DTE | FinancialEngine no expone `get_dte_info()` | ❌ |
| G9 SHOPIFY no integrado | FinancialEngine | `query_ledger(marketplace='shopify')` — 0 rows | ✅ |
| G10 Sin settlement_id/pack_id | FinancialEngine | `query_ledger()` — columnas no existen | ✅ |
| G11 Liquidacion_FF no procesado | FinancialEngine | `query_ledger(archivo_origen LIKE '%Liquidacion_FF%')` — 0 rows | ✅ |
| G12 Poscobro no eliminado | FinancialEngine | `query_ledger(financial_group='ajustes')` — datos persisten | ✅ |

**Todos los gaps excepto G8 son detectables mediante contratos públicos existentes.** G8 (DTE info) requiere nuevo método público en FinancialEngine.

---

## 1. ESLABONES EXISTENTES (Por marketplace)

### 1.1 Cadena completa (ML)

```
RAW Facturacion (18 XLSX)
  →  SurgicalLoader.load_facturacion()          # ✅ Existe. 100% coverage. ID: id_orden.
  →  marketplace_ledger_v1 (107,542 rows)       # ✅ Existe. 17 columnas, 89.4% con folio_xml.
  →  run_classification()                       # ✅ Existe. Vectorized. 250+ reglas.
  →  marketplace_ledger_clasificado_v1          # ✅ Existe. 100% clasificado.
  →  run_financial_closing()                    # ✅ Existe. 18 periods.
  →  marketplace_cierre_financiero_v1           # ✅ Existe. $0 delta certificado.

RAW Liberaciones (18 XLSX)
  →  SurgicalLoader.load_liberaciones()         # ✅ Existe. 31,284/31,506 orders matched.
  →  marketplace_ledger_v1                      # ✅ Como "Retiro de dinero" (1,787 rows).

RAW XML (196 Documentos Recepcionados)
  →  DTEIndexer                                 # ✅ Existe. 192 indexados en dte_truth_v1.
  →  dte_truth_v1                               # ✅ Existe. 192 rows (DTE 33/43/56/61).
  →  MeliXMLMatcher                             # ✅ Existe. 97.6% coverage ledger→XML.
  →  estado_xml='CERTIFICADO' en ledger         # ✅ Existe. 88,323 rows.

RAW Poscobro (5 XLSX)
  →  SurgicalLoader.load_poscobro()             # ✅ Existe. 11,914 rows.
  →  marketplace_ledger_v1 (include_in_op_pnl=0) # ✅ DEC-019 aplicado.

RAW Liquidacion_FF (90 XLSX)
  →  NO CARGADO por V4                          # ❌ Solo raw files, no pipeline.
```

### 1.2 RIPLEY (cadena parcial)

```
RAW XLSX (11) + CSV (132)
  →  SurgicalLoader.load_ripley()               # ✅ Existe. Melt + semicolon CSV.
  →  marketplace_ledger_v1 (219,901 rows)       # ✅ Existe. 97.3% folio_xml.
  →  run_classification()                       # ✅ Existe. 12 SIGNAL / 20 NOISE.
  →  marketplace_cierre_financiero_v1           # ✅ Existe. 17 periods, $0 delta.

RAW XML (472 Facturacion + 407 DTEIndexer dir)
  →  DTEIndexer                                 # ✅ 407 indexados.
  →  dte_truth_v1                               # ✅ 407 rows ($186.7M).
  →  MeliXMLMatcher                             # ❌ 0 matches — folios incompatibles.

"A pagar" estructural
  →  marketplace_ledger_v1 (12,262 rows)        # ✅ Espejo del neto P&L.
  →  Liquidación real                           # ❌ No existe fuente de cash.
```

### 1.3 PARIS (cadena parcial)

```
RAW XLSX (22 Transacciones)
  →  SurgicalLoader.load_paris()                # ✅ Existe. Split gross/commission.
  →  marketplace_ledger_v1 (74,062 rows)        # ✅ 81.2% folio_xml.
  →  run_classification()                       # ✅ 14 SIGNAL / 1 NOISE.
  →  marketplace_cierre_financiero_v1           # ✅ $0 delta.

RAW XML (69 Facturacion)
  →  DTEIndexer                                 # ✅ 62 indexados.
  →  dte_truth_v1                               # ✅ 62 rows ($816.6M).
  →  MeliXMLMatcher                             # ❌ 0 matches — heuristic fails.

Cash source                                     # ❌ No existe.
```

### 1.4 FALABELLA (cadena parcial)

```
RAW XLSX (8: 4 Facturacion + 4 Ordenes)
  →  SurgicalLoader.load_falabella()            # ✅ Existe.
  →  marketplace_ledger_v1 (678 rows)           # ⚠️ 0% folio_xml.
  →  run_classification()                       # ✅ 15 SIGNAL / 1 NOISE.
  →  marketplace_cierre_financiero_v1           # ✅ 3/4 $0 delta.

RAW XML (8 Documentos Recepcionados)
  →  DTEIndexer                                 # ✅ 6 indexados.
  →  dte_truth_v1                               # ✅ 6 rows ($2.1M).
  →  MeliXMLMatcher                             # ❌ 0 matches.

Cash source                                     # ❌ No existe.
```

### 1.5 SHOPIFY

```
RAW XML (110 Facturacion)                       # ❌ No procesado.
RAW XLSX (18 Mercado Pago)                      # ❌ No procesado.
RAW CSV (2: Orders + Ventas totales)            # ❌ No procesado.
RAW .dat (3 Transbank)                          # ❌ No procesado. Única fuente bancaria real.
Loader                                          # ❌ No existe.
Ledger                                          # ❌ 0 rows.
```

---

### 1.6 ClosingContribution (estado por marketplace)

La relación ledger → cierre existe para todos los MPs cargados. Cada transacción en `marketplace_ledger_v1` con `periodo` definido participa en el cierre cuyo `periodo_fin` coincide.

| Marketplace | Relación | Estado |
|---|---|---|
| ML | `periodo` JOIN `periodo_fin` + `op_pnl=1` | ✅ 18/18 períodos |
| RIPLEY | `periodo` JOIN `periodo_fin` + SIGNAL taxonomy | ✅ 17/17 períodos $0 delta |
| PARIS | `periodo` JOIN `periodo_fin` | ✅ 18/18 períodos $0 delta |
| FALABELLA | `periodo` JOIN `periodo_fin` | ⚠️ 3/4 $0 delta (1 row $12K no clasificada) |
| SHOPIFY | No aplica (0 rows en ledger) | ❌ |

**No se necesita tabla nueva.** ClosingContribution es una consulta:

```sql
-- ¿Qué transacciones contribuyen al cierre ML 2026-01?
SELECT lv.id_transaccion, lv.marketplace, lv.periodo,
       lv.financial_group, cfv.batch_id AS closing_batch
FROM marketplace_ledger_v1 lv
JOIN marketplace_cierre_financiero_v1 cfv
  ON LOWER(lv.marketplace) = LOWER(cfv.marketplace)
 AND lv.periodo = cfv.periodo_fin
WHERE lv.marketplace = ?
  AND lv.periodo = ?
  AND COALESCE(lv.include_in_operational_pnl, 1) = 1
```

### 1.7 CashTrace (estado por marketplace)

La cadena XML → Settlement → Pago → Banco → Cobro NO existe para ningún marketplace.

| Marketplace | XML → Settlement | Settlement → DB | Settlement → Pago | Pago → Banco | Banco → Cobro |
|---|---|---|---|---|---|
| ML | ⚠️ Liberaciones RAW (99.3%) | ❌ No en DB | ❌ No integrado | ❌ No integrado | ❌ No integrado |
| RIPLEY | ❌ "A pagar" es espejo P&L | ❌ No existe | ❌ No integrado | ❌ No integrado | ❌ No integrado |
| PARIS | ❌ No existe | ❌ No existe | ❌ No integrado | ❌ No integrado | ❌ No integrado |
| FALABELLA | ❌ No existe | ❌ No existe | ❌ No integrado | ❌ No integrado | ❌ No integrado |
| SHOPIFY | ⚠️ Transbank .dat RAW | ❌ No procesado | ❌ No integrado | ⚠️ .dat disponible | ❌ No integrado |

**CashTrace es el verdadero vacío del sistema.** Ningún otro gap bloquea más certificaciones.

---

## 2. ESLABONES FALTANTES (Por toda la cadena)

### 2.1 RAW → Ledger

| Gap | Marketplaces afectados | Evidencia |
|---|---|---|
| **Liquidacion_FF no cargado** | ML | 90 archivos, 15,511 rows, ~$330M sin procesar |
| **SHOPIFY no cargado** | SHOPIFY | 133 archivos, 0 rows en ledger |
| **folio_xml no poblado en FALABELLA** | FALABELLA | Loader tiene código para leer "N° Documento Tributario" pero 0/678 rows lo tienen |
| **Liberaciones no almacenadas en tabla dedicada** | ML | Tabla `liberaciones` en DB: 0 rows |
| **Poscobro no eliminado** | ML | DEC-009 (DELETE) no ejecutado — datos persisten en ledger |

### 2.2 Ledger → XML (certificación legal)

| Gap | Marketplaces | Evidencia |
|---|---|---|
| **RIPLEY folio_xml no son folios SII** | RIPLEY | Ledger: 500K-592K (orden de compra). XML: 1.9M-53M (folios SII). 0/407 matches. |
| **PARIS heurística monto+fecha falla** | PARIS | Ledger=neto, XML=bruto. Sin order_id en XML. 0/62 matches. |
| **FALABELLA sin folio_xml en ledger** | FALABELLA | 0/678 rows. No se puede matchear. |
| **DTEIndexer no procesa SHOPIFY** | SHOPIFY | 110 XMLs en raw no indexados. |
| **XMLMatcher no usa Referencia tag** | PARIS, RIPLEY | DTE 43 contiene `<Referencia>` con order_id del DTE 33 origen — no usado. |

### 2.3 Ledger → Liquidación (cash)

| Gap | Marketplaces | Evidencia |
|---|---|---|
| **Sin fuente de cash para RIPLEY** | RIPLEY | Único proxy es "A pagar" (espejo P&L, no cash real) |
| **Sin fuente de cash para PARIS** | PARIS | No hay liberaciones, no hay settlements |
| **Sin fuente de cash para FALABELLA** | FALABELLA | No hay liberaciones, no hay settlements |
| **Liberaciones ML solo como "Retiro de dinero"** | ML | 1,787 rows (-$2.2M) vs 18 raw files ($69.9M neto) |
| **Tabla liberaciones DB: vacía** | ML | Schema existe, 0 rows poblados |
| **Tabla retiros DB: vacía** | ALL | Schema existe, 0 rows |
| **4.07% cash conversion sin traza granular** | ML | No hay join directo ledger→liberaciones por transacción |

### 2.4 Liquidación → Pago

| Gap | Marketplaces | Evidencia |
|---|---|---|
| **No hay integración con gateway de pago** | ALL | No existe conexión con Mercado Pago, Transbank, etc. |
| **No hay datos de comisiones de pago** | ALL | Las comisiones del procesador no están capturadas |
| **No hay datos de timing de pago** | ALL | No se sabe cuándo se liquida realmente cada transacción |
| **PosCobro en ML es ajuste, no pago** | ML | 96% = ruido contable, no flujo de caja |

### 2.5 Pago → Banco

| Gap | Marketplaces | Evidencia |
|---|---|---|
| **Tabla bank_statement DB: vacía** | ALL | Schema existe desde V4, nunca poblada |
| **Sin API bancaria** | ALL | No hay conexión con ningún banco |
| **Sin extractos bancarios cargados** | ALL | SHOPIFY tiene archivos .dat Transbank sin procesar |
| **Libro banco no implementado** | ALL | No hay reconciliación contra estado de cuenta bancario |

### 2.6 Identificadores transversales

| Gap | Marketplaces | Evidencia |
|---|---|---|
| **No hay settlement_id en ledger** | ALL | No se captura el ID de liquidación del marketplace |
| **No hay payment_id en ledger** | ALL | No se captura el ID de pago del procesador |
| **No hay pack_id en ledger** | ML | Existe en source XLSX pero no se almacena |
| **No hay shipment_id en ledger** | ML | Existe en source XLSX pero no se almacena |
| **id_transaccion es generado por loader** | ALL | Formato inconsistente: `SALE_`, `COMM_`, `POS_`, `RIP_`, etc. |
| **No hay clave natural única por transacción** | ALL | Dependencia de id_transaccion generado |

---

## 3. ¿Qué impide certificar una transacción completa?

### 3.1 Para ML

**Se puede certificar:** hasta el eslabón Ledger → XML (97.6% coverage).

**No se puede certificar:** el cash real de cada transacción.

**Causa raíz:** Aunque Liberaciones existe como source, el pipeline almacena solo "Retiro de dinero" agregado, no el detalle por transacción. No hay join directo `marketplace_ledger_v1.id_orden ↔ liberaciones.order_id` en la DB. La certificación SALE_TO_BANK_TRUTH se hizo manual contra archivos RAW, no contra un engine automatizado.

### 3.2 Para RIPLEY

**Se puede certificar:** hasta Ledger → Cierre ($0 delta).

**No se puede certificar:** nada desde Ledger → XML (0%) ni Ledger → Cash (0%).

**Causas raíz:**
1. Los folios XLSX (orden de compra) y los folios SII (DTE) son sistemas diferentes. No hay overlap posible por folio.
2. No existe Settlement Bridge que agregue por monto+periodo.
3. No existe fuente de cash — "A pagar" es contrapartida contable, no movimiento bancario.

### 3.3 Para PARIS

**Se puede certificar:** hasta Ledger → Cierre ($0 delta).

**No se puede certificar:** Ledger → XML (0%) ni Ledger → Cash (0%).

**Causas raíz:**
1. Heurística monto+fecha falla porque ledger guarda neto y XML guarda bruto.
2. No se extrae `order_id` del tag `<Referencia>` en DTE 43.
3. No existe fuente de cash — no hay liberaciones, no hay settlements.

### 3.4 Para FALABELLA

**Se puede certificar:** hasta Ledger → Cierre (3/4 periods).

**No se puede certificar:** Ledger → XML (0%) ni Ledger → Cash (0%).

**Causas raíz:**
1. Loader no popula `folio_xml` aunque el source XLSX tiene "N° Documento Tributario".
2. Solo 4 meses de datos — data freshness gap.
3. No existe fuente de cash.

### 3.5 Para SHOPIFY

**No se puede certificar nada:** el marketplace no está integrado al pipeline.

**Potencial:** SHOPIFY tiene la única fuente de datos bancarios (Transbank .dat) de todo el sistema.

---

## 4. RESUMEN DE GAPS ESTRUCTURALES

Reordenados por prioridad según P40R1.

**Prioridad ALTA** (bloquean certificación cash):

| # | Gap | Marketplaces | Tipo | Bloquea |
|---|---|---|---|---|
| G1 | CashTrace: Sin cadena XML→Settlement→Pago→Banco→Cobro | ALL | Arquitectura | Certificación cash completa |
| G2 | Liberaciones ML no almacenadas en DB | ML | Pipeline | Trazabilidad cash automatizada |
| G3 | Sin fuente cash RIPLEY/PARIS/FALABELLA | 3 MPs | Data | Cash certification |
| G4 | Sin integración bancaria | ALL | Data | Banco certification |

**Prioridad MEDIA** (bloquean certificación XML/legal):

| # | Gap | Marketplaces | Tipo | Bloquea |
|---|---|---|---|---|
| G5 | RIPLEY folio≠SII estructural | RIPLEY | Matching | Certificación legal |
| G6 | PARIS heuristic match fails | PARIS | Matching | Certificación legal |
| G7 | FALABELLA folio_xml no poblado | FALABELLA | Loader bug | Certificación XML |
| G8 | Sin Referencia tag extraction | PARIS, RIPLEY | Matching | Order_id bridge |
| G9 | SHOPIFY no integrado | SHOPIFY | Pipeline | Trazabilidad completa |

**Prioridad BAJA** (mejoras, no bloquean):

| # | Gap | Marketplaces | Tipo | Bloquea |
|---|---|---|---|---|
| G10 | Sin settlement_id/payment_id/pack_id en ledger | ALL | Schema | Trazabilidad granular |
| G11 | Liquidacion_FF no procesado | ML | Pipeline | $330M sin verificar |
| G12 | Poscobro no eliminado (DEC-009) | ML | Pipeline | Deuda técnica |

---

## 5. ¿Qué información falta exactamente?

### 5.1 Lo que YA EXISTE (no necesita reconstruirse)

| Eslabón | MPs | Estado |
|---|---|---|
| RAW → Ledger (vía SurgicalLoader) | ML, RIPLEY, PARIS, FALABELLA | ✅ 100% cargado |
| Ledger → Clasificación (vía run_classification) | ML, RIPLEY, PARIS, FALABELLA | ✅ 100% clasificado |
| Clasificación → Cierre (vía run_financial_closing) | ML, RIPLEY, PARIS, FALABELLA | ✅ Cobertura total |
| ClosingContribution (ledger periodo → cierre periodo) | ML, RIPLEY, PARIS, FALABELLA | ✅ Consultable sin tabla nueva |
| Ledger → XML (folio_xml como identificador) | ML, PARIS | ✅ 89.4% / 81.2% |
| DTE Index (XMLs cargados en dte_truth_v1) | ML, RIPLEY, PARIS, FALABELLA | ✅ 100% indexado |

### 5.2 Lo que FALTA (por eslabón)

| # | Eslabón faltante | MPs | Información necesaria |
|---|---|---|---|
| 1 | **Ledger → Settlement** | ALL | Liberaciones cargadas en DB. Settlement Bridge por monto+periodo para RIPLEY. |
| 2 | **Settlement → Pago** | ALL | Integración con gateway de pago (Mercado Pago API, Transbank API). |
| 3 | **Pago → Banco** | ALL | Extractos bancarios cargados. SHOPIFY tiene Transbank .dat sin procesar. |
| 4 | **Banco → Cobro** | ALL | Confirmación de fondo recibido. book_banco no implementado para ningún MP. |
| 5 | **XML Matching (folio SII)** | RIPLEY, PARIS, FALABELLA | Settlement Bridge por monto+periodo. Referencia tag extraction. |
| 6 | **folio_xml poblado** | FALABELLA | Bug en load_falabella() — no popula "N° Documento Tributario". |
| 7 | **SHOPIFY pipeline** | SHOPIFY | Loader + Ledger + Clasificación + Cierre completos. |

### 5.3 Prioridad de implementación

```
1. EvidenceLinkRegistry     (consultas sobre datos existentes — inmediato)
2. ClosingContribution      (consulta SQL — inmediato)
3. CoverageAnalyzer         (consultas SQL — inmediato)
4. GapAnalyzer              (reportes sobre gaps conocidos — inmediato)
5. CashTrace (diseño)       (contratos + documentación — preparatorio)
6. CashTrace (datos)        (cargar Liberaciones, Transbank .dat — futuro)
7. CashTrace (integración)  (API bancaria, gateway — futuro)
```

### 5.4 Por marketplace

- **ML**: Solo falta CashTrace. La cadena RAW→Ledger→XML→Settlement existe pero los datos de Settlement están en archivos RAW, no en DB.
- **RIPLEY**: Falta XML matching (Settlement Bridge) + CashTrace completo. Sin fuente de cash identificada.
- **PARIS**: Falta XML matching (Referencia tag) + CashTrace completo. Sin fuente de cash.
- **FALABELLA**: Falta folio_xml poblado + XML matching + CashTrace completo. Solo 4 meses de datos.
- **SHOPIFY**: Falta pipeline completo + CashTrace (único MP con datos bancarios disponibles en Transbank .dat).
