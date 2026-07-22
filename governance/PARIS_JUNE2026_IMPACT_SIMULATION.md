# PARIS June 2026 — Impact Simulation

**Fecha:** 2026-06-11
**Auditoría:** FASE 6 de 7 — PARIS June 2026 Data Completeness Certification

---

## 1. Estado Actual (Ledger, Jun 1-5)

| Concepto | Monto |
|----------|-------|
| Ingresos | $19,018,872 |
| Devoluciones | -$526,856 |
| Costos Operacionales | -$833,870 |
| **Resultado Neto** | **$17,658,146** |

## 2. Estado Completo Proyectado (RAW Completo, Jun 1-8)

Incluyendo días 6-8 cargados (sin diferencia gross/net):

| Concepto | Actual | Días 6-8 (RAW Net) | Completo |
|----------|--------|-------------------|----------|
| Ingresos | $19,018,872 | +$84,960 | $19,103,832 |
| Devoluciones | -$526,856 | -$165,870 | -$692,726 |
| Costos Operacionales | -$833,870 | +$9,120 | -$824,750 |
| **Resultado Neto** | **$17,658,146** | **-$71,790** | **$17,586,356** |

### Efecto de días 6-8 cargados

- **RN reduce en -$71,790** (días 6-8 tienen más devoluciones que ventas netas)
- Impacto material: **0.4%** del RN actual

## 3. Estado Full-Month Estimado (30 días)

Usando promedio diario de días 1-8 (excluyendo días 6-8 que tienen rezago):

| Método | Estimado Full Month |
|--------|-------------------|
| Promedio DS diario (días 1-5) × 30 | $18.8M net/mes |
| Promedio FF diario (días 1-5) × 30 | $1.1M net/mes |
| **Total estimado** | **~$19.9M net/mes** |

### Comparación Mensual (Ledger)

| Mes | Ingresos | Devoluciones | Costos | Neto |
|-----|----------|-------------|--------|------|
| Abr 2026 | ~$17.2M | ~-$8.1M | ~-$1.3M | ~$7.8M |
| May 2026 | $17.0M | -$7.7M | -$1.1M | **$8.3M** |
| Jun 2026 (actual, 5 días) | $19.0M | -$0.5M | -$0.8M | **$17.7M** |
| Jun 2026 (estimado 30d) | ~$26M | ~-$10M | ~-$2M | **~$14M** |

## 4. Impacto en Waterfall

### Waterfall Actual (Ledger Jun 1-5)
```
Ventas:      $19,018,872
Devoluciones:  -$526,856
Costos:        -$833,870
─────────────────────────────
Disponible:  $17,658,146
```

### Waterfall Proyectado (Carga Completa Jun 1-30)
```
Ventas:      ~$26,000,000
Devoluciones: ~$10,000,000
Costos:        ~$2,000,000
─────────────────────────────
Disponible:  ~$14,000,000
```

## 5. Impacto en Certificaciones Anteriores

| Certificación | Impacto |
|---------------|---------|
| Single Financial Truth (69 period-MP combos) | ⚠️ Periodo Junio 2026 NO incluido |
| DATA_FRESHNESS_CERTIFICATION.md | ✅ Confirmado: Junio 2026 NO incorporado |
| Dashboard Database Certification | ✅ Sin impacto (dashboard usa cierre, no ledger raw) |

## 6. Simulación: ¿Qué pasa si no se carga?

- Si Junio 2026 no se carga nunca: el período queda **incompleto permanentemente**
- El total PARIS en ledger ($337M) está **subestimado** en ~$12-14M (un mes completo de Junio)
- Las certificaciones de integridad que cubren "todos los períodos" pierden validez para Junio 2026
- Dashboard (cierre_financiero_v1) no tiene este período, no hay impacto downstream en UI
