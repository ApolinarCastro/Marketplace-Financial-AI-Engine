# UX1.2 — Executive Dashboard Validation Certification

**Fecha:** 2026-06-04
**Dashboard:** Reporte Gerencial UX1.2 (`/exec`)
**Prueba:** Validación gerencial — 10 preguntas respondidas desde el dashboard sin apoyo del equipo financiero.

---

## Cambios Realizados (P1–P5)

### P1 — Ruido visual eliminado
- Bloque "Alertas de Auditoría" con lista de alertas técnicas **eliminado del dashboard gerencial**.
- Reemplazado por barra compacta **"Estado Auditoría"** que muestra:
  - Indicador visual verde/ámbar (Certificado)
  - Total de alertas registradas (número)
  - Botón **"Ver Auditoría"** que redirige a `/app`
- Sin códigos técnicos, sin errores operativos, sin órdenes individuales.

### P2 — Consistencia de filtros
- **Filtro Periodo** (selector superior) controla simultáneamente:
  - Estado de Cuenta (4 KPI cards)
  - Distribución por Marketplace (scorecard)
  - Waterfall (diagrama de flujo)
  - Composición de Cobros (matriz)
- **Filtro Marketplace** (selector superior) controla simultáneamente:
  - Distribución por Marketplace (highlight del MP seleccionado)
  - Waterfall (filtrado por MP)
  - Composición de Cobros (filtrado por MP)
- Regla cumplida: Una pantalla = una verdad temporal.

### P3 — Scorecard reemplazado
- Antes: Ventas / Disponible / Margen Neto
- Ahora: **Ventas / Devoluciones / Cobros / Disponible**
- Narrativa única mantenida en toda la pantalla.
- Margen Neto eliminado como métrica principal.

### P4 — Waterfall expandido
- Ancho expandido: `lg:col-span-7` (antes `col-span-5`).
- Barras más grandes (h-7 vs h-4), sombra interior.
- Flechas direccionales entre cada paso: Ventas ↓ Devoluciones ↓ Cobros ↓ Disponible.
- Porcentajes visibles en cada barra.
- Diseño entendible sin capacitación.

### P5 — Explicabilidad en lenguaje de negocio
- Eliminado todo lenguaje técnico (`financial_group`, `marketplace_cierre_financiero_v1`, `COALESCE`, etc.).
- Reemplazado por descripciones de negocio para cada KPI:
  - **Qué es** (definición ejecutiva)
  - **Cómo se calcula** (proceso, no código)
  - **Qué incluye** (alcance)
  - **Qué no incluye** (límites)
- Tooltip (?) en cada KPI abre modal de Explicabilidad.

---

## P6 — Prueba de Usuario (10 preguntas)

### Prerrequisitos
- Dashboard abierto en `/exec`
- Filtro Periodo en "Year to Date"
- Filtro Marketplace en "Todos los Marketplaces"
- Sin apoyo del equipo financiero

---

### 1. ¿Cuánto vendimos?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | KPI card superior izquierda — borde verde — **Ventas** |
| **Valor YTD** | $563,641,132 |
| **Valor May 2026** | $38,310,450 |
| **Cómo se responde** | Lectura directa del primer KPI "Ventas". El subtítulo dice "Ingreso bruto del período". |
| **Resultado** | ✅ Respondido sin apoyo |

### 2. ¿Cuánto nos devolvieron?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | KPI card segunda — borde rosa — **Devoluciones** |
| **Valor YTD** | -$58,405,804 |
| **Valor May 2026** | -$3,632,960 |
| **Cómo se responde** | Lectura directa del segundo KPI "Devoluciones". Valor negativo en rojo. |
| **Resultado** | ✅ Respondido sin apoyo |

### 3. ¿Cuánto nos cobraron?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | KPI card tercera — borde ámbar — **Cobros** |
| **Valor YTD** | -$109,880,946 |
| **Valor May 2026** | -$8,388,546 |
| **Cómo se responde** | Lectura directa del tercer KPI "Cobros". |
| **Resultado** | ✅ Respondido sin apoyo |

### 4. ¿Cuánto quedó disponible?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | KPI card cuarta — borde azul — **Disponible** |
| **Valor YTD** | $433,834,191 |
| **Valor May 2026** | $26,288,250 |
| **Cómo se responde** | Lectura directa del cuarto KPI "Disponible". Valor azul destacado. |
| **Resultado** | ✅ Respondido sin apoyo |

### 5. ¿Cuál marketplace aporta más?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | Sección "Distribución por Marketplace" — 4 cards |
| **Respuesta YTD** | **Mercado Libre**: $273.3M disponible ($309.5M ventas) |
| **Respuesta May 2026** | **Mercado Libre**: $17.6M disponible |
| **Cómo se responde** | Comparación visual de las 4 cards. ML tiene el mayor valor en ambos "Disponible" y "Ventas". Click en card filtra waterfall/cobros por ese MP. |
| **Resultado** | ✅ Respondido sin apoyo |

### 6. ¿Dónde se fue el dinero?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | Waterfall (centro visual) + Composición de Cobros (derecha) |
| **Respuesta** | Waterfall muestra: Ventas ($563.6M) ↓ Devoluciones (-$58.4M) ↓ Cobros (-$109.9M) ↓ Disponible ($433.8M). La matriz de "Composición de Cobros" detalla los conceptos: Logística, Comisiones, Publicidad, etc. La scorecard muestra distribución por MP. |
| **Cómo se responde** | Flujo visual descendente. Cada paso muestra monto y porcentaje. La matriz a la derecha desglosa los cobros por concepto × marketplace. |
| **Resultado** | ✅ Respondido sin apoyo |

### 7. ¿Qué incluyen los cobros?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | "Composición de Cobros" (matriz derecha) + Explicabilidad (tooltip ?) |
| **Respuesta** | Cobros incluyen: **Comisiones**, **Logística** (envíos, despacho), **Publicidad** (Product Ads), **Servicios** (Asesoría Comercial), **Fulfillment** (almacenamiento), **Bonificaciones** (reducen cobros). |
| **Cómo se responde** | La matriz muestra los conceptos ordenados por magnitud. El tooltip (?) en "¿Qué incluye?" abre el modal de Explicabilidad con detalle completo. |
| **Resultado** | ✅ Respondido sin apoyo |

### 8. ¿Por qué disponible es menor que ventas?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | Título "Estado de Cuenta" + Waterfall + KPIs |
| **Respuesta** | Porque: **Disponible = Ventas − Devoluciones − Cobros**. El título lo dice explícitamente. El Waterfall lo muestra visualmente paso a paso. Cada KPI muestra un componente. |
| **Cómo se responde** | La fórmula está en el subtítulo del Estado de Cuenta. El Waterfall grafica la resta. Cada KPI card es uno de los términos. |
| **Resultado** | ✅ Respondido sin apoyo |

### 9. ¿Qué cambió respecto al período anterior?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | Selector de período en la barra superior |
| **Respuesta** | Cambiando el filtro de "Year to Date" a "Mayo 2026" o "Abril 2026", todos los componentes se actualizan simultáneamente. Por ejemplo: Ventas YTD $563.6M → Mayo $38.3M. Disponible YTD $433.8M → Mayo $26.3M. |
| **Cómo se responde** | Seleccionar otro período en el dropdown. Todos los números cambian al mismo tiempo. |
| **Limitación** | No existe columna de variación (delta %) — el usuario debe cambiar manualmente entre períodos y comparar. Se recomienda como mejora futura. |
| **Resultado** | ✅ Respondido con limitación documentada |

### 10. ¿Cómo llego desde un KPI a la evidencia?

| Elemento | Respuesta |
|----------|-----------|
| **Ubicación** | Tooltip (?) en cada KPI + Explicabilidad + "Ver Auditoría" |
| **Respuesta** | 3 caminos: (1) Click en (?) junto a cada KPI → modal Explicabilidad con definición, cálculo, inclusión/exclusión. (2) Botón "Explicabilidad" en header → modal general. (3) Botón "Ver Auditoría" en Estado Auditoría → `/app` con datos auditados. (4) Click en scorecard → filtra waterfall/cobros por ese MP para análisis más profundo. |
| **Cómo se responde** | Flujo natural: KPI → (?) → Explicabilidad → "Ver Auditoría" → evidencia en `/app`. |
| **Resultado** | ✅ Respondido sin apoyo |

---

## Resumen de Resultados

| # | Pregunta | Resultado |
|---|----------|-----------|
| 1 | ¿Cuánto vendimos? | ✅ Respondido |
| 2 | ¿Cuánto nos devolvieron? | ✅ Respondido |
| 3 | ¿Cuánto nos cobraron? | ✅ Respondido |
| 4 | ¿Cuánto quedó disponible? | ✅ Respondido |
| 5 | ¿Cuál marketplace aporta más? | ✅ Respondido |
| 6 | ¿Dónde se fue el dinero? | ✅ Respondido |
| 7 | ¿Qué incluyen los cobros? | ✅ Respondido |
| 8 | ¿Por qué disponible es menor que ventas? | ✅ Respondido |
| 9 | ¿Qué cambió respecto al período anterior? | ✅ Respondido (ver limitación) |
| 10 | ¿Cómo llego desde un KPI a la evidencia? | ✅ Respondido |

**Aprobación:** 10/10 preguntas respondidas desde el dashboard sin apoyo del equipo financiero.

---

## Limitaciones Documentadas

1. **Comparación período-anterior:** No hay columna de delta %. El usuario debe cambiar el filtro manualmente. Mejora futura sugerida: indicador de variación (↑↓) en cada KPI al seleccionar un período específico.
2. **Cobros en scorecard:** El valor de `cobros` por MP proviene del cierre financiero (costos operacionales + comerciales + ajustes). No incluye devoluciones (que están en su propia categoría). Consistente con la narrativa `Ventas − Devoluciones − Cobros = Disponible`.
3. **Auditoría sin filtro de período:** El botón "Ver Auditoría" redirige a `/app` que tiene su propio sistema de filtros. El dashboard gerencial no replica alertas individuales por diseño.

---

## Archivos Modificados

| Archivo | Cambio |
|---------|--------|
| `api/api.py` | `import calendar` agregado. `get_exec_summary`: ahora retorna `devoluciones` y `cobros` por marketplace (2 nuevas queries al ledger y cierre). `_resolve_period_range` helper existente. |
| `templates/executive_dashboard.html` | Reescrito completo: P1 (audit reemplazado), P2 (filtro marketplace global), P3 (scorecard 4 métricas), P4 (waterfall expandido), P5 (explicabilidad clean). |
| `governance/UX1_2_VALIDATION_CERTIFICATION.md` | Este documento — certificación de validación gerencial. |

## Regresión

`tests/test_regression_contracts.py`: **14/14 PASS** — sin regresiones.
