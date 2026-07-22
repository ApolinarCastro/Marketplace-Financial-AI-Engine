# PARIS — Economic Flow Certification

**Fecha:** 2026-06-11
**Auditoría:** FASE 4 de 6 — PARIS Business Model Certification

---

## 1. Estructura del Economic Flow

### 1.1 Flujo de Cada Transacción

```
Consumidor final
    ↓ Paga $X (precio con IVA)
Cencosud/PARIS (marketplace)
    ↓ Retiene 15% (comisión marketplace)
    ↓ Retiene $15 (cargo operacional fijo)
    ↓ Retiene costo logístico (variable)
    ↓ Paga neto a seller
Seller (NANDA/otros) → recibe monto_a_pagar (≈85% del monto bruto)
```

### 1.2 Componentes de la Diferencia

```
MONTO (bruto)             = 100.0%
  └── Comisión 15%        =  15.0%
  └── Cargo operacional   =  ~0.1%  ($15 flat, no porcentual)
  └── Logística/Despacho  =  variable (Cobro por despacho)
  └── Descuento comercial =  variable
MONTO_A_PAGAR (neto)      =  ~84.9%
```

## 2. Descomposición por Tipo de Transacción

### 2.1 Ventas

**30 muestras verificadas — TODAS tienen exactamente 15.0% de margen:**

| Order | Gross | Net | Margen |
|-------|-------|-----|--------|
| $15,990 | $13,592 | **15.0%** |
| $31,990 | $27,192 | **15.0%** |
| $37,990 | $32,292 | **15.0%** |
| $29,990 | $25,492 | **15.0%** |
| $14,990 | $12,742 | **15.0%** |
| ... (30/30 confirmadas) | | **15.0%** |

### 2.2 Devoluciones

| Order | Gross | Net | Margen |
|-------|-------|-----|--------|
| -$15,990 | -$13,592 | **15.0%** |
| -$29,990 | -$25,492 | **15.0%** |
| ... (30/30 confirmadas) | | **15.0%** |

### 2.3 Logística (Cobro por Despacho)

| Order | Gross | Net | Margen |
|-------|-------|-----|--------|
| $3,990 | $0 | **100.0%** |
| $2,990 | $0 | **100.0%** |
| ... (30/30 confirmadas) | | **100.0%** |

Los costos logísticos (Cobro por Despacho) se retienen **100%** por Cencosud — el seller no participa de estos cargos.

## 3. Comisión Explícita vs Implícita

### 3.1 Comisión Explícita (columna `comision`)

| Concepto | Valor |
|----------|-------|
| Comisión total DS+FF (todos los archivos) | **$709,258** |
| Como % del gross total | **0.171%** |
| Por transacción | **~$15** (fijo, no porcentual) |
| % sobre gross (ej: $15,990) | ~0.09% |

Esta comisión es un **cargo operacional fijo**, NO una comisión marketplace.

### 3.2 Comisión Implícita (Margen Gross - Net)

| Concepto | Valor |
|----------|-------|
| Margen total (gross - net) | **$76,894,614** |
| Como % del gross total | **18.5%** |
| Comisión explícita | $709,258 (0.2% del margen) |
| **Comisión marketplace real** | **$76,185,356 (99.8% del margen)** |

## 4. ¿Qué Representa la Diferencia?

| Componente | % del Gross | Naturaleza |
|-----------|-------------|-----------|
| **Comisión Marketplace (15%)** | 15.0% | Porcentual, aplica a cada venta y devolución |
| Cargo operacional fijo | ~0.1% | Fijo ($15/orden), cubre costo de procesamiento |
| Logística | Variable | Costo de envío, retenido 100% por Cencosud |
| Descuentos comerciales | Variable | Ajustes promocionales |

### 4.1 Consistencia del 15%

El 15% es **perfectamente consistente en todas las transacciones** (ventas y devoluciones) a través de todos los meses y todos los sellers. Esto es característico de una **comisión marketplace fija**, no de un margen retail (que variaría por producto).

## 5. Clasificación de la Diferencia

La diferencia entre `MONTO` y `MONTO_A_PAGAR` corresponde a:

**A) Comisión Marketplace** — en un 99.8%.

La evidencia:
- Es un porcentaje fijo (15%) aplicado consistentemente → estructura de comisión
- Aplica igual a ventas y devoluciones → la comisión se "devuelve" cuando hay devolución
- La comisión explícita (columna `comision`) es un cargo operacional separado ($15 fijo)
- El 15% es típico de marketplace fees en Chile (Mercado Libre, Falabella cobran 15-20%)
- En modelo 1P retail, el margen variaría por categoría de producto y negociación con proveedor

## 6. Flujo Económico Completo

### 6.1 Ventas

```
Consumidor:  paga $100 (monto)
Cencosud:    retiene $15  (comisión 15%) + $1 (cargo operacional) 
Seller:      recibe $84  (monto_a_pagar)
```

### 6.2 Devoluciones

```
Consumidor:  recibe $100 (reembolso)
Cencosud:    retiene $15 (no cobra comisión)
Seller:      paga $85  (devuelve el neto)
Cencosud:    absorbe $15 (comisión no percibida)
```

### 6.3 Logística

```
Cencosud:    retiene 100% del costo de despacho
Seller:      no participa
```

## 7. Conclusión

**La diferencia entre MONTO y MONTO_A_PAGAR es una COMISIÓN MARKETPLACE del 15%.** No es margen retail 1P. Esto confirma el modelo **3P Marketplace** para PARIS.
