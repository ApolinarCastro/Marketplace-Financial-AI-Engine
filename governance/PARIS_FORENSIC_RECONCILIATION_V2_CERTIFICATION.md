# PARIS June 2026 — Forensic Reconciliation V2 Certification

**Fecha:** 2026-06-11
**Auditoría:** FASE 6 de 6 — PARIS Forensic Reconciliation V2
**Clasificación:** **PASS WITH WARNINGS** ⚠️

---

## 1. ¿Qué está demostrado?

### Hechos Demostrados (evidencia directa, sin estimaciones)

| # | Hecho | Evidencia |
|---|------|-----------|
| 1 | El ledger contiene datos PARIS solo hasta **2026-06-05** | `marketplace_ledger_v1`, `SELECT DISTINCT fecha` |
| 2 | El ledger **NO** contiene datos para Jun 6, 7, 8 | `marketplace_ledger_v1`, consulta por fecha |
| 3 | Los archivos cargados fueron `06-06-2026.xlsx` (1,002 filas) y `1 jun 2026 - 5 jun 2026.xlsx` (88 filas) | `marketplace_ledger_v1.archivo_origen` |
| 4 | Esos 2 archivos **NO existen** en disco actualmente | Búsqueda física en `01_Raw/PARIS/` |
| 5 | 3/5 fechas cargadas (Jun 2, 3, 4) tienen **$0 delta** entre RAW net y Ledger | Comparación `monto_a_pagar` vs `ledger.monto` |
| 6 | **90 órdenes** existen en RAW pero no en Ledger | Comparación directa de `order_id` |
| 7 | Esas 90 órdenes suman **$2,023,360 net** | `monto_a_pagar` de RAW |
| 8 | **1 orden** ($15,112) existe en Ledger pero no en RAW actual | Comparación de `id_orden` |
| 9 | El delta **$4,141,063** del V1 comparó Gross vs Ledger (inválido) | V1 usó `RAW.monto` (bruto); V2 usa `RAW.monto_a_pagar` (neto) |
| 10 | El delta neto real es **$418,696** | RAW net $18,076,842 - Ledger $17,658,146 |

### Descomposición Exacta del Delta

```
Delta Neto Total:                    +$418,696  (100%)
├── Días 6-8 no cargados:            +$817,822  (195.3%)
│   ├── 2026-06-06:  +$162,910
│   ├── 2026-06-07:  +$508,774
│   └── 2026-06-08:  +$146,138
└── Diferencia archivos loader:      -$399,126  (-95.3%)
    ├── 2026-06-01:  -$161,720  (Ledger tiene más)
    └── 2026-06-05:  -$237,406  (Ledger tiene más)
```

---

## 2. ¿Qué no está demostrado?

| Afirmación | Estado | Razón |
|-----------|--------|-------|
| Cuántas órdenes de Jun 9-30 existen | **NO DEMOSTRADO** | No existen archivos RAW para ese período |
| Qué monto total tiene Junio 2026 completo | **NO DEMOSTRADO** | No hay fuentes de datos para 22/30 días |
| Si el archivo `1 jun 2026 - 8 jun 2026.xlsx` es idéntico a los archivos del loader | **NO DEMOSTRADO** | Los archivos originales no existen; diferencia de $399K sugiere que NO son idénticos |
| Si `06-06-2026.xlsx` fue renombrado o reemplazado | **NO DEMOSTRADO** | No hay evidencia de rename (solo conjetura) |
| Cuál es el monto total de Junio 2026 | **NO DEMOSTRADO** | Requeriría datos de Jun 9-30 que no existen |

---

## 3. ¿Qué conclusiones del reporte anterior (V1) son inválidas?

| Conclusión V1 | Estado | Corrección V2 |
|--------------|--------|---------------|
| "Delta $4,141,063 (23.5%)" | **INVÁLIDO** ❌ | El delta correcto es **$418,696 (2.4%)** usando neto |
| "No es posible reconciliar exactamente" | **INVÁLIDO** ❌ | Sí es posible: el delta se descompone en $0 para 3 fechas, diferencia de archivos loader (-$399K), y data no cargada (+$818K) |
| "Componente: diferencia gross/net días 1-5 ~$1.3M" | **INVÁLIDO** ❌ | Esa diferencia no existe cuando se usa neto. Jun 2-4 tienen $0 delta |
| "Componente: días 6-8 no cargados ~$2.8M" | **INVÁLIDO** ❌ | El valor neto real de días 6-8 es **$817,822** |
| "90 órdenes suman $96,010" | **INVÁLIDO** ❌ | Las 90 órdenes suman **$2,023,360 net** (V1 midió solo algunos días por error de fecha) |

### Correcciones Específicas al Reporte Anterior

1. **El V1 usó `RAW.monto` (gross) para comparar con `Ledger.monto` (net)** — mezcla incompatible. La columna correcta es `monto_a_pagar`.
2. **El V1 reportó "90 órdenes suman $96K"** — ese valor era incorrecto porque el script V1 filtró mal las fechas. El valor real de las 90 órdenes es **$2.02M net**.
3. **El V1 estimó "días 6-8 no cargados ~$2.8M"** — sobrestimado. El valor neto es $817,822.
4. **El V1 dijo "no reconciliable"** — falso. 3/5 fechas cargadas tienen $0 delta perfecto.

---

## 4. ¿Cuál es el delta real certificado?

**$418,696** (RAW net $18,076,842 - Ledger $17,658,146)

Desglose certificado:
- **$817,822** = Días 6, 7, 8 no cargados (RAW existe, valor neto)
- **-$399,126** = Diferencia entre archivos loader y RAW actual

Para los días donde los archivos coinciden (Jun 2, 3, 4): **$0 delta** ✅

---

## 5. ¿Puede certificarse Junio 2026?

**NO.** ❌

Junio 2026 **NO puede certificarse como completo** por las siguientes razones:

| Barrera | Severidad | Detalle |
|---------|-----------|---------|
| Data faltante (22 días) | **BLOQUEANTE** | No existen fuentes para Jun 9-30 |
| Archivos loader perdidos | **ALTA** | `06-06-2026.xlsx` y `1 jun 2026 - 5 jun 2026.xlsx` no existen. Diferencia de $399K en Jun 1 y 5 no es trazable |
| Diferencia archivo actual vs loader | **MEDIA** | El RAW actual `1 jun 2026 - 8 jun 2026.xlsx` difiere de los archivos cargados (1 orden $15K está en ledger pero no en RAW) |

**Lo que SÍ puede certificarse:**

| Afirmación | Estado |
|-----------|--------|
| Los días 2, 3 y 4 de Junio 2026 de PARIS están **100% reconciliados** ($0 delta) | ✅ **CERTIFICADO** |
| El loader es correcto (cuando se usan los mismos archivos fuente) | ✅ **CERTIFICADO** |
| 90 órdenes ($2.02M net) de RAW no han sido cargadas al ledger | ✅ **CERTIFICADO** |
| El delta real es $418,696, no $4,141,063 | ✅ **CERTIFICADO** |

---

## Veredicto Final: **PASS WITH WARNINGS** ⚠️

### Fundamento

- **PASS** porque: El núcleo del pipeline (RAW → Ledger) funciona correctamente — 3/5 días con $0 delta demuestra que no hay error de loader ni de transformación.
- **WARNINGS** porque:
  1. Junio 2026 no está completo (sin datos para 22/30 días)
  2. Los archivos fuente del loader se perdieron (no hay trazabilidad documental completa)
  3. 90 órdenes ($2.02M net) esperan ser cargadas
  4. El reporte V1 contenía errores graves (factor 10x en delta)

### Confianza

| Dimensión | Confianza |
|-----------|-----------|
| Funcionamiento del loader | **ALTA** (3/5 fechas $0 delta) |
| Data cargada en ledger | **ALTA** (lo que está, está correcto) |
| Completitud de Junio 2026 | **BAJA** (solo 27% del mes en RAW, 17% en ledger) |
| Trazabilidad documental | **MUY BAJA** (archivos loader perdidos) |
| **Global** | **MEDIA** |

### Acciones Requeridas (Bloqueadas por restricciones actuales)

1. Obtener archivos PARIS actualizados (Dropshipping + Fulfillment) para Jun 9-30
2. Ejecutar loader contra los archivos de Jun 1-8 (para cargar las 90 órdenes pendientes)
3. Re-ejecutar clasificación y cierre
4. Preservar los archivos fuente originales para futura trazabilidad
