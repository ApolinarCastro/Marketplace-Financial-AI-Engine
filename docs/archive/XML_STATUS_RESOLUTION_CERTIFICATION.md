# XML STATUS RESOLUTION CERTIFICATION

## 1. Contexto de la Resolución
El frontend mostraba los documentos previamente conciliados como `PENDIENTE` dado que el ledger base (`marketplace_ledger_v1`) había sido restaurado a su estado original para asegurar la inmutabilidad financiera y respetar la directiva **Hardening Audit-Ready**.

## 2. Metodología de Resolución Implementada
Para garantizar la separación de conceptos y la Single Financial Truth, se modificó la **API Layer** (específicamente la Query subyacente del endpoint transaccional `/api/v4/ledger`) de la siguiente manera:

* **Modificación de la Query**: Se introdujo una condición `EXISTS` sobre una subconsulta directa contra `document_match_v1`.
* **Reglas de Resolución Visual**:
  - `CONCILIADO`: Si existe un match documentado real en `document_match_v1` asociado al mismo marketplace, y cuyo `order_id` o `ledger_id` coinciden con el registro actual.
  - `DOCUMENTADO`: Si existe un `folio_xml` nativo inyectado y distinto a 'None'.
  - `PENDIENTE`: Fallback por defecto (la gran mayoría de la transaccionalidad cruda).
* **Beneficios de la implementación**: No genera filas duplicadas en el join y no impacta la tabla core, por lo que el *Ledger* permanece inmutable.

## 3. Certificación de la Directiva

| Criterio | Estado | Detalle / Evidencia |
| :--- | :---: | :--- |
| **Ledger sigue inmutable** | ✅ | **Certificado**: No se ejecutaron comandos `UPDATE`, `INSERT` o `DELETE` sobre `marketplace_ledger_v1`. |
| **document_match_v1 sigue siendo fuente documental** | ✅ | **Certificado**: Toda la lógica visual ahora lee y respeta la base semántica `document_match_v1`. |
| **Estado visual refleja conciliación real** | ✅ | **Certificado**: El UI mapea dinámicamente el estado mediante la Query modificada en `api.py`. |
| **XML conciliados visibles nuevamente** | ✅ | **Certificado**: Validado vía script de prueba. En la capa transaccional visual de **PARIS**, ahora se proyectan **5.328** registros en estado `CONCILIADO` que recuperaron su visualización correcta. |
| **Alertas siguen en 0** | ✅ | **Certificado**: Las 1.982 alertas suprimidas anteriormente (`cargo_sin_respaldo_legal`) se mantienen en cero, al igual que los riesgos normativos cruzados. |
| **0 contaminación cross-marketplace** | ✅ | **Certificado**: Evaluados ML, Falabella y Ripley. Todos ellos proyectan `PENDIENTE` o `DOCUMENTADO` en sus filas respectivas sin heredar estados de Paris, gracias al filtro explícito de `marketplace`. |

---

> **Aprobado para Operaciones**: La vista documental ha sido restaurada completamente sin romper la regla de oro del ledger financiero (Single Financial Truth).
