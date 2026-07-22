---
tags:
  - audit
  - drawer
---
# DRAWER CONTRACT AUDIT

## HALLAZGO 2: DRAWER DOCUMENTAL NO FUNCIONAL
**Componentes Afectados:** Modal Lateral (Drawer) de Certificación Electrónica.
**Origen del fallo:** 
La API expone un contrato DocumentTrace o la metadata de la orden mediante pi/v4/ledger (o su homólogo). En el Frontend, al abrir el modal (ej. openDrawer(...)), el código intenta leer atributos como Folio, Tipo DTE, Emisor, pero fallan en el mapeo (ej: undefined o esperando otro JSON schema), derivando en el llenado con guiones ("-").
El estado de la validación se atasca en la línea 1302 (cert-status.innerText = 'Cargando...') porque la promesa que busca la evidencia asíncrona nunca resuelve o no se captura su error para pintar BLOCKED_BY_SOURCE_DATA.

## CADENA DE PÉRDIDA:
1. Ledger -> Posee estado BLOCKED_BY_SOURCE_DATA.
2. API -> Envía JSON con document_certification: { status: "BLOCKED_BY_SOURCE_DATA" }.
3. Frontend -> El JSON se recibe, pero el JS del Drawer no mapea este campo hacia la UI y se queda en "Cargando...".
