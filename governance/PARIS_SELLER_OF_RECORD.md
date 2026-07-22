# PARIS — Seller of Record Certification

**Fecha:** 2026-06-11
**Auditoría:** FASE 1 de 6 — PARIS Business Model Certification

---

## 1. Muestras Analizadas

| Fuente | Archivos | Filas Muestra |
|--------|---------|-------------|
| Dropshipping | 6 archivos (2026: 01-06) | 50 órdenes |
| Fulfillment | 3 archivos (2026) | 50 órdenes |
| Devoluciones | Mixto DS+FF | 20 devoluciones |
| Total transacciones analizadas | 22 archivos | 10,447 filas (muestra + total) |

## 2. Vendedores Identificados

### 2.1 Dropshipping — 17 vendedores únicos

La columna `categoria` contiene **UUIDs de 36 caracteres** que identifican vendedores individuales:

| Vendedor UUID | Filas | Monto |
|--------------|-------|-------|
| 38c46083-c944-4147-bdd9-b70e10e2ce33 | 1,691 | $34,102,590 |
| a557e215-7ea2-42a3-816d-20ae219d514b | 1,191 | $10,444,610 |
| e4e3ffa8-e471-4bc6-8245-5474bc88cb09 | 401 | $3,823,230 |
| 7567f168-3c2d-46eb-83ba-6ff8e7fc278b | 388 | $17,661,660 |
| c9a85b1f-295a-4552-8900-56a7ada83783 | 477 | $5,372,010 |
| +12 más | 527 | $4,564,718 |
| **Total** | **8,335** | **$76,158,818** |

### 2.2 Fulfillment — 13 vendedores únicos

| Vendedor UUID | Filas |
|--------------|-------|
| (blank) | 697 |
| 38c46083-c944-4147-bdd9-b70e10e2ce33 | 519 |
| 3b6e9753-5cd8-466e-b2d7-f0c2c93e0381 | 314 |
| c9a85b1f-295a-4552-8900-56a7ada83783 | 192 |
| +9 más | 390 |
| **Total** | **2,112** |

### 2.3 NANDA SPA — Vendedor Único en DTE

Todos los **62 DTE XML** en `Facturacion/` tienen:
- **Emisor**: Cencosud Retail S.A. (RUT 81201000-K) — el operador de PARIS
- **Receptor**: NANDA SPA (RUT 77898100-9) — el vendedor

**NANDA SPA** es el único receptor de DTE en toda la documentación tributaria. Sin embargo, las transacciones RAW muestran **17 UUIDs diferentes**, indicando múltiples sellers.

## 3. Quién Vende

| Actor | Rol |
|-------|-----|
| Cencosud | Operador del marketplace PARIS. Emite DTE 43 (liquidación) a los sellers. Emite DTE 33 (factura de servicios) a los sellers |
| NANDA SPA + 16 sellers | **Vendedores económicos reales**. Venden productos a consumidores a través de PARIS. Cencosud les liquida el neto |

**Evidencia:**
- DTE 43 (Liquidación-Factura) → Cencosud liquida a NANDA (flujo de agente a principal)
- No existen DTE de NANDA a Cencosud (inconsistente con modelo 1P donde proveedor factura al retailer)
- 17 UUIDs = 17 sellers diferentes usando la plataforma

## 4. Quién Cobra

| Actor | Qué Cobra |
|-------|-----------|
| Cencosud | **Comisión del 15%** sobre cada venta + $15 operacional por transacción |
| NANDA/otros sellers | Cobran el **85% neto** (monto_a_pagar) de cada venta |

## 5. Quién Liquida

**Cencosud** liquida a los sellers mediante DTE 43. La liquidación es el neto después de deducir:
- Comisión 15%
- Costos de despacho/logística

## 6. Quién Figuras Como Vendedor

**Los sellers (NANDA SPA + otros)** figuran como vendedores económicos. Cencosud actúa como **agente/marketplace**, no como retailer. Esto se demuestra por:

1. DTE 43 (no DTE 33 a consumidores) — Cencosud liquida, no vende
2. 17 vendedores independientes con sus propios UUID
3. `acuerdo_comercial = "No"` en 100% de las transacciones (sin acuerdo comercial especial = términos estándar de marketplace)
4. La comisión del 15% es consistente con un marketplace fee, no un margen retail

## 7. Quién Recibe el Dinero

**Los sellers (NANDA + otros)** reciben el dinero de las ventas neto de comisiones. Cencosud recibe la comisión del 15% más cargos operacionales.

## 8. Respuesta

**¿Quién es el vendedor económico real?**

**NANDA SPA y los otros 16 sellers** son los vendedores económicos reales. Cencosud/PARIS opera como marketplace intermediario, no como retailer 1P.

**Contradicción con auditoría anterior:**
La certificación previa (PARIS_ECONOMIC_MODEL_FINAL_CERTIFICATION.md, 2026-06-11) concluyó "PARIS = Dropshipping 1P". Esa conclusión es **INCORRECTA**. La evidencia de 17 sellers, DTE 43 (liquidación), y comisión del 15%, apunta inequívocamente a un modelo **3P Marketplace**.
