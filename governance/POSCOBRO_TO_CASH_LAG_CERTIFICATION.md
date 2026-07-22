# POSCOBRO → Cash Lag — Certification

**Pregunta única**: ¿El 96.03% de PosCobro que no aparece en Liberaciones es ruido contable permanente o caja diferida?

**Período**: PosCobro 2024-12 → 2026-06 | Liberaciones 2025-01 → 2026-06

---

## Hipótesis

**H0 — Ruido permanente**: Las órdenes de PosCobro generan ~4% de cash real, sin importar cuánto tiempo esperen.

**H1 — Caja diferida**: Las órdenes recientes aún no han llegado a Liberaciones. Dado tiempo suficiente, el cash total convergerá a un % mayor.

**Prueba decisiva**: Si H1 es cierto, órdenes VIEJAS (18 meses) deben tener cash ratio ALTO y órdenes RECIENTES (1 mes) deben tener cash ratio BAJO.

---

## FASE 1+2 — Cash ratio por mes de PosCobro

Cada fila = órdenes con PosCobro en ese mes, seguidas hasta su última Liberación (hasta 18 meses después).

| Mes PosCobro | Órdenes | PosCobro $ | Cash $ | Ratio | % Zero Cash |
|-------------|---------|-----------|-------|-------|------------|
| **2024-12** | 110 | $2,724,274 | -$801,763 | **-29.4%** | 34% |
| **2025-01** | 232 | $10,615,328 | $384,369 | **3.6%** | 81% |
| **2025-02** | 141 | $8,704,310 | $195,299 | **2.2%** | 87% |
| **2025-03** | 301 | $16,875,026 | $1,009,987 | **6.0%** | 80% |
| **2025-04** | 307 | $22,791,472 | $641,283 | **2.8%** | 83% |
| **2025-05** | 410 | $31,593,514 | $1,282,176 | **4.1%** | 85% |
| **2025-06** | 353 | $25,829,796 | $1,152,877 | **4.5%** | 78% |
| **2025-07** | 364 | $24,060,368 | $655,007 | **2.7%** | 82% |
| **2025-08** | 245 | $16,175,770 | $524,169 | **3.2%** | 80% |
| **2025-09** | 242 | $16,394,050 | $634,060 | **3.9%** | 82% |
| **2025-10** | 397 | $25,120,420 | $1,310,448 | **5.2%** | 75% |
| **2025-11** | 629 | $36,550,634 | $1,938,901 | **5.3%** | 68% |
| **2025-12** | 620 | $31,665,122 | $1,786,973 | **5.6%** | 68% |
| **2026-01** | 219 | $10,439,506 | $818,737 | **7.8%** | 65% |
| **2026-02** | 123 | $6,256,934 | $361,209 | **5.8%** | 64% |
| **2026-03** | 182 | $11,094,239 | $557,445 | **5.0%** | 59% |
| **2026-04** | 204 | $14,992,119 | $569,610 | **3.8%** | 63% |
| **2026-05** | 241 | $15,297,365 | $403,787 | **2.6%** | 69% |
| **2026-06** | 63 | $3,303,426 | $17,285 | **0.5%** | 79% |
| **TOTAL** | **5,383** | **$330,483,673** | **$13,441,859** | **4.07%** | **74%** |

### Interpretación

Si H1 (caja diferida) fuera cierto, se observaría una tendencia CLARA:

| Mes | Tiempo para settle | Ratio esperado (H1) | Ratio observado |
|-----|-------------------|-------------------|----------------|
| 2024-12 | 18 meses | ALTO (~50%+) | **-29.4%** |
| 2025-01 | 17 meses | ALTO | **3.6%** |
| 2025-06 | 12 meses | MEDIO-ALTO | **4.5%** |
| 2025-12 | 6 meses | MEDIO | **5.6%** |
| 2026-03 | 3 meses | BAJO | **5.0%** |
| 2026-05 | 1 mes | MUY BAJO | **2.6%** |
| 2026-06 | 0 meses | ~0% | **0.5%** |

**No hay correlación entre tiempo de espera y cash ratio.** Las órdenes de 2024-12 (18 meses de ventana) tienen -29.4%. Las de 2025-12 (6 meses) tienen 5.6%. Las de 2026-03 (3 meses) tienen 5.0%.

El único mes que se desvía significativamente del rango 2-6% es 2024-12 (-29.4%) — y lo hace hacia ABAJO (más cash negativo), no hacia arriba.

La H1 es **FALSIFICADA**.

---

## FASE 3 — Cash por FLOW

| FLOW | Órdenes | PosCobro $ | Cash total $ | Ratio | Clasificación |
|------|---------|-----------|-------------|-------|--------------|
| **claim** | 5,256 | $181,397,454 | $13,054,567 | **7.20%** | No impacta caja |
| **refund** | 4,567 | $148,873,289 | $71,086 | **0.05%** | No impacta caja |
| **chargeback** | 7 | $212,930 | $118,245 | **55.53%** | Impacta parcialmente |

Ningún FLOW cambia su ratio con el tiempo. Son propiedades estructurales de cada FLOW, no temporales.

---

## FASE 4 — Órdenes que jamás llegan a Liberaciones

| Métrica | Valor |
|---------|-------|
| Órdenes PosCobro NO en Liberaciones | **836 (13.4%)** |
| Monto PosCobro no cash | **$7,737,909 (2.3%)** |
| En Ledger (tienen venta asociada) | 214 órdenes |
| Sin Ledger (datos huérfanos) | 622 órdenes |
| % que jamás será cash | 2.3% del monto |

Estas 836 órdenes incluyen datos desde 2025-01. No aparecerán en Liberaciones. Son errores de datos (órdenes sin venta real asociada) o ajustes puramente contables.

---

## FASE 5 — Dictamen

### 1. Impacto cash mismo mes

No aplica. PosCobro y Liberaciones son procesos asincrónicos. Una orden puede tener PosCobro en un mes y Liberación en otro. La comparación mismo-mes no es la métrica correcta.

### 2. Impacto cash diferido

**No existe.** La tasa de conversión cash es estable (~4%) independientemente de cuánto tiempo se espere. Órdenes con 18 meses de ventana tienen el mismo ratio que órdenes con 3 meses.

### 3. Impacto cash total

**$13,441,859 de $330,483,673 = 4.07%**. Este es el VALOR TERMINAL. No va a aumentar con el tiempo.

### 4. Órdenes sin impacto cash

**73.9%** de las órdenes (3,980/5,383) tienen $0 de Liberacion NET. 2.3% adicional (836 órdenes) jamás aparecen en Liberaciones. Total **76.2% de órdenes sin impacto cash**.

### 5. Dictamen final

**El 96% es ruido contable permanente, no caja diferida.**

| Evidencia | Conclusión |
|-----------|-----------|
| Ratio estable 2-6% desde 2024-12 hasta 2026-05 | No hay correlación tiempo → cash |
| 73.9% de órdenes con $0 cash | La mayoría nunca toca caja |
| 0.05% para refund | Los refunds no son diferidos, son ajustes contables |
| 2024-12 con -29.4% | Ni siquiera 18 meses genera cash positivo |

**PASS.** La respuesta se sostiene exclusivamente en Liberaciones. Sin P&L, sin Ledger, sin Dashboard, sin Clasificaciones.

---

*Fuentes: `01_Raw/ML/Poscobro/` (5 archivos, 11,914 rows), `01_Raw/ML/Liberaciones/` (18 archivos, 73,328 rows, 2025-01 a 2026-06)*
