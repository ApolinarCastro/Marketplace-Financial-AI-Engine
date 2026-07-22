# PARIS — RFC Impact Decision

**Fecha:** 2026-06-11
**Auditoría:** FASE 5 de 6 — PARIS Business Model Certification

---

## 1. Contexto

El **RFC_PARIS_ECONOMIC_MODEL** fue diseñado para modificar la implementación del modelo económico de PARIS, asumiendo que el modelo actual (net revenue) era incorrecto y debía migrarse a un modelo de gross revenue + comisión explícita.

El RFC asumía que PARIS operaba como **1P Dropshipping** y que el modelo contable actual no reflejaba correctamente la realidad económica.

## 2. Determinación del Modelo

Con base en la evidencia de FASE 1-4:

| Evidencia | Conclusión |
|-----------|-----------|
| 17 sellers independientes (UUIDs en `categoria`) | Marketplace multi-seller |
| DTE 43 (Liquidación-Factura) de Cencosud a NANDA | Cencosud es agente, NANDA es principal |
| Ausencia de DTE de NANDA a Cencosud | Inconsistente con 1P (proveedor→retailer) |
| Consistencia exacta del 15% en todas las Ventas | Comisión marketplace fija, no margen retail |
| Devoluciones con mismo 15% | Comisión no percibida, consistente con marketplace |
| Logística 100% retenida por Cencosud | Costo de operación del marketplace |

**PARIS es 3P Marketplace.** No 1P Retail ni 1P Dropshipping.

## 3. Evaluación del RFC

### Escenario 1: PARIS es 1P (DESCARTADO por evidencia)

| Pregunta | Respuesta |
|----------|-----------|
| ¿Debe ejecutarse RFC? | **N/A** — PARIS no es 1P. Escenario descartado. |

### Escenario 2: PARIS es 3P (CONFIRMADO por evidencia)

| Pregunta | Respuesta |
|----------|-----------|
| ¿Debe ejecutarse RFC_PARIS_ECONOMIC_MODEL? | **NO** |
| ¿Por qué? | El modelo actual (net revenue) es el correcto para un marketplace 3P. Cencosud debe reconocer solo su comisión como ingreso, no el valor bruto de las transacciones. |

## 4. Modelo Actual vs Modelo RFC

| Aspecto | Modelo Actual | Modelo RFC Propuesto | Correcto para 3P |
|---------|--------------|---------------------|-------------------|
| Ingreso en ledger | **Neto** (monto_a_pagar) | Gross + comisión explícita | **Actual** ✅ |
| Comisión | Implícita (15% en spread) | Explícita | **Actual** (el 15% es comisión implícita) |
| Gross revenue | No registrado como ingreso | Registrado como ingreso | **Actual** (en 3P, el gross no es ingreso de Cencosud) |
| Tratamiento devoluciones | Neto (85%) | Gross + ajuste comisión | **Actual** (más simple y correcto) |

### 4.1 Por qué el Modelo Actual es Correcto para 3P

En un modelo 3P marketplace:
- Cencosud **NO es dueño** del producto
- Cencosud **NO reconoce** la venta como ingreso propio
- Cencosud **solo reconoce** su comisión como ingreso
- El ledger registra el neto (monto_a_pagar) porque eso es lo que Cencosud paga al seller
- El gross no es ingreso de Cencosud — es un "paso" de fondos del consumidor al seller

### 4.2 Diferencias con el Modelo RFC

El RFC_PARIS_ECONOMIC_MODEL propone:
- Registrar gross como ingreso (incorrecto para 3P — inflaría los ingresos de Cencosud)
- Hacer explícita la comisión (innecesario — la comisión implícita del 15% es la correcta)

## 5. Decisión

| Decisión | Veredicto |
|----------|-----------|
| **RFC_PARIS_ECONOMIC_MODEL** | **RECHAZADO** ❌ — No debe ejecutarse |
| **Modelo actual (net revenue)** | **CORRECTO** ✅ — Debe mantenerse |
| **Acción** | Archivar el RFC. No se requiere cambio. |

## 6. Justificación

El RFC_PARIS_ECONOMIC_MODEL estaba basado en una premisa falsa (que PARIS es 1P). La evidencia demuestra que PARIS es **3P Marketplace**, y el modelo contable actual (net revenue = monto_a_pagar en ledger) es el apropiado para esta realidad económica.

Implementar el RFC cambiaría el modelo de net revenue a gross revenue, lo cual:
1. Inflaría artificialmente los ingresos de Cencosud (registrando $338M en vez de ~$77M)
2. Distorsionaría la comparabilidad con otros marketplaces
3. Crearía un riesgo tributario (reconocer ventas que no son de Cencosud)
4. No cambiaría el resultado neto (RN sería el mismo)
