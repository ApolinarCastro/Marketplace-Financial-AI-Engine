# PRODUCTION IMPACT SIMULATION

**Status:** READ ONLY — simulation evidence only
**Date:** 2026-06-06
**Source:** `snapshot_pre_poscobro_fix_20260605_155052/`

---

## Escenario A — Estado Actual

RN actual con todos los registros del ledger, incluyendo mecanismos apareados.

| Marketplace | RN (all-time) | Períodos |
|---|---|---|
| ML | $842,250,301 | 2025-01 a 2026-12 (futuro) |
| PARIS | $378,104,933 | 2025-01 a 2026-04 |
| RIPLEY | $206,946,843 | 2025-01 a 2026-05 |
| FALABELLA | $2,583,016 | 2026-03 a 2026-04 |
| **TOTAL** | **$1,429,885,093** | |

---

## Escenario B — RN Corregido

RN excluyendo mecanismos apareados (BPP, Poscobro Conciliado, Poscobro General) del cálculo de cierre financiero. Root events (Talla/Garantía, Arrepentimiento, Dañado) preservados en P&L.

| Marketplace | RN (all-time) | Delta vs A | Delta % |
|---|---|---|---|
| ML | **$699,024,767** | **-$143,225,534** | **-17.0%** |
| PARIS | $378,104,933 | $0 | 0.0% |
| RIPLEY | $206,946,843 | $0 | 0.0% |
| FALABELLA | $2,583,016 | $0 | 0.0% |
| **TOTAL** | **$1,286,659,559** | **-$143,225,534** | **-10.0%** |

### ML: Impacto Mensual (15 meses certificados)

| Periodo | RN Actual | RN Sin Mecanismos | Delta | Delta % |
|---|---|---|---|---|
| 2025-01 | 27,632,446 | 19,686,303 | -7,946,143 | -28.8% |
| 2025-02 | 27,087,937 | 19,826,623 | -7,261,314 | -26.8% |
| 2025-03 | 61,088,960 | 49,386,835 | -11,702,125 | -19.2% |
| 2025-04 | 66,687,557 | 55,965,772 | -10,721,785 | -16.1% |
| 2025-05 | 78,998,029 | 67,526,740 | -11,471,289 | -14.5% |
| 2025-06 | 67,662,744 | 57,216,094 | -10,446,650 | -15.4% |
| 2025-07 | 56,104,810 | 44,246,836 | -11,857,974 | -21.1% |
| 2025-08 | 42,943,149 | 34,120,433 | -8,822,716 | -20.5% |
| 2025-09 | 46,665,778 | 38,036,437 | -8,629,341 | -18.5% |
| 2025-10 | 67,381,165 | 58,451,566 | -8,929,599 | -13.3% |
| 2025-11 | 85,197,335 | 70,936,009 | -14,261,326 | -16.7% |
| 2025-12 | 78,128,274 | 66,137,025 | -11,991,249 | -15.3% |
| 2026-01 | 20,384,518 | 17,097,496 | -3,287,022 | -16.1% |
| 2026-02 | 16,027,573 | 13,796,979 | -2,230,594 | -13.9% |
| 2026-03 | 32,908,199 | 29,257,277 | -3,650,922 | -11.1% |
| **15 meses** | **774,908,457** | **641,688,425** | **-133,220,032** | **-17.2%** |

### ML: Impacto por Concepto Excluido

| Concepto | Clasificación | Rows | Monto bruto | Event Role |
|---|---|---|---|---|
| Ajuste por Compra Protegida (BPP) | MECHANISM | 3,254 | $93,999,912 | Paired mechanism |
| Ajuste Poscobro Conciliado | MECHANISM | 1,244 | $40,845,693 | Paired mechanism |
| Ajuste Poscobro General | MECHANISM | 634 | $3,108,659 | Paired mechanism |
| **Total** | | **5,132** | **$137,954,264** | |

---

## Escenario C — RN Corregido + Junio Incorporado

No es posible simular con precisión porque los archivos de Junio 2026 no están cargados en el DB snapshot. El DB contiene solo 69 rows de Junio 2026 ($1.8M) que son ajustes Poscobro, no revenue real.

**Estimación conservadora:**
- ML Junio: ~$25-35M en revenue (basado en tendencia mensual de 2026)
- PARIS May+Jun: ~$40-50M en revenue
- FALABELLA May+Jun: ~$1-2M en revenue
- RIPLEY Junio: $0 (sin archivo fuente)

**RN Total con Escenario C (estimado):** $1,470-1,500M

---

## Comparativa

| Escenario | RN Total | ML RN | PARIS RN | RIPLEY RN | FAL RN |
|---|---|---|---|---|---|
| **A** Actual | $1,429.9M | $842.3M | $378.1M | $206.9M | $2.6M |
| **B** Corregido | $1,286.7M | $699.0M | $378.1M | $206.9M | $2.6M |
| **C** Corregido+Junio | ~$1,470-1,500M | ~$725-735M | ~$418-428M | $206.9M | ~$3.6-4.6M |

---

## Verdict

| Escenario | Impacto |
|---|---|
| **A → B** | RN baja $143.2M (-10.0%) por exclusión de mecanismos ML. Es el cambio esperado. |
| **B → C** | RN sube ~$180-210M por incorporación de Junio 2026 en ML+PARIS+FALABELLA. |
| **A → C** | RN neto sube ~$40-70M — la incorporación de Junio compensa parcialmente la corrección de mecanismos. |
