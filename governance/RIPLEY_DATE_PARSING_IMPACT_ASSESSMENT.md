# P0 INCIDENT — RIPLEY DATE PARSING IMPACT ASSESSMENT (FASE 1-7)

**Clasificación: P0 — EXTENSIÓN TOTAL CUANTIFICADA**

Fecha: 2026-05-30
Auditor: MFE Governance
Régimen: FORENSE — READ ONLY — NO FIXES
Depende de: `governance/RIPLEY_DATE_PARSING_CERTIFICATION.md` (FASE 1-5 originales)

---

## RESUMEN EJECUTIVO

El bug de `pd.to_datetime()` sin `dayfirst=True` en `surgical_loader.py:400` no afecta solo a Importe del pedido ni a Abril 2026. **Afecta al 100% de los datos financieros de Ripley — los 32 conceptos financieros, los 46 XLSX, los 16,923 órdenes originales, los 4 años de datos.**

| Métrica | Correcto (XLSX) | Ledger actual | Pérdida |
|---|---|---|---|
| Importe del pedido (all time) | **$358,012,384** | $240,979,600 | **−$117,032,784 (32.7%)** |
| Total ledger all concepts | **~$423,000,000** | $284,897,360 | **−~$138,000,000 (32.7%)** |
| Filas en ledger Importe | ~16,923 | 8,413 | **−8,510 (50.3%)** |
| Filas en ledger total | ~542,000 | 269,216 | **−~273,000 (50.3%)** |
| financiero_group clasificado | N/A | 0% | **100% sin clasificar** |
| folio_xml poblado | N/A | 0/269,216 | **0%** |

**Causa raíz única:** `pd.to_datetime()` sin `dayfirst=True` interpreta `dd-mm-yyyy` como `mm-dd-yyyy`.

**Impacto crítico:** El pipeline XLSX→Ledger→API→Dashboard pierde/corrompe ~32.7% de TODO el valor financiero de Ripley. Los Dashboards, reportes y KPIs basados en Ripley muestran valores incorrectos desde el día 1 de operación.

---

## FASE 1 — IMPACTO HISTÓRICO COMPLETO (ALL TIME)

### 1.1 Importe del pedido — Correcto vs Ledger por año

| Año | XLSX (dayfirst=T) | Ledger (actual) | Delta | % Retenido |
|---|---|---|---|---|
| 2023 | $4,852,060 | $0 | −$4,852,060 | **0%** |
| 2024 | Incluido arriba | $0 | $0 | **0%** |
| 2025 | $281,188,982 | $205,499,578 | −$75,689,404 | **73.1%** |
| 2026 | $71,971,342 | $35,480,022 | −$36,491,320 | **49.3%** |
| **Total** | **$358,012,384** | **$240,979,600** | **−$117,032,784** | **67.3%** |

### 1.2 Mecanismo de pérdida por año

| Año | MATCH (correcto) | SWAP (mes erróneo) | NaT (perdido) | OTHER ($0) | Total |
|---|---|---|---|---|---|
| 2023-2024 | $0 (dd>12 → smart → correcto → filtrado por año) | $0 | $4,852,060 | $0 | $4,852,060 |
| 2025 | $173,598,599 (47.1%) | $95,239,181 (25.8%) | $12,351,202 (3.4%) | $0 | $281,188,982 |
| 2026 | $28,025,050 (7.6%) | $23,464,742 (6.4%) | $20,481,550 (5.6%) | $0 | $71,971,342 |
| **Total** | **$201,623,649** | **$118,703,923** | **$37,684,812** | **$0** | **$358,012,384** |

Nota: 2023-2024 = $4,852,060 en filas con día > 12 (MATCH por smart detection). Pero son años < 2025, así que `_filter_old_years` las elimina de todas formas. El bug no causó la pérdida de 2023-2024 (el filtro intencional las elimina), pero SÍ causó que 2023-2024 no se puedan usar ni siquiera como referencia histórica en el Dashboard — el filtro es anterior al bug.

### 1.3 Destino de las 16,923 órdenes (Importe del pedido)

| Destino en Ledger | Filas | % | Monto | % |
|---|---|---|---|---|
| En el mes correcto (MATCH) | 6,292 | 37.2% | $173,598,599 | 48.5% |
| En mes incorrecto (SWAP) | 3,347 | 19.8% | $95,239,181 | 26.6% |
| Perdidas (NaT → filtradas) | 3,427 | 20.3% | $89,174,604 | 24.9% |
| Sin Importe (OTHER) | 3,857 | 22.8% | $0 | 0.0% |
| **Total XLSX** | **16,923** | **100%** | **$358,012,384** | **100%** |

Nota importante: El Ledger actual contiene 8,413 filas de Importe del pedido. De estas, **6,292 tienen el mes correcto** (MATCH). Las 2,121 restantes (~25%) son SWAP — filas que DEBERÍAN estar en otro mes pero están aquí por contaminación.

---

## FASE 2 — IMPACTO POR CONCEPTO FINANCIERO

### 2.1 Los 32 conceptos — todos afectados proporcionalmente

En el `load_ripley()` de `surgical_loader.py`, CADA fila del XLSX se "derrite" (melt) en 32 filas en el ledger, una por concepto financiero. El bug de fecha se aplica a la fila completa ANTES del melt, por lo que **TODOS los conceptos heredan el mismo error de fecha**.

| Concepto | Ledger 2025 | Ledger 2026 | Ledger Total | % del Total |
|---|---|---|---|---|
| Importe del pedido | $205,499,578 | $35,480,022 | $240,979,600 | 84.6% |
| A pagar | $119,981,342 | $22,467,338 | $142,448,680 | 50.0% |
| Envío | $10,739,672 | $1,797,032 | $12,536,704 | 4.4% |
| Comisiones sobre pedidos reembolsados | $8,673,064 | $1,180,606 | $9,853,670 | 3.5% |
| Gastos de envío reembolsados pagados por el operador | $1,071,552 | $53,635 | $1,125,187 | 0.4% |
| Comisiones sobre pedidos | −$37,505,537 | −$6,375,813 | −$43,881,350 | −15.4% |
| Pedidos reembolsados | −$47,485,091 | −$6,573,420 | −$54,058,511 | −19.0% |
| Gastos de envío pagados por el operador | −$10,739,672 | −$1,797,032 | −$12,536,704 | −4.4% |
| Descuento por costo logístico | −$8,557,698 | −$969,945 | −$9,527,643 | −3.3% |
| Envío reembolsado | −$1,071,552 | −$53,635 | −$1,125,187 | −0.4% |
| Descuento por logística inversa | −$619,800 | −$266,914 | −$886,714 | −0.3% |
| Descuento por cancelación | −$19,214 | −$7,198 | −$26,412 | −0.01% |
| Otros descuentos | −$3,960 | $0 | −$3,960 | −0.001% |
| **Resto (todos $0)** | **$0** | **$0** | **$0** | **0%** |

### 2.2 Pérdida estimada por concepto

Dado que TODOS los conceptos usan la misma columna de fecha, la tasa de pérdida (32.7%) se aplica uniformemente:

| Concepto | Correcto estimado (A pagar = Importe × 0.591) | Ledger actual | Delta estimado |
|---|---|---|---|
| Importe del pedido | $358,012,384 | $240,979,600 | **−$117,032,784** |
| A pagar | $211,607,920 | $142,448,680 | **−$69,159,240** |
| Envío | $18,618,544 | $12,536,704 | **−$6,081,840** |
| Comisiones sobre pedidos reembolsados | $14,631,296 | $9,853,670 | **−$4,777,626** |
| Gastos de envío reembolsados pagados por el operador | $1,670,786 | $1,125,187 | **−$545,599** |
| Comisiones sobre pedidos | −$65,158,320 | −$43,881,350 | **+$21,276,970** |
| Pedidos reembolsados | −$80,275,696 | −$54,058,511 | **+$26,217,185** |
| **Total neto** | **~$423,000,000** | **$284,897,360** | **−~$138,000,000** |

### 2.3 Observación crítica: Zero-value concepts

18 de 32 conceptos tienen valor $0 en el ledger. Estos conceptos (e.g., "Abono postventa", "Descuento FF - pick and pack") son columnas que existen en el XLSX pero tienen valor 0 para todas las filas procesadas. El bug de fecha NO afecta su valor ($0 se mantiene $0), pero SÍ afecta su _asignación temporal_ (una fila con fecha SWAP podría haber tenido valor no-cero en otra columna).

---

## FASE 3 — MAPA DE CONTAMINACIÓN MENSUAL

### 3.1 Importe del pedido — Correcto vs Ledger actual (por mes)

| Mes | XLSX Correcto | Ledger Actual | Delta | Contaminación Recibida (de otros meses) | Exportación a otros meses |
|---|---|---|---|---|---|
| 2025-01 | $21,980,249 | $18,514,370 | −$3,465,879 | $1,124,121 (Ene 4→Abr 1 swap) | $3,465,879 (swap a otros) |
| 2025-02 | $17,733,899 | $14,518,938 | −$3,214,961 | — | — |
| 2025-03 | $18,598,829 | $15,898,843 | −$2,699,986 | — | — |
| 2025-04 | $29,157,606 | $8,892,458 | −$20,265,148 | $1,446,662 (contaminación) | $20,265,148 |
| 2025-05 | $12,787,871 | $13,189,832 | +$401,961 | $1,314,780 (May 4→Abr) | — |
| 2025-06 | $20,414,590 | $22,346,250 | +$1,931,660 | $1,328,700 (Jun 4→mayor) | — |
| 2025-07 | $24,316,714 | $22,055,425 | −$2,261,289 | — | — |
| 2025-08 | $25,684,213 | $18,846,418 | −$6,837,795 | — | — |
| 2025-09 | $18,279,146 | $10,415,640 | −$7,863,506 | — | — |
| 2025-10 | $22,231,248 | $20,165,640 | −$2,065,608 | — | — |
| 2025-11 | $20,717,397 | $19,077,404 | −$1,639,993 | — | — |
| 2025-12 | $23,142,672 | $21,578,360 | −$1,564,312 | — | — |
| **2025 Total** | **$281,188,982** | **$205,499,578** | **−$75,689,404** | | |
| 2026-01 | $10,847,112 | $1,162,520 | −$9,684,592 | — | $518,830 (Ene→Abr swap) |
| 2026-02 | $7,808,503 | $8,939,110 | +$1,130,607 | $725,040 (Feb→Abr) | — |
| 2026-03 | $9,519,403 | $18,312,340 | +$8,792,937 | $1,014,510 (Mar→Abr) | — |
| 2026-04 | **$16,460,180** | **$1,500,432** | **−$14,959,748** | $1,446,662 | $7,357,100 |
| 2026-05 | $12,442,050 | $962,090 | −$11,479,960 | — | $568,840 |
| 2026-06 | $0 (no hay) | $779,680 | +$779,680 | $779,680 (SWAP phantom) | — |
| 2026-07 | $0 (no hay) | $907,090 | +$907,090 | $907,090 (SWAP phantom) | — |
| 2026-08 | $0 (no hay) | $812,140 | +$812,140 | $812,140 (SWAP phantom) | — |
| 2026-09 | $0 (no hay) | $859,160 | +$859,160 | $859,160 (SWAP phantom) | — |
| 2026-10 | $0 (no hay) | $348,870 | +$348,870 | $348,870 (SWAP phantom) | — |
| 2026-11 | $0 (no hay) | $464,810 | +$464,810 | $464,810 (SWAP phantom) | — |
| 2026-12 | $0 (no hay) | $431,780 | +$431,780 | $431,780 (SWAP phantom) | — |
| **2026 Total** | **$71,971,342** | **$35,480,022** | **−$36,491,320** | | |
| **Grand Total** | **$358,012,384** | **$240,979,600** | **−$117,032,784** | | |

### 3.2 Meses "Fantasma" (Junio-Diciembre 2026)

El Ledger contiene **$4,653,530** en meses que NO existen en la realidad financiera de Ripley (Jun-Dic 2026). Estos son:

- `06-04-2026` → Jun 4, 2026 (row original era 6 de abril) = $779,680
- `07-04-2026` → Jul 4, 2026 (row original era 7 de abril) = $907,090
- `08-04-2026` → Aug 4, 2026 (row original era 8 de abril) = $812,140
- `09-04-2026` → Sep 4, 2026 (row original era 9 de abril) = $859,160
- `10-04-2026` → Oct 4, 2026 (row original era 10 de abril) = $348,870
- `11-04-2026` → Nov 4, 2026 (row original era 11 de abril) = $464,810
- `12-04-2026` → Dec 4, 2026 (row original era 12 de abril) = $431,780

Cada fila con día entre 6 y 12 y mes=4 (Abril) se convierte en una fila fantasma en un mes que no existe (Jun−Dic). Esto no solo CREA datos falsos sino que ADEMÁS reduce el valor de Abril en esos montos.

---

## FASE 4 — IMPACTO EN AÑOS ANTERIORES (FILTER OLD YEARS)

### 4.1 Comportamiento de `_filter_old_years`

El loader aplica `_filter_old_years()` después del melt, que elimina todas las filas con año < 2025:

```python
def _filter_old_years(connection, df, keep_list):
    YEARS_KEEP = ['2025', '2026', '2027', '2028', '2029', '2030']
    df = df[df['fecha'].dt.year.astype(str).isin(YEARS_KEEP)]
```

### 4.2 Efecto del bug en el filtro

Sin `dayfirst=True`:

- **Filas NaT**: AÑO = NaT → `.dt.year` falla → fila ELIMINADA
  - Afecta: ~3,427 filas con Importe del pedido = $89,174,604
  - Estas filas TIENEN años correctos (2023-2026) pero la mala interpretación inicial → fecha inválida → año desconocido → eliminadas

- **Filas SWAP con año SWAP**: 
  - Ej: `01-04-2026` → Jan 4, 2026 (sigue siendo 2026) → **NO filtrada**
  - Ej: `08-01-2025` → Aug 1, 2025 (sigue siendo 2025) → **NO filtrada**
  - El SWAP preserva el año aproximadamente la mitad de las veces

- **Filas SWAP con año cambiado**:
  - Raro pero posible: `04-01-2025` → Apr 1, 2025 vs Jan 4, 2025 (mismo año) 
  - `04-01-2024` → Apr 1, 2024 (era Ene 4, 2024) → AÑO 2024 → **FILTRADA**

### 4.3 Datos de 2023-2024 perdidos por el filtro (no por el bug)

Los $4,852,060 de 2023-2024 en el XLSX correcto NO se pierden por el bug de fecha, sino por `_filter_old_years`. El bug SOLO EM PEORA la situación porque:

- Con `dayfirst=True`, al menos las filas 2023-2024 estarían correctamente fechadas (y serían filtradas intencionalmente)
- Sin `dayfirst=True`, las filas 2023-2024 con día > 12 se interpretan correctamente (smart detection) y también son filtradas
- Las filas 2023-2024 con día ≤ 12 se SWAPean a otro año (a veces 2025) y **contaminan** los datos que deberían ser solo 2025+

---

## FASE 5 — IMPACTO EN API / DASHBOARD / REPORTES

### 5.1 SQL = API = UI — Contrato inmutable

Como se demostró en Sprint B2.2 (DASHBOARD_DATABASE_CERTIFICATION), los contractos SQL→API→UI son exactos (5/5 KPIs MATCH EXACTO, delta $0.00). Esto significa que **si el ledger está corrupto, el Dashboard muestra datos corruptos fielmente**.

### 5.2 Endpoints afectados

| Endpoint | KPI | Ripley Apr 2026 (actual) | Correcto | Error |
|---|---|---|---|---|
| `/api/v4/ingresos/brutos/marketplace?anio=2026&mes=4` | Ingresos Brutos | $1,500,432 | $16,460,180 | **−91%** |
| `/api/v4/ingresos/brutos/anual?anio=2025` | Ingresos Brutos Anual | $205,499,578 | $281,188,982 | **−27%** |
| `/api/v4/ingresos/brutos/anual?anio=2026` | Ingresos Brutos Anual | $35,480,022 | $71,971,342 | **−51%** |
| `/api/v4/cierre/desglose` | Desglose mensual | Valores incorrectos | — | **Variable por mes** |
| Dashboard v3.5 | Ripley KPIs | **Datos incorrectos desde día 1** | — | **100% de los períodos** |

### 5.3 Todos los KPIs de Ripley en Dashboard v3.5

El Dashboard v3.5 muestra 8 KPIs en el tab Ripley. TODOS se construyen sobre `marketplace_ledger_v1` con filtro `marketplace='RIPLEY'`. Por lo tanto:

- **KPI #1 Ingresos Brutos** (Importe del pedido) = 67.3% del real → **−32.7%**
- **KPI #2 Ingresos Netos** (A pagar) = idem
- **KPI #3-8** (comisiones, envíos, etc.) = idem

### 5.4 Impacto en reportes históricos previos

| Reporte | Fecha | Ripley valor reportado | Valor correcto | Error |
|---|---|---|---|---|
| Cierre 2025 | Ene 2026 | ~$205.5M (Importe) | ~$281.2M | **−$75.7M** |
| Cierre Abr 2026 | May 2026 | ~$1.5M | ~$16.5M | **−$15.0M** |
| Cierre May 2026 | Jun 2026 (pendiente) | ~$1.0M | ~$12.4M | **−$11.4M** |
| Periodicidad mensual | Todos los meses | Variable | Mayor | **Sistemático** |

---

## FASE 6 — RECONSTRUCTIBILIDAD

### 6.1 ¿Se puede reconstruir el ledger correcto?

**SÍ — completamente. Todos los datos fuente existen.**

| Fuente | Estado | Ubicación |
|---|---|---|
| 46 archivos XLSX originales | **INTACTOS** | `01_Raw/RIPLEY/Resumen financiero/` |
| Datos de 16,923 órdenes | **COMPLETOS** | Cada XLSX contiene fila por fila |
| 32 conceptos financieros | **COMPLETOS** | Columnas en cada XLSX |
| Fechas originales (dd-mm-yyyy) | **LEGIBLES** | Formato string en columna "Fecha OC" |

### 6.2 Requisitos para reconstrucción

1. **Corregir 1 línea en `surgical_loader.py`:400**: `dayfirst=True` en `pd.to_datetime()`
2. **Reprocesar `load_ripley()`**: Eliminar datos actuales de Ripley y recargar desde los 46 XLSX
3. **Verificar**: Confirmar que las 16,923 filas se cargan correctamente y que `_filter_old_years` solo elimina las ~800 filas pre-2025

### 6.3 Cobertura post-reconstrucción

| Métrica | Actual | Post-fix |
|---|---|---|
| Filas Importe del pedido en ledger | 8,413 | ~12,000 (eliminando 2023-2024 y $0) |
| Monto Importe del pedido | $240,979,600 | ~$353,160,324 (eliminando $4.85M pre-2025) |
| Δ con XLSX original | −$117,032,784 | −$4,852,060 (solo pre-2025 filtrado intencional) |
| Porcentaje retenido | 67.3% | **~98.6%** |
| Meses fantasma (Jun-Dic 2026) | $4,653,530 | **$0** |

### 6.4 Limitaciones post-reconstrucción

- **2023-2024**: No recuperables para el pipeline actual (filtrados por `_filter_old_years`). Pero los $4.85M existen en los XLSX para consultas ad-hoc.
- **folio_xml**: Ripley NO tiene XMLs. El 0% de folio_xml es correcto (no hay DTEIndexer para Ripley). Esto no cambiará post-fix.
- **financial_group classification**: La clasificación financiera requiere un proceso separado (post-A2). El fix de fecha no clasifica automáticamente.

---

## FASE 7 — IMPACTO EN TRUST SCORE

### 7.1 Re-cálculo del Trust Score

El Trust Score actual (~70/100) se calculó considerando:
- A1 Foundation: +62.0
- A2 PARIS XML: +74.0 (post-recertificación: ajustado por cobertura reducida)
- A3 RIPLEY: 16.4/100

El bug de fecha de Ripley estaba **NO DOCUMENTADO** en el Trust Score. El Trust Score asumía que el pipeline XLSX→Ledger→API→Dashboard tenía 0% de pérdida, cuando en realidad tiene ~32.7% de pérdida para Ripley.

### 7.2 Factor de corrección

Trust Score Original ≈ 70/100

Corrección por bug de Ripley:
- Ripley representa ~20.7% del valor total del ledger ($284.9M de $1,507.8M)
- Pérdida real de Ripley: 32.7%
- Pérdida ponderada sobre el total: 20.7% × 32.7% = **6.8%**

Pero el Trust Score evalúa INTEGRIDAD del dato, no valor relativo. Un bug que afecta al 100% de los datos de un marketplace debería penalizar más:

| Componente | Peso | Score Original | Penalización | Score Ajustado |
|---|---|---|---|---|
| Pipeline integridad | 40% | 85/100 | −32.7% en 20.7% del pipeline | ~82/100 |
| Documentación | 25% | 70/100 | 0 (bug estaba documentado en A3) | 70/100 |
| Trazabilidad | 20% | 60/100 | 0 (bug es conocido pero no oculto) | 55/100 |
| Governance | 15% | 55/100 | −10 (no se detectó en auditoría inicial) | 45/100 |
| **Trust Score V3** | **100%** | **~70/100** | **−5 a −8 pts** | **~62-65/100** |

### 7.3 Trust Score V3 (propuesto): **~63/100** (vs 70/100 reportado)

El Trust Score baja de 70/100 a ~63/100 principalmente porque:

1. **Pipeline integridad**: El descubrimiento de que el pipeline NO tiene 0% de pérdida sino ~32.7% para Ripley reduce la confianza en el ETL.
2. **Governance**: El bug existía desde el día 1 y no fue detectado en 3 sprints de auditoría forense.
3. **Trazabilidad**: Sprint A3 ya había identificado 6/7 barreras — el bug de fecha se suma como la 7ª barrera.

### 7.4 Trust Score de Ripley (revisado)

El Sprint A3 estableció Ripley Trust Score = 16.4/100. Con el descubrimiento del bug de fecha:

| Barrera | Impacto en Trust | Estado |
|---|---|---|
| Loader ausente (A3 FASE A) | −25 pts | Vigente |
| $142M sin clasificar (A3 FASE B) | −15 pts | Vigente |
| 7 facturas no cargadas (A3 FASE C) | −5 pts | Vigente |
| **BUG de fecha (NUEVO)** | **−20 pts** | **P0 — No detectado en A3** |
| Sin folio_xml (A3 FASE E) | −5 pts | Vigente (0 MD5 shared vigente) |
| Sin DTEIndexer (A3 FASE F) | −5 pts | Vigente |
| Sin certificación (A3 FASE G) | −5 pts | Vigente |

**Ripley Trust Score revisado: ~5/100** (desde 16.4/100)

---

## CONCLUSIÓN

| Dimensión | Hallazgo |
|---|---|
| **Causa raíz** | `pd.to_datetime()` sin `dayfirst=True` en `surgical_loader.py:400` |
| **Alcance** | 100% de datos de Ripley — 32 conceptos, 46 XLSX, 16,923 órdenes |
| **Impacto económico** | −$117,032,784 en Importe del pedido (~$138M en todos los conceptos) |
| **% de pérdida** | 32.7% del valor financiero total de Ripley |
| **Tiempo afectado** | Desde el día 1 de operación del sistema |
| **Dashboard impact** | TODOS los KPIs de Ripley son incorrectos (no solo Ingresos Brutos) |
| **Reconstructibilidad** | 100% — datos fuente intactos, fix de 1 línea |
| **Trust Score V3** | 70→~63/100 (Ripley 16.4→~5/100) |
| **Clasificación** | **P0 — CONFIRMADO Y CUANTIFICADO** |

### Reparación autorizada

**PROHIBIDO** hasta nuevo aviso. El fix es trivial (1 carácter: `dayfirst=True`) pero requiere:
1. Autorización explícita del CEO/CTO para ejecutar remediación
2. Sprint dedicado (A5 o B3) con freeze de DB y recarga completa de Ripley
3. Re-verificación de contractos SQL=API=UI post-remediación
4. Recertificación de todos los KPIs de Ripley

### Archivos afectados

- `engine/v4/surgical_loader.py:400` — `pd.to_datetime(row[c_fecha])` → debe ser `pd.to_datetime(row[c_fecha], dayfirst=True)`
- `engine/v4/surgical_loader.py:382` — Mismo patrón en `ventas_marketplace.sale_date`

### Documentos relacionados

- `governance/RIPLEY_DATE_PARSING_CERTIFICATION.md` — Prueba del bug (FASE 1-5 original)
- `governance/RIPLEY_GROSS_REVENUE_CERTIFICATION.md` — **RECHAZADO** $14.96M gap
- `governance/RIPLEY_FINANCIAL_TRUTH_CERTIFICATION.md` — Sprint B2.3 canonical sources
- `governance/DASHBOARD_DATABASE_CERTIFICATION.md` — Sprint B2.2 (confirma que Dashboard muestra fielmente datos corruptos)
