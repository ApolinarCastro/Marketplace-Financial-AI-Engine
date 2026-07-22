import duckdb
import pandas as pd
import json
import os
from pathlib import Path

db_path = "data/db/meli_financial_v4_copy.db"
conn = duckdb.connect(db_path, read_only=True)

artifacts_dir = Path("C:/Users/ASUS Zenbook/.gemini/antigravity-ide/brain/2c921f1a-4258-4b8e-be46-1ad937059ee6")

# FASE 1: COBERTURA DE COLUMNAS
df_cov = conn.execute("""
    SELECT 
        strftime(fecha, '%Y-%m') as periodo,
        strftime(fecha, '%Y') as ano,
        COUNT(*) as total_filas,
        COUNT(monto_bruto) as count_monto_bruto,
        COUNT(comision_marketplace) as count_comision_marketplace,
        COUNT(monto) as count_monto,
        -- Assuming monto is monto_a_pagar
        COUNT(monto) as count_monto_a_pagar 
    FROM marketplace_ledger_v1
    WHERE marketplace = 'PARIS' AND detalle = 'Venta'
    GROUP BY strftime(fecha, '%Y-%m'), strftime(fecha, '%Y')
    ORDER BY periodo
""").df()

total_filas = int(df_cov['total_filas'].sum())
total_bruto = int(df_cov['count_monto_bruto'].sum())
total_comision = int(df_cov['count_comision_marketplace'].sum())

cov_md = f"""# PARIS V2 COLUMN COVERAGE CERTIFICATION

## Cobertura Histórica Total
- Total Filas: {total_filas}
- Filas con monto_bruto: {total_bruto}
- Filas con comision_marketplace: {total_comision}
- Filas con monto: {int(df_cov['count_monto'].sum())}

## Cobertura por Período
```
{df_cov.to_string(index=False)}
```
"""
with open(artifacts_dir / "PARIS_V2_COLUMN_COVERAGE_CERTIFICATION.md", "w", encoding="utf-8") as f:
    f.write(cov_md)

# FASE 2: NULL ANALYSIS
df_null = conn.execute("""
    SELECT 
        strftime(fecha, '%Y-%m') as mes,
        strftime(fecha, '%Y') as ano,
        SUM(CASE WHEN monto_bruto IS NULL THEN 1 ELSE 0 END) as null_bruto,
        SUM(CASE WHEN comision_marketplace IS NULL THEN 1 ELSE 0 END) as null_comision,
        SUM(CASE WHEN monto_bruto = 0 THEN 1 ELSE 0 END) as cero_bruto,
        SUM(CASE WHEN comision_marketplace = 0 THEN 1 ELSE 0 END) as cero_comision
    FROM marketplace_ledger_v1
    WHERE marketplace = 'PARIS' AND detalle = 'Venta'
    GROUP BY strftime(fecha, '%Y-%m'), strftime(fecha, '%Y')
    ORDER BY mes
""").df()

null_md = f"""# PARIS V2 NULL ANALYSIS

## Resumen de Ausencias y Ceros
```
{df_null.to_string(index=False)}
```
"""
with open(artifacts_dir / "PARIS_V2_NULL_ANALYSIS.md", "w", encoding="utf-8") as f:
    f.write(null_md)

# FASE 3: FALLBACK DETECTION
df_fallback = conn.execute("""
    SELECT 
        COUNT(*) as total_filas,
        SUM(CASE WHEN ROUND(monto_bruto, 2) = ROUND(monto / 0.85, 2) THEN 1 ELSE 0 END) as fallback_bruto_085,
        SUM(CASE WHEN ROUND(comision_marketplace, 2) = ROUND(monto_bruto - monto, 2) THEN 1 ELSE 0 END) as derivada_comision
    FROM marketplace_ledger_v1
    WHERE marketplace = 'PARIS' AND detalle = 'Venta'
""").df()

fallback_md = f"""# PARIS V2 FALLBACK CERTIFICATION

## Resultados
- Total Filas: {df_fallback['total_filas'].iloc[0]}
- Filas donde monto_bruto = monto / 0.85: {df_fallback['fallback_bruto_085'].iloc[0]}
- Filas donde comision_marketplace = monto_bruto - monto: {df_fallback['derivada_comision'].iloc[0]}

Nota: El cálculo `comision_marketplace = monto_bruto - monto` puede ser derivado matemáticamente válido en datos reales o un cálculo inyectado. La presencia de `monto_bruto = monto / 0.85` sería el verdadero indicador de fallback sintético si es dominante.
"""
with open(artifacts_dir / "PARIS_V2_FALLBACK_CERTIFICATION.md", "w", encoding="utf-8") as f:
    f.write(fallback_md)

# FASE 4: SOURCE TRACEABILITY
df_trace = conn.execute("""
    SELECT 
        fecha, archivo_origen, monto, monto_bruto, comision_marketplace 
    FROM marketplace_ledger_v1 
    WHERE marketplace = 'PARIS' AND detalle = 'Venta'
    ORDER BY RANDOM() LIMIT 30
""").df()

trace_md = f"""# PARIS V2 SOURCE TRACEABILITY

## Muestra Aleatoria
```
{df_trace.to_string(index=False)}
```
"""
with open(artifacts_dir / "PARIS_V2_SOURCE_TRACEABILITY.md", "w", encoding="utf-8") as f:
    f.write(trace_md)

# FASE 5: PERIOD COVERAGE
per_md = f"""# PARIS V2 PERIOD COVERAGE

## Análisis de Meses
```
{df_cov[['periodo', 'total_filas', 'count_monto_bruto']].to_string(index=False)}
```
"""
with open(artifacts_dir / "PARIS_V2_PERIOD_COVERAGE.md", "w", encoding="utf-8") as f:
    f.write(per_md)

# FASE 6: GO / NO GO
null_bruto = int(df_null['null_bruto'].sum())
null_com = int(df_null['null_comision'].sum())
fallback_085 = int(df_fallback['fallback_bruto_085'].sum())

if total_filas > 0 and null_bruto == 0 and null_com == 0 and fallback_085 == 0:
    verdict = "GO"
elif total_filas > 0 and (null_bruto > 0 or null_com > 0):
    verdict = "NO GO"
else:
    verdict = "GO WITH WARNINGS"

gate_md = f"""# PARIS V2 IMPLEMENTATION GATE

1. ¿monto_bruto tiene cobertura 100%? {'Sí' if null_bruto == 0 and total_filas > 0 else 'No'}
2. ¿comision_marketplace tiene cobertura 100%? {'Sí' if null_com == 0 and total_filas > 0 else 'No'}
3. ¿Existen NULL? {'Sí' if (null_bruto > 0 or null_com > 0) else 'No'}
4. ¿Existen fallback? {'Sí' if fallback_085 > 0 else 'No'}
5. ¿Es seguro eliminar la lógica actual? {'Sí' if verdict == 'GO' else 'No'}
6. ¿Puede ejecutarse la remediación final? {'Sí' if verdict == 'GO' else 'No'}

## VEREDICTO FINAL
{verdict}
"""
with open(artifacts_dir / "PARIS_V2_IMPLEMENTATION_GATE.md", "w", encoding="utf-8") as f:
    f.write(gate_md)

print(verdict)
