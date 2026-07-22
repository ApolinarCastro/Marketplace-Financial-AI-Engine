# P40R2 EVIDENCE GRAPH — Trazabilidad Financiera Completa

## Cadena de evidencia universal

```
RAW ──► ETL ──► LEDGER ──► CLASIFICACIÓN ──► CIERRE ──► XML ──► SETTLEMENT ──► PAGO ──► BANCO ──► COBRO
```

Cada marketplace tiene una implementación diferente de esta cadena. Este documento mapea cada eslabón, los identificadores que lo conectan, y el porcentaje de cobertura actual.

> **Corrección P40R2B**: El Orchestrator solo depende de FinancialEngine, LedgerEngine, ReconciliationEngine y CertificationEngine. **No depende de CopilotEngine** — el Copilot es capa de presentación, no proveedor de datos. La información DTE (folio_xml, tipo_dte, emisor) debe exponerse desde FinancialEngine como método público; hasta entonces es GAP arquitectónico.

## Contrato público que expone cada eslabón (P40R2B)

| Eslabón | Engine | Contrato público | Accesible desde Orchestrator |
|---------|--------|-----------------|------------------------------|
| RAW → ETL | FinancialEngine | `query_ledger(archivo_origen=...)` — archivo_origen en cada fila | ✅ |
| ETL → Ledger | FinancialEngine | `query_ledger()` — todas las filas del ledger | ✅ |
| Ledger → Clasificación | FinancialEngine | `query_desglose()` — breakdown por financial_group | ✅ |
| Clasificación → Cierre | FinancialEngine | `query_cierre()` — cierre por período | ✅ |
| Cierre → Dashboard | FinancialEngine | `query_exec_summary()` — KPIs certificados | ✅ |
| Ledger → folio_xml | FinancialEngine | `query_ledger()` — columna folio_xml en cada fila | ✅ |
| folio_xml → DTE info | ❌ GAP-DTE | FinancialEngine no expone método público para DTE lookup | ❌ Pendiente |
| Evidencia → Validación | ❌ GAP-EVIDENCE | CertificationEngine no expone validate_evidence() público | ❌ Pendiente |
| Ledger → Settlement | ❌ No disponible | CashTrace (diseño) | ❌ Futuro |
| Settlement → Pago | ❌ No disponible | CashTrace (diseño) | ❌ Futuro |
| Pago → Banco | ❌ No disponible | CashTrace (diseño) | ❌ Futuro |
| Banco → Cobro | ❌ No disponible | CashTrace (diseño) | ❌ Futuro |

---

## 1. MERCADO LIBRE (ML)

### 1.1 Cadena real de evidencia

```
01_Raw/ML/Facturacion/18 XLSX
    │  Cobertura: 18/18 meses (Ene 2025 – Jun 2026) — 100%
    │  Identificadores: id_orden, folio_xml (formato 033-XXXXXXXXX)
    ▼
01_Raw/ML/Poscobro/5 XLSX
    │  Cobertura: Ene 2025 – Jun 2026 (irregular)
    │  Identificadores: operation_external_reference, order_id
    ▼
01_Raw/ML/Liberaciones/18 XLSX
    │  Cobertura: 18/18 meses — 100%
    │  Identificadores: ID_DE_LA_ORDEN (float64, requiere float64→int→str)
    ▼
SurgicalLoader.load_facturacion()
    │  Transformación: 1 row → 1-2 ledger rows (split Cargo por Venta en Venta+Comision)
    │  folio_xml: desde columna "folio" del XLSX — 89.4% coverage
    ▼
SurgicalLoader.load_poscobro()
    │  Transformación: mapeo directo a financial_group='ajustes'
    │  Dedup: (operation_id, detalle, monto, fecha)
    ▼
SurgicalLoader.load_liberaciones()
    │  Transformación: ledger como "Retiro de dinero" — solo 1,787 rows
    │  NO se almacena en tabla liberaciones
    ▼
marketplace_ledger_v1 (107,542 ML rows)
    │  89.4% con folio_xml (desde XLSX)
    │  financial_group: ingresos, devoluciones, costos_*, ajustes, NULL (paired mechanisms)
    │  include_in_operational_pnl: TRUE (P&L) / FALSE (paired mechanisms post DEC-019)
    ▼
MarketplaceAuditorEngine.run_classification()
    │  Cobertura: 100% clasificado (70 SIGNAL / 1 NOISE)
    │  Identificadores usados: detalle → normalize_detail → NORMALIZED_CLASSIFICATION_MAP
    ▼
marketplace_ledger_clasificado_v1 (107,542 rows)
    │  incluye clasificacion_operativa, financial_group, include_in_operational_pnl
    ▼
MarketplaceAuditorEngine.run_financial_closing()
    │  Fórmula: RN = ingresos + devoluciones + costos_op + costos_com + ajustes
    │  Solo filas con include_in_operational_pnl=TRUE
    ▼
marketplace_cierre_financiero_v1 (18 periods ML)
    ▼
DTEIndexer (01_Raw/ML/Documentos Recepcionados/)
    │  192 XMLs → 192 rows en dte_truth_v1 (100% indexado)
    │  Tipos: DTE 33 (30), DTE 43 (89), DTE 56 (17), DTE 61 (50)
    ▼
MeliXMLMatcher / XMLJustifier
    │  Heurística: ABS(monto) = MntTotal + fecha ±7 days
    │  Resultado ML: 97.6% coverage ($522.6M de $535.6M P&L)
    │  → estado_xml = 'CERTIFICADO' en ledger
    ▼
Liberaciones (archivos RAW XLSX)
    │  Solo 4.07% de PosCobro → cash real en Liberaciones
    │  99.3% de órdenes traza bles (31,284/31,506)
    │  Relación: Liberacion NET ≈ Ledger NET (ventas normales)
    │  Relación: Liberacion NET ≪ Ledger NET (claims/chargebacks)
    ▼
Banco
    │  NO INTEGRADO — tabla bank_statement: VACÍA
    │  Liberaciones es proxy (fuente: archivos XLSX, no API bancaria)
```

### 1.2 Relaciones existentes

| Desde | Hasta | Identificador | Cobertura |
|---|---|---|---|
| RAW Facturacion XLSX | marketplace_ledger_v1 | id_orden + folio_xml | 100% (18/18 meses) |
| RAW Liberaciones XLSX | marketplace_ledger_v1 | ID_DE_LA_ORDEN → id_orden | 99.3% (31,284/31,506) |
| marketplace_ledger_v1 | marketplace_ledger_clasificado_v1 | id_transaccion | 100% (107,542/107,542) |
| marketplace_ledger_v1 | dte_truth_v1 | folio_xml ↔ folio | 97.6% via XMLMatcher |
| RAW Documentos XLSX | dte_truth_v1 | folio_xml | 89.4% of ledger rows |
| RAW XML | dte_truth_v1 | archivo_xml → folio+tipo | 100% (192/192 DTEIndexer) |
| dte_truth_v1 | marketplace_ledger_v1 (estado_xml) | folio ↔ folio_xml | 97.6% (heuristic) |

### 1.3 Relaciones faltantes

| Desde | Hasta | Identificador faltante | Impacto |
|---|---|---|---|
| RAW Poscobro | marketplace_ledger_v1 | operation_id → id_transaccion existente | 10,002 rows sin folio_xml |
| marketplace_ledger_v1 | Liberaciones | id_orden → ID_DE_LA_ORDEN (float64 bug) | Match requiere conversión de tipo |
| Liberaciones RAW | tabla liberaciones (DB) | N/A — tabla nunca poblada | $0 cash data en DB |
| Liberaciones RAW | Banco | N/A — no hay integración bancaria | No se puede verificar cash real |
| Liquidacion_FF (90 files) | marketplace_ledger_v1 | N/A — no cargado por V4 | $330M en source sin procesar |
| RAW Facturacion (folio) | dte_truth_v1 (tipo+folio) | Formato 033-XXXXXXX vs folio numérico | Requiere regex join |

### 1.4 Cobertura por eslabón (ML)

| Eslabón | Cobertura | Certificado |
|---|---|---|
| RAW → ETL | 100% | ✅ V4 pipeline |
| ETL → Ledger | 100% | ✅ 107,542 rows |
| Ledger → Clasificación | 100% | ✅ DEC-033 |
| Clasificación → Cierre | 100% | ✅ 18/18 periods |
| Cierre → Dashboard | 100% | ✅ Single Financial Truth |
| Ledger → XML (folio_xml) | 89.4% | ✅ 96,143/107,542 |
| XML → DTE Index | 100% | ✅ 192/192 XMLs |
| DTE → Ledger (certificación) | 97.6% | ✅ $522.6M/$535.6M |
| Ledger → Settlement | 4.07% | ⚠️ Solo 1,787 "Retiro de dinero" |
| Settlement → Pago | 0% | ❌ Tablas liberaciones/retiros vacías |
| Pago → Banco | 0% | ❌ Sin integración bancaria |
| Banco → Cobro | 0% | ❌ Sin confirmación de cobro |

### 1.5 ClosingContribution (ML)

El cierre de ML usa 18 períodos (Ene 2025 – Jun 2026). Cada transacción en `marketplace_ledger_v1` con `include_in_operational_pnl=1` participa en exactamente un cierre, determinado por su `periodo` (YYYY-MM).

| Aspecto | Valor |
|---|---|
| Transacciones en ledger | 107,542 |
| Transacciones op_pnl=1 (contribuyen a RN) | ~103,879 (post DEC-019) |
| Transacciones op_pnl=0 (excluidas DEC-019) | 3,663 paired mechanisms |
| Períodos de cierre | 18 (Ene 2025 – Jun 2026) |
| Relación ledger → cierre | `periodo` = `periodo_fin` en cierre |
| Gap | No hay trazabilidad granular de "qué transacciones fueron excluidas del batch de cierre" |

### 1.6 CashTrace (ML)

| Eslabón | Estado | Identificador | Cobertura |
|---|---|---|---|
| XML → Settlement | ⚠️ Parcial | Liberaciones RAW (XLSX) | 99.3% órdenes match |
| Settlement → DB | ❌ No cargado | settlement_id | 0 rows en DB |
| Settlement → Pago | ❌ No integrado | payment_id | No existe |
| Pago → Banco | ❌ No integrado | bank_id | No existe |
| Banco → Cobro | ❌ Sin confirmación | cobro_id | No existe |

La única fuente de cash es Liberaciones (18 archivos XLSX). No está en DB. No hay API bancaria.

---

## 2. RIPLEY

### 2.1 Cadena real de evidencia

```
01_Raw/RIPLEY/XLSX (11 archivos principales)
    │  Cobertura: Ene 2025 – Jun 2026
    │  Identificadores: id_orden, Número documento liquidación → folio_xml
    │  Transformación: melt a detalle/monto pairs
    ▼
01_Raw/RIPLEY/Ciclos de facturación/52 CSV
    │  Cobertura: 52 ciclos (Dic 2024 – Jul 2026)
    │  Identificadores: numero de factura → folio_xml
    │  Formato: semicolon-delimited, coma-decimal
    ▼
01_Raw/RIPLEY/Historial de transacciones/8 CSV
    │  Cobertura: Ene 2025 – Jun 2026 (semestral+mensual)
    ▼
01_Raw/RIPLEY/Realización Ripley/72 CSV
    │  36 realización + 36 abonos/descuentos
    ▼
01_Raw/RIPLEY/Cumplimiento vendedor/51 XLSX
    │  Sequential IDs 312-383
    ▼
SurgicalLoader.load_ripley()
    │  Transformaciones complejas: melt, semicolon CSV, comma-decimal
    │  folio_xml: desde "Número documento liquidación" (XLSX) y "numero de factura" (CSV)
    ▼
marketplace_ledger_v1 (219,901 RIPLEY rows)
    │  97.3% con folio_xml (213,960 rows)
    │  PERO: folio_xml son números de orden de compra (500K-592K)
    │  NO son folios SII (DTE 33: 1.9M-2.4M, DTE 43: 108K-124K)
    │  financial_group: INGRESOS (uppercase — requiere LOWER())
    │  32 valores detalle distintos: 12 SIGNAL / 20 NOISE
    ▼
MarketplaceAuditorEngine.run_classification()
    │  100% clasificado
    │  financia l_group: ingresos, devoluciones, costos_operacionales, costos_comerciales, tesoreria, NULL
    ▼
marketplace_cierre_financiero_v1 (17 periods RIPLEY)
    │  $206.9M neto
    ▼
DTEIndexer (01_Raw/RIPLEY/XML/)
    │  No usa RIPLEY/Facturacion/ — usa RIPLEY/XML/ (407 discovered)
    │  407 XMLs → 407 rows en dte_truth_v1
    │  Tipos: DTE 33 (253), DTE 43 (105), DTE 52 (30), DTE 61 (19)
    │  Total $186.7M (45.1% de ledger)
    ▼
MeliXMLMatcher / XMLJustifier
    │  Resultado: 0 matches
    │  Causa raíz: folio_xml en ledger ≠ folios SII (diferentes sistemas de numeración)
    │  Zero overlap — 1 falso positivo (substring)
    ▼
"A pagar" (12,262 rows, $221.7M)
    │  financial_group=NULL (tesorería, no P&L)
    │  Estructuralmente = 50% del ledger RIPLEY
    │  Es el espejo del neto P&L — certificado por B2.5C
    ▼
Liquidación / Pago / Banco
    │  NO EXISTE — sin fuentes de cash identificadas
```

### 2.2 Relaciones existentes

| Desde | Hasta | Identificador | Cobertura |
|---|---|---|---|
| RAW XLSX | marketplace_ledger_v1 | id_orden + folio_xml | 100% (11 archivos) |
| RAW CSV (Ciclos) | marketplace_ledger_v1 | numero de factura → folio_xml | 100% (52 ciclos) |
| RAW CSV (TH) | marketplace_ledger_v1 | N/A (monto con signo) | 100% |
| marketplace_ledger_v1 | marketplace_ledger_clasificado_v1 | id_transaccion | 100% (219,901 rows) |
| marketplace_ledger_v1 | marketplace_cierre_financiero_v1 | financial_group | 100% (17 periods) |
| RAW XML | dte_truth_v1 | archivo → folio | 100% (407/407 DTEIndexer) |

### 2.3 Relaciones faltantes

| Desde | Hasta | Causa | Impacto |
|---|---|---|---|
| marketplace_ledger_v1.folio_xml | dte_truth_v1.folio | Diferentes sistemas de numeración | 0/407 matches — RIPLEY no certificable por folio |
| Ledger (P&L) | Liquidación real | No existe fuente de cash | $0 cash traceability |
| Ledger ("A pagar") | Pago real | "A pagar" es P&L mirror, no pago real | No se puede verificar cobro |
| RAW FF (Cumplimiento vendedor) | Ledger | No hay mapeo claro | 51 XLSX sin procesar |
| XML DTE 33/43/52/61 | Ledger | Settlement Bridge no implementado | $186.7M sin certificación legal |

### 2.4 Cobertura por eslabón (RIPLEY)

| Eslabón | Cobertura | Certificado |
|---|---|---|
| RAW → ETL | 100% | ✅ load_ripley() |
| ETL → Ledger | 100% | ✅ 219,901 rows |
| Ledger → Clasificación | 100% | ✅ DEC-033 (12 SIGNAL) |
| Clasificación → Cierre | 100% | ✅ 17/17 periods $0 delta |
| Cierre → Dashboard | 100% | ✅ Single Financial Truth |
| Ledger → XML (folio_xml column) | 97.3% | ⚠️ NO son folios SII |
| XML → DTE Index | 100% | ✅ 407/407 XMLs |
| DTE → Ledger (certificación) | 0% | ❌ Cero matches |
| Ledger → Settlement | 0% | ❌ Sin fuente de cash |
| Settlement → Pago | 0% | ❌ No existe |
| Pago → Banco | 0% | ❌ No existe |
| Banco → Cobro | 0% | ❌ Sin confirmación |

### 2.5 ClosingContribution (RIPLEY)

| Aspecto | Valor |
|---|---|
| Transacciones en ledger | 219,901 |
| Transacciones SIGNAL (contribuyen a RN) | 12/32 detalles |
| Períodos de cierre | 17 (certificados $0 delta) |
| Relación ledger → cierre | `periodo` → `periodo_fin` |
| Gap | financial_group en RIPLEY es UPPERCASE (INGRESOS) — requiere LOWER() para matching |

### 2.6 CashTrace (RIPLEY)

| Eslabón | Estado | Identificador | Cobertura |
|---|---|---|---|
| XML → Settlement | ❌ No existe | settlement_id | No hay fuente |
| Settlement → DB | ❌ No existe | N/A | 0 rows |
| Settlement → Pago | ❌ No existe | N/A | No integrado |
| Pago → Banco | ❌ No existe | N/A | No integrado |
| Banco → Cobro | ❌ No existe | N/A | Sin confirmación |

RIPLEY no tiene ninguna fuente de cash identificada. "A pagar" (12,262 rows, $221.7M) es espejo contable del P&L neto, no un flujo de caja real.

---

## 3. PARIS

### 3.1 Cadena real de evidencia

```
01_Raw/PARIS/Transacciones/Dropshipping/18 XLSX
    │  Cobertura: Ene 2025 – Jun 2026
    │  Identificadores: id_orden, número factura → folio_xml
    │  Formato: monto_bruto + monto_neto (comisión implícita)
    ▼
01_Raw/PARIS/Transacciones/Fulfillment/4 XLSX
    │  Cobertura limitada
    ▼
SurgicalLoader.load_paris()
    │  Transformación: 1 row → GROSS (monto_bruto) + COMM (monto_neto - monto_bruto)
    │  folio_xml: desde columna "número factura" (int)
    ▼
marketplace_ledger_v1 (74,062 PARIS rows)
    │  81.2% con folio_xml (60,107 rows)
    │  financial_group: ingresos, devoluciones, costos_operacionales, costos_comerciales
    │  15 valores detalle: 14 SIGNAL / 1 NOISE (Despacho = $0)
    ▼
MarketplaceAuditorEngine.run_classification()
    │  100% clasificado
    ▼
marketplace_cierre_financiero_v1 (PARIS)
    │  Single Financial Truth: $0 delta PARIS
    ▼
DTEIndexer (01_Raw/PARIS/Facturacion/)
    │  62 XMLs → 62 rows en dte_truth_v1
    │  Tipos: DTE 33 (66), DTE 43 (114), DTE 56 (17), DTE 61 (51)
    │  Total $816.6M (nota: cubre más períodos que ledger)
    ▼
MeliXMLMatcher / XMLJustifier
    │  Resultado: 0 matches
    │  Causa raíz: heurística monto+fecha falla porque ledger=neto vs XML=bruto
    │  No hay order_id en XML para hacer match
    ▼
Liquidación / Pago / Banco
    │  NO EXISTE — sin fuentes de cash identificadas
```

### 3.2 Relaciones existentes

| Desde | Hasta | Identificador | Cobertura |
|---|---|---|---|
| RAW XLSX | marketplace_ledger_v1 | id_orden | 100% |
| RAW XLSX → folio_xml | marketplace_ledger_v1 | número factura | 81.2% (60,107/74,062) |
| marketplace_ledger_v1 | marketplace_ledger_clasificado_v1 | id_transaccion | 100% |
| RAW XML | dte_truth_v1 | archivo → folio | 100% (62/62) |

### 3.3 Relaciones faltantes

| Desde | Hasta | Causa | Impacto |
|---|---|---|---|
| marketplace_ledger_v1.folio_xml | dte_truth_v1.folio | monto_neto ≠ monto_total DTE | 0% certification |
| Ledger (P&L) | Liquidación real | No existe fuente de cash | $0 cash traceability |
| Dropshipping XLSX | Fulfillment XLSX | Diferentes formatos | Coverage parcial |
| XML DTE | Ledger | No hay order_id en XML | DEC-036 aceptado |

### 3.4 Cobertura por eslabón (PARIS)

| Eslabón | Cobertura | Certificado |
|---|---|---|
| RAW → ETL | 100% | ✅ load_paris() |
| ETL → Ledger | 100% | ✅ 74,062 rows |
| Ledger → Clasificación | 100% | ✅ DEC-033 (14 SIGNAL) |
| Clasificación → Cierre | 100% | ✅ $0 delta |
| Cierre → Dashboard | 100% | ✅ Single Financial Truth |
| Ledger → XML (folio_xml column) | 81.2% | ✅ 60,107/74,062 |
| XML → DTE Index | 100% | ✅ 62/62 XMLs |
| DTE → Ledger (certificación) | 0% | ❌ 0 matches |
| Ledger → Settlement | 0% | ❌ Sin fuente de cash |
| Settlement → Pago | 0% | ❌ No existe |
| Pago → Banco | 0% | ❌ No existe |
| Banco → Cobro | 0% | ❌ Sin confirmación |

### 3.5 ClosingContribution (PARIS)

| Aspecto | Valor |
|---|---|
| Transacciones en ledger | 74,062 |
| Períodos de cierre | 18 ($0 delta certificado) |
| Relación ledger → cierre | `periodo` → `periodo_fin` |

### 3.6 CashTrace (PARIS)

PARIS no tiene ninguna fuente de cash identificada. Sin liberaciones, sin settlements, sin API bancaria.

---

## 4. FALABELLA

### 4.1 Cadena real de evidencia

```
01_Raw/FALABELLA/Facturación/4 XLSX
    │  Cobertura: Feb – Jun 2026 (solo 4 meses)
    │  Identificadores: N° Documento Tributario
    │  Formato: montos sin desglose
    ▼
01_Raw/FALABELLA/Órdenes y Transacciones/4 XLSX
    │  Cobertura: Mar – Jun 2026
    ▼
SurgicalLoader.load_falabella()
    │  Transformación: Precio del producto → ingreso, otros → CARGO o PAGO
    │  folio_xml: desde "N° Documento Tributario" (int, strip decimal)
    │  PERO: 0 rows tienen folio_xml en DB
    ▼
marketplace_ledger_v1 (678 FALABELLA rows)
    │  0% con folio_xml (0/678)
    │  financial_group: ingresos, devoluciones, costos_operacionales, costos_comerciales, ajustes
    │  16 valores detalle: 15 SIGNAL / 1 NOISE ($12K "Cobro por comisión por cancelación")
    ▼
MarketplaceAuditorEngine.run_classification()
    │  100% clasificado
    ▼
marketplace_cierre_financiero_v1 (FALABELLA)
    │  Single Financial Truth: 3/4 periods $0 delta, 1 row $12K ⚠️
    ▼
DTEIndexer (01_Raw/FALABELLA/Documentos Recepcionados/)
    │  6 XMLs → 6 rows en dte_truth_v1
    │  Tipos: DTE 33 (2), DTE 61 (2)
    │  Total $2.1M
    ▼
MeliXMLMatcher / XMLJustifier
    │  Resultado: 0 matches (misma causa que PARIS)
    ▼
Liquidación / Pago / Banco
    │  NO EXISTE
```

### 4.2 Relaciones existentes

| Desde | Hasta | Identificador | Cobertura |
|---|---|---|---|
| RAW XLSX | marketplace_ledger_v1 | id_orden | 100% |
| marketplace_ledger_v1 | marketplace_ledger_clasificado_v1 | id_transaccion | 100% |
| RAW XML | dte_truth_v1 | archivo → folio | 100% (6/6) |

### 4.3 Relaciones faltantes

| Desde | Hasta | Causa | Impacto |
|---|---|---|---|
| RAW XLSX "N° Documento Tributario" | marketplace_ledger_v1.folio_xml | Loader no popula (0/678) | 0% XML-ready en ledger |
| marketplace_ledger_v1.folio_xml | dte_truth_v1.folio | Sin folio_xml en ledger | 0% certification |
| Ledger (P&L) | Liquidación real | No existe fuente de cash | $0 cash traceability |
| RAW | Ledger | Solo 4 meses de datos | Data freshness FAIL |

### 4.4 Cobertura por eslabón (FALABELLA)

| Eslabón | Cobertura | Certificado |
|---|---|---|
| RAW → ETL | 100% | ✅ load_falabella() |
| ETL → Ledger | 100% | ✅ 678 rows |
| Ledger → Clasificación | 100% | ✅ DEC-033 (15 SIGNAL) |
| Clasificación → Cierre | 100% | ✅ 3/4 $0 delta |
| Cierre → Dashboard | 100% | ✅ Single Financial Truth |
| Ledger → XML (folio_xml column) | 0% | ❌ 0/678 |
| XML → DTE Index | 100% | ✅ 6/6 XMLs |
| DTE → Ledger (certificación) | 0% | ❌ 0 matches |
| Ledger → Settlement | 0% | ❌ Sin fuente de cash |
| Settlement → Pago | 0% | ❌ No existe |
| Pago → Banco | 0% | ❌ No existe |
| Banco → Cobro | 0% | ❌ Sin confirmación |

### 4.5 ClosingContribution (FALABELLA)

| Aspecto | Valor |
|---|---|
| Transacciones en ledger | 678 |
| Períodos de cierre | 4 (Feb–May 2026, 3/4 $0 delta, 1 row $12K no clasificada) |

### 4.6 CashTrace (FALABELLA)

FALABELLA no tiene fuente de cash. Sin liberaciones, sin settlements, sin API bancaria. Solo 4 meses de datos históricos.

---

## 5. SHOPIFY

### 5.1 Estado actual

SHOPIFY no está integrado en el pipeline V4. No existe `load_shopify()` ni marketplace en la lista de marketplaces procesados.

| Componente | Estado | Evidencia |
|---|---|---|
| RAW XML (Facturacion) | Existe (110 archivos, 52 compartidos con ML) | `01_Raw/SHOPIFY/Facturacion/` |
| RAW Mercado Pago | Existe (18 XLSX, mismo formato que ML) | `01_Raw/SHOPIFY/Mercado Pago/` |
| RAW Orders CSV | Existe (1 archivo, 18 meses) | `01_Raw/SHOPIFY/Pedidos (SF)/` |
| RAW Ventas CSV | Existe (1 archivo, 18 meses) | `01_Raw/SHOPIFY/Ventas totales (SF)/` |
| RAW Transbank (.dat) | Existe (3 archivos, Jun 2026) | `01_Raw/SHOPIFY/Transbank/` |
| DTEIndexer | NO procesa SHOPIFY | No en target directories |
| Loader V4 | NO implementado | No existe `load_shopify()` |
| Ledger | 0 rows | No hay datos SHOPIFY |
| Dashboard | 0 datos | Sin cobertura |

### 5.2 Oportunidad

SHOPIFY tiene la cadena más completa después de ML: XML + Facturacion + Orders + Ventas + Transbank (.dat bancario real). La presencia de archivos `.dat` de Transbank (crédito, débito, prepago) representa la única fuente de datos bancarios reales en todo el sistema.

---

## 6. RESUMEN MULTI-MARKETPLACE

### 6.1 Cobertura comparativa

| Eslabón | ML | RIPLEY | PARIS | FALABELLA | SHOPIFY |
|---|---|---|---|---|---|
| RAW archivos disponibles | 333 | 659 | 91 | 16 | 133 |
| RAW → Loader | 100% | 100% | 100% | 100% | 0% |
| Loader → Ledger | 107,542 | 219,901 | 74,062 | 678 | 0 |
| Ledger → Clasificación | 100% | 100% | 100% | 100% | N/A |
| Clasificación → Cierre | 18/18 | 17/17 | 18/18 | 4/4 | N/A |
| Cierre → Dashboard | ✅ | ✅ | ✅ | ✅ | N/A |
| folio_xml en ledger | 89.4% | 97.3% | 81.2% | 0% | N/A |
| folio_xml = SII real | 97.6% | 0% | 0% | 0% | N/A |
| ClosingContribution | ✅ period-based | ✅ period-based | ✅ period-based | ✅ period-based | N/A |
| Ledger → Settlement | 4.07% | 0% | 0% | 0% | N/A |
| Settlement → Pago | ❌ | ❌ | ❌ | ❌ | ❌ |
| Pago → Banco | ❌ | ❌ | ❌ | ❌ | Transbank (.dat RAW) |
| Banco → Cobro | ❌ | ❌ | ❌ | ❌ | ❌ |
| Cash source real | Liberaciones (XLSX) | ❌ | ❌ | ❌ | Transbank (.dat) |
| Banco integrado | ❌ | ❌ | ❌ | ❌ | ❌ |

### 6.2 Identificadores disponibles para EvidenceLinkRegistry

| Identificador | ML | RIPLEY | PARIS | FALABELLA | En DB |
|---|---|---|---|---|---|
| id_transaccion | ✅ | ✅ | ✅ | ✅ | marketplace_ledger_v1 |
| id_orden (order_id) | ✅ | ✅ | ✅ | ✅ | marketplace_ledger_v1 |
| folio_xml (desde source) | 033-XXXXXXX | Orden de compra (500K-592K) | N° factura (int) | N° Doc. Trib. (int) | marketplace_ledger_v1 |
| folio SII (desde XML) | 1.9M-2.4M | 108K-53M (4 rangos) | 1.9M-2.4M | ~ | dte_truth_v1 |
| shipment_id | ✅ (en source) | ❌ | ❌ | ❌ | No en ledger |
| pack_id | ✅ (en source) | ❌ | ❌ | ❌ | No en ledger |
| settlement_id | ❌ | ⚠️ "Número liquidación" | ❌ | ❌ | No en ledger |
| payment_id | ❌ | ❌ | ❌ | ❌ | No capturado |
| archivo_origen | ✅ | ✅ | ✅ | ✅ | marketplace_ledger_v1 |
| periodo | ✅ | ✅ | ✅ | ✅ | marketplace_ledger_v1 |

### 6.3 Hallazgos estructurales

1. **La cadena RAW→Ledger→Clasificación→Cierre existe para 4/5 MPs.** Está certificada. No necesita reconstrucción. El Evidence Engine debe consumirla, no reemplazarla.

2. **ClosingContribution existe por diseño**: cada transacción en ledger tiene `periodo` que corresponde a `periodo_fin` en cierre. La relación es `periodo = periodo_fin` + `LOWER(marketplace)`. No necesita tabla nueva — es una consulta.

3. **ML es el único con cadena XML → Settlement**: Liberaciones RAW cubren 99.3% de órdenes. Pero NO están en DB. El gap es DB, no disponibilidad de datos.

4. **RIPLEY tiene 219,901 rows pero 0% linkage XML-SII**: Los folios en ledger son órdenes de compra (500K-592K), no folios SII (1.9M-53M). Sistemas de numeración diferentes — no hay overlap por folio.

5. **PARIS tiene 62 XMLs y 60,107 ledger rows con folio_xml, pero 0 matches**: Heurística monto+fecha falla porque ledger guarda neto y XML guarda bruto. Sin order_id en XML para hacer match directo.

6. **FALABELLA tiene 0/678 rows con folio_xml en ledger**: Loader no popula el campo aunque el source XLSX tiene "N° Documento Tributario". Bug de loader.

7. **Ningún marketplace tiene CashTrace implementado**: Las tablas `bank_statement`, `retiros`, `liberaciones` existen en schema pero están vacías. La única fuente de cash son archivos RAW: Liberaciones ML (18 XLSX) y Transbank SHOPIFY (3 .dat).

8. **SHOPIFY tiene la única fuente bancaria real**: Archivos Transbank .dat (crédito, débito, prepago) no procesados. 133 archivos RAW total, 0 en pipeline.

9. **El verdadero vacío del sistema es CashTrace**: Desde XML hasta Cobro. Es un diseño por construir, no un bug por corregir.
