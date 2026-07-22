# PARIS — Inventory Ownership Certification

**Fecha:** 2026-06-11
**Auditoría:** FASE 2 de 6 — PARIS Business Model Certification

---

## 1. Dueño del Inventario

| Aspecto | Evidencia | Conclusión |
|---------|-----------|------------|
| ¿Quién listó los productos? | 17 UUIDs de seller en `categoria` | Los sellers listan sus productos |
| ¿Quién fija el precio? | `monto` en RAW refleja precio final | Los sellers definen el precio (Cencosud aplica 15%) |
| ¿Quién posee el stock? | No hay registros de inventario de Cencosud | **Los sellers poseen el inventario** |
| `seller_sku` en RAW | 1,223 SKU únicos en DS, 610 en FF | Los sellers proveen sus propios SKU |

**Clasificación: B) Seller** — Los sellers (NANDA + 16) son dueños del inventario.

## 2. Quién Absorbe Pérdida

| Tipo de Pérdida | Quién Absorbe | Evidencia |
|----------------|--------------|-----------|
| Producto dañado en tránsito | Seller (a través de devolución) | Devolución neta para seller es 85% del monto |
| Producto no vendido | Seller | Nunca se transfiere propiedad a Cencosud |
| Merma operacional | No determinado | Sin evidencia en datos disponibles |

**Clasificación: B) Seller** para pérdida de producto, **C) Compartido** para costos operacionales.

## 3. Quién Absorbe Merma

Sin evidencia directa de merma en los datos disponibles.

**Clasificación: B) Seller** (por defecto, quien posee el inventario absorbe la merma).

## 4. Quién Absorbe Devolución

### 4.1 Estructura de Devolución

Cada devolución tiene la misma estructura que una venta:
- **Gross**: -$X (precio de venta original)
- **Net**: -85% de X (85% del monto bruto)
- **Cencosud absorbe**: 15% del monto bruto

### 4.2 Ejemplos de 30 Devoluciones Muestreadas

```
DEVOLUCIONES - Margen exactamente 15.0% en cada una:
  $-15,990.00 → $-13,592.00 (15.0%)
  $-29,990.00 → $-25,492.00 (15.0%)
  $-26,990.00 → $-22,942.00 (15.0%)
  ... todas iguales
```

### 4.3 Cómo se Distribuye el Costo de Devolución

| Actor | Absorbe | Monto Ejemplo ($29,990) |
|-------|---------|------------------------|
| Seller (NANDA) | 85% del monto | $25,492 devuelto por seller |
| Cencosud | 15% (comisión no percibida) | $4,498 comisión no cobrada |

**Clasificación: C) Compartido** — El seller absorbe el 85% del valor del producto devuelto, Cencosud absorbe el 15% (su comisión no percibida). Estructura típica de marketplace.

### 4.4 Devoluciones en Ledger

Total devoluciones PARIS en ledger: **-$121,458,109**

| Componente | Monto | Absorbido por |
|-----------|-------|---------------|
| Valor del producto devuelto (85%) | -$103,239,393 | Sellers |
| Comisión no percibida (15%) | -$18,218,716 | Cencosud |

## 5. Conclusión

| Aspecto | Clasificación |
|---------|--------------|
| Dueño del inventario | **B) Seller** |
| Quién absorbe pérdida de producto | **B) Seller** |
| Quién absorbe merma | **B) Seller** (por defecto) |
| Quién absorbe devolución | **C) Compartido** (85% seller + 15% Cencosud) |

**Implicancia:** Este perfil de ownership es **característico de un modelo 3P Marketplace**, donde el seller retiene la propiedad del inventario y el riesgo asociado, y el marketplace solo facilita la transacción a cambio de una comisión.
