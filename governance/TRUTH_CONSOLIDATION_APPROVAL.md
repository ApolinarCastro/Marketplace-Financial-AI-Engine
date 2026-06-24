# Truth Consolidation Approval

## Approval Record

| Field | Value |
|-------|-------|
| **Fecha** | 2026-06-05 |
| **RFC Origen** | `governance/RFC_FINANCIAL_TRUTH_CONSOLIDATION.md` |
| **Estado** | APPROVED |
| **Tipo** | Governance — Source of Truth |

---

## Decisiones Aprobadas

### D1 — Source of Truth
**Marketplace Financial** es la única fuente oficial corporativa de verdad financiera.

Base técnica:
- DB DuckDB `data/db/meli_financial_v4.db` (125 MB, SHA256 e1e341ef)
- API v4 (`api/api.py`)
- Dashboard UX1.2/UX1.1 (`/app`, `/exec`)
- 14/14 regression tests PASS en cada sprint
- Certificaciones: B2.2 (Dashboard vs DB, $0 delta), G5.6 (Revenue Engine, 4 PASS)

### D2 — Legacy Status
**Reporte_Gerencial_Marketplaces** pasa a estado LEGACY.

Preservado como referencia histórica. No se modifica. No es fuente autoritativa para KPIs.

### D3 — KPI Definitions
| KPI | Source Oficial | Fórmula |
|-----|---------------|---------|
| **Ventas** | `marketplace_ledger_v1.financial_group='ingresos'` | `SUM(monto) WHERE financial_group='ingresos' AND include_in_operational_pnl=1` |
| **Devoluciones** | `marketplace_ledger_v1.financial_group='devoluciones'` | `SUM(monto) WHERE financial_group='devoluciones'` |
| **Disponible** | `marketplace_cierre_financiero_v1.resultado_neto` | `total_ingresos + total_costos_operacionales + total_costos_comerciales + total_ajustes` |
| **Cobros** | Computado desde cierre + ledger | `Ventas + Devoluciones - Disponible` (por componente económico) |

---

## Impacto

| Área | Antes | Después |
|------|-------|---------|
| **Ventas** | Dos definiciones (Reporte GMV vs DB fee income) | Una definición: ledger.ingresos |
| **Devoluciones** | Dos fuentes (Poscobro vs ledger) | Una fuente: ledger.devoluciones |
| **Disponible** | Reporte ($9.2M ML Feb) vs DB ($16.0M ML Feb) | Una fuente: cierre.resultado_neto |
| **Reporte_Gerencial** | Referenciado como fuente | LEGACY — referencia histórica |
| **Looker Studio** | Visualización externa | No es fuente oficial |

---

## Alcance

- **Incluye**: Todos los marketplaces (ML, RIPLEY, PARIS, FALABELLA), todos los períodos
- **Excluye**: Modificaciones a código, DB, APIs, cálculos, clasificación
- **Preserva**: Reporte_Gerencial archivos, backups, guías Power Query (LEGACY)

---

## Estado Final

```
Source of Truth:    Marketplace Financial (DB + API + Dashboard)
Legacy System:      Reporte_Gerencial_Marketplaces (LEGACY, no modificar)
KPIs Definidos:     4/4 (Ventas, Devoluciones, Cobros, Disponible)
Conciliación:       Trazable — todo delta explicado por componentes estructurales
Ajustes Pendientes: Documentación governance actualizada (este archivo + DECISIONS_LOG.md + CLAUDE.md)
```
