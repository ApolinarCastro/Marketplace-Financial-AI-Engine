---
tags:
  - audit
  - certification
---
# UI CERTIFICATION REPORT

## ESTADOS OFICIALES
- 🟢 **Financial Certification:** COMPLETADA (Backend y ETL de Ripley validados 100%).
- 🟡 **Document Certification:** BLOCKED_BY_SOURCE_DATA (Asignado formalmente en backend).
- 🔴 **Frontend End-to-End Certification:** PENDIENTE.

## GAPS A RESOLVER (Frontend Exclusivo)
1. Conectar #estado-proceso-container a pi/v4/exec/summary para reflejar el estado oficial, eliminando el hardcode.
2. Refactorizar la función openDrawer() para que asimile correctamente el Enum DocumentCertificationStatus (específicamente BLOCKED_BY_SOURCE_DATA), rompiendo el loop de "Cargando...".
3. Arreglar el filtro de la Estructura Financiera (uildLedgerUrl) para asegurar que Δ = 0 al hacer drill-down.
4. Conectar los 4 widgets inferiores de Cobertura Documental a los endpoints vivos, borrando los placeholders fijos.

La certificación total de Ripley quedará congelada hasta que la UI se adhiera al principio BACKEND FIRST.
