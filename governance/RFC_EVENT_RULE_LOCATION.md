# RFC_EVENT_RULE_LOCATION.md — Dónde debe vivir la regla ROOT_EVENT vs MECHANISM

**Date:** 2026-06-05  
**Scope:** Análisis arquitectónico de las 4 opciones  
**Contexto certificado:** RFC_EVENT_MODEL_CERTIFICATION = PASS  

---

## Pipeline actual

```
LOADER → LEDGER (v1) → CLASIFICACIÓN → CLASIFICADO (v1) → CIERRE (v1) → API → DASHBOARD
   L1         L2              L3                L4             L5         L6       L7
```

| Capa | Tabla | Responsabilidad |
|------|-------|----------------|
| Ledger | `marketplace_ledger_v1` | Ingesta raw de source files. Columnas: `id_transaccion, id_orden, detalle, monto`. Sin enriquecimiento semántico. |
| Clasificación | `marketplace_ledger_clasificado_v1` | Enriquecimiento row-level: `clasificacion_operativa`, `financial_group`, `include_in_operational_pnl`. 1:1 con ledger. |
| Cierre | `marketplace_cierre_financiero_v1` | Agregación mensual: `SUM(monto)` filtrado por `financial_group`. NO usa `include_in_operational_pnl`. |
| API/Dashboard | `api.py` / `templates/*` | Consumidor pasivo de datos certificados. |

---

## La regla certificada

```
Por cada orden (id_orden):

  Si tiene SOLO UN concepto:
    → El concepto participa en Resultado Neto

  Si tiene MULTIPLES conceptos, uno ROOT_EVENT y otro MECHANISM:
    → El ROOT_EVENT participa en Resultado Neto
    → El MECHANISM es EXCLUIDO de Resultado Neto
    → Ambos permanecen en ledger para auditoría

  En cualquier otro caso:
    → Todos los conceptos participan en Resultado Neto
```

Esta regla requiere **análisis por orden** (cross-row), no por fila individual.

---

## Opción A — `marketplace_clasificacion_v1`

### Ventajas
- Ya tiene `include_in_operational_pnl` (columna existente, mismo propósito semántico)
- Ya conoce los conceptos (`clasificacion_operativa`)
- Backend decide
- No requiere nueva tabla

### Riesgos
- **Violación de Single Responsibility**: Clasificación responde "¿qué es esta fila?". La regla de eventos responde "¿qué relación tiene esta fila con otras filas en la misma orden?" Son preguntas diferentes.
- **Procesamiento actual es vectorizado fila-por-fila** (líneas 357-448 de `marketplace_auditor.py`). No tiene contexto de orden. Agregar detección de pares requiere un segundo pase completo (groupby por id_orden), duplicando el pipeline de clasificación.
- **`include_in_operational_pnl` es BOOLEAN** (True/False). La regla requiere 3 estados (ROOT_EVENT, MECHANISM_PAIRED, MECHANISM_STANDALONE). Cambiar el tipo de columna rompe el contrato actual.
- **Propagación a ledger_v1** (líneas 467-509) copia `include_in_operational_pnl` como booleano. Habría que modificar también ledger_v1.

### Compatibilidad con Shopify
Media — requiere modificar el mapa de clasificación y la lógica de op_pnl por marketplace.

### Compatibilidad con Multiempresa
Media — la columna `marketplace` existe, pero la lógica de pares es global.

### Compatibilidad con auditoría
Alta — todo está en una tabla, trazabilidad directa.

### Compatibilidad con restauración quirúrgica
Alta — basta reprocesar clasificación.

### Riesgo de split-brain
**ALTO** — Si la clasificación y el cierre no usan la misma lógica de pares, el RN calculado desde clasificado (vía cierre) diferiría del RN calculado directamente desde ledger. Esto ya ocurre parcialmente hoy (Poscobro Conciliado tiene op_pnl mixto: 7.9% op_pnl=1 vs 92.1% op_pnl=0).

---

## Opción B — `marketplace_cierre_financiero_v1`

### Ventajas
- El resultado_neto ES el output que la regla modifica — parece el lugar natural
- No requiere nuevas tablas ni columnas

### Riesgos
- **El cierre es una agregación simple** — `SUM(monto)` con filtro por `financial_group`. No tiene contexto de orden. Para implementar la regla, el SQL del cierre tendría que hacer subconsultas de pareo por id_orden.
- **El SQL del cierre actual** (líneas 519-528) es plano: 5 SUMs con CASE. Agregar lógica de detección de pares lo convertiría en una monstruosidad SQL de múltiples subconsultas.
- **Violación del principio "Backend decide"**: La regla viviría en un query SQL de agregación, no en una capa semántica. Cualquier cambio requeriría modificar el SQL del cierre.
- **No determinista**: El mismo conjunto de datos clasificados podría producir diferente RN si la lógica de pares cambia en el query.
- **El cierre NO usa `include_in_operational_pnl`**. Hoy la regla ignoraría completamente el campo.

### Compatibilidad con Shopify
Baja — requeriría reescribir el SQL de cierre por tenant.

### Compatibilidad con Multiempresa
Baja — SQL embebido no escala a N empresas.

### Compatibilidad con auditoría
Baja — la lógica estaría oculta en un query SQL de agregación. No hay trazabilidad row-level.

### Compatibilidad con restauración quirúrgica
Baja — para restaurar un período hay que reescribir el query de cierre.

### Riesgo de split-brain
**MUY ALTO** — Si el cierre calcula RN distinto al que se obtendría sumando los montos del ledger clasificado (que es lo que el API expone), hay dos verdades financieras. Esto VIOLA DIRECTAMENTE el principio de Single Financial Truth.

---

## Opción C — `marketplace_ledger_v1`

### Ventajas
- Es la capa más temprana del pipeline — cualquier cambio downstream es automático
- Es la fuente oficial de verdad financiera (Single Financial Truth)

### Riesgos
- **El ledger es raw source data**. Al momento del loader, NO existe clasificación. No se sabe si una fila es "Talla/Garantía" o "BPP" — solo se tiene el `detalle` crudo del source file.
- **No se puede detectar pareo sin clasificación**. La regla dice "si un ROOT_EVENT y un MECHANISM están en la misma orden". Sin saber qué es ROOT_EVENT y qué es MECHANISM, no se puede aplicar.
- **Forzaría a duplicar lógica de clasificación en el loader**. Esto viola "Sin lógica financiera duplicada".
- **Contaminaría el ledger con lógica derivada**. El ledger debe ser la fuente inalterable de verdad transaccional.
- **Modificar ledger_v1 requeriría recargar todos los archivos source** — 154+ archivos XLSX.

### Compatibilidad con Shopify
Baja — requeriría modificar el loader de Shopify.

### Compatibilidad con Multiempresa
Baja — igual.

### Compatibilidad con auditoría
Alta — el ledger es la fuente oficial, cualquier cambio ahí es visible.

### Compatibilidad con restauración quirúrgica
MUY BAJA — restaurar una fila en ledger requiere recargar el source file completo.

### Riesgo de split-brain
**MEDIO** — Si el ledger tiene la regla pero la clasificación no (o viceversa), hay dos fuentes de verdad de clasificación. Pero como el ledger es el source de clasificación, el split sería temporal.

---

## Opción D — Nueva capa conceptual de evento económico

### Ventajas
- **Single Responsibility**: Una sola función: detectar pares ROOT_EVENT+MECHANISM por orden y asignar `tipo_evento_economico`.
- **No modifica ninguna capa existente**: Ledger intacto, clasificación intacta, cierre intacto.
- **Determinista**: Mismo clasificado → mismo evento económico → mismo RN.
- **Shopify-ready**: Solo requiere mapear conceptos Shopify a ROOT_EVENT/MECHANISM en la nueva capa. Sin tocar loader, clasificación ni cierre.
- **Multiempresa-ready**: Agregar `tenant_id` a la nueva capa. Sin modificar tablas existentes.
- **Multimarketplace-ready**: El mismo algoritmo de detección de pares funciona para cualquier marketplace. Solo cambia qué conceptos son ROOT_EVENT vs MECHANISM.
- **Auditable**: La nueva tabla o columna es un artifact verificable independientemente. Se puede auditar "¿en esta orden, el mechanism estaba pareado?" sin tocar ledger ni clasificación.
- **Backend decide**: La regla vive en el backend, no en el frontend.
- **Frontend consumidor pasivo**: La API expone el campo `tipo_evento_economico`; el dashboard lo consume sin lógica.
- **Sin lógica duplicada**: La regla existe exactamente una vez.

### Riesgos
- **Nueva complejidad**: Un paso más en el pipeline.
- **Coordinación con cierre**: El cierre debe modificarse para usar `tipo_evento_economico` en lugar de (o además de) `financial_group` para el cálculo de RN. Pero el cambio en cierre es MÍNIMO: agregar un filtro `WHERE tipo_evento_economico != 'MECHANISM_PAREDO'`.

### Mapa de implementación conceptual

```
Pipeline actual:
Loader → Ledger → Clasificación → Clasificado → Cierre → API

Pipeline con capa D:
Loader → Ledger → Clasificación → Clasificado → EventModel → Cierre → API
                                                         │
                                              Nueva función
                                              run_event_model()
                                              ──────────────
                                              1. Lee clasificado
                                              2. Groupby id_orden
                                              3. Detecta pares
                                              4. Escribe tipo_evento
                                              5. Closing lo consume
```

La capa D se inserta entre clasificación y cierre como una transformación pura:

```python
def run_event_model(self):
    clasificado = self.db.query("SELECT * FROM marketplace_ledger_clasificado_v1")
    orders = clasificado.groupby('id_orden')
    event_types = []
    for oid, rows in orders:
        concepts = set(rows['clasificacion_operativa'])
        has_root = any(concept in ROOT_EVENTS for concept in concepts)
        has_mech = any(concept in MECHANISMS for concept in concepts)
        for _, row in rows.iterrows():
            if row['clasificacion_operativa'] in MECHANISMS and has_root and has_mech:
                event_types.append('MECHANISM_PAIRED')
            else:
                event_types.append('ROOT_EVENT')
    # Escribir columna en clasificado o nueva tabla
```

### Compatibilidad con Shopify
**SÍ** — solo agregar conceptos Shopify a ROOT_EVENTS / MECHANISMS en la nueva capa.

### Compatibilidad con Multiempresa
**SÍ** — agregar `tenant_id` como columna de filtro.

### Compatibilidad con auditoría
**SÍ** — la nueva tabla es verificable independientemente.

### Compatibilidad con restauración quirúrgica
**SÍ** — basta re-ejecutar `run_event_model()` para un período.

### Riesgo de split-brain
**BAJO** — la nueva capa es downstream de clasificación y upstream de cierre. No hay dos caminos alternativos para el RN. El flujo es lineal y determinista.

---

## DICTAMEN FINAL

```
Opción seleccionada: D

Razones de descarte:

  Opción A (Clasificación):
    - Clasificación responde "qué es esta fila".
      EventModel responde "qué relación tiene esta fila con otras".
      Son responsabilidades diferentes. La regla requiere groupby por orden,
      que no existe en clasificación vectorizada fila-por-fila.
    - include_in_operational_pnl es BOOLEAN. La regla requiere 3 estados.
      Cambiarlo rompe el contrato existente.
    - Riesgo de split-brain ALTO: si clasificación y cierre no sincronizan
      la lógica de pares, hay dos verdades de RN.

  Opción B (Cierre):
    - El cierre debe ser una agregación SIMPLE y DETERMINISTA.
      Meter lógica de detección de pares en un SQL de SUM viola todos los
      principios: Single Financial Truth, Backend decide, Determinismo.
    - Riesgo de split-brain MUY ALTO: el cierre produciría un RN distinto
      al que se obtendría sumando el clasificado sin filtrar. Dos verdades.
    - No escalable a Shopify (habría que reescribir SQL por tenant).

  Opción C (Ledger):
    - El ledger es raw source. Al momento del loader NO hay clasificación.
      No se puede detectar ROOT_EVENT vs MECHANISM sin clasificar primero.
    - Forzaría DUPLICAR lógica de clasificación en el loader.
      Violación directa de "Sin lógica financiera duplicada".
    - Modificar ledger_v1 requiere recargar todos los source files.

  Opción D (Nueva capa conceptual):
    - Única opción que respeta TODOS los principios obligatorios.
    - No modifica ninguna capa existente. Pipeline sigue siendo lineal.
    - Determinista: mismo clasificado → mismo evento → mismo RN.
    - Shopify-ready: solo mapear conceptos en la nueva capa.
    - Multiempresa-ready: solo agregar tenant_id.
    - Auditabilidad total: la nueva capa es verificable independientemente.
    - Riesgo de split-brain BAJO: flujo lineal clasificado → evento → cierre.
```

---

## Formato final

```
PASS

Ubicación correcta:
D

Riesgo:
bajo

Compatibilidad Shopify:
sí

Compatibilidad Multiempresa:
sí

Compatible con Single Financial Truth:
sí

Recomendación final: Nueva capa conceptual de evento económico entre clasificación y cierre. Única opción que respeta los 10 principios obligatorios sin modificar capas certificadas existentes.
```
