---
tags:
  - audit
  - filter
---
# FILTER CONSISTENCY AUDIT

## HALLAZGO 1: ESTRUCTURA FINANCIERA ≠ LEDGER
**Componentes Afectados:** Panel Izquierdo (Estructura Financiera) vs Panel Derecho (Ledger Transaccional / Total Seleccionado).

**Origen del fallo:** 
Cuando el usuario hace clic en un agregado de la Estructura Financiera (ej. "Ingresos" por .3M), se activa selectFinancialFilter(). 
Sin embargo, el query parameter que se envía a la API (inancial_group) para filtrar las transacciones del Ledger no incluye las sub-reglas exactas de agrupación, o la tabla de la derecha está limitada visualmente por paginación (limit=200) mientras el "Total Seleccionado" solo suma lo visible y no el agregado real del motor.
El delta (Δ) es mayor a 0 porque los cálculos de backend (/api/v4/exec/summary) y el filtrado del grid (/api/v4/ledger?financial_group=...) tienen asimetría en su clausula WHERE (ej. omisión de cuentas contables secundarias que la Estructura sí suma).

## HALLAZGO 3: ALERTA DOCUMENTAL PERMANENTE
**Alerta:** FOLIO_ESTRUCTURAL_SIN_RESPALDO_SII
La alerta no se condiciona contextualmente por Marketplace. En Ripley, no existen DTE físicos. Por lo tanto, el sistema la pinta ciegamente en base al total de Gaps de la plataforma sin aislar Ripley, o bien, está quemada en HTML.
