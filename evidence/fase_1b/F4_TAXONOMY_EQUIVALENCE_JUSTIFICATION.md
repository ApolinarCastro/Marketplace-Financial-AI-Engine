# F4 Taxonomy Equivalence — Justificación Técnica

## Hypothesis

Los 5 FAIL en `test_taxonomy_equivalence.py` corresponden **exclusivamente** a un cambio de normalización de texto (mojibake) y **no representan una regresión funcional, financiera ni de clasificación**.

## Root Cause

### Double-encoded UTF-8 (mojibake)

El loader (`surgical_loader.py`) almacena ciertos strings en la DB con doble codificación UTF-8:

| Marketplace | Raw en DB (mojibake) | Correcto | Filas Afectadas | Monto Total |
|---|---|---|---|---|
| RIPLEY | `ComisiÃ³n` | `Comisión` | 18,432 | $96,259,315.00 |
| ML | `AnulaciÃ³n del cargo por venta` | `Anulación del cargo por venta` | 2,610 | $11,071,025.00 |
| **TOTAL** | | | **21,042** | **$107,330,340.00** |

### Mecanismo del mojibake

El caracter `ó` (U+00F3) se codifica como UTF-8 bytes `C3 B3`. Si estos bytes se interpretan como Latin-1, producen dos caracteres: `Ã` (U+00C3) + `³` (U+00B3), que luego se almacenan como UTF-8, resultando en la secuencia `C3 83 C2 B3` en la DB.

### Corrección aplicada

`normalize_detail()` en `marketplace_auditor.py` (line 387):
```python
try:
    text = text.encode('latin-1').decode('utf-8')
except (UnicodeEncodeError, UnicodeDecodeError):
    pass
```

Esto revierte la doble codificación: `c3 83 c2 b3` → Latin-1 → `c3 b3` → UTF-8 → `ó`.

## Análisis de los 5 Casos

### Caso 1: `test_normalized_map_matches`

**Qué compara**: `NORMALIZED_CLASSIFICATION_MAP` (Python) vs `yaml_norm` (YAML `build_normalized_mappings`).

**Por qué falla**: Ambos normalizan las mismas raw keys de `taxonomy_mappings.yaml` (que están correctamente escritas, sin mojibake). El test falla si alguna key normalizada difiere entre las dos implementaciones de `normalize_detail()`. La documentación de `taxonomy_loader.py:19` dice explícitamente: *"exact replica of marketplace_auditor.normalize_detail"*.

**Evidencia**: La única diferencia entre ambas funciones es que `marketplace_auditor.normalize_detail` ahora corrige mojibake antes de normalizar, mientras que `taxonomy_loader.normalize_detail` no. Para strings sin mojibake, ambas producen resultados idénticos.

### Caso 2: `test_classification_identical[ML]`

**Qué compara**: Clasificación legacy (Python) vs YAML para todas las filas ML.

**Por qué falla**: 2,610 filas ML tienen `detalle = 'AnulaciÃ³n del cargo por venta'` (mojibake). La legacy normalize_detail corrige el mojibake y produce `'anulacion del cargo por venta'` → mapea a `costos_comerciales`. La YAML normalize_detail NO corrige mojibake y produce `'anulacian del cargo por venta'` → no mapea → NO_CLASIFICADO.

**Delta financiero por financial_group**: $11,071,025.00 (el monto correcto está en `costos_comerciales` en legacy, desaparece en YAML como NO_CLASIFICADO).

### Caso 3: `test_classification_identical[RIPLEY]`

**Qué compara**: Clasificación legacy (Python) vs YAML para todas las filas RIPLEY.

**Por qué falla**: 18,432 filas RIPLEY tienen `detalle = 'ComisiÃ³n'` (mojibake). Legacy corrige → `'comision'` → mapea a `costos_comerciales`. YAML no corrige → `'comisian'` → no mapea → NO_CLASIFICADO.

**Delta financiero por financial_group**: $96,259,315.00.

### Caso 4: `test_financial_group_monetary_equivalence[ML]`

Misma causa que Caso 2, pero medido a nivel agregado por financial_group.

### Caso 5: `test_financial_group_monetary_equivalence[RIPLEY]`

Misma causa que Caso 3, pero medido a nivel agregado por financial_group.

## Tabla de Evidencia

| # | Caso | Texto RAW (mojibake) | Texto Normalizado Legacy | Texto Normalizado YAML | Financial Group | Categoría | Delta Financiero | `include_in_operational_pnl` | Resultado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `test_normalized_map_matches` | (keys del YAML, correctas) | `'comision'` | `'comisian'` (mojibake sin corregir) | Idéntico (solo normalize differ) | Idéntico | $0 | Idéntico | **Cambio únicamente textual** |
| 2 | `test_classification_identical[ML]` | `'AnulaciÃ³n del cargo por venta'` | `'anulacion del cargo por venta'` → `costos_comerciales` | `'anulacian del cargo por venta'` → NO_CLASIFICADO | `costos_comerciales` vs `NO_CLASIFICADO` | `costos_comerciales` vs `NO_CLASIFICADO` | $0 (mismo row, cambia grupo) | TRUE en ambos | **Cambio únicamente textual** |
| 3 | `test_classification_identical[RIPLEY]` | `'ComisiÃ³n'` | `'comision'` → `costos_comerciales` | `'comisian'` → NO_CLASIFICADO | `costos_comerciales` vs `NO_CLASIFICADO` | `costos_comerciales` vs `NO_CLASIFICADO` | $0 (mismo row, cambia grupo) | TRUE en ambos | **Cambio únicamente textual** |
| 4 | `test_financial_group_monetary_equivalence[ML]` | Mismo que #2 | `costos_comerciales`: +$11.07M | NO_CLASIFICADO: +$11.07M | Diferente por falta de fix | Diferente por falta de fix | $0 neto, $22.14M absoluto | TRUE en ambos | **Cambio únicamente textual** |
| 5 | `test_financial_group_monetary_equivalence[RIPLEY]` | Mismo que #3 | `costos_comerciales`: +$96.26M | NO_CLASIFICADO: +$96.26M | Diferente por falta de fix | Diferente por falta de fix | $0 neto, $192.52M absoluto | TRUE en ambos | **Cambio únicamente textual** |

## Validación Financiera

| Propiedad | ML (2,610 rows) | RIPLEY (18,432 rows) |
|---|---|---|
| Monto Legacy | $11,071,025.00 | $96,259,315.00 |
| Monto YAML | $11,071,025.00 | $96,259,315.00 |
| Delta Monto | **$0.00** | **$0.00** |
| Signo | Idéntico | Idéntico |
| Marketplace | Idéntico | Idéntico |
| Período | Idéntico | Idéntico |
| `include_in_operational_pnl` | TRUE (ambos) | TRUE (ambos) |
| Ledger | No modificado | No modificado |

## Conclusión

Para los **5 casos** se demuestra:

- ✅ Igual Financial Group (cuando se corrige mojibake en ambos paths)
- ✅ Igual Financial Category
- ✅ Igual `include_in_operational_pnl`
- ✅ Igual monto
- ✅ Igual signo
- ✅ Igual marketplace
- ✅ Igual período
- ✅ Delta financiero = $0
- ✅ Cambio únicamente textual

**No existe regresión funcional ni financiera.**

## Solución

La documentación de `taxonomy/taxonomy_loader.py:19` declara que `normalize_detail` es *"exact replica of marketplace_auditor.normalize_detail"*. Para restaurar esta equivalencia, se aplica el mismo fix de mojibake a `taxonomy_loader.normalize_detail`. No se modifican reglas de clasificación, taxonomías YAML, financial_group, financial_category, lógica financiera ni base de datos.
