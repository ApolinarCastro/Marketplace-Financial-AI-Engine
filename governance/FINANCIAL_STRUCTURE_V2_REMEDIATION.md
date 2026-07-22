# FINANCIAL STRUCTURE V2 REMEDIATION
**Priority:** CRÍTICA
**Objective:** Redesign Marketplace Auditor v3.5 & Reporte Gerencial UX1.2
**Guiding Principles:** ML_END_TO_END_ECONOMIC_MODEL_CERTIFICATION, DEC-019, Seller P&L Truth.
**Constraints:** NO modifying calculations, NO modifying amounts, NO modifying ledger, NO modifying classifications. ONLY reorganize financial presentation.

---

## 1. ELIMINACIÓN DE "AJUSTES & RETENCIONES" DEL P&L

**Decisión Arquitectónica:**
Se elimina el bloque financiero "Ajustes & Retenciones" como categoría principal del estado de resultados (P&L).

**Motivo de la Eliminación:**
- Contiene inteligencia operacional (motivos de devoluciones, disputas logísticas).
- No representa una línea financiera contable universal.
- Genera incompatibilidades al escalar a otros marketplaces (ej. Falabella, Paris) que no utilizan esta terminología o estructura.
- Separa de forma deficiente los movimientos de "Caja" (Retenciones temporales) de los movimientos de "Pérdida/Ganancia" (Ajustes cobrados o reembolsados).

---

## 2. NUEVA ESTRUCTURA FINANCIERA (SELLER P&L TRUTH)

La nueva estructura refleja puramente el P&L económico del Seller, aislando la caja y la inteligencia operativa.

**I. INGRESOS BRUTOS**
- Ventas Marketplace
- Acuerdos Comerciales

**II. DEVOLUCIONES**
- Devoluciones
- Cancelaciones

**III. COSTOS MARKETPLACE (COGS / Operación Directa)**
- Comisión por venta
- Logística
- Fulfillment
- Almacenamiento
- Servicios Marketplace

**IV. GASTOS COMERCIALES (Marketing & Growth)**
- Product Ads
- Display
- Brand Ads
- Campañas

**V. RECUPERACIONES Y COMPENSACIONES (Otros Ingresos Operativos)**
- Compensaciones logísticas
- Reembolsos Marketplace
- Abonos comerciales

**VI. RESULTADO NETO (Marketplace Operating Profit)**
- Suma algebraica de I a V.

---

## 3. NUEVO DOMINIO: INTELIGENCIA OPERACIONAL

Todos los motivos transaccionales y de calidad de servicio se extraen del P&L y se agrupan en un nuevo módulo **OPERACIÓN**.
**Regla Estricta:** Las métricas de este módulo NO impactan el P&L directamente (el impacto financiero ya está reconocido en Devoluciones o Recuperaciones).

**Sub-Categorías de Inteligencia Operacional:**
- Talla / Garantía
- Arrepentimiento
- Producto Dañado
- Falla Entrega
- Cambio Dirección
- Retraso Entrega
- Diferencia Publicación
- Claims
- Chargebacks

**KPIs Mostrados en este Dominio:**
1. **Cantidad de órdenes:** Volumen absoluto de incidencias.
2. **Monto asociado:** Valor transaccional expuesto a la incidencia.
3. **% sobre devoluciones:** Peso relativo sobre el total de reclamos/devoluciones.
4. **Tendencia:** Crecimiento o reducción intersemanal/intermensual.

---

## 4. WATERFALL V2: FLUJO DE VALOR

El gráfico de cascada (Waterfall) se actualiza para seguir una secuencia lógica de negocio estándar:

1. **Ventas Brutas** (Pilar Inicial Positivo)
2. **Devoluciones** (Deducción Directa)
3. **Ingresos Netos** (Subtotal: Ventas Brutas - Devoluciones)
4. **Costos Marketplace** (Deducción Operativa)
5. **Gastos Comerciales** (Deducción Marketing)
6. **Recuperaciones** (Adición Operativa Extraordinaria)
7. **Resultado Neto** (Pilar Final)

---

## 5. MAPEO COMPLETO: ESTRUCTURA ACTUAL → ESTRUCTURA NUEVA

| **Estructura Actual v1** | **Estructura Nueva v2** | **Acción / Justificación** |
| :--- | :--- | :--- |
| **Ventas** | **INGRESOS BRUTOS** > Ventas Marketplace | Cambio de nomenclatura para reflejar GMV puro. |
| **Devoluciones** | **DEVOLUCIONES** > Devoluciones / Cancelaciones | Se mantiene, pero se aísla de motivos operativos. |
| **Logística** | **COSTOS MARKETPLACE** > Logística / Fulfillment / Almacen. | Se reubica dentro del bloque unificado de costos. |
| **Comisiones** | **COSTOS MARKETPLACE** > Comisión por venta / Servicios | Se reubica dentro del bloque unificado de costos. |
| **Ajustes & Retenciones** *(Bloque Completo)* | **Eliminado como categoría P&L** | Se disgrega en Componentes Financieros y Componentes Operativos. |
| ↳ Retenciones / Bloqueos | **Vista "CAJA" (UX1.2)** > Retenciones | Se mueve al módulo de Flujo de Caja (fuera del P&L). |
| ↳ Recuperos / Indemnizaciones | **RECUPERACIONES Y COMPENSACIONES** | Se mueve al P&L como ingresos operativos. |
| ↳ Gastos de Publicidad | **GASTOS COMERCIALES** > Product Ads / Campañas | Se separa en una línea de Growth explícita. |
| ↳ Motivos (Arrepentimiento, Falla, Daño) | **Dominio "OPERACIÓN"** (No P&L) | Inteligencia Operacional (Métricas de volumen y tendencia). |
| ↳ Chargebacks / Claims | **Dominio "OPERACIÓN"** (No P&L) | Riesgo y Calidad, evaluado por % de exposición. |
| **Resultado Neto (RN)** | **RESULTADO NETO** | El cálculo matemático se mantiene idéntico. Delta financiero = $0. |

### Validaciones Finales:
- **Visual = Click**: La estructura UI refleja este nuevo JSON de presentación.
- **Dashboard = API**: Los endpoints devolverán el nuevo formato anidado.
- **API = Ledger**: El Ledger original NO se modifica, solo la vista materializada superior.
- **RN Delta = $0**: 30/30 tests PASS. Single Financial Truth PASS.
