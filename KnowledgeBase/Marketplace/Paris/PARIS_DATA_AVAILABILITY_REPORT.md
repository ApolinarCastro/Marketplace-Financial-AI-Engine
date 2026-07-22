---
tags:
  - paris
  - data_availability
  - p26
status: active
---

# PARIS DATA AVAILABILITY REPORT

## 1. Inventario Físico (XML)
- **XML físicos encontrados**: 0
- **XML válidos**: 0
- **XML corruptos**: 0
- **XML duplicados**: 0
- **XML huérfanos**: 0

## 2. Inventario Financiero (Ledger V4)
- **Órdenes Paris**: 74,028
- **Órdenes con folio / id_transaccion**: 74,028
- **Órdenes sin folio**: 0
- **Órdenes con referencia documental**: 74,028
- **Órdenes sin referencia documental**: 0

## 3. Métricas de Cobertura
- **Cobertura XML**: 0%
- **Cobertura DTE**: 0%
- **Cobertura Ledger**: 100%
- **Cobertura Document Trace**: 0%

## 4. Diagnóstico y Clasificación
La causa de la nula cobertura documental de Paris ha sido clasificada oficialmente como:
**MISSING_SOURCE_DATA**

*Nota: Esto NO es un SYSTEM_FAILURE. La plataforma, los motores y el pipeline están operativos, pero los insumos físicos jamás fueron provistos.*

## 5. Origen de Datos (Resolución Operativa Requerida)
Para desbloquear la Fase C1, se requiere respuesta del equipo operativo a:
- **¿Cuál es la fuente oficial?**: Portal de proveedores de Cencosud / Paris B2B.
- **¿Cómo llegarán al pipeline?**: Deben descargarse y depositarse en data/raw/paris/ de forma nativa o en .zip, y luego pasarse por el UI Ingestor.
- **¿Quién los provee?**: Equipo de Finanzas/Contabilidad Corporativa con accesos al portal Cencosud.
- **¿Con qué periodicidad?**: Debe ser semanal para mantener el SLA de conciliación, idealmente automatizado vía RPA si no existe API.
- **¿Qué cobertura histórica existe?**: Se requieren los XML correspondientes a las 74,028 transacciones históricas registradas en el Ledger.
