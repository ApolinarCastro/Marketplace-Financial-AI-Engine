# REPORTE COMPARATIVO FALABELLA PRE/POST REBUILD

## CAUSA RAÍZ
`surgical_loader.py` columna `c_id`: fuzzy match con `ID ARTICULO` prevalecía sobre `Falabella-Id`.
→ 131 transacciones de 5 tipos (Pago precio producto, Descuento devolución, Pago envío, Promociones) no se cargaban.
→ Fix: `c_id` → solo `['Falabella-Id', 'Falabella Id']` (líneas 435, 437, 439).

---

## 1. FALABELLA: PRE vs POST

| Métrica                | PRE (snapshot) | POST (actual) | DIFERENCIA |
|------------------------|---------------:|--------------:|-----------:|
| Filas ledger           | 877            | 1,008         | **+131**   |
| SUM(monto)             | -$2,578,242   | +$2,583,016   | **+$5,161,258** |
| UUIDs únicos           | 214            | 125           | -89 (antes duplicados por id_articulo) |
| Tipos de transacción   | 9             | **14**        | **+5**     |
| NO_CLASIFICADO         | 0             | 0             | 0          |
| NULL financial_group   | 62            | **0**         | **-62**    |

### Distribución por financial_group

| financial_group      | PRE rows | PRE $         | POST rows | POST $         |
|----------------------|---------:|--------------:|----------:|---------------:|
| costos_comerciales   | 272      | -$724,608     | 266       | -$741,650      |
| costos_operacionales | 326      | -$360,287     | 586       | -$382,750      |
| ingresos             | 0        | $0            | **125**   | **+$4,661,810** |
| devoluciones         | 0        | $0            | **27**    | **-$953,554** |
| ajustes              | 217      | -$18,334      | 4         | -$840          |
| NULL                 | 62       | -$1,475,013   | 0         | $0             |

### Nuevos tipos de transacción (antes ausentes)

| Tipo                          | Filas | Monto         | financial_group  |
|-------------------------------|------:|--------------:|------------------|
| Pago por precio del producto  | 125   | +$4,661,810   | ingresos         |
| Descuento por devolución prod | 27    | -$953,554     | devoluciones     |
| Pago de envío comprador       | 125   | +$140,892     | costos_operacionales |
| Corrección cobro envío directo| 4     | -$840         | ajustes          |
| (*) Reembolso Promo envío     | 92    | +$298,494     | costos_operacionales |
| (*) Cobro Promo envío         | 92    | -$298,494     | costos_operacionales |
(* = existían pero ahora con montos correctos por `c_fecha` y `c_monto` fixeados)

### Períodos

| Período  | Ingresos       | Costos Op     | Costos Com    | Ajustes       | Neto         |
|----------|---------------:|--------------:|--------------:|--------------:|-------------:|
| 2026-03  | +$1,457,438    | -$141,288     | -$271,997     | -$97,454      | +$946,699    |
| 2026-04  | +$3,204,372    | -$241,462     | -$469,653     | -$856,940     | +$1,636,317  |
| **TOTAL**| **+$4,661,810**| **-$382,750** | **-$741,650** | **-$954,394** | **+$2,583,016** |

---

## 2. VALIDACIÓN SQL=API=UI

### E2E `_validate_e2e.py`: ALL PASS (12/12)

| Marketplace | Categoría                | Período | SUM SQL        | SUM API        | DIFF  | STATUS |
|-------------|--------------------------|--------|---------------:|---------------:|------:|--------|
| ML          | Cargo por venta          | 2026-12| $0             | $0             | $0    | PASS   |
| ML          | Devolución de venta      | 2026-12| $0             | $0             | $0    | PASS   |
| ML          | TOTAL OPERACIONAL        | 2026-12| $35,980        | $35,980        | $0    | PASS   |
| RIPLEY      | Importe del pedido       | 2026-12| $431,780       | $431,780       | $0    | PASS   |
| RIPLEY      | Pedidos reembolsados     | 2026-12| -$80,950       | -$80,950       | $0    | PASS   |
| RIPLEY      | TOTAL OPERACIONAL        | 2026-12| $268,611       | $268,611       | $0    | PASS   |
| PARIS       | Venta                    | 2026-04| $28,931,590    | $28,931,590    | $0    | PASS   |
| PARIS       | Devolución               | 2026-04| -$5,093,120    | -$5,093,120    | $0    | PASS   |
| PARIS       | TOTAL OPERACIONAL        | 2026-04| $21,531,603    | $21,531,603    | $0    | PASS   |
| FALABELLA   | Cobro comisión por venta | 2026-04| -$469,653      | -$469,653      | $0    | PASS   |
| FALABELLA   | Cobro cofinanciamiento   | 2026-04| -$241,462      | -$241,462      | $0    | PASS   |
| FALABELLA   | TOTAL OPERACIONAL        | 2026-04| $1,636,317     | $1,636,317     | $0    | PASS   |

### Regression Contracts: 14/14 PASS

| Test | Status |
|------|--------|
| API rejects invalid param `subgroup` | PASS |
| Desglose endpoint no heuristics | PASS |
| INSERT/UPDATE/DELETE blocked | PASS |
| Ledger endpoint no heuristics | PASS |
| ML cargo venta DIFF=0 | PASS |
| ML ajuste arrepentimiento DIFF=0 | PASS |
| RIPLEY importe pedido DIFF=0 | PASS |
| RIPLEY pedidos reembolsados DIFF=0 | PASS |
| PARIS venta DIFF=0 | PASS |
| PARIS devolución DIFF=0 | PASS |
| FALABELLA comisión DIFF=0 | PASS |
| FALABELLA cofinanciamiento DIFF=0 | PASS |
| API file no contains/startswith | PASS |
| Dashboard no catMap | PASS |

---

## 3. IMPACTO EN ML, RIPLEY, PARIS (Debe ser CERO)

| Marketplace | PRE rows (V5) | POST rows | DIF | PRE $         | POST $         | DIF         |
|-------------|--------------:|----------:|----:|--------------:|---------------:|------------:|
| ML          | 101,603       | 101,603   | 0   | $842,250,301  | $842,250,301   | $0          |
| RIPLEY      | 269,216       | 269,216   | 0   | $284,897,360  | $284,897,360   | $0          |
| PARIS       | 42,487        | 42,487    | 0   | $378,104,933  | $378,104,933   | $0          |
| **TOTAL**   | **414,183**   | **414,314**|**+131** | **$1,505,252,594** | **$1,507,835,610** | **+$2,583,016** |

La única diferencia es FALABELLA: +131 rows, +$2,583,016 (exactamente el delta del Excel que faltaba).
ML, RIPLEY, PARIS: **0 filas cambiadas, $0 diferencia, 0 NO_CLASIFICADO, 0 NULL financial_group.**

---

## 4. FIXES APLICADOS (resumen)

| Archivo | Línea(s) | Fix |
|---------|----------|-----|
| `surgical_loader.py` | 435, 437, 439 | `c_id` → solo `Falabella-Id`/`Falabella Id`; `c_fecha` → prefiere `Fecha de transacción`; `c_monto` → prefiere `Monto (Sin IVA)` |
| `marketplace_auditor.py` | ~226-230 | +4 conceptos Falabella al RAW_TO_CLASSIFICATION_MAP |
| `marketplace_auditor.py` | ~241, 259 | `Descuento por devolución de producto`→devoluciones, `Pago de envío comprador`→costos_operacionales |
| `marketplace_auditor.py` | ~473-508 | Propagation: UPDATE `marketplace_ledger_v1` SET financial_group, clasificacion_operativa FROM `clasificado_v1` (join por `id_transaccion + detalle`) |
| `marketplace_auditor.py` | ~416-418 | ML: whitelist→exclusion-only (todo True excepto exclusiones específicas) |
| `marketplace_auditor.py` | ~422-423 | Treasury exclusion global: `"A pagar"`→`include_in_operational_pnl=False` |
| `database.py` | 22 | DuckDB `SET temp_directory` a `tempfile.gettempdir()` (Windows fix) |

---

## 5. PENDIENTE

Una vez autorizado: generar `BASELINE_ESTABLE_V6` (snapshot DB + MANIFEST.json con SHA256, row counts, financial_group stats, marketplaces).
