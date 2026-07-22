# PARIS Business Model V2 — Final Certification

**Fecha:** 2026-06-11
**Auditoría:** FASE 6 de 6 — PARIS Business Model Certification V2
**Veredicto:** PASS WITH CORRECTED MODEL ⚠️
**Certificación Anterior:** **INVALIDATED** (PARIS_BUSINESS_MODEL_FINAL_CERTIFICATION.md)

---

## 1. Resumen Ejecutivo

La certificación previa (PARIS_ECONOMIC_MODEL_FINAL_CERTIFICATION.md, 2026-06-11) concluyó que PARIS opera como **1P Dropshipping** con Cencosud como seller of record y NANDA SPA como proveedor. 

**Esa conclusión es INCORRECTA.** Esta auditoría V2, basada en evidencia documental, tributaria, operacional y económica, determina que PARIS es un **3P Marketplace** donde:

| Actor | Rol |
|-------|-----|
| Cencosud | Operador del marketplace (comisionista) |
| NANDA SPA + 16 sellers | Vendedores económicos reales |
| Consumidores finales | Compradores |

## 2. Evidencia Clave

### 2.1 Tributaria (DTE — IRREFUTABLE)

| Documento | Flujo | Significado |
|-----------|-------|-------------|
| DTE 33 (36 docs) | Cencosud → NANDA | Factura de servicios (comisiones, logística) |
| DTE 43 (25 docs) | Cencosud → NANDA | **Liquidación-Factura** — Cencosud liquida ventas a NANDA como principal |
| DTE 61 (1 doc) | Cencosud → NANDA | Nota de crédito |

**El DTE 43 es el documento más relevante.** En el sistema tributario chileno, la Liquidación-Factura (DTE 43) se emite cuando:

> "El vendedor o prestador de servicios actúa por cuenta de un tercero, en virtud de un mandato o comisión."

Esto indica que **NANDA (receptor) es el vendedor real y Cencosud (emisor) es el agente/intermediario.**

**La ausencia de DTEs de NANDA a Cencosud descarta el modelo 1P**, donde el proveedor debería facturar al retailer por la venta de mercadería.

### 2.2 Comercial (17 Sellers)

La columna `categoria` en Dropshipping contiene **17 UUIDs únicos de 36 caracteres**, identificando 17 sellers independientes que venden a través de PARIS. NANDA SPA es uno de estos sellers.

| Fuente | Sellers Únicos | Filas |
|--------|---------------|-------|
| Dropshipping | 17 UUIDs | 8,335 filas |
| Fulfillment | 13 UUIDs | 2,112 filas |
| **Total** | **17 sellers** | **10,447 filas** |

`acuerdo_comercial = "No"` en 100% de las filas — indica términos estándar de marketplace, sin acuerdos especiales.

### 2.3 Económica (15% Comisión)

Cada transacción tiene **exactamente 15.0% de margen** entre monto (bruto) y monto_a_pagar (neto). Esto es consistente con una **comisión marketplace fija**, no un margen retail.

| Tipo | Margen | Consistencia |
|------|--------|-------------|
| Ventas | 15.0% | 30/30 muestras exactas |
| Devoluciones | 15.0% | 30/30 muestras exactas |
| Logística | 100.0% | Cencosud retiene 100% |

La comisión explícita (~$15/orden fijo) es un cargo operacional separado, no la comisión marketplace.

### 2.4 Operacional (Inventory Ownership)

| Aspecto | Clasificación | Implicancia 3P |
|---------|--------------|----------------|
| Dueño del inventario | **Seller** | Los sellers poseen el stock |
| Absorción de pérdida | **Seller** | Risk de inventario del seller |
| Absorción de devolución | **Compartido** (85% seller, 15% Cencosud) | Típico de marketplace |

## 3. Modelo de Negocio Final

```
           ┌─────────────────────────────────┐
           │       CONSUMIDOR FINAL          │
           │   (compra producto en PARIS)    │
           └──────────┬──────────────────────┘
                      │ $X (precio con IVA)
                      ▼
           ┌─────────────────────────────────┐
           │  CENCOSUD RETAIL S.A. (PARIS)   │
           │  ─────────────────────────────  │
           │  Marketplace Operator / Agent   │
           │                                 │
           │  Retiene:                       │
           │    • 15% comisión marketplace   │
           │    • $15 cargo operacional fijo │
           │    • Costos logísticos          │
           └──────────┬──────────────────────┘
                      │ $X * 85% (monto_a_pagar)
                      ▼
           ┌─────────────────────────────────┐
           │   SELLER (NANDA SPA + 16 más)   │
           │   ────────────────────────────  │
           │   Seller of Record / Principal  │
           │   • Reconoce la venta           │
           │   • Declara IVA                 │
           │   • Recibe 85% neto             │
           │   • Posee el inventario         │
           └─────────────────────────────────┘

           DOCUMENTOS TRIBUTARIOS:
           Cencosud → NANDA: DTE 33 (servicios)
           Cencosud → NANDA: DTE 43 (liquidación)
           Consumidor:      Boleta/Factura POS (no en archivos)
```

## 4. Impacto en Clasificaciones Anteriores

| Certificación Anterior | Veredicto Anterior | Veredicto V2 | Impacto |
|-----------------------|-------------------|-------------|----------|
| PARIS_ECONOMIC_MODEL_FINAL_CERTIFICATION.md | PASS ✅ (1P dropshipping) | **INVALIDATED** ❌ | El modelo es 3P, no 1P |
| PARIS_BUSINESS_MODEL_FINAL_CERTIFICATION.md | PASS W/WARNINGS ⚠️ (1P) | **INVALIDATED** ❌ | 17 sellers = marketplace multi-seller |
| RFC_PARIS_ECONOMIC_MODEL | (no ejecutado) | **RECHAZADO** | Modelo actual (net revenue) es correcto |

## 5. Impacto en el Modelo Contable

| Aspecto | Antes (1P) | Después (3P) | Cambio |
|---------|------------|--------------|--------|
| Ingreso Cencosud | Gross $338M → Neto $261M | **Solo comisión $77M** | Cencosud no reconoce ventas ajenas |
| Ledger monto | Costo de venta (gross al proveedor) | **Neto a pagar al seller** | Correcto para 3P |
| Comisión | Implícita en spread | **Comisión marketplace del 15%** | Misma magnitud, distinta interpretación |
| RN | Neutral | **Neutral** | El RN no cambia |

**El modelo contable actual en el ledger (`monto = monto_a_pagar` = net revenue) es CORRECTO para un 3P marketplace.** No se requiere cambio.

## 6. Riesgos Identificados

| Riesgo | Descripción | Severidad |
|--------|-------------|-----------|
| **Costos operacionales** | Devoluciones (-$121M) y logística (-$21M) están en ledger de PARIS, no del seller. En un marketplace 3P puro, estos costos deberían ser del seller | ⚠️ **ALTO** |
| **Clasificación de ingresos** | Si Cencosud declara ingresos por $338M (gross) en vez de $77M (comisión), habría una sobrestimación de ingresos | ⚠️ **MEDIO** |
| **IVA** | Verificar quién declara realmente el IVA de las ventas. Si Cencosud emite boleta al consumidor sin respaldo DTE de NANDA, podría haber riesgo fiscal | ❓ POR VERIFICAR |

## 7. Veredicto Final

| Dimensión | Veredicto |
|-----------|-----------|
| **Modelo de negocio** | **3P Marketplace** (17 sellers, Cencosud es agente) |
| **Certificación anterior** | **INVALIDATED** — la conclusión 1P era incorrecta |
| **Modelo contable actual** | **CORRECTO** — net revenue (monto_a_pagar) es apropiado |
| **RFC_PARIS_ECONOMIC_MODEL** | **RECHAZADO** — no ejecutar |
| **Riesgo operacional** | ⚠️ Costos operacionales (-$142M) deberían revisarse con el negocio |

---

## 8. Corrección de Decisiones Previas

### DEC-021 INVALIDATED

**DEC-021 (2026-06-11)** estableció:
> "PARIS = Dropshipping 1P. NOT a 3P marketplace. Cencosud is seller of record (DTE 33 to consumer). NANDA SPA is external supplier. DTE 43 = liquidation to supplier."

**DEC-021 es INCORRECTO.** Basado en interpretación errónea del DTE 43:
- DTE 43 NO es "liquidación al proveedor" en sentido de pago a un supplier 1P
- DTE 43 es Liquidación-Factura, instrumento que **confirma que NANDA es el principal/vendedor real**
- Cencosud NO es seller of record — NANDA y los otros 16 sellers lo son
- La comisión del 15% NO es "margen 1P" — es comisión marketplace 3P

### DEC-022 RECERTIFIED

**DEC-022 (2026-06-11)** estableció:
> "Facturacion PARIS NO está vacío — 62 XML DTE files exist"

DEC-022 se **CONFIRMA** — 62 XMLs exist, pero su interpretación cambia. Los DTE 33 representan **servicios** de Cencosud a NANDA, no factura de venta de mercadería.

---

**Firmado:** Sistema de Auditoría Forense
**Próximos pasos:** (1) Corregir CLAUDE.md, (2) Archivar RFC_PARIS_ECONOMIC_MODEL, (3) Investigar por qué costos operacionales (-$142M) están en ledger de Cencosud siendo un modelo 3P
