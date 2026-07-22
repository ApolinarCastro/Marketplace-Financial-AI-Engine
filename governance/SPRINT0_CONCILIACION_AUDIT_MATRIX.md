# Sprint 0 — Auditoría de Conciliación: Matriz Legacy → Adopción

**Fecha:** 2026-07-14  
**Objetivo:** Determinar qué reglas del legacy RTU pueden incorporarse como Reconciliation Engine satélite sin modificar MARKETPLACE_AUDITOR_V3_5_RC1.  
**Modo:** READ-ONLY. No se modificó código, DB, taxonomías ni motores certificados.  
**Fuentes:** Esquema real DuckDB, `surgical_loader.py`, `marketplace_auditor.py`, `reconciliation_engine.py`, `financial_engine.py`, `certification_engine.py`, `evidence/contracts.py`, evidencia FASE 1B.

---

## Resumen de decisión

| Decisión | Cantidad | Reglas |
|----------|----------|--------|
| **ADOPT** | 8 | Reglas maduras, sin conflicto con certificación, evidencia completa |
| **ADAPT** | 5 | Requieren modificación para alinearse con Single Financial Truth |
| **REJECT** | 6 | Legacy muerto, duplicado, o fuera del alcance financiero |
| **INSUFFICIENT_EVIDENCE** | 6 | Datos insuficientes para determinar adopción segura |

---

## Matriz completa

### R1 — SAP Conciliación (Orden de Venta vs Número SAP)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Conciliar `Orden de Venta` (MP) vs `Número SAP` (ERP) usando `harmonizar_id()` |
| **Marketplace** | ML, PARIS, RIPLEY |
| **Source Files** | `_archive/ARCHIVED/engine/data_loader_v4.py` (líneas 9-61), `engine/v4/utils.py` (línea 28) |
| **Source Fields** | `Orden de Venta` → `order_id`, `Número SAP` → `doc_num`, `Total Sin Despacho` → `total_product`, `Despacho` → `shipping_sap`, `canal` (ML/PARIS/RIPLEY) |
| **Economic Meaning** | Validación cruzada entre el sistema de facturación del marketplace y el ERP corporativo. Detección de diferencias en montos facturados vs contabilizados. |
| **Target Public Contract** | `FinancialEngine.query_ledger()` con parámetros `folio_xml`, `archivo_origen` (RFC-040R1). No existe endpoint SAP. |
| **Required Fixture** | SAP XLSX de prueba con columnas `Orden de Venta`, `Número SAP`, `Total Sin Despacho`, `Despacho`, `canal`. Requiere `data/db/sap_reconciliation.db` o tabla `sap_raw` en DuckDB. |
| **Expected Result** | Para cada marketplace, delta entre SUM(`total_product + shipping_sap`) vs SUM(ledger `monto` para `financial_group='ingresos'`). Delta esperado = 0 cuando SAP está actualizado. |
| **Evidence** | `engine/v4/utils.py:28` (comentario: "Normalize marketplace / SAP order IDs"). No hay datos SAP en DuckDB actual. |
| **Risk** | ALTO. SAP es un sistema externo no controlado. Los archivos SAP referencian paths externos (`C:\Users\...\SAP\`). La tabla `sap_raw` no existe en la DB oficial. |
| **Adoption Decision** | **REJECT** — Datos SAP no están disponibles, la tabla `sap_raw` tiene 0 filas, el código legacy está archivado. No hay evidencia de que SAP sea relevante para el modelo financiero actual. |

---

### R2 — RTU Conciliación Transacciones

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Conciliar transacciones contra el proyecto `Conciliacion_Meli_RTU` |
| **Marketplace** | ML, PARIS |
| **Source Files** | `governance/RIPLEY_SOURCE_RECOVERY_REPORT.md` (línea 29) |
| **Source Fields** | Referencia a path externo: `Proyectos\Conciliacion_Meli_RTU\01_Raw\` |
| **Economic Meaning** | Proyecto anterior de conciliación ML—RTU (Registro de Transacciones Únicas). Desconocido. |
| **Target Public Contract** | Ninguno. RTU no tiene representación en DB, API ni código activo. |
| **Required Fixture** | N/A — proyecto externo, datos no disponibles en este repositorio. |
| **Expected Result** | N/A |
| **Evidence** | Una mención en governance report. Cero código activo. Cero referencias en DB. |
| **Risk** | CRÍTICO. No hay datos, no hay schema, no hay contrato. Cualquier implementación sería especulativa. |
| **Adoption Decision** | **REJECT** — Legacy muerto. Proyecto externo sin representación en el repositorio actual. |

---

### R3 — Saldo Pendiente RIPLEY

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Columna `Saldo Pendiente` en XLSX legacy de RIPLEY representa dinero no liberado (en tránsito/reserva/contracargo) |
| **Marketplace** | RIPLEY |
| **Source Files** | `_archive/Scripts/Migration/certify_ml_fase1.py` (línea 58), `governance/RIPLEY_SOURCE_RECOVERY_REPORT.md` (línea 39) |
| **Source Fields** | `Saldo Pendiente`, `Saldo Conciliación`, `Detalle Conciliación` (columnas de XLSX legacy RIPLEY) |
| **Economic Meaning** | Representa la diferencia entre lo facturado y lo efectivamente liberado/pagado por RIPLEY. Análogo a `cuentas por cobrar` o `provision`. |
| **Target Public Contract** | `FinancialEngine.query_ledger(financial_group='tesoreria')`. La tabla `marketplace_ledger_v1` tiene filas con `financial_group='tesoreria'` solo si fueron clasificadas así. |
| **Required Fixture** | Archivo XLSX legacy de RIPLEY con columna `Saldo Pendiente`. No existe en `01_Raw/RIPLEY/` actual. |
| **Expected Result** | `Saldo Pendiente` = `SUM(tesoreria) + SUM(ajustes_no_operacionales)`. Debe cuadrar con `Liberaciones - P&L Neto`. |
| **Evidence** | Cero columnas `saldo_pendiente` en DB actual. El campo existía en XLSX legacy del proyecto RTU externo. No hay evidencia de que RIPLEY actual genere este campo. |
| **Risk** | ALTO. Campo legacy sin representación actual. Si se incorpora sin datos reales, genera ruido en el modelo. |
| **Adoption Decision** | **INSUFFICIENT_EVIDENCE** — No hay datos actuales de `Saldo Pendiente` en la DB ni en los archivos fuente actuales. No se puede determinar si la regla es aplicable al pipeline V4. |

---

### R4 — Poscobro Deduplicación (ML)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Deduplicar Poscobro por `(operation_id, detalle, monto, fecha)` — elimina duplicados de origen Excel |
| **Marketplace** | ML |
| **Source Files** | `engine/v4/surgical_loader.py` (línea 296) |
| **Source Fields** | `operation_id` (extraído de `id_transaccion` vía regex `r'POS_(\d+)_'`), `detalle`, `monto`, `fecha` |
| **Economic Meaning** | Los archivos Poscobro contienen filas duplicadas por diseño (múltiples descargas/exports). La dedup evita doble contabilización de ajustes. |
| **Target Public Contract** | `ReconciliationEngine.validate_marketplace_consistency()` — Nivel 1 interna valida que clasificado == cierre. El satélite podría verificar que no existen duplicados residuales. |
| **Required Fixture** | Conjunto de datos Poscobro con duplicados conocidos. Por ejemplo, `data/snapshots/pre_poscobro_fix_20260605_155052/poscobro_correction_map.json`. |
| **Expected Result** | Cero pares `(id_transaccion, detalle, monto, fecha)` duplicados en `marketplace_ledger_v1` para ML Poscobro. Si existen, son doble contabilización real. |
| **Evidence** | `surgical_loader.py:296` contiene la lógica activa de dedup. `snapshot_pre_poscobro_fix_20260605_155052/` tiene el mapa de correcciones. |
| **Risk** | BAJO. La regla ya está implementada en el loader. El satélite solo verificaría post-facto que la dedup funcionó. |
| **Adoption Decision** | **ADOPT** — Regla madura, implementada, con evidencia. El satélite puede agregar validación: "Verificar que no existan duplicados Poscobro en ledger post-carga". |

---

### R5 — Liberaciones ID Matching (ML)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Matching `id_orden` entre Ledger y Liberaciones requiere `float64 → int → str` + padding especial Meli (IDs cortos que empiezan con '2' → padding a 16 dígitos con ceros a la izquierda) |
| **Marketplace** | ML |
| **Source Files** | `engine/v4/utils.py` (`harmonize_id()`), `engine/v4/surgical_loader.py` (carga Liberaciones) |
| **Source Fields** | `ID DE LA OPERACIÓN EN MERCADO PAGO` → `id_transaccion` (PAYOUT_*), `ID DE LA ORDEN` → `id_orden`, `MONTO NETO ACREDITADO` / `MONTO NETO DEBITADO` → `monto` |
| **Economic Meaning** | Liberaciones representan el flujo de caja real. Matching correcto permite trazar cada orden desde la venta (P&L) hasta el efectivo recibido (tesorería). |
| **Target Public Contract** | `FinancialEngine.query_ledger(folio_xml=...)` o `query_ledger(order_id=...)`. El satélite cruzaría `ledger.id_orden = liberaciones.id_orden`. |
| **Required Fixture** | Archivo Liberaciones XLSX de prueba (ej. `01_Raw/ML/Liberaciones/2026-06 Junio/1jun2026 a 30jun2026.xlsx`). Registro en `ventas_marketplace` para matching. |
| **Expected Result** | Para cada orden con Liberación, delta entre `Ledger SUM(monto)` (operacional) y `Liberación SUM(neto_acreditado - neto_debitado)` debe ser ≤ tolerancia. |
| **Evidence** | `SALE_TO_BANK_TRUTH_CERTIFICATION.md` certifica 31,284/31,506 (99.3%) órdenes ledger encontradas en Liberaciones. `harmonize_id()` implementa el padding Meli. |
| **Risk** | MEDIO. Depende del formato del archivo Liberaciones (cambia periódicamente). Los nombres de columna varían entre períodos. |
| **Adoption Decision** | **ADOPT** — Regla certificada y documentada. El satélite puede implementar verificación periódica de matching Liberaciones vs Ledger. |

---

### R6 — RIPLEY Layer Detection (CICLOS/TH/FF)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Detectar capa de origen de cada transacción RIPLEY por patrón de `id_transaccion`: `RIP_TH_%` = Transaction History, `RIP_FF_%` = Fulfillment, `RIP_CSV_%` = CICLOS, `RIP_*.xlsx` = Seller. |
| **Marketplace** | RIPLEY |
| **Source Files** | `engine/v4/domain/financial_engine.py` (query_desglose(), líneas 484-491) |
| **Source Fields** | `id_transaccion` (patrón `RIP_TH_`, `RIP_FF_`, `RIP_CSV_`, `RIP_LIQ`), `archivo_origen` (`.xlsx`, `.csv`, `.xml`) |
| **Economic Meaning** | Cada capa representa una verdad financiera distinta: TH = transaccional (real), FF = logística (costo), CICLOS = settlement (neto), XLSX = seller (operacional). Permite reconciliación por capa. |
| **Target Public Contract** | `FinancialEngine.query_desglose()` ya implementa layer detection via `CASE WHEN id_transaccion LIKE 'RIP_TH_%'`. El satélite puede extender a reconciliation por capa. |
| **Required Fixture** | Datos RIPLEY cargados con todos los tipos de archivo (CICLOS CSV, TH CSV, FF CSV, XLSX). Los archivos existen en `01_Raw/RIPLEY/`. |
| **Expected Result** | Layer TH + FF + CSV + XLSX debe reconciliarse con CICLOS CSV (settlement oficial). `SUM(TH) + SUM(FF) + SUM(CSV) ≈ SUM(XLSX)`. |
| **Evidence** | `financial_engine.py:484-491` implementa la detección. `reconciliation_engine.py` Nivel 3 (TESORERÍA) y Nivel 2 (OPERACIONAL) ya usan esta división implícitamente. |
| **Risk** | BAJO. Ya implementado en query_desglose(). El satélite solo agregaría validación explícita de reconciliación entre capas. |
| **Adoption Decision** | **ADOPT** — Regla implementada y probada. El satélite puede consolidar la reconciliación por capa RIPLEY como nivel de validación adicional. |

---

### R7 — PARIS Commission Splitting (_GROSS / _COMM)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Cada transacción PARIS genera dos registros en ledger: `_GROSS` (monto bruto = ingreso) y `_COMM` (comisión = costo). Solo si `abs(comision) > 0.01`. |
| **Marketplace** | PARIS |
| **Source Files** | `engine/v4/surgical_loader.py` (carga PARIS, línea 448) |
| **Source Fields** | `monto_bruto` (columna 'monto' raw), `monto_neto` (columna 'monto a pagar'), `comision = monto_neto - monto_bruto`. En DB: `monto_bruto`, `comision_marketplace`. |
| **Economic Meaning** | PARIS es canal 3P (DEC-023). El `monto_neto = monto_bruto + comisión`. La comisión es el ingreso real de Eccsa. Separar _GROSS y _COMM permite reportar comisión vs ingreso bruto. |
| **Target Public Contract** | `FinancialEngine.query_ledger(financial_group='ingresos')` devuelve _GROWS + _COMM. `query_desglose()` ya separa mediante `_apply_paris_desglose()`. |
| **Required Fixture** | Archivo PARIS XLSX con columnas `id`, `tipo`, `número orden`, `monto a pagar`, `monto`, `fecha`. Existen en `01_Raw/PARIS/Transacciones/`. |
| **Expected Result** | Para cada `id_transaccion`, `_GROSS + _COMM = 0` (la comisión es negativa, el gross es positivo). El neto total = comisión = ingreso real de Eccsa. |
| **Evidence** | `surgical_loader.py:448` con `abs(comision) > 0.01`. `DEC-023` certifica PARIS como 3P. `financial_engine.py` `_apply_paris_desglose()`. |
| **Risk** | BAJO. Regla estable, documentada y certificada. El split lleva meses en producción. |
| **Adoption Decision** | **ADOPT** — El satélite puede verificar que toda transacción PARIS tenga par _GROSS/_COMM y que la suma neta = comisión. |

---

### R8 — Sign Convention (positive = seller-favorable)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | `monto` positivo → flujo favorable al seller (ingreso, abono). `monto` negativo → flujo desfavorable al seller (costo, comisión, devolución). |
| **Marketplace** | TODOS (ML, PARIS, RIPLEY, FALABELLA) |
| **Source Files** | `engine/v4/surgical_loader.py` (docstring clase SurgicalLoader) |
| **Source Fields** | `monto`, `tipo_movimiento` (PAGO/INGRESO/CARGO/EGRESO). Signo determinado por loader según detalle. |
| **Economic Meaning** | Convención contable estándar: ingresos positivos, costos negativos. El `resultado_neto` = suma algebraica. Refleja P&L desde perspectiva del seller (Eccsa). |
| **Target Public Contract** | `query_waterfall()`: `ventas + devoluciones + cobros + recuperaciones = disponible`. Devoluciones y costos son negativos por diseño. `query_exec_summary()`: `gross_sales + returns + costs = net_profit`. |
| **Required Fixture** | Cualquier transacción con monto conocido. Todos los test fixtures existentes. |
| **Expected Result** | `ingresos > 0`, `devoluciones < 0`, `costos_operacionales < 0`, `costos_comerciales < 0`, `ajustes > 0` (la mayoría) o `< 0` (cargos). `resultado_neto = ingresos + devoluciones + costos + ajustes`. |
| **Evidence** | 374,285 filas en ledger con signo consistente. `waterfall` endpoint certificado con conservación: `ventas + devoluciones + cobros + recuperaciones ≡ disponible`. |
| **Risk** | Muy BAJO. Convención universal, implementada en todos los loaders, probada en todos los endpoints, certificada en SFT. |
| **Adoption Decision** | **ADOPT** — Regla fundacional. El satélite debe verificar que toda transacción nueva respete la convención de signo. |

---

### R9 — Year Filter (< 2025)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Filtrar filas con año < 2025. No cargar datos anteriores a 2025. |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/surgical_loader.py` (`_filter_old_years()`, línea 846) |
| **Source Fields** | `fecha` (DATE). Función: `df[fecha].dt.year < 2025` → excluir. |
| **Economic Meaning** | Datos anteriores a 2025 no son confiables (cambios de formato, loaders legacy). Excluirlos evita contaminación del ledger actual. |
| **Target Public Contract** | `FinancialEngine._build_ledger_where()` usa `fecha >= ?`. El rango de períodos empieza en 2025-01. |
| **Required Fixture** | Archivo fuente con fecha < 2025 para verificar exclusión. |
| **Expected Result** | Cero filas en ledger con año < 2025. Períodos certificados cubren 2025-01 en adelante. |
| **Evidence** | `surgical_loader.py:846`. SFT certifica 69 períodos desde 2025-01. |
| **Risk** | BAJO. Regla estable. Si cambia el criterio, requiere modificar loader + recargar datos históricos. |
| **Adoption Decision** | **ADOPT** — El satélite puede verificar que no existan filas con fecha < 2025 en el ledger. Validación de integridad temporal. |

---

### R10 — Financial Classification Mapping (normalize_detail → 200+ entries)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Mapear `detalle` normalizado → `financial_group` y `clasificacion_operativa` usando diccionario de 200+ entradas con normalized key |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/marketplace_auditor.py` (`run_classification()`, `normalize_detail()`, `NORMALIZED_CLASSIFICATION_MAP`) |
| **Source Fields** | `detalle` (raw string del ledger). Normalización: lowercase, NFD, strip non-alphanumeric. Luego lookup en `NORMALIZED_CLASSIFICATION_MAP`. |
| **Economic Meaning** | Cada concepto financiero (detalle) debe clasificarse en un grupo (ingresos/devoluciones/costos/comisiones/ajustes). Esta clasificación es la base de todo el reporting financiero. |
| **Target Public Contract** | `FinancialEngine.query_ledger()` retorna `financial_group`. `query_desglose()` y `financial-structure` endpoint dependen de esta clasificación. |
| **Required Fixture** | Para cada marketplace, archivo de prueba con todos los detalles conocidos. Los archivos `_archive/Scripts/OneShot/` tienen pruebas históricas. `tests/test_ripley_classification.py` es el test específico. |
| **Expected Result** | `COUNT(*) WHERE financial_group IS NULL` = 0 (100% clasificado). Cada `detalle` conocido debe mapear al grupo correcto según DEC-033. |
| **Evidence** | `NORMALIZED_CLASSIFICATION_MAP` con 200+ entradas en `marketplace_auditor.py`. DEC-033 certifica 4 taxonomías (ripley_v1.json 32 entries, ml_v1.json 71, paris_v1.json 15, falabella_v1.json 16). |
| **Risk** | BAJO si se usa el mapa existente. ALTO si se modifica el mapa (afecta Single Financial Truth). |
| **Adoption Decision** | **ADAPT** — Implementar como validación READ-ONLY en el satélite: verificar que todo `detalle` nuevo tenga asignación en el mapa. NO modificar el mapa existente. |

---

### R11 — Document Matching (document_match_v1)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Cada transacción en ledger debe tener un documento de respaldo (XML DTE, XLSX factura). Matching por `ledger_id ↔ id_transaccion`. |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/reconciliation/reconciliation_engine.py` (Nivel 4 — DOCUMENTAL), `evidence/coverage_analyzer.py` |
| **Source Fields** | `document_match_v1.ledger_id` JOIN `marketplace_ledger_clasificado_v1.id_transaccion`. `match_status = 'CONCILIATED'`. |
| **Economic Meaning** | Sin respaldo documental, una transacción en ledger no tiene validez fiscal. El matching documental es requisito para auditoría. |
| **Target Public Contract** | `ReconciliationEngine.validate_marketplace_consistency()` Nivel 4. `EvidenceOrchestrator.get_full_evidence()` → `CoverageAnalyzer.analyze()`. |
| **Required Fixture** | Registros en `document_match_v1` con `match_status='CONCILIATED'`. Datos DTE en `dte_truth_v1`. |
| **Expected Result** | `document_coverage = matched / total * 100 >= 95%` para CERTIFICADO. |
| **Evidence** | 9,431 filas en `document_match_v1`. Nivel 4 del ReconciliationEngine. `CoverageAnalyzer` calcula cobertura. |
| **Risk** | MEDIO. `document_match_v1.match_status` usa 'MATCHED' en datos reales pero el engine busca 'CONCILIATED' → 0% coverage si no se normaliza. |
| **Adoption Decision** | **ADAPT** — El satélite debe normalizar `match_status` ('MATCHED' y 'CONCILIATED' son equivalentes) antes de aplicar la regla. Adoptar la regla con normalización. |

---

### R12 — DTE Linking via folio_xml

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Vincular transacciones del ledger con DTEs reales (XML del SII) a través del campo `folio_xml`. |
| **Marketplace** | TODOS (ML 89.4%, RIPLEY 100% XLSX, PARIS ~51%, FALABELLA 0%) |
| **Source Files** | `engine/v4/dte_indexer.py`, `engine/v4/dte_matcher.py`, `dte_truth_v1`, `dte_link_v1` |
| **Source Fields** | `marketplace_ledger_v1.folio_xml` ↔ `dte_truth_v1.folio`. `dte_link_v1.folio ↔ ledger.folio_xml` y `dte_link_v1.id_transaccion`. |
| **Economic Meaning** | Cada transacción puede estar respaldada por un Documento Tributario Electrónico (DTE). La existencia de DTE válido es requisito para certification fiscal. |
| **Target Public Contract** | `FinancialEngine.query_ledger(folio_xml='...')` (RFC-040R1). EvidenceOrchestrator usa folio_xml para confidence='CERTIFICADO'. |
| **Required Fixture** | DTEs XML en `01_Raw/*/Documentos Recepcionados/`. Archivos DTE indexados en `dte_truth_v1`. |
| **Expected Result** | `dte_linked_rows / total_rows * 100 >= threshold`. ML tiene 339,112 filas en `dte_link_v1` (coverage real = 89.4%). PARIS/FALABELLA tienen 0% (DEC-036). |
| **Evidence** | `dte_truth_v1` con 667 filas. `dte_link_v1` con 339,112 filas. `DEC-036` acepta limitación heurística del DTEIndexer. |
| **Risk** | ALTO. DTEIndexer tiene limitación heurística (DEC-036): no vincula PARIS/FALABELLA porque no hay order_id en los XML. Forzar matching sin order_id genera falsos negativos. |
| **Adoption Decision** | **ADAPT** — Aceptar la regla para ML y RIPLEY. Para PARIS/FALABELLA, requiere order_id matcher (no implementado). El satélite debe reportar cobertura DTE diferenciada por MP. |

---

### R13 — Decimal/Number Normalization

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Normalizar montos usando `parse_amt()` (comma→period, trim), `clean_amount()` (float coercion), `harmonize_id()` (ID padding) |
| **Marketplace** | TODOS (especialmente RIPLEY CSV con coma como separador decimal) |
| **Source Files** | `engine/v4/utils.py`, `engine/v4/surgical_loader.py` (parse_amt en RIPLEY CICLOS) |
| **Source Fields** | `monto` (raw string → float), `id_orden` (string → float → int → str con padding) |
| **Economic Meaning** | Los archivos fuente usan formatos inconsistentes (coma decimal europea, notación científica, IDs numéricos con decimales). Sin normalización, los montos se malinterpretan (P0 date bug probó esto). |
| **Target Public Contract** | `FinancialEngine.query_ledger()` retorna `monto` como DOUBLE. No hay normalización visible en el contrato público. |
| **Required Fixture** | Archivo CSV con coma decimal (ej. RIPLEY CICLOS `01_Raw/RIPLEY/CICLOS/*.csv`). |
| **Expected Result** | `monto` en ledger debe ser numérico. Filas con error de parseo deben ser rechazadas (registradas en ingestion_registry.errors). |
| **Evidence** | `parse_amt()` activo en RIPLEY CICLOS. P0 date bug certifica que errores de formato causan contaminación. `ingestion_registry` tiene columna `errors` para tracking. |
| **Risk** | BAJO. Regla ya implementada en todos los loaders. |
| **Adoption Decision** | **ADOPT** — El satélite puede verificar post-carga que todos los montos en ledger sean numéricos válidos y que `ingestion_registry.errors` esté vacío. |

---

### R14 — Date Parsing (dayfirst=True)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Usar `dayfirst=True` en `pd.to_datetime()` para fechas en español (día/mes/año). NO usar el default (mes/día/año americano). |
| **Marketplace** | RIPLEY, PARIS (ML usa ISO) |
| **Source Files** | `engine/v4/surgical_loader.py` (líneas 496, 514 — corrección P0) |
| **Source Fields** | `fecha` (string DD/MM/YYYY → DATE). |
| **Economic Meaning** | Sin `dayfirst=True`, fechas como "03/02/2026" se interpretan como 3 de febrero (correcto) vs 2 de marzo (incorrecto). Esto causó el P0 que contaminó 47% de fechas RIPLEY. |
| **Target Public Contract** | `FinancialEngine._build_ledger_where()` usa `fecha >= ?`. Los períodos asumen fechas correctas en ledger. |
| **Required Fixture** | Archivo fuente RIPLEY con fechas en formato DD/MM/YYYY. |
| **Expected Result** | `MONTH(fecha)` debe ser consistente con el período del archivo fuente. Cero fechas intercambiadas (no more SWAP dates). |
| **Evidence** | `RIPLEY_DATE_PARSING_CERTIFICATION.md` (P0 confirmado, 100 sample proof). `RIPLEY_VALUE_CONSERVATION_CERTIFICATION.md` ($0 permanent loss). Corrección en `surgical_loader.py:496,514`. |
| **Risk** | BAJO. Regla corregida, certificada, documentada. |
| **Adoption Decision** | **ADOPT** — El satélite debe verificar que todas las fechas en ledger tengan mes consistente con período esperado. Detección temprana de SWAP dates. |

---

### R15 — Ventas_marketplace Dedup

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Insertar en `ventas_marketplace` con dedup por `order_id` (ML, PARIS) o `(order_id, sku)` (RIPLEY). |
| **Marketplace** | ML, PARIS, RIPLEY, FALABELLA |
| **Source Files** | `engine/v4/surgical_loader.py` (cada loader tiene su propia inserción en ventas_marketplace) |
| **Source Fields** | `order_id`, `sku`, `quantity`, `unit_price`, `gross_amount`, `sale_date`, `marketplace`, `source_file` |
| **Economic Meaning** | `ventas_marketplace` es el registro transaccional de ventas (order-level). Sirve como puente entre raw XLSX y ledger. La dedup evita doble conteo de la misma orden. |
| **Target Public Contract** | `FinancialEngine.query_ledger()` cruza con `ventas_marketplace` vía `id_orden` en `query_desglose()`. |
| **Required Fixture** | Archivos fuente de cada MP con órdenes repetidas. |
| **Expected Result** | `COUNT(DISTINCT order_id) = COUNT(*)` en `ventas_marketplace`. Cero order_id duplicados. |
| **Evidence** | `ventas_marketplace` con 53,326 filas. Cada loader implementa dedup propio. |
| **Risk** | BAJO. Regla estable, implementada en cada loader. |
| **Adoption Decision** | **ADOPT** — El satélite puede verificar integridad de ventas_marketplace: cero duplicados por MP, consistencia con ledger. |

---

### R16 — include_in_operational_pnl (DEC-019)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Transacciones con mecanismos pareados (Poscobro) deben excluirse del P&L operacional mediante `include_in_operational_pnl = 0`. |
| **Marketplace** | ML |
| **Source Files** | `engine/v4/marketplace_auditor.py` (ml_mandatory_exclusions), `DEC-019_EXECUTION_REPORT.md` |
| **Source Fields** | `marketplace_ledger_v1.include_in_operational_pnl` (BOOLEAN). Excluye 21 patrones específicos (paired BPP, Poscobro, mediaciones, cashback). |
| **Economic Meaning** | $94.4M en mecanismos pareados representan el mismo evento económico que la devolución original. Incluirlos en P&L infla el resultado operacional en 4.59%. Excluirlos corrige el P&L. |
| **Target Public Contract** | `FinancialEngine.query_ledger(operational_only=True)` → `COALESCE(include_in_operational_pnl, 1) = 1`. Endpoints waterfall, exec-summary, financial-structure usan este filtro. |
| **Required Fixture** | Transacciones ML con `include_in_operational_pnl=0` (3,663 filas pareadas). |
| **Expected Result** | `SUM(monto WHERE include_in_operational_pnl=0) = 0` en reportes operacionales. `query_exec_summary(operational_only=True) != query_exec_summary(operational_only=False)` para ML. |
| **Evidence** | `DEC-019` certificado. `RN_SOURCE_CERTIFIED` (2026-06-07). `economic_event_truth_certification` confirma same-event. |
| **Risk** | MUY ALTO. Violar DEC-019 rompe Single Financial Truth. Cualquier modificación al filtro require RFC. |
| **Adoption Decision** | **ADAPT** — El satélite debe verificar que DEC-019 se mantiene. NO modificar el filtro. Solo lectura: reportar cuántas filas están excluidas y su monto total. |

---

### R17 — Total Ajustes = devoluciones + ajustes (compound field)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | `total_ajustes` en `cierre_financiero_v1` es suma de `devoluciones + ajustes + riesgos_y_compensaciones + recuperaciones_y_bonificaciones + impuestos`. No es solo "ajustes". |
| **Marketplace** | TODOS (pero especialmente ML donde devoluciones es grande) |
| **Source Files** | `engine/v4/reconciliation/reconciliation_engine.py` (líneas 287-291), `engine/v4/marketplace_auditor.py` (run_financial_closing) |
| **Source Fields** | `marketplace_cierre_financiero_v1.total_ajustes`, `marketplace_ledger_clasificado_v1.financial_group` |
| **Economic Meaning** | Legacy constraint: `total_ajustes` originalmente almacenaba devoluciones + ajustes para compatibilidad con reportes V3. El ReconciliationEngine compensa sumando grupos adicionales. |
| **Target Public Contract** | `query_cierre_all()` retorna `total_ajustes` con el compound. Nivel 1 del ReconciliationEngine usa la suma compuesta para comparar. |
| **Required Fixture** | Filas en `cierre_financiero_v1` para cualquier marketplace/periodo. |
| **Expected Result** | `cierre_v1.total_ajustes = SUM(devoluciones) + SUM(ajustes) + SUM(riesgos) + SUM(recuperaciones) + SUM(impuestos)` en clasificado. |
| **Evidence** | `reconciliation_engine.py:287-291` con la suma compuesta. 246 filas en `cierre_financiero_v1`. |
| **Risk** | BAJO si es READ-ONLY. ALTO si se modifica el cierre (rompe compatibilidad V3). |
| **Adoption Decision** | **ADAPT** — El satélite puede verificar que la suma compuesta sea correcta. NO modificar el cierre. Reportar si algún grupo no está incluido. |

---

### R18 — RIPLEY Financial Mapping (UPPERCASE)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | `ripley_financial_mapping` table usa `financial_group` en UPPERCASE (`INGRESOS`, `DEVOLUCIONES`, `COMISIONES`). |
| **Marketplace** | RIPLEY |
| **Source Files** | `engine/v4/domain/financial_engine.py` (`_build_signal_filter()` usa LOWER()), `engine/v4/surgical_loader.py` (inserta lowercase) |
| **Source Fields** | `ripley_financial_mapping.financial_group` (VARCHAR, valores: 'INGRESOS', 'DEVOLUCIONES', 'COMISIONES', 'COSTOS_LOGISTICOS', 'AJUSTES', 'LIQUIDACION') |
| **Economic Meaning** | La tabla de mapeo RIPLEY se creó con UPPERCASE por convención del archivo fuente. El ledger real usa lowercase. El LOWER() en todas las queries compensa. |
| **Target Public Contract** | `_build_ledger_where()` usa `LOWER(financial_group)`. `query_ledger()` también. |
| **Required Fixture** | `ripley_financial_mapping` table (34 filas). Cualquier query que filtre por `financial_group`. |
| **Expected Result** | `SELECT COUNT(*) FROM ripley_financial_mapping WHERE LOWER(financial_group) IN (LOWER('ingresos'),...)` debe encontrar todas las filas. La tabla debe usarse con LOWER(). |
| **Evidence** | `ripley_financial_mapping` con 34 filas. `financial_engine.py` línea 1003 usa `LOWER()`. |
| **Risk** | BAJO si siempre se usa LOWER(). ALTO si alguien hace JOIN directo sin LOWER(). |
| **Adoption Decision** | **ADOPT** — El satélite debe usar `LOWER()` en todas las comparaciones con `financial_group`. Validar que `ripley_financial_mapping` sea consistente con el ledger. |

---

### R19 — Signal/Noise Taxonomy (RIPLEY-only)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Los detalles RIPLEY se clasifican como SIGNAL (11, representan flujo financiero real) o NOISE (21, representan movimientos contables internos). Por defecto, mostrar solo SIGNAL. |
| **Marketplace** | RIPLEY |
| **Source Files** | `knowledge/taxonomy/ripley_v1.json` (32 detalles: 12 SIGNAL, 20 NOISE), `financial_engine.py` (`_build_signal_filter()`) |
| **Source Fields** | `marketplace_ledger_v1.detalle`, `ripley_v1.json` entries con `classification: "SIGNAL"` o `"NOISE"`. |
| **Economic Meaning** | RIPLEY usa 32 conceptos contables diferentes, pero solo 12 representan flujo financiero real (SIGNAL). Los 20 NOISE son movimientos contables internos que distorsionan el P&L. Eliminarlos reduce el ruido en 54.1%. |
| **Target Public Contract** | `FinancialEngine.query_ledger(signal_mode='SIGNAL')`. `query_waterfall()`, `query_exec_summary()`, `financial-structure` endpoint. Ambos dashboards usan signal_mode=SIGNAL como default. |
| **Required Fixture** | `knowledge/taxonomy/ripley_v1.json`. Datos RIPLEY en ledger con todos los 32 detalles. |
| **Expected Result** | `SUM(SIGNAL) = 100% del P&L real`. `SUM(NOISE) = 0% del P&L real` (son movimientos contables que se cancelan). |
| **Evidence** | DEC-028, DEC-033. Phase 13 certification. `_build_signal_filter()` en financial_engine.py. |
| **Risk** | BAJO. Taxonomía certificada, implementada, probada. |
| **Adoption Decision** | **ADOPT** — El satélite debe usar signal_mode='SIGNAL' para reconciliación y 'ALL' para auditoría completa. |

---

### R20 — Waterfall Conservation Formula

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | `ventas + devoluciones + cobros + recuperaciones = disponible`. Propiedad de conservación del P&L: toda transacción cae en exactamente un grupo. |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/domain/financial_engine.py` (`query_waterfall()`, líneas 794-802) |
| **Source Fields** | `financial_group`: `ingresos` → Ventas, `devoluciones` → Devoluciones, `costos_operacionales/costos_comerciales/costos_logisticos/comisiones/ajustes` → Cobros, `recuperaciones_y_bonificaciones` → Recuperaciones. |
| **Economic Meaning** | La suma de todos los grupos financieros operacionales debe ser igual al neto (disponible). Cualquier diferencia indica transacciones no clasificadas o error de asignación. |
| **Target Public Contract** | `query_waterfall()` endpoint certificado. `test_certification_gate.py` prueba conservación. |
| **Required Fixture** | Cualquier conjunto de datos en ledger. |
| **Expected Result** | `ventas + devoluciones + cobros + recuperaciones - disponible = 0` (delta < 0.01). |
| **Evidence** | `query_waterfall()` en financial_engine.py. `test_certification_gate.py` (test_conservation). | 
| **Risk** | MUY BAJO. Propiedad matemática del modelo. Si se rompe, hay bug. |
| **Adoption Decision** | **ADOPT** — El satélite debe verificar la conservación del waterfall como prueba de humo básica en cada ejecución. |

---

### R21 — Tolerance 0.01

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Usar `abs(x) < 0.01` como tolerancia para considerar dos valores iguales. `abs(x) > 0.01` para considerar diferencia real. |
| **Marketplace** | TODOS |
| **Source Files** | 17+ ocurrencias en código activo y archive. `reconciliation_rules.yaml` (`allowed_delta: 0`, `critical_delta: 1`), `certification_engine.py:265` (`abs(net) < 0.01`) |
| **Source Fields** | Todos los campos DOUBLE (monto, comisión, totales). |
| **Economic Meaning** | Errores de redondeo en float64 pueden generar diferencias sub-peso. 0.01 CLP es el mínimo divisible. | 
| **Target Public Contract** | `ReconciliationEngine` usa `abs(delta) <= allowed_delta` donde `allowed_delta: 0` pero en la práctica `abs(delta) < 0.01`. `CertificationEngine` usa `abs(net) < 0.01`. |
| **Required Fixture** | Dos valores que difieran en < 0.01 CLP. |
| **Expected Result** | `abs(A - B) < 0.01` → considerar igual. |
| **Evidence** | 17+ ocurrencias de `< 0.01` en el código. `reconciliation_rules.yaml`. |
| **Risk** | Muy BAJO. Estándar de la industria para float64 financiero. |
| **Adoption Decision** | **ADOPT** — El satélite debe usar `abs(x) < 0.01` como tolerancia universal. |

---

### R22 — Silent try/except pass en _register_file

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | `_register_file()` ejecuta INSERT en file_registry dentro de `try/except pass` — los errores de registro son invisibles. |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/surgical_loader.py` (encontrado durante P39 cleanup) |
| **Source Fields** | `file_registry.file_hash`, `file_name`, `source`, `rows_processed`, `processed_at` |
| **Economic Meaning** | El registro de archivos procesados no debe fallar silenciosamente. Si no se registra, la trazabilidad se pierde. |
| **Target Public Contract** | `file_registry` table con `PRIMARY KEY (file_hash)`. |
| **Required Fixture** | Archivo de prueba que cause error en INSERT (ej. hash duplicado). |
| **Expected Result** | El error debe registrarse en `ingestion_registry.errors` o log, no ser silenciado. |
| **Evidence** | Mencionado en P39 Sprint 1 Foundation Reset como "3 critical `try/except pass` patterns eliminated". El patrón fue corregido. |
| **Risk** | BAJO si ya fue corregido en P39. |
| **Adoption Decision** | **REJECT** — Ya corregido en P39. No es una regla a adoptar, es un bug ya resuelto. |

---

### R23 — Consumo Único

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | No existe. Búsqueda exhaustiva de "consumo único", "consumo_unico", "single_use" — 0 resultados. |
| **Marketplace** | N/A |
| **Source Files** | N/A |
| **Source Fields** | N/A |
| **Economic Meaning** | N/A |
| **Target Public Contract** | N/A |
| **Required Fixture** | N/A |
| **Expected Result** | N/A |
| **Evidence** | 0 resultados en código, DB, governance. |
| **Risk** | N/A — regla no existe. |
| **Adoption Decision** | **REJECT** — No existe. No implementar nada. |

---

### R24 — 2% Closing Threshold (V3 Legacy)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | V3 cerraba períodos si `abs(diferencia) <= neto_esperado * 0.02` (2% de tolerancia). |
| **Marketplace** | TODOS (V3 legacy, no activo) |
| **Source Files** | `_archive/ARCHIVED/engine/financial_closing.py:48` (no existe en path activo, documentado en `financial_engine.py` legacy references) |
| **Source Fields** | `neto_esperado`, `diferencia` |
| **Economic Meaning** | En V3, se aceptaba un 2% de diferencia para cerrar un período. En V4, se exige delta=0. |
| **Target Public Contract** | ReconciliationEngine usa `allowed_delta: 0` — NO 2%. Cambio intencional. |
| **Required Fixture** | Datos V3 con diferencias < 2%. |
| **Expected Result** | V4 rechazaría estos períodos (delta != 0). |
| **Evidence** | `reconciliation_rules.yaml` con allowed_delta=0. |
| **Risk** | N/A — regla legacy reemplazada intencionalmente por V4 más estricto. |
| **Adoption Decision** | **REJECT** — La regla V3 (2% tolerance) fue reemplazada intencionalmente por V4 (allowed_delta=0). Re-adoptar sería un retroceso. |

---

### R25 — Empty Tables (10 legacy tables)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Existen 10 tablas con 0 filas en la DB: `financial_reconciliation`, `order_reconciliation`, `liberaciones`, `retiros`, `bank_statement`, `transaction_ledger`, `exceptions`, `cargos_no_clasificados`, `inconsistencias_financieras`, `ai_suggestions_log`. |
| **Marketplace** | TODOS |
| **Source Files** | DB schema via DuckDB `SHOW TABLES`. |
| **Source Fields** | Cada tabla tiene su schema pero 0 filas. |
| **Economic Meaning** | Estas tablas fueron creadas para funcionalidades planeadas pero nunca implementadas o migradas. |
| **Target Public Contract** | Ninguno. No son consumidas por ningún endpoint certificado. |
| **Required Fixture** | N/A — tablas vacías. |
| **Expected Result** | N/A. |
| **Evidence** | DuckDB `SHOW TABLES` + `SELECT COUNT(*)` para cada tabla. |
| **Risk** | MEDIO. Si alguien intenta leer estas tablas esperando datos, obtendrá 0 resultados sin error. |
| **Adoption Decision** | **INSUFFICIENT_EVIDENCE** — No hay suficiente información para determinar si estas tablas deben poblarse o eliminarse. Requieren RFC para decisión. |

---

### R26 — document_match_v1.match_status filter mismatch

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | ReconciliationEngine Nivel 4 filtra por `match_status='CONCILIATED'`. Pero los datos reales usan `'MATCHED'`. |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/reconciliation/reconciliation_engine.py` (línea 513), `document_match_v1` datos reales |
| **Source Fields** | `document_match_v1.match_status` — valores reales: 'MATCHED'. Valor esperado por engine: 'CONCILIATED'. |
| **Economic Meaning** | El motor busca un estado que no existe en los datos. Esto causa que document_coverage = 0% aunque haya matching. |
| **Target Public Contract** | ReconciliationEngine Nivel 4 endpoint no tiene consumo directo desde frontend. |
| **Required Fixture** | Filas en document_match_v1 con match_status='CONCILIATED'. |
| **Expected Result** | `CONCILIATED` debe ser el status después de confirmación manual. Pero los datos actuales solo tienen 'MATCHED'. |
| **Evidence** | `reconciliation_engine.py:513` y datos `document_match_v1` reales. |
| **Risk** | ALTO. Bug real: document_coverage reportado como 0% aunque hay 9,431 registros con match. |
| **Adoption Decision** | **ADAPT** — El satélite debe normalizar `match_status`: tratar 'MATCHED' como 'CONCILIATED' (o viceversa). Reportar el mismatch como gap. |

---

### R27 — Closing formula neto = ing + dev + cop + ccm + aju

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | `resultado_neto = SUM(ingresos) + SUM(devoluciones) + SUM(costos_operacionales) + SUM(costos_comerciales) + SUM(ajustes)`. TODO desde clasificado. |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/marketplace_auditor.py` (run_financial_closing). |
| **Source Fields** | `marketplace_ledger_clasificado_v1.financial_group`, `.monto`. |
| **Economic Meaning** | Fórmula single-source-of-truth para el P&L. Cualquier desviación de esta fórmula rompe el SFT. |
| **Target Public Contract** | `query_waterfall()`: `disponible = ventas + devoluciones + cobros + recuperaciones`. `query_exec_summary()`: `net_profit = gross_sales + returns + costs`. Ambas deben ser equivalentes a `resultado_neto`. |
| **Required Fixture** | Un periodo completo de cualquier MP con datos en ledger, clasificado y cierre. |
| **Expected Result** | `query_waterfall().disponible = query_exec_summary().net_profit = cierre.resultado_neto.` Delta = 0. |
| **Evidence** | `SINGLE_FINANCIAL_TRUTH_CERTIFICATION.md` (69/69 periodos PASS). |
| **Risk** | MUY BAJO. Fórmula base, certificada, probada. |
| **Adoption Decision** | **ADOPT** — El satélite debe verificar la equivalencia waterfall = cierre como validación principal de integridad financiera. |

---

### R28 — Post-Upload Copilot Question

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Después de una carga exitosa, el copiloto debe poder responder preguntas sobre los datos cargados con trazabilidad al execution_id. |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/copilot/copilot_engine.py`, `api/api.py` (`/api/v4/copilot/ask`) |
| **Source Fields** | `ingestion_registry.execution_id`, Copilot pregunta → SQL → respuesta con evidence chain. |
| **Economic Meaning** | El copiloto no es solo una interfaz conversacional. Debe poder trazar cada respuesta a su origen: execution_id de la carga, query SQL, fuente de datos. |
| **Target Public Contract** | `GET /api/v4/copilot/ask?question=...&marketplace=...&periodo=...`. El CopilotEngine devuelve answer + explanation + breakdown + evidence. |
| **Required Fixture** | Una carga exitosa con execution_id registrado en `ingestion_registry`. |
| **Expected Result** | Copilot responde con `evidence.chain[0].evidence_source = 'Ledger'` o similar, y `evidence.execution_id = ingestion_registry.execution_id`. |
| **Evidence** | `CopilotEngine` implementado con evidence validation (`_validate_evidence()`). 309 Copilot tests PASS. |
| **Risk** | MEDIO. Depende de que el execution_id se propague correctamente desde upload hasta copilot. Actualmente `ingestion_registry` tiene 1 fila, no hay prueba E2E que conecte upload → copilot. |
| **Adoption Decision** | **INSUFFICIENT_EVIDENCE** — El código existe (CopilotEngine, handlers, tests) pero no hay evidencia E2E que conecte una carga real con una respuesta del copiloto trazable al execution_id. Se requiere fixture: upload test file → copilot pregunta → respuesta con execution_id. |

---

### R29 — Zero-Logic Frontend (DEC-026)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Cero lógica financiera en el frontend. Todo cálculo debe hacerse en el backend. |
| **Marketplace** | TODOS |
| **Source Files** | `templates/executive_dashboard.html`, `templates/dashboard.html` (corregidos en Phase 12E/12F). |
| **Source Fields** | N/A — regla de arquitectura, no de datos. |
| **Economic Meaning** | Previene inconsistencias entre lo que muestra el dashboard y lo que calcula el backend. |
| **Target Public Contract** | Todos los endpoints de API. El frontend solo consume y renderiza. |
| **Required Fixture** | N/A — regla de diseño, no de fixture. |
| **Expected Result** | Cero `mapDetalleToConcept()` o lógica financiera en JS. |
| **Evidence** | `FRONTEND_ZERO_LOGIC_REMEDIATION.md`. 30/30 tests PASS. |
| **Risk** | Muy BAJO. Regla de diseño, ya implementada y probada. |
| **Adoption Decision** | **REJECT** — No es una regla de conciliación. Es una regla de arquitectura ya implementada. El satélite no debe tocar frontend. |

---

### R30 — Observability Metrics (reconciliation_delta, taxonomy_coverage, etc.)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | ReconciliationEngine debe exponer métricas de observabilidad: `reconciliation_delta`, `taxonomy_coverage`, `document_coverage`, `orphan_records`, `certification_status`. |
| **Marketplace** | TODOS |
| **Source Files** | `engine/v4/reconciliation/reconciliation_rules.yaml` (sección observability), `engine/v4/observability/` (Phase 5) |
| **Source Fields** | Métricas derivadas de reconciliation, no campos directos de DB. |
| **Economic Meaning** | Sin observabilidad, no se puede detectar degradación del SFT. Las métricas permiten monitoreo continuo. |
| **Target Public Contract** | `GET /api/v4/health/financial` (health score), `GET /api/v4/health/metrics`. |
| **Required Fixture** | Un período completo reconciliado. |
| **Expected Result** | Métricas reportadas sin error. |
| **Evidence** | `reconciliation_rules.yaml` sección observability. Phase 5-6 implementación. |
| **Risk** | BAJO. Ya implementado en observability engine. |
| **Adoption Decision** | **ADOPT** — El satélite debe reportar estas métricas como parte de su salida de reconciliación. |

---

### R31 — PARIS/FALABELLA DTE Order ID Matcher

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | No existe. DEC-036 acepta que DTEIndexer no puede vincular PARIS/FALABELLA porque no hay order_id en los XML. |
| **Marketplace** | PARIS, FALABELLA |
| **Source Files** | `engine/v4/dte_indexer.py`, `engine/v4/dte_matcher.py` |
| **Source Fields** | `dte_truth_v1.folio`, `marketplace_ledger_v1.folio_xml`. |
| **Economic Meaning** | Sin order_id en XML, no se puede hacer matching automático. PARIS tiene 62 XMLs indexados pero 0 vinculados. FALABELLA tiene 6 XMLs, 0 vinculados. |
| **Target Public Contract** | `FinancialEngine.query_ledger(folio_xml='...')`. |
| **Required Fixture** | XML PARIS/FALABELLA con order_id presente (no existe actualmente). |
| **Expected Result** | No aplica (no hay datos). |
| **Evidence** | DEC-036. |
| **Risk** | ALTO. No hay datos para implementar. |
| **Adoption Decision** | **INSUFFICIENT_EVIDENCE** — No hay suficiente evidencia para implementar matching PARIS/FALABELLA DTE. Se requiere order_id en XML, que actualmente no existe. |

---

### R32 — FALABELLA Unclassified Row ($12K)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | 1 fila FALABELLA (`b0ccbb6b...`, "Cobro por comisión por cancelación", $12,099) no tiene clasificación. |
| **Marketplace** | FALABELLA |
| **Source Files** | `engine/v4/marketplace_auditor.py` (NORMALIZED_CLASSIFICATION_MAP), `SINGLE_FINANCIAL_TRUTH_CERTIFICATION.md` |
| **Source Fields** | `detalle = 'Cobro por comisión por cancelación'`, `financial_group = NULL`. |
| **Economic Meaning** | Una transacción sin clasificar no contribuye al P&L. $12K es inmaterial (0.0007% del total) pero rompe el 100% de cobertura. |
| **Target Public Contract** | `query_ledger(financial_group='sin_clasificar')`. |
| **Required Fixture** | La fila específica con `id_transaccion = 'b0ccbb6b...'`. |
| **Expected Result** | Después de clasificación manual, `financial_group` no es NULL. |
| **Evidence** | `SINGLE_FINANCIAL_TRUTH_CERTIFICATION.md`. |
| **Risk** | MUY BAJO. $12K es inmaterial. Pero el SFT requiere 100% de cobertura. |
| **Adoption Decision** | **INSUFFICIENT_EVIDENCE** — No hay suficiente contexto para determinar si debe clasificarse como `costos_comerciales`, `ajustes`, u otro grupo. Se requiere decisión del área financiera. |

---

### R33 — PRE/POST Payout Logic (Retiro de dinero classification)

| Campo | Valor |
|-------|-------|
| **Legacy Rule** | Transacciones con patrones `pre_payout_`, `post_payout_`, `withdraw`, `retiro de dinero`, `reserve_for_dispute` → clasificar como `financial_group='tesoreria'`. |
| **Marketplace** | ML |
| **Source Files** | `engine/v4/marketplace_auditor.py` (run_classification) |
| **Source Fields** | `detalle` (contiene 'pre_payout_', 'post_payout_', 'withdraw', 'retiro de dinero', 'reserve_for_dispute') |
| **Economic Meaning** | Estos conceptos representan movimientos de tesorería (caja), no de P&L. Excluirlos del P&L operacional es correcto DEC-019. |
| **Target Public Contract** | `FinancialEngine.query_ledger(financial_group='tesoreria')`. |
| **Required Fixture** | Transacciones ML con detalle que contenga 'retiro de dinero'. |
| **Expected Result** | `financial_group='tesoreria'`, `include_in_operational_pnl=0`. |
| **Evidence** | `marketplace_auditor.py` payout rule. DEC-019. |
| **Risk** | BAJO. Regla estable, implementada. |
| **Adoption Decision** | **ADOPT** — El satélite puede verificar que transacciones con estos patrones estén correctamente clasificadas como tesorería. |

---

## Estadísticas de adopción

| Decisión | Cantidad | Reglas |
|----------|----------|--------|
| **ADOPT** | 13 | R4, R5, R6, R7, R8, R9, R13, R14, R15, R18, R19, R20, R21, R27, R30, R33 |
| **ADAPT** | 5 | R10, R11, R12, R16, R17, R26 |
| **REJECT** | 5 | R1, R2, R22, R23, R24 |
| **INSUFFICIENT_EVIDENCE** | 5 | R3, R25, R28, R31, R32 |

---

## Arquitectura propuesta para Satellite Reconciliation Engine

Basado en esta auditoría, el motor satélite debe:

1. **READ-ONLY** — Solo consultar `marketplace_ledger_v1`, `marketplace_ledger_clasificado_v1`, `marketplace_cierre_financiero_v1`, `document_match_v1`, `dte_truth_v1`
2. **No modificar** — ninguna tabla, taxonomía, engine certificado
3. **Validar 7 reglas centrales**:
   - Waterfall conservation (R20)
   - Sign convention (R8)
   - Neto formula equivalence (R27)
   - DEC-019 compliance (R16) — solo monitoreo
   - Document coverage (R11 adaptada)
   - Layer reconciliation RIPLEY (R6)
   - Classification coverage (R10 adaptada)
4. **Reportar 5 métricas**:
   - reconciliation_delta
   - taxonomy_coverage
   - document_coverage
   - orphan_records
   - certification_status
5. **Ignorar** SAP (R1), RTU (R2), Consumo Único (R23), V3 2% (R24)

**No crear nuevo engine separado.** Extender `EvidenceOrchestrator` existente con nuevas validaciones. No modificar `ReconciliationEngine`.
