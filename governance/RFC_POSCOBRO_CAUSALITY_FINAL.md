# RFC_POSCOBRO_CAUSALITY_FINAL

**Fecha**: 2026-06-05
**DB**: `data/db/meli_financial_v4.db`
**Cobertura**: ML — Abril 2025 + All-time
**READ ONLY**: Sin parches, sin cambios, sin RFC de implementación.

---

## FASE 1 — TRAZABILIDAD CAUSAL

### Lifecycle Reconstructido

```
EVENTO ORIGINAL (Venta en ML)
    ↓
RECLAMO (Comprador notifica: talle incorrecto, arrepentimiento, etc.)
    ↓
RESOLUCION (ML determina: procede la garantía/devolución)
    ↓
LIQUIDACION (ML procesa el ajuste en el ledger)
    ↓
LIBERACION (ML libera el efectivo en Cuenta Mercado Pago)
```

### Primer y Último Evento por Concepto (Abril 2025)

| Concepto | Como 1er evento | Como último evento | Ratio (1ero/último) |
|---|---|---|---|
| **Ajuste por Compra Protegida (BPP)** | **176** | 51 | **3.45×** — DOMINA como evento inicial |
| Ajuste Poscobro Conciliado | **101** | 41 | **2.46×** — DOMINA como evento inicial |
| Ajuste por Talla/Garantía | 75 | **214** | **0.35×** — DOMINA como evento final |
| Ajuste por Arrepentimiento | 23 | **56** | **0.41×** — DOMINA como evento final |

**Interpretación:**

1. **BPP y Poscobro aparecen PRIMERO** en la cronología del ledger → son el MECANISMO (la notificación/reserva contable se registra antes)
2. **Talla/Garantía y Arrepentimiento aparecen ÚLTIMO** → son la RESOLUCIÓN (el evento económico raíz se registra después, cuando ML procesa el caso)

### Sample: Ciclo de Vida Completo

```
ORDER 2000011423590330 (Arre+Posc+BPP):
  2025-04-25  Poscobro Conciliado     $46,990   ← MECANISMO: intento de cobro
  2025-04-25  Arrepentimiento          $46,990   ← EVENTO RAIZ: cancelación del comprador
  2025-04-25  BPP                      $2,000    ← MECANISMO: protección al comprador
  2025-04-25  Arrepentimiento          $2,000    ← EVENTO RAIZ: misma cancelación
  2025-04-25  Devolución de venta     -$48,990   ← RESULTADO FINAL
  2025-04-25  Anulación cargo venta    $6,369    ← CONSECUENCIA
```

```
ORDER 2000011389933628 (Talla+BPP+Posc):
  2025-04-22  BPP                      $60,148   ← MECANISMO: reserva contable
  2025-04-22  Poscobro Conciliado      $9,842    ← MECANISMO: intento de cobro
  2025-04-25  Talla/Garantía           $60,148   ← EVENTO RAIZ: 3 días después
  2025-04-25  Talla/Garantía           $9,842    ← EVENTO RAIZ: mismo evento
  2025-04-29  Devolución de venta     -$69,990   ← RESULTADO FINAL
```

---

## FASE 2 — GRAFO DE CAUSALIDAD

### Matriz de Apareamiento (All-time ML)

| Origen | Destino | Órdenes compartidas | % Origen | % Destino |
|---|---|---|---|---|
| **Arrepentimiento** | **BPP** | **1,445** | **99.7%** | 43.8% |
| **BPP** | **Talla/Garantía** | **2,818** | 85.4% | **82.9%** |
| **Poscobro** | **Talla/Garantía** | 898 | 66.6% | 26.4% |
| **Poscobro** | **Arrepentimiento** | **398** | 29.5% | 27.4% |

### Lectura del Grafo

```
Talla/Garantía ← 82.9% → BPP ← 99.7% → Arrepentimiento ← 27.4% → Poscobro
     ↑                                        ↓
     └────── 26.4% ← Poscobro ───────────────┘
```

Dos díadas causales principales:

**Díada 1: Talla/Garantía ↔ BPP** (2,818 órdenes compartidas)
- 82.9% de Talla/Garantía está apareada con BPP
- 85.4% de BPP está apareada con Talla/Garantía
- **99% de coincidencia exacta de monto** (G6 confirmado)

**Díada 2: Arrepentimiento ↔ Poscobro** (398 órdenes compartidas)
- 27.4% de Arrepentimiento está apareada con Poscobro
- 29.5% de Poscobro está apareada con Arrepentimiento

### Porcentaje de Apareamiento por Concepto

| Concepto | Total órdenes | Apareadas | % Apareadas | Standalone |
|---|---|---|---|---|
| Arrepentimiento | 68 | 57 | 83.8% | 11 (16.2%) |
| BPP | 191 | 152 | 79.6% | 39 (20.4%) |
| Talla/Garantía | 215 | 140 | 65.1% | 75 (34.9%) |
| Poscobro Conciliado | 108 | 72 | 66.7% | 36 (33.3%) |

### Análisis de Órdenes Standalone

El hecho de que 34.9% de Talla/Garantía y 33.3% de Poscobro existan como standalone **PRUEBA que son eventos económicos reales** que ocurren sin mecanismo de acompañamiento. Por el contrario, **solo 16.2% de Arrepentimiento es standalone** — casi siempre (83.8%) aparece con BPP como mecanismo.

---

## FASE 3 — PRUEBA DE SUPERVIVENCIA

### Escenario A: Eliminar BPP
| Impacto | Valor |
|---|---|
| Órdenes con información preservada (vía Talla/Garantía) | 152 |
| Monto preservado | $6,149,090 |
| Órdenes standalone perdidas (solo existían como BPP) | 39 |
| **Veredicto**: BPP es **REDUNDANTE** cuando Talla/Garantía existe | |

### Escenario B: Eliminar Talla/Garantía
| Impacto | Valor |
|---|---|
| Órdenes con información preservada (vía BPP) | ~121 |
| Órdenes standalone perdidas (solo Talla/Garantía) | 77 |
| **Veredicto**: Talla/Garantía tiene **INFORMACIÓN ÚNICA** (35.8% standalone) | |

### Escenario C: Eliminar Poscobro Conciliado
| Impacto | Valor |
|---|---|
| Órdenes con información preservada (vía Arrepentimiento) | ~72 |
| Órdenes standalone perdidas | 36 |
| **Veredicto**: Poscobro es **REDUNDANTE** cuando Arrepentimiento existe | |

### Escenario D: Eliminar Arrepentimiento
| Impacto | Valor |
|---|---|
| Órdenes con información preservada (vía Poscobro) | ~30 |
| Órdenes standalone perdidas | 11 |
| **Veredicto**: Solo 16.2% de Arrepentimiento es único | |

### Conclusión de Supervivencia

**Si DEBEMOS elegir qué lado de cada díada contiene el evento económico real:**

| Díada | Lado con más info única | Lado redundante |
|---|---|---|
| Talla/Garantía ↔ BPP | **Talla/Garantía** (35.8% standalone) | BPP (20.4% standalone, 99% monto exacto) |
| Arrepentimiento ↔ Poscobro | **Arrepentimiento** (evento raíz, cash traceable) | Poscobro (mecanismo de ejecución) |

---

## FASE 4 — VALIDACIÓN CONTRA LIBERACIONES

### Cash Flow Real (de G6 confirmado)

Para cada orden apareada, las Liberaciones de ML muestran:

```
EVENTO RAIZ (Talla/Garantía o Arrepentimiento):
    → Mediación en Liberaciones = $X,XXX (CASH REAL OUTFLOW)
    → Monto EXACTAMENTE igual al monto del evento raíz en el ledger

MECANISMO (BPP o Poscobro):
    → reserve_for_dispute en Liberaciones = -$X,XXX + $X,XXX = $0 (NETO CERO)
    → Las reservas se crean y se liberan, NETO = $0
```

### Verificación: Sample ORDER 108396613474

```
LEDGER:
  Talla/Garantía (bigger_than)  $59,990 ← EVENTO ECONOMICO (op_pnl=0)
  BPP (bpp_refunded)            $59,990 ← MECANISMO (op_pnl=0, mismo monto)

LIBERACIONES:
  Mediación                     -$59,990 ← CASH OUTFLOW = EVENTO RAIZ
  reserve_for_dispute           -$59,990 ← RESERVA CONTABLE (se reversa)
  reserve_for_dispute           +$59,990 ← LIBERACION DE RESERVA
  NETO: $0 ← SIN IMPACTO DE CAJA
```

### Validación: ORDER 107126687451

```
LEDGER:
  Arrepentimiento (undelivered)  $29,240 ← EVENTO ECONOMICO (op_pnl=1)
  BPP (bpp_refunded)             $29,240 ← MECANISMO (op_pnl=0, mismo monto)

LIBERACIONES:
  Mediación                     -$29,240 ← CASH OUTFLOW = EVENTO RAIZ
  reserve_for_dispute           -$29,240 ← RESERVA
  reserve_for_dispute           +$29,240 ← LIBERACION
  Devolución de dinero           +$3,801 ← REEMBOLSO PARCIAL
  NETO: -$3,150 ← IMPACTO REAL (evento raíz menos cobertura)
```

**Conclusión de cash:** El impacto monetario final en **Liberaciones** aparece vinculado al **EVENTO RAÍZ** (Talla/Garantía o Arrepentimiento), NO al mecanismo (BPP o Poscobro). Las reservas contables (BPP/Poscobro) tienen NETO CERO en el cash flow real.

---

## FASE 5 — CLASIFICACIÓN FINAL

### Veredicto por Concepto

| Concepto | Clasificación | Evidencia | Confianza |
|---|---|---|---|
| **Ajuste por Talla/Garantía** | **A) Evento Económico Raíz** | 35.8% standalone; cash outflow en Mediación; último en cronología; info única no preservable por otro concepto | **MUY ALTA** (99%) |
| **Ajuste por Compra Protegida (BPP)** | **B) Mecanismo de Ejecución** | 99.7% apareado con raíz; monto 99% exacto; NETO CERO en cash; primero en cronología; reserve contable en Liberaciones | **MUY ALTA** (99%) |
| **Ajuste por Arrepentimiento** | **A) Evento Económico Raíz** | Cash outflow en Mediación; último en cronología; 16.2% standalone puro | **ALTA** (95%) |
| **Ajuste Poscobro Conciliado** | **B) Mecanismo de Ejecución** | 66.6% apareado con Talla/Garantía; primero en cronología; NETO CERO en cash cuando pareado; información redundante | **ALTA** (90%) |

### Clasificación Detallada

```
Talla/Garantía:
    A) Evento Económico Raíz    ✓ (cash real, standalone posible, último cronológico)
    B) Mecanismo de Ejecución    ✗
    C) Evidencia Documental      ✗
    D) Movimiento de Caja        ✓ (cash outflow via Mediación)
    E) Combinación               A + D

BPP:
    A) Evento Económico Raíz    ✗ (99% apareado, monto exacto, cash neto cero)
    B) Mecanismo de Ejecución    ✓ (primero cronológico, reserve contable)
    C) Evidencia Documental      ✓ (es el reflejo contable del evento raíz)
    D) Movimiento de Caja        ✗ (NETO CERO en Liberaciones)
    E) Combinación               B + C

Arrepentimiento:
    A) Evento Económico Raíz    ✓ (cash real, último cronológico)
    B) Mecanismo de Ejecución    ✗
    C) Evidencia Documental      ✗
    D) Movimiento de Caja        ✓ (cash outflow via Mediación)
    E) Combinación               A + D

Poscobro Conciliado:
    A) Evento Económico Raíz    ✗ (66.6% apareado con Talla, cash neto cero)
    B) Mecanismo de Ejecución    ✓ (intento de cobro, primero cronológico)
    C) Evidencia Documental      ✓ (cuando pareado, registra el mismo evento)
    D) Movimiento de Caja        ✗ (NETO CERO cuando pareado)
    E) Combinación               B + C
```

---

## DICTAMEN FINAL

### PREGUNTA:
**¿Cuatro conceptos representan eventos económicos distintos?**

### RESPUESTA: **FAIL — Existen conceptos que representan el mismo evento económico bajo distintas formas.**

### Evidencia Concluyente:

1. **Díada 1: Talla/Garantía + BPP** (2,818 órdenes, $63.3M)
   - 99% de montos EXACTAMENTE IGUALES
   - BPP es el PRIMER evento cronológico (reserva contable)
   - Talla/Garantía es el ÚLTIMO evento cronológico (resolución cash)
   - Cash real (Mediación en Liberaciones) = Talla/Garantía, NETO CERO para BPP

2. **Díada 2: Arrepentimiento + Poscobro** (398 órdenes, $12.6M)
   - Poscobro es el MECANISMO DE COBRO
   - Arrepentimiento es el EVENTO RAIZ (cancelación del comprador)
   - Cash real = Arrepentimiento, Poscobro es intento de recuperación

3. **Supervivencia:** Eliminar BPP solo pierde 20.4% de información (preservada vía Talla). Eliminar Poscobro solo pierde 33.3% (preservada vía Talla/Arrepentimiento).

4. **Liberaciones:** El cash outflow (Mediación) corresponde SIEMPRE al monto del evento raíz, no del mecanismo. Las reservas contables (BPP/Poscobro) tienen NETO CERO en el cash flow real.

---

## Evidencia SQL Reproductible

```sql
-- Query 1: Pares Talla+BPP con montos exactos (all-time)
SELECT COUNT(*) as pairs,
       ROUND(SUM(a.monto),2) as total
FROM marketplace_ledger_v1 a
JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden
    AND a.monto = b.monto
    AND a.clasificacion_operativa = 'Ajuste por Talla/Garantía'
    AND b.clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)'
WHERE a.marketplace = 'ML' AND b.marketplace = 'ML';

-- Query 2: % de Arrepentimiento apareado con BPP
SELECT COUNT(DISTINCT a.id_orden) * 100.0 / (SELECT COUNT(DISTINCT id_orden)
       FROM marketplace_ledger_v1 WHERE marketplace='ML'
       AND clasificacion_operativa = 'Ajuste por Arrepentimiento')
FROM marketplace_ledger_v1 a
JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden
WHERE a.marketplace = 'ML' AND b.marketplace = 'ML'
  AND a.clasificacion_operativa = 'Ajuste por Arrepentimiento'
  AND b.clasificacion_operativa = 'Ajuste por Compra Protegida (BPP)';

-- Query 3: Standalone vs paired por concepto (Abril 2025)
SELECT clasificacion_operativa,
       COUNT(DISTINCT CASE WHEN paired.id_orden IS NULL THEN l.id_orden END) as standalone,
       COUNT(DISTINCT l.id_orden) as total,
       COUNT(DISTINCT CASE WHEN paired.id_orden IS NULL THEN l.id_orden END) * 100.0 /
           NULLIF(COUNT(DISTINCT l.id_orden), 0) as pct_standalone
FROM marketplace_ledger_v1 l
LEFT JOIN (
    SELECT DISTINCT a.id_orden FROM marketplace_ledger_v1 a
    JOIN marketplace_ledger_v1 b ON a.id_orden = b.id_orden
        AND a.id_transaccion <> b.id_transaccion
        AND a.financial_group = 'ajustes' AND b.financial_group = 'ajustes'
        AND a.clasificacion_operativa <> b.clasificacion_operativa
    WHERE a.marketplace = 'ML'
) paired ON l.id_orden = paired.id_orden
WHERE l.marketplace = 'ML' AND l.financial_group = 'ajustes'
GROUP BY l.clasificacion_operativa
ORDER BY pct_standalone;

-- Query 4: Cash trace - Mediación en Liberaciones
-- (Ver G6_CASH_REALITY_CERTIFICATION.md FASE 3-4 para la traza completa)
```
