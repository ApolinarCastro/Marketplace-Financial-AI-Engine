# CERTIFICACIÓN DE DEFECTO 003: COSTOS MARKETPLACE
*Fecha de Certificación: 2026-06-08 17:40:30*
*Mercado: ML*
*Periodo: 2026-02*

## 1. QUERY LEDGER UTILIZADA
Se consultó directamente `marketplace_ledger_v1` utilizando la lógica productiva de exclusión y sumatoria.
```sql
SELECT 
    c.marketplace,
    strftime(c.fecha, '%Y-%m'),
    COALESCE(SUM(CASE WHEN c.financial_group IN ('costos_operacionales', 'costos_comerciales', 'ajustes') AND COALESCE(c.include_in_operational_pnl,1)=1 THEN c.monto ELSE 0 END), 0) as total_costos
FROM marketplace_ledger_v1 c
WHERE c.marketplace = 'ML' AND c.fecha BETWEEN '2026-02-01' AND '2026-02-28'
GROUP BY c.marketplace, strftime(c.fecha, '%Y-%m')
```

## 2. EXTRACCIÓN DE FUENTES (TOTALES)
*   **Ledger Total:** `$-4,598,814.50`
*   **Summary API:** `$-4,598,814.50`
*   **Waterfall API:** `$-4,598,814.50`
*   **Breakdown API:** `$-4,598,814.50`
*   **UI Dashboard:** `$-4,598,814.50`

## 3. TABLA DE CONCILIACIÓN (TOTALES)

| Fuente | Valor |
| :--- | :--- |
| **Ledger** | `$-4,598,814.50` |
| **Summary API** | `$-4,598,814.50` |
| **Waterfall API** | `$-4,598,814.50` |
| **Breakdown API** | `$-4,598,814.50` |
| **UI** | `$-4,598,814.50` |
| **Delta Máximo** | **$0.00** |

## 4. DESGLOSE INTERNO (COMPOSICIÓN DE COSTOS)
A continuación se demuestra que la composición detallada por categoría también coincide con el Ledger 1:1.

| Concepto | Ledger | Breakdown API | Delta |
| :--- | :--- | :--- | :--- |
| Comisiones | `$-2,374,025.00` | `$-2,374,025.00` | `$0.00` |
| Fulfillment | `$-111,141.00` | `$-111,141.00` | `$0.00` |
| Logística | `$-1,253,092.50` | `$-1,253,092.50` | `$0.00` |
| Otros | `$194,303.00` | `$194,303.00` | `$0.00` |
| Servicios | `$-1,054,859.00` | `$-1,054,859.00` | `$0.00` |

## 5. EVIDENCIA VISUAL
Se adjunta la captura del entorno activo en el Dashboard P&L mostrando que la UI representa fielmente la API sin hardcodes.
![Dashboard Costos Marketplace](evidence_costos_marketplace.png)
