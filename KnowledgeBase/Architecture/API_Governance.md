---
tags:
  - architecture
  - governance
  - api
status: active
version: 1.0
---

# API Governance Layer

## Overview
All external APIs are governed by a strict mutability policy to protect the `Single Financial Truth`.

## API Certification Matrix

| API | Nivel | Uso | Modifica Core | Modifica Ledger | Riesgo | Estado |
|---|---|---|---|---|---|---|
| `POST /api/v4/upload/dte` | Nivel B | Enriquecimiento documental | NO | NO | Bajo | Permitida (Delega al Pipeline Core) |
| `POST /api/v4/run-audit` | Nivel A | Executive | NO | NO | Medio | Permitida (Ejecuta orquestadores oficiales) |
| `GET /api/v4/cierre` | Nivel A | Executive | NO | NO | Bajo | Permitida (Solo lectura) |
| `GET /api/v4/dte/document-gap` | Nivel A | Drawer | NO | NO | Bajo | Permitida (Solo lectura) |

## Mutability Rule
`Toda API externa deberá cumplir: No modificar Ledger. No modificar ETL. No modificar MarketplaceAuditorEngine. No modificar cálculos.`
