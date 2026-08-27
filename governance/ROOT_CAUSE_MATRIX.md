# ROOT CAUSE MATRIX

**Proyecto:** Marketplace Financial AI Engine  
**Fase:** Initial Data Migration Phase II  
**Fecha:** 2026-07-24

---

## Análisis de Causa Raíz de Archivos Pendientes

| Clasificación | Cantidad | Motivo Técnico | Motivo Funcional | Acción Requerida |
| :--- | :--- | :--- | :--- | :--- |
| **YA EXISTE (Ingeridos)** | 144 | SHA256 / Nombre coincidente | Archivo base procesado en el Ledger v1 | Ninguna. Representa el 100% de transacciones principales. |
| **REQUIERE ADAPTADOR (DTE XML)** | 971 | Estructura XML Schema SII | Documentos tributarios de proveedores | Indexar mediante `DTEIndexer` para vincular a `folio_xml`. |
| **NO SOPORTADO (Shopify)** | 20 | Canal e-Commerce directo sin conector SQL | Ventas directas sin comisión de marketplace | Integrar conector Shopify en versión V5. |
| **REQUIERE VALIDACIÓN MANUAL** | 52 | Cartolas bancarias / pasarelas | Reportes de tesorería y liquidación de dinero | Revisión operacional de tesorería. |
| **NO MIGRADO / FORMATO SECUNDARIO** | 155 | Títulos/banners en filas superiores de Excel | Sub-reportes auxiliares o extractos parciales | Carga mediante parser de encabezados variables. |
