# RIPLEY Financial Taxonomy V1

## Status: CERTIFIED ✅

## Overview

Official financial taxonomy for RIPLEY marketplace. Classifies all 32 `detalle` values in `marketplace_ledger_v1` as SIGNAL (canonical P&L) or NOISE (duplicate/derived/treasury).

## Canonical Groups

| Grupo Canónico | Display Name | Detalles SIGNAL |
|---------------|-------------|-----------------|
| `ingresos` | Ingresos Brutos | `Importe del pedido` |
| `devoluciones` | Devoluciones de Venta | `Importe del pedido reembolsado` |
| `costos_logisticos` | Costos Logísticos & Operacionales | `Envío`, `Gastos de envío pagados por el operador`, `Descuento por costo logístico`, `Descuento por logistica inversa` |
| `comisiones` | Comisiones & Comerciales | `Comisión`, `Comisión de reembolso` |
| `ajustes` | Ajustes & Retenciones | `Factura manual`, `Abono manual`, `Otros descuentos`, `Descuento por cancelación` |

## SIGNAL vs NOISE Summary

| Classification | Count | Total ($) |
|---------------|-------|-----------|
| SIGNAL | 11 | $767,635,714 |
| NOISE | 18 | $905,539,159 |
| Treasury (NOISE) | 4 | — |
| **Total** | 32 | $1,673,174,873 |

**54.1% of RIPLEY financial data is NOISE** — duplicate or derived concepts that inflate the P&L.

## Key Exclusions

| Excluded Detalle | Reason | Amount Impact |
|-----------------|--------|--------------|
| `Precio total` | Duplicado de Importe del pedido | $535.3M overstatement |
| `Subtotal` | Duplicado operacional | $513.3M overstatement |
| `Comisiones` | Duplicado de Comisión | -$84.3M noise |
| `Comisiones sobre pedidos` | Agrupación derivada | -$68.1M noise |
| `Pedidos reembolsados` | Duplicado de Importe del pedido reembolsado | -$86.5M noise |

## Source

`knowledge/taxonomy/ripley_v1.json`

**Date:** 2026-06-17
