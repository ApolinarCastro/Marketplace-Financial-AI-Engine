# Aristas Completas por Marketplace

## MERCADO LIBRE

### 1. Sección CARGOS
- **Cargo por venta**: Comisión principal del marketplace
  - Porcentaje por categoría
  - Costo por ofrecer cuotas
  - Costo fijo (para productos bajo precio mínimo)
  - Descuentos comerciales aplicados
- **Cargo por envío**: Costos logísticos
- **Cargo por publicación**: Costos de publicidad y promoción
- **Percepciones impositivas**: Retenciones fiscales según condición
- **Estado del cargo**: Descontado automáticamente o pendiente de pago manual
- **Bonificaciones/Anulaciones**: Créditos y reversiones

### 2. Sección DESCUENTOS
- Descuentos comerciales por acuerdos
- Motivo del descuento

### 3. Sección VENTA
- Número de venta
- Fecha de venta
- Total de la venta (GMV)
- Número de pago (para conciliación con Mercado Pago)
- Canal de venta
- Tipo de medio de pago
- Tipo de operación

### 4. Sección ENVÍO
- Número de envío
- Número de paquete
- Costo de envío a cargo del cliente
- Modalidad de envío (Mercado Envíos, Full, etc.)

### 5. Sección PUBLICACIÓN
- Número de publicación
- Título del producto
- Cuotas agregadas en publicación
- Categoría
- Código ML (SKU)

### 6. Datos de POSCOBRO (Devoluciones)
- Fecha de devolución
- ID de transacción
- Monto de devolución (refund)
- SKU afectado
- Estado (refunded)

### Métricas Calculables:
- Venta Neta = GMV - Comisión - Costo Envío - Devoluciones
- Tasa de devolución
- Costo total de marketplace
- Rentabilidad por canal

---

## PARÍS MARKETPLACE

### 1. Reportes de FINANZAS
- **Transacciones**: Filtrable por tipo, estado y antigüedad
  - Número de orden
  - Código SKU
  - Descripción del producto
  - Montos (GMV)
  - Comisión
  - Estado de la transacción

### 2. Reportes Disponibles (según documentación)
- **Finanzas**: Cobros y ventas detalladas
- **Comercial**: Datos de ventas y rendimiento
- **Productos**: Información de catálogo
- **Logística**: Envíos y despachos
- **Órdenes**: Gestión de pedidos
- **Fulfillment**: Operaciones de almacenamiento
- **Reputación**: Métricas de desempeño

### 3. Estados de Transacción
- Pendiente
- Completado
- Cancelado
- Devuelto (según proceso de devolución)

### 4. Comisiones
- Comisión por categoría (variable según familia de producto)
- Porcentaje aplicado sobre el precio de venta

### 5. Aristas Faltantes en Reporte Actual
- Devoluciones (proceso de post-venta)
- Cancelaciones
- Ajustes de precio
- Promociones y descuentos
- Costos de envío
- Estados de pedido (entregado, en tránsito, cancelado)
- Penalizaciones por incumplimiento
- Datos de fulfillment

### Métricas Calculables:
- Venta Neta = GMV - Comisión
- Tasa de cancelación
- Tasa de devolución
- Rendimiento por categoría

---

## RIPLEY MARKETPLACE

### 1. VENTAS (Pedidos)
- Fecha de creación
- Número de pedido
- SKU de oferta (Tienda)
- Importe (GMV)
- Comisión (sin impuestos)
- Estado del pedido

### 2. COMISIONES
- **Comisión por categoría**: Variable según tipo de producto
- **Costo fijo operacional**: $990 por unidad vendida ≤ $5,000
  - Aplica a todas las modalidades de entrega

### 3. AJUSTES FINANCIEROS (Historial)
- Fecha de creación
- Número de pedido
- Importe (negativo para reembolsos)
- SKU de oferta
- Tipo de ajuste:
  - Reembolsos
  - Cancelaciones
  - Penalizaciones

### 4. COSTOS LOGÍSTICOS
- **Modalidades de entrega**:
  - Flota Propia
  - Flujo Chilexpress (retiro en bodega o entrega en sucursal)
  - Flujo Blue Express (retiro en bodega o entrega en sucursal)
  - Flujo Crossdock Ripley
  - Retiro Cercano Proveedor
- Costos variables según peso y dimensiones del paquete

### 5. POST-VENTA
- Devoluciones (primeros 90 días)
- Cambios
- Reparaciones
- Incidencias en Seller Center

### 6. Aristas Faltantes en Reporte Actual
- Costos logísticos detallados por modalidad
- Tipo de ajuste (separar devoluciones de cancelaciones)
- Promociones y descuentos
- Penalizaciones por incumplimiento
- Estados detallados de pedido
- Datos de fulfillment

### Métricas Calculables:
- Venta Neta = GMV - Comisión - Costo Fijo - Costo Logístico - Ajustes
- Tasa de devolución
- Tasa de cancelación
- Costo total de marketplace
- Rentabilidad por modalidad de envío

---

## DIMENSIONES TRANSVERSALES PARA TODOS LOS MARKETPLACES

### 1. Dimensión TEMPORAL
- Fecha de transacción
- Fecha de pago/liquidación
- Fecha de devolución/cancelación
- Período de reporte

### 2. Dimensión PRODUCTO
- SKU
- Descripción/Título
- Categoría
- Precio de venta (GMV)

### 3. Dimensión TRANSACCIÓN
- ID de transacción/pedido
- Tipo de transacción:
  - Venta
  - Devolución
  - Cancelación
  - Ajuste
  - Promoción
- Estado:
  - Pendiente
  - Completado
  - Cancelado
  - Devuelto
  - Reembolsado

### 4. Dimensión FINANCIERA
- GMV (Gross Merchandise Value)
- Comisión del marketplace
- Costos de envío
- Costos fijos
- Descuentos y promociones
- Ajustes y devoluciones
- Venta Neta
- Margen Bruto

### 5. Dimensión LOGÍSTICA
- Modalidad de envío
- Costo de envío
- ¿Quién paga el envío? (vendedor/comprador)
- Estado de envío

### 6. Dimensión MARKETPLACE
- Nombre del marketplace (ML, París, Ripley)
- Canal de venta
- Políticas específicas

---

## MODELO DE DATOS PROPUESTO

### Tabla de Hechos: TRANSACCIONES_UNIFICADAS
- ID_Transaccion (PK)
- Fecha
- ID_Marketplace (FK)
- ID_Producto (FK)
- ID_Tipo_Transaccion (FK)
- ID_Estado (FK)
- GMV
- Comision
- Costo_Envio
- Costo_Fijo
- Descuentos
- Ajustes
- Venta_Neta

### Dimensiones:
1. **DIM_MARKETPLACE**
   - ID_Marketplace (PK)
   - Nombre
   - Pais

2. **DIM_PRODUCTO**
   - ID_Producto (PK)
   - SKU
   - Descripcion
   - Categoria
   - COGS

3. **DIM_TIEMPO**
   - ID_Fecha (PK)
   - Fecha
   - Año
   - Mes
   - Trimestre
   - Semana

4. **DIM_TIPO_TRANSACCION**
   - ID_Tipo (PK)
   - Tipo (Venta, Devolución, Cancelación, Ajuste)

5. **DIM_ESTADO**
   - ID_Estado (PK)
   - Estado (Pendiente, Completado, Cancelado, Devuelto)

6. **DIM_LOGISTICA**
   - ID_Logistica (PK)
   - Modalidad_Envio
   - Proveedor_Logistico
   - Quien_Paga_Envio
