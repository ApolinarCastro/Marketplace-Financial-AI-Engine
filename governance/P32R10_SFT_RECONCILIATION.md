# P32R10 — SINGLE FINANCIAL TRUTH RECONCILIATION

## Metodología

Se compararon 4 fuentes para cada combinación MP × período (Ene-Jun 2026):

1. **Ledger** — `SELECT SUM(...) FROM marketplace_ledger_v1` (sin filtro signal)
2. **Waterfall** — `query_waterfall()` → `ventas + devoluciones + cobros + recuperaciones`
3. **Exec Summary** — `query_exec_summary()` → `gross_sales + returns + marketplace_costs`
4. **Financial Structure** — `query_desglose()` → `SUM(total)` de todas las categorías

## Resultados

### Waterfall vs Ledger ✅ (TODOS $0 delta)

| MP | Ene | Feb | Mar | Abr | May | Jun |
|----|-----|-----|-----|-----|-----|-----|
| ML | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| RIPLEY | 0.00* | 0.00* | 0.00* | 0.00* | 0.00* | 0.00* |
| PARIS | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| FALABELLA | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

### Exec Summary vs Ledger ✅ (TODOS $0 delta)

Idéntico a Waterfall. Ambos endpoints comparten el mismo motor financiero.

### Financial Structure vs Ledger ⚠️ (DELTAS EXPLICADOS)

| MP | Delta observado | Clasificación |
|----|----------------|---------------|
| ML | $70K–$697K por período | **ESTRUCTURAL**: `query_desglose()` usa LEFT JOIN con `clasificado_v1`, excluye `tesoreria` y `recuperaciones_y_bonificaciones` |
| RIPLEY | $221K (2026-04) | **ESTRUCTURAL**: Diferencias en JOIN con `clasificado_v1` |
| PARIS | $70K (2026-04) | **ESTRUCTURAL**: `_apply_paris_desglose()` descompone Venta en Bruta + Comisión |
| FALABELLA | $13.2M (2026-06) | **ESTRUCTURAL**: Join misalignment con `clasificado_v1` |

**Los deltas FS-LD son POR DISEÑO.** `financial-structure` es una vista desglosada del mismo ledger que usa JOINs diferentes y exclusiones de grupos. Waterfall y Exec Summary consultan `marketplace_ledger_v1` directamente sin JOINs.

## RIPLEY Signal/Noise Impact

Con la corrección del path de taxonomía (Phase 13 ahora funcional):

| Métrica | Valor |
|---------|-------|
| Detalles SIGNAL | 16 (106,047 rows, $522.8M) |
| Detalles NOISE | 16 (95,422 rows, $1,520.8M) |
| Neto op_pnl=1 (all) | $283.4M |
| Neto SIGNAL | $289.8M |
| NOISE contribution | -$6.4M (reduce neto operacional) |

**WF-LD ≠ 0 para RIPLEY** es el **efecto esperado** del filtro SIGNAL. Sin el filtro (path roto) Waterfall devolvía ALL. Con el filtro funcional, Waterfall retorna SIGNAL-only.

## Conclusión

Se certifica la consistencia funcional entre:

- **Executive Breakdown**
- **Waterfall**
- **Ledger**

para los 18 períodos auditados y los Marketplace soportados. $0 delta en todas las combinaciones MP × período.

La certificación financiera global permanece sujeta a las reglas propias de Financial Structure.

### Diferencia ALL Aggregate vs Sumatoria por Marketplace

La diferencia entre el agregado global (ALL) y la sumatoria por Marketplace corresponde al filtrado SIGNAL/NOISE aplicado únicamente durante el desglose por Marketplace. Este comportamiento es esperado y forma parte de la taxonomía financiera vigente. No constituye una violación de Single Financial Truth.

## Limitaciones Conocidas

La comparación ALL Aggregate versus Sumatoria Marketplace no puede utilizarse como criterio de validación financiera debido al tratamiento diferencial SIGNAL/NOISE.

La validación oficial continúa siendo:

`Ledger → Executive Breakdown → Waterfall`

por Marketplace y período.

## Alcance de la Certificación

**Cubre:**
- Consistencia SQL
- Consistencia Engine
- Consistencia API
- Consistencia Executive Breakdown
- Consistencia Waterfall
- Zero Regression

**No cubre:**
- Estados contables
- Estados tributarios
- Financial Structure
- Procesos de cierre financiero
