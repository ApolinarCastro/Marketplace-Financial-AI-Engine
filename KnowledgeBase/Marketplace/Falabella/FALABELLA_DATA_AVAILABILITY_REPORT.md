---
tags:
  - falabella
  - data_availability
  - p26
status: active
---

# FALABELLA DATA AVAILABILITY REPORT

## 1. Inventario Físico (XML)
- **XML físicos encontrados**: 0
- **XML válidos**: 0
- **XML huérfanos**: 0

## 2. Inventario Financiero (Ledger V4)
- **Total órdenes Ledger**: 2,609
- **Órdenes con folio / id_transaccion**: 2,609
- **Órdenes sin folio**: 0

## 3. Métricas de Cobertura
- **Cobertura XML**: 0%
- **Cobertura DTE**: 0%
- **Cobertura Ledger**: 100%
- **Cobertura Documental (Trace)**: 0%

## 4. Diagnóstico y Clasificación
La causa de la nula cobertura documental de Falabella es oficialmente:
**BLOCKED_BY_SOURCE_DATA**

*El pipeline y la API responderán determinísticamente con este estado sin generar excepciones ni fallos de sistema.*
