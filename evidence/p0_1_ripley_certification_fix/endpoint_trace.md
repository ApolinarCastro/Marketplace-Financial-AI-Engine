# LOOP 1 — Auditoría del Endpoint de Certificación Electrónica

**Execution ID:** `f8d2e3c1-4a5b-4c6d-8e9f-0a1b2c3d4e5f`
**Endpoint auditado:** `GET /api/v4/electronic_certification/status/{tx_id}` — `api/api.py:865`

---

## Preguntas de auditoría

### ¿Dónde obtiene cert_type?
**NO consulta `dte_link_v1` ni `dte_truth_v1` ni `document_match_v1`.** El endpoint (api.py:865-916) consulta
únicamente `marketplace_ledger_v1` (por `id_transaccion` o `id_orden`, con fallback `LIKE`). Toda la respuesta se
construye a partir de la fila del ledger. `cert_type` nunca es leído — **el bug es que el folio del ledger se asume
automáticamente como certificación fiscal**.

### ¿Dónde asigna CRYPTOGRAPHIC_CERTIFIED?
`api/api.py:914` — `"level": "CRYPTOGRAPHIC_CERTIFIED"`, dentro del bloque `evidencia`, que se retorna **incondicionalmente**
para toda fila encontrada que tenga `folio_xml` poblado (o que falleback a `id_orden`). No existe condición previa.

### ¿Dónde asigna confidence?
`api/api.py:913` — `"confidence": "100.0%"`, hardcodeado en el mismo bloque incondicional.

### ¿Dónde asigna certified?
El campo `estado` en `api/api.py:904` — `"estado": "CERTIFICADO"`, también hardcodeado.

### ¿Dónde usa LEDGER_EXISTING?
**En ninguna parte del endpoint.** El término `LEDGER_EXISTING` existe solo como `cert_type` en `dte_link_v1`
(210,232 filas RIPLEY, 96,098 ML, todos `certified=True` por la columna BOOLEAN), pero el endpoint no lo consulta.
La equivalencia `LEDGER_EXISTING → CRYPTOGRAPHIC_CERTIFIED` es **implícita** (no explícita en código): como toda fila
del ledger con folio se marca CERTIFICADO, y la mayoría de folios RIPLEY provienen de `dte_link_v1.cert_type=LEDGER_EXISTING`,
el resultado efectivo es que `LEDGER_EXISTING` produce `CRYPTOGRAPHIC_CERTIFIED` con 100%.

### ¿Dónde consulta dte_truth?
**No consulta.** `dte_truth_v1` (el índice SII real: 667 folios totales, 407 RIPLEY / 192 ML / 62 PARIS / 6 FALABELLA)
no aparece en el SQL del endpoint. Confirmado: **0 folios del ledger coinciden con dte_truth_v1** en cualquier
marketplace.

### ¿Dónde consulta XML?
**No consulta.** No hay lectura de archivos XML ni de `dte_truth_v1` (que deriva de XMLs). El `pipeline.xml/xsd/sig/caf`
se devuelve `PASS` hardcodeado (api.py:905-910) sin ejecutar validación alguna.

---

## Ruta de la decisión actual (bug)

```
tx_id
  └─ marketplace_ledger_v1 (WHERE id_transaccion OR id_orden, fallback LIKE)
       ├─ ¿fila existe? NO  → {"status":"INSUFFICIENT_EVIDENCE", pipeline ALL FAIL, 0%}
       └─ ¿fila existe? SÍ  → {"estado":"CERTIFICADO", pipeline ALL PASS,
                               evidencia:{confidence:"100.0%", level:"CRYPTOGRAPHIC_CERTIFIED"}}
                               ↑ INCONDICIONAL — no consulta dte_truth/document_match/dte_link
```

## Falsos positivos demostrados

| Marketplace | filas dte_link LEDGER_EXISTING | folios ledger en dte_truth | document_match MATCHED | Falso positivo |
|---|---|---|---|---|
| RIPLEY | 210,232 | **0** | 0 | SÍ (100%) |
| ML | 96,098 | **0** | 0 | SÍ (100%) |
| PARIS | (XLSX_EXTRACT 32,572) | 0 | 9,431 (18 con dte real) | Parcial |
| FALABELLA | (XLSX_EXTRACT 210) | 0 | 0 | Parcial |

**RIPLEY = 210,232 transacciones presentadas como CRYPTOGRAPHIC_CERTIFIED 100% sin vínculo a dte_truth_v1 ni XML.**

## Transición prohibida a eliminar

```
LEDGER_EXISTING  →  CRYPTOGRAPHIC_CERTIFIED   (PROHIBIDO — ver LOOP 3)
```
