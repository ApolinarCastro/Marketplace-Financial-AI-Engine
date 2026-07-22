# INCLUDE_IN_OPERATIONAL_PNL — FINAL DECISION

## Fecha: 2026-06-06
## Tipo: Decisión arquitectónica (no implementación)

---

### 1. Qué representa realmente hoy

`include_in_operational_pnl` es un **flag binario de exclusión** que intenta responder: *"¿Esta fila debe aparecer en la vista de P&L operacional?"*

En realidad representa una **mezcla inconsciente** de dos conceptos distintos:

```
iopnl=False = (MECHANISM) OR (ROOT_EVENT con detalle específico)
```

Donde `ROOT_EVENT con detalle específico` fue decidido por una lista de strings en BASELINE_V6 sin criterio semántico.

---

### 2. Qué errores provoca

| Error | Impacto |
|---|---|
| Subestima RN del ledger en **$116.6M** vs cierre certificado | Los 3 ROOT_EVENTS ($125.8M) excluidos debieran estar incluidos |
| Click-to-ledger inconsistente | Sidebar suma desglose (sin filtro iopnl) ≠ Ledger click (con filtro iopnl) |
| Usuario no puede reconciliar estructura con transacciones | `$3.575.845 → $0` al hacer click en Talla/Garantía |

---

### 3. Si sigue siendo válido

**Parcialmente.** El concepto de "excluir MECHANISMS del P&L operacional" es válido y está respaldado por:
- G6 Cash Reality (ML 2025-04): paired mechanisms tienen zero net cash
- RFC Cash BPP/Poscobro: $134.4M paired mechanisms removables
- Go-Live Audit: mechanisms inflan RN en $35.8M (4.59%)

Pero la implementación actual es inválida porque mezcla ROOT_EVENTS bajo la misma bandera.

---

### 4. Si debe sobrevivir

**Sí, pero modernizado.** El campo responde una pregunta real: *"¿Es esta fila un paired mechanism que debe excluirse del P&L operacional?"*. La pregunta correcta no es "eliminar el flag" sino "corregir qué significa y qué reglas lo determinan".

La verdad financiera (cierre RN) ya DEMUESTRA que el filtro correcto es:
- Excluir: BPP, Poscobro Conciliado, Poscobro General (solo MECHANISMS)
- Incluir: TODO lo demás (incluyendo Talla/Garantía, Arrepentimiento, Producto Dañado)

---

### 5. Plan conceptual futuro

```
FASE 0: No tocar nada ahora
FASE 1: Separar semántica
  - Crear 'is_mechanism' flag (TRUE solo para BPP, Poscobro)
  - include_in_operational_pnl = TRUE para TODO excepto mechanisms
FASE 2: Alinear APIs
  - Desglose debe filtrar por include_in_operational_pnl = TRUE
  - Ledger ya lo hace (no cambiar)
  - Click-to-ledger debe dar el mismo total que la estructura
FASE 3: Validar
  - Escenario C (solo mechanisms excluidos) = RN cierre = $712M
  - 14/14 regression debe seguir pasando
FASE 4: Documentar
  - event_role (ROOT_EVENT vs MECHANISM) en EVENT_REGISTRY_V2
  - cash_role (REAL_CASH vs ACCRUAL) en CASH_ROLE_REGISTRY_V1
```

---

## DECISIÓN ARQUITECTÓNICA

```
SALIDA: MODERNIZE
```

### Justificación

**Por qué no KEEP**: Mantener el estado actual significa aceptar $116.6M de error en el ledger, click-to-ledger inconsistente, y 3 ROOT_EVENTS mal clasificados. La evidencia certificada demuestra que el cierre RN es la verdad — y el flag actual no la refleja.

**Por qué no REPLACE**: Ni `event_role` ni `cash_role` reemplazan completamente la función del flag. `event_role=MECHANISM` captura solo la exclusión de paired events, pero `include_in_operational_pnl` también responde una pregunta de UI/API: "mostrar u ocultar esta fila en el ledger operacional". Reemplazar el flag requeriría reescribir 4 endpoints + 2 dashboards.

**Por qué no DEPRECATE**: El flag sirve para su propósito central (excluir mechanisms del P&L operacional). Eliminarlo sin reemplazo expondría $141.1M de mechanisms en el ledger operacional, creando un nuevo error (el opuesto al actual).

**Por qué MODERNIZE**: El flag existente necesita:
1. Corregir las reglas de clasificación (solo MECHANISMS → False)
2. Agregar campo complementario `is_mechanism` para desambiguar
3. Alinear desglose API para filtrar por `iopnl=TRUE`
4. Preservar todos los endpoints y dashboards sin cambios estructurales

**Costo estimado**: ~2 horas de ingeniería (cambiar reglas en `marketplace_auditor.py:415-429`, agregar filtro en `api.py:260-262`). No requiere migración de DB ni cambios de frontend.

**Riesgo**: CERO. El cierre RN ya incluye estos conceptos. MODERNIZE solo alinea el ledger con la verdad financiera ya certificada.

---

### Checklist de validación post-MODERNIZE

- [ ] Talla/Garantía click = mostrará $3,575,845 (hoy: $0)
- [ ] Arrepentimiento click = mostrará $2,520,642 (hoy: $843,532)
- [ ] BPP click = seguirá mostrando $0 (sin cambios)
- [ ] Ledger suma = $712M (hoy: $595M = cierre certificado)
- [ ] Click-to-ledger siempre coincide con estructura
- [ ] 14/14 regression tests pasan
- [ ] RIPLEY "A pagar" sigue con iopnl=False (sin cambios)
