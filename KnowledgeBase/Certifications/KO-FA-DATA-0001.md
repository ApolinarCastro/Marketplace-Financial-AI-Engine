---
tags:
  - certification
  - ko
  - falabella
  - blocked
status: draft
---

# KO-FA-DATA-0001: Bloqueo Operativo Falabella

## 1. Evidencia
- Consulta a data/raw/falabella/ arroja 0 archivos.
- Consulta al Ledger arroja 2,609 órdenes pendientes de XML.

## 2. Causa
BLOCKED_BY_SOURCE_DATA. Insumos documentales físicos inexistentes.

## 3. Impacto
- Certificación documental suspendida.
- Pipeline C1 y C2 de Falabella en pausa oficial.

## 4. Acción Requerida
- Descargar XML de facturación del portal Seller Center de Falabella (o fuente oficial proveída por Operaciones) y depositarlos en data/raw/falabella/.

## 5. Responsable y Dependencias
- **Responsable**: Equipo de Operaciones / Finanzas corporativas.
- **Dependencia externa**: Portal Falabella.
