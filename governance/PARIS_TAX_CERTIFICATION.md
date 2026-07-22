# PARIS — Tax Certification (DTE Analysis)

**Fecha:** 2026-06-11
**Auditoría:** FASE 3 de 6 — PARIS Business Model Certification

---

## 1. Resumen de DTE

| DTE | Tipo | Cantidad | Monto Total | IVA Total | Neto |
|-----|------|----------|-------------|-----------|------|
| 33 | Factura Electrónica | 36 | $59,926,401 | $9,568,079 | $50,358,322 |
| 43 | Liquidación-Factura | 25 | $138,154,627 | $25,851,834 | $136,062,267 |
| 61 | Nota de Crédito | 1 | $7,818,947 | $1,248,403 | $6,570,544 |
| **Total** | | **62** | **$205,899,975** | **$36,668,316** | **$192,991,133** |

## 2. Dirección del Flujo Documental

**TODOS los documentos** fluyen en la misma dirección:

```
Cencosud Retail S.A. (RUT 81201000-K) → NANDA SPA (RUT 77898100-9)
```

No existe ningún DTE en la dirección inversa (NANDA → Cencosud).

## 3. Quién Reconoce Tributariamente la Venta

### 3.1 DTE 33 (Factura Electrónica)

Emisor: **Cencosud Retail S.A.** → Receptor: **NANDA SPA**

Este documento representa una factura de **Cencosud a NANDA** por servicios prestados. **NO** es una factura al consumidor final.

### 3.2 DTE 43 (Liquidación-Factura)

Emisor: **Cencosud Retail S.A.** → Receptor: **NANDA SPA**

El DTE 43 (Liquidación-Factura) es un documento tributario especial del SII chileno diseñado para:

> "Operaciones en que el vendedor o prestador de servicios actúa por cuenta de un tercero, en virtud de un mandato o comisión."

En el DTE 43:
- **NANDA** (receptor) es el **mandante/principal** — el vendedor real
- **Cencosud** (emisor) es el **mandatario/agente** — quien facilita la venta

**Quién reconoce la venta:** NANDA SPA reconoce tributariamente la venta al consumidor final. Cencosud actúa como intermediario.

### 3.3 DTE 61 (Nota de Crédito)

Crédito de Cencosud a NANDA por $7.8M. Corrige operaciones anteriores.

## 4. Quién Declara IVA Débito

**NANDA SPA** declara el IVA débito de las ventas realizadas a través de PARIS. Esto se determina porque:

- DTE 43 no traspasa la obligación del IVA al emisor (Cencosud)
- En la Liquidación-Factura, el receptor (NANDA) es quien debe reconocer el hecho gravado
- Cencosud solo declara su comisión como ingreso

## 5. Quién Declara IVA Crédito

**NANDA SPA** declara IVA crédito por los servicios que Cencosud le factura:
- DTE 33: IVA Crédito para NANDA por servicios de Cencosud
- DTE 43: IVA Crédito para NANDA por las liquidaciones (el IVA de las ventas líquidas menos comisión)

## 6. Quién Emite el Documento Final

**No se ha encontrado evidencia de DTE emitidos a consumidores finales.** Los archivos en `01_Raw/PARIS/Facturacion/` contienen solo DTEs B2B (Cencosud ↔ NANDA).

El documento final al consumidor (boleta o factura) podría ser:
- Emitido por el sistema POS de PARIS (Cencosud) a nombre del consumidor
- **No está en nuestros archivos RAW** porque esos DTEs van al SII, no a nuestra carpeta

## 7. Conclusión Tributaria

| Pregunta | Respuesta |
|----------|-----------|
| Quién reconoce tributariamente la venta | **NANDA SPA** (a través de DTE 43) |
| Quién declara IVA débito | **NANDA SPA** |
| Quién declara IVA crédito | **NANDA SPA** |
| Quién emite el documento final | **POS PARIS (Cencosud)** al consumidor final, pero no está en nuestros archivos |

**Esto es consistente con un modelo 3P Marketplace**, donde el vendedor (NANDA) es el contribuyente de IVA y Cencosud actúa como intermediario que facilita la operación.

## 8. Contradicción con Certificación Anterior

La certificación previa (PARIS_ECONOMIC_MODEL_FINAL_CERTIFICATION.md) afirmó:

> "DTE 33 emitidos por Cencosud a NANDA SPA — Cencosud es seller of record"
> "DTE 43 liquidaciones — NANDA es proveedor real"

**Esta interpretación es incorrecta.** En el sistema tributario chileno:
- DTE **33** de Cencosud a NANDA representa **servicios prestados por Cencosud a NANDA** (comisiones, logística, etc.)
- DTE **43** de Cencosud a NANDA representa **liquidación de ventas** donde NANDA es el principal/vendedor real
- La ausencia de DTEs de NANDA a Cencosud descarta el modelo 1P (donde el proveedor facturaría al retailer)

**La tributación confirma un modelo 3P Marketplace.**
