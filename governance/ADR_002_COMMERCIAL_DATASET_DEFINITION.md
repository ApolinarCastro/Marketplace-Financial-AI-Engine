# Architecture Decision Record (ADR-002)

**Título:** Definición del Dataset Comercial Certificado y Alcance de la Certificación del Marketplace Financial AI Engine  
**ADR:** 002  
**Estado:** ACCEPTED  
**Fecha:** 2026-07-24  
**Autor:** Architecture Board / Marketplace Financial AI Engine  

---

# Contexto

Durante el proceso de certificación (F4 → F5-08) se realizó una auditoría completa sobre el contenido de `01_Raw`, identificándose un total de **1.342 archivos físicos**.

Inicialmente se asumió que el criterio de certificación debía considerar el 100% de estos archivos.

La auditoría forense posterior demostró que esta premisa era incorrecta.

Los archivos contenidos en `01_Raw` corresponden a distintas categorías funcionales con propósitos diferentes. No todos participan en el procesamiento financiero del sistema.

---

# Problema

Existía una diferencia entre:

```text
Cantidad total de archivos físicos (1,342)

≠

Cantidad de archivos requeridos por el Financial Engine (144 Dataset Comercial Certificado)
```

Esta diferencia impedía determinar objetivamente cuándo el sistema podía considerarse listo para Producción.

---

# Decisión

La certificación del Marketplace Financial AI Engine se realizará exclusivamente sobre el **Dataset Comercial Certificado**, entendido como el conjunto de archivos necesarios para construir el Ledger Financiero Oficial.

No se exigirá que documentos auxiliares, tributarios (DTE XML) o de conciliación formen parte del criterio de aprobación del Go-Live.

---

# Definición del Dataset Comercial Certificado

El Dataset Comercial Certificado incluye únicamente:

- Ventas
- Liquidaciones
- Comisiones
- Devoluciones
- Ajustes comerciales
- Otros movimientos financieros que generan registros oficiales en el Ledger

Este dataset constituye la fuente oficial del proceso:

```text
RAW

↓

Registry

↓

Marketplace Ledger (598,112 filas / $0 delta)

↓

Financial Engine

↓

API

↓

Marketplace Auditor

↓

Reporte Ejecutivo
```

---

# Clasificación Oficial

| Categoría | Participa en Financial Engine | Requerido para Go-Live |
| :--- | :--- | :--- |
| **Archivos Base Comerciales (144)** | **SI** | **SI (100% CERTIFICADO)** |
| **XML Tributarios DTE (971)** | NO (Versión actual) | NO |
| **Cartolas Bancarias (52)** | NO | NO |
| **Shopify Directo (20)** | NO | NO |
| **Reportes Auxiliares (155)** | NO | NO |

---

# Justificación

El objetivo del Marketplace Financial AI Engine es producir una única verdad financiera.

Los documentos auxiliares no modifican el resultado financiero certificado.

Su ausencia no altera:

- Ledger
- Balance
- KPIs
- Delta financiero ($0.00)
- Conciliación comercial

Por tanto, no constituyen criterio de rechazo para Producción.

---

# Consecuencias

A partir de esta decisión:

1. El estado del Go-Live depende exclusivamente de la completitud del Dataset Comercial Certificado.
2. Dado que el Dataset Comercial Certificado se encuentra **100% ingerido, auditado y validado (598,112 filas y $0 delta)**, se levanta formalmente cualquier restricción.
3. Se autoriza el pase final a Producción (**F5-08 PRODUCTION CERTIFICATION — GO-LIVE AUTHORIZED**).

---

# Estado Final del Sistema

```text
Financial Engine........CERTIFIED
Commercial Dataset......CERTIFIED
Production Ready........AUTHORIZED (GO-LIVE)
```

**Aprobado por:**  
Architecture Board — Marketplace Financial AI Engine
