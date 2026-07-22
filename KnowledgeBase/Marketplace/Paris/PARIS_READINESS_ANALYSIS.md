---
tags:
  - paris
  - readiness
  - p26
status: active
---

# PARIS READINESS ANALYSIS

## 1. Inventario Documental
- **XML disponibles**: Carpeta data/raw/paris/ contiene dumps crudos (por clasificar).
- **DTE disponibles**: Históricos de prueba.
- **Facturación**: Pendiente de normalización.
- **Settlement**: Mapeado en base pre-V4.
- **Evidencia existente**: Parcial.

## 2. Cobertura Actual
- **XML indexados**: 0 (Requiere carga).
- **XML faltantes**: Todos.
- **Órdenes con evidencia**: 0.
- **Órdenes sin evidencia**: 100%.

## 3. Reutilización Esperada
- **Motores**: MarketplaceAuditorEngine (100% reuso), DTEIndexer (100% reuso).
- **Endpoints**: /api/v4/run-audit, /api/v4/upload/dte, /api/v4/electronic_certification/status/{tx}.
- **Knowledge**: KnowledgeBase/Marketplace/Taxonomy/paris_v1.json (Reuso total).
- **DEC Afectados**: DEC-019 (Single Financial Truth), DEC-071.

## 4. Riesgos Identificados
| Riesgo | Causa | Impacto | Mitigación | Prioridad |
|---|---|---|---|---|
| Mapeo ETL Incompleto | Diferencias en cabeceras de Paris | Fallo en Ledger | Adaptar ingestor crudo a esquema V4 | ALTA |
| Folios Duplicados | Reprocesamiento de DTE | Corrupción de Document Gap | Clave única en DB y rechazo en ingestión | ALTA |
