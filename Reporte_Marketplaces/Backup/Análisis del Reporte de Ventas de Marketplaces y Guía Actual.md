# Análisis del Reporte de Ventas de Marketplaces y Guía Actual

## Estructura del Archivo ReporteVentasMP.xlsx

### Hojas Procesadas (Limpias):
1. **ML_VENTAS_LIMPIO** (2,144 registros)
   - Columnas: FECHA, ID_TRANSACCION, GMV, COMISION, MONTO_DEVOLUCION, Venta_Neta_Ajustada, SKU
   - Incluye: Ventas y devoluciones combinadas

2. **PARIS_VENTAS_LIMPIO** (473 registros)
   - Columnas: FECHA, ID_TRANSACCION, GMV, COMISION, SKU, ESTADO
   - Incluye: Solo ventas (todas con estado "Pendiente")
   - **FALTA**: Devoluciones, ajustes, cancelaciones

3. **RIPLEY_VENTAS_LIMPIO** (1,181 registros)
   - Columnas: FECHA, ID_TRANSACCION, SKU, GMV, COMISION, MONTO_DEVOLUCION, Venta_Neta_Ajustada
   - Incluye: Ventas y devoluciones combinadas

### Hojas RAW (Datos Fuente):
4. **ML_Facturacion_RAW** (3,658 registros)
   - Datos de facturación de Mercado Libre
   - Incluye múltiples tipos de cargos por transacción

5. **ML_Poscobro_RAW** (367 registros)
   - Devoluciones (refunds) de Mercado Libre

6. **Ripley_Ajustes** (194 registros)
   - Ajustes financieros negativos (reembolsos, cancelaciones)

7. **Ripley_Ventas** (1,187 registros)
   - Datos de ventas de Ripley

## Análisis de la Guía Actual

### Fortalezas:
- Proceso ETL bien estructurado
- Automatización mediante Power Query
- Carga incremental desde carpetas
- Combinación de ventas y devoluciones para ML y Ripley

### Limitaciones Identificadas:

#### 1. **Aristas Faltantes por Marketplace**

**MERCADO LIBRE:**
- ✅ Ventas
- ✅ Devoluciones (refunds)
- ❌ Envíos y costos logísticos
- ❌ Promociones y descuentos
- ❌ Cargos adicionales (financiamiento, publicidad)
- ❌ Cancelaciones
- ❌ Reclamos y mediaciones
- ❌ Costos de envío al comprador vs. vendedor

**PARÍS:**
- ✅ Ventas
- ❌ Devoluciones
- ❌ Cancelaciones
- ❌ Ajustes de precio
- ❌ Promociones
- ❌ Costos de envío
- ❌ Estados de pedido (entregado, en tránsito, cancelado)
- ❌ Penalizaciones

**RIPLEY:**
- ✅ Ventas
- ✅ Ajustes (parcial)
- ❌ Devoluciones completas vs. parciales
- ❌ Cancelaciones
- ❌ Promociones
- ❌ Costos de envío
- ❌ Penalizaciones por incumplimiento
- ❌ Estados de pedido

#### 2. **Dimensiones de Análisis Faltantes**
- Estado del pedido (pendiente, entregado, cancelado, devuelto)
- Tipo de transacción (venta, devolución, ajuste, cancelación)
- Canal de venta (marketplace específico)
- Método de envío
- Método de pago
- Región/ubicación del comprador
- Categoría de producto
- Rentabilidad neta por transacción

#### 3. **Métricas Gerenciales Faltantes**
- Tasa de devolución por marketplace
- Tasa de cancelación
- Costo total de marketplace (comisión + envío + promociones)
- Margen neto después de todos los costos
- Ticket promedio por marketplace
- Productos más devueltos
- Impacto de promociones en rentabilidad

## Recomendaciones para la Nueva Guía

### 1. Expandir la Estructura de Datos
- Incluir todas las aristas de cada marketplace
- Crear tablas separadas por tipo de transacción
- Unificar con un modelo de datos relacional

### 2. Nuevas Consultas Power Query
- ML_Envios_RAW
- ML_Promociones_RAW
- ML_Cargos_Adicionales_RAW
- Paris_Devoluciones_RAW
- Paris_Cancelaciones_RAW
- Paris_Estados_RAW
- Ripley_Devoluciones_RAW (separado de ajustes)
- Ripley_Cancelaciones_RAW
- Ripley_Envios_RAW

### 3. Modelo de Datos Mejorado
- Tabla de hechos: TRANSACCIONES_UNIFICADAS
- Dimensiones: DIM_MARKETPLACE, DIM_PRODUCTO, DIM_TIEMPO, DIM_ESTADO, DIM_TIPO_TRANSACCION

### 4. Dashboard Ampliado
- KPIs por marketplace
- Análisis de devoluciones
- Análisis de costos totales
- Rentabilidad neta
- Comparativa entre marketplaces
