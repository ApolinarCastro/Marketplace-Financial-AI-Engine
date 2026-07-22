---
tags:
  - certification
  - ko
  - paris
  - blocked
status: draft
---

# KO-PA-DATA-0001: Bloqueo de Disponibilidad de Datos Paris

## 1. Estado Actual
Bloqueado (FASE C0). El pipeline de indexación (FASE C1) y la certificación (FASE C2) no pueden iniciar.

## 2. Causa del Bloqueo
MISSING_SOURCE_DATA. 

## 3. Evidencia
- Consulta en crudo a data/raw/paris/ arroja 0 archivos.
- Consulta al Ledger arroja 74,028 transacciones pendientes de su par documental.

## 4. Datos Faltantes
- XMLs físicos correspondientes a las facturas/boletas de Paris.

## 5. Acción Requerida
- Proveer el dump histórico de DTEs desde el portal B2B de Cencosud y depositarlos en data/raw/paris/.
- Responder a las preguntas operativas planteadas en PARIS_DATA_AVAILABILITY_REPORT.md.
