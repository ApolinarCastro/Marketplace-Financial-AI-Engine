# RFC — Financial Truth Consolidation

## Context

Hay dos sistemas financieros activos con KPIs de nombre idéntico pero significado y cifras distintas:

| KPI | Reporte Gerencial (Legacy) | Marketplace Financial (Certified) |
|-----|---------------------------|-----------------------------------|
| **Ventas** | $16,431,010 (fee income, matches DB) | $16,431,010 (ledger.ingresos) |
| **Devoluciones** | $2,812,963 (Poscobro source, 122 rows) | $871,130 (ledger.devoluciones, 37 rows) |
| **Cobros** | Implícito en Venta Neta | $467,692.50 (ventas + devoluciones - neto) |
| **Disponible** | Venta Neta Real = $9,190,587.50 | Neto = $16,027,572.50 |
| **Ajustes** | $0 — no existen en modelo | $5,158,442 — incluidos en P&L |

Ambos leen los mismos archivos Excel fuente. La divergencia está en el pipeline de transformación.

---

## Propuesta: Marketplace Financial como Source of Truth

### Decisión 1: Source of Truth

**Marketplace Financial** (DB DuckDB `data/db/meli_financial_v4.db` + API v4 + UX1.2/UX1.1) es la fuente oficial corporativa.

Fundamento:
- Certificado en Sprint B2.2 (Dashboard vs Database: 5/5 KPIs MATCH, $0 delta)
- Certificado en Sprint G5.6 (Revenue Engine Decomposition: 4 certificados PASS)
- Ha pasado 14/14 regression tests en cada sprint (A1, B1, UX1.0, UX1.1)
- Trazabilidad RAW → ETL → Ledger → API → Dashboard documentada y auditada

### Decisión 2: Legacy Status

**Reporte_Gerencial_Marketplaces** pasa a estado **LEGACY**. Se preserva como referencia histórica pero no se considera source of truth corporativa.

Implicaciones:
- El archivo `Reporte_Marketplaces/Reporte Gerencial 360 Marketplaces.xlsx` y su backup no se modifican
- Las guías Power Query en `Reporte_Marketplaces/Backup/` se archivan como documentación histórica
- El directorio `Reporte_Marketplaces/Mercado Libre/{ML_Facturacion, ML_Poscobro}/` y equivalentes (Ripley, Paris) se preservan como raw source input

---

## Definiciones Únicas Por KPI

Tras la consolidación, cada KPI tiene UNA definición corporativa:

### Ventas

| Aspecto | Definición |
|---------|-----------|
| **Concepto** | Ingresos por comisiones/fees cobrados por marketplace a Eccsa |
| **Source** | `marketplace_ledger_v1.financial_group = 'ingresos'` |
| **Excluye** | GMV (valor de venta al consumidor), devoluciones, ajustes |
| **Fórmula** | `SUM(monto) WHERE financial_group='ingresos' AND include_in_operational_pnl=1` |
| **En Dashboard** | KPI "Ventas" en UX1.1 (Reporte Gerencial dashboard /exec) |

### Devoluciones

| Aspecto | Definición |
|---------|-----------|
| **Concepto** | Devoluciones de productos clasificadas vía pipeline ETL |
| **Source** | `marketplace_ledger_v1.financial_group = 'devoluciones'` |
| **Excluye** | Chargebacks de Poscobro no clasificados como devolución pura |
| **Fórmula** | `SUM(monto) WHERE financial_group='devoluciones'` |
| **En Dashboard** | KPI "Devoluciones" en UX1.1 waterfall |

### Cobros

| Aspecto | Definición |
|---------|-----------|
| **Concepto** | Neto de cobros por servicios (logística, publicidad, comisiones, etc.) |
| **Source** | Computado desde cierre + ledger: `Ventas + Devoluciones - Neto` |
| **Fórmula** | `cierre.total_ingresos + ledger.devoluciones - cierre.resultado_neto` |
| **En Dashboard** | KPI "Cobros" en UX1.1 (Display positivo por convención) |

### Disponible

| Aspecto | Definición |
|---------|-----------|
| **Concepto** | Resultado neto del período = Ingresos - Costos + Ajustes (incl. recoveries) |
| **Source** | `marketplace_cierre_financiero_v1.resultado_neto` |
| **Fórmula** | `total_ingresos + total_costos_operacionales + total_costos_comerciales + total_ajustes` |
| **En Dashboard** | KPI "Disponible" en UX1.1 (mayor, con estrella ★ para líder) |

---

## Conciliación Trazable Reporte Gerencial → Marketplace Financial

Para cada período, toda diferencia debe explicarse mediante:

```
Marketplace_Financial_value = Reporte_Gerencial_value + Σ(Concept_Delta)
```

Donde Concept_Delta se origina de:

| Delta Type | Origen | Ejemplo ML Feb 2026 |
|-----------|--------|---------------------|
| Ajustes no capturados | BPP, Arrepentimiento, Talla/Garantía, etc. | +$5,158,442 |
| Devoluciones Poscobro vs Ledger | Cobertura Poscobro más amplia que `devoluciones` clasificadas | +$1,941,833 |
| Comisión fuente distinta | Columna origen diferente en Excel | +$235,400 |
| Mantenimiento Mi Página | Clasificado como otro concepto en Reporte | +$16,990 |

---

## Próximos Pasos

1. [ ] Aprobar RFC — confirmar Marketplace Financial como Source of Truth
2. [ ] Documentar en CLAUDE.md: "Reporte_Gerencial = LEGACY, no source of truth"
3. [ ] Crear governance/TRUTH_CONSOLIDATION_RFC.md con firma de aprobación
4. [ ] Remover referencias a Reporte_Gerencial como fuente autoritativa en documentación existente
5. [ ] Opcional: generar dashboard de conciliación automática (Reporte vs DB) para transición
