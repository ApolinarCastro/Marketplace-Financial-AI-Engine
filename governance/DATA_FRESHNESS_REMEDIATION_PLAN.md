# DATA FRESHNESS REMEDIATION PLAN

**Status:** PLAN CERTIFIED
**Date:** 2026-06-06

---

## ML

| Ítem | Detalle |
|---|---|
| Archivos pendientes | ML_Facturacion (17 files, Jan 2025 a May 2026), Liberaciones Junio (1 file), Poscobro Junio (1 file) |
| Períodos afectados | Junio 2026 completo (actualmente solo 69 rows, $1.8M, todos ajustes) |
| Loader | `surgical_loader.py:load_facturacion()` + `load_poscobro()` |
| Punto de ruptura | `surgical_loader.py:11` — `DIR_FACTURACION` apunta a `01_Raw/ML/ML_Facturacion/` que NO EXISTE. Los archivos reales están en `Reporte_Marketplaces/Mercado Libre/ML_Facturacion/`. |
| Acción requerida | 1. Corregir `DIR_FACTURACION` a la ruta correcta. 2. Ejecutar `SurgicalLoader().load_marketplace('ML')`. 3. Ejecutar `MarketplaceAuditorEngine().run_classification()`. 4. Ejecutar `run_financial_closing()` para todos los períodos. |
| Impacto esperado | ~31,091 nuevas filas "Cargo por venta" aproximadamente. RN ML aumenta con nuevos ingresos de Junio. |

### ML_Facturacion Path Fix

```
ANTES (roto):
DIR_FACTURACION = ROOT / "01_Raw" / "ML" / "ML_Facturacion"
→ Directorio no existe → glob() devuelve [] → 0 archivos procesados → silencio

DESPUÉS (corregido):
DIR_FACTURACION = ROOT / "Reporte_Marketplaces" / "Mercado Libre" / "ML_Facturacion"
→ Directorio existe con 17 archivos XLSX
```

**Archivos en ML_Facturacion (Reporte_Marketplaces):**
```
Reporte_Facturacion_MercadoLibre_Ene2025.xlsx
Reporte_Facturacion_MercadoLibre_Feb2025.xlsx
... (17 archivos, Ene 2025 a May 2026)
```

---

## PARIS

| Ítem | Detalle |
|---|---|
| Archivos pendientes | Dropshipping May 2026 (`05-2026.xlsx`), Dropshipping Jun 2026 (`06-06-2026.xlsx`), Fulfillment May 2026 (`1 may 2026 - 31 may 2026.xlsx`), Fulfillment Jun 2026 (`1 jun 2026 - 5 jun 2026.xlsx`) |
| Períodos afectados | Mayo 2026 + Junio 2026 (ambos ausentes — última data es Abril 2026) |
| Loader | `surgical_loader.py:load_paris()` |
| Punto de ruptura | La ruta es correcta (`01_Raw/PARIS/Transacciones/`). El loader simplemente no fue re-ejecutado después de que los archivos de Mayo/Junio existieran. |
| Acción requerida | 1. Ejecutar `SurgicalLoader().load_marketplace('PARIS')`. 2. Ejecutar clasificación + cierre. |
| Riesgo | `reset_db('PARIS')` borra datos existentes y recarga desde cero. Los 42,487 rows actuales serán reemplazados. Los datos de Abril 2026 deben estar presentes en los archivos de Dropshipping + Fulfillment. |
| Impacto esperado | Recuperación de ~2 meses de data PARIS (~$50M en ingresos aproximadamente). |

---

## FALABELLA

| Ítem | Detalle |
|---|---|
| Archivos pendientes | `1 mayo 2026 al 31 mayo 2026.xlsx`, `1 junio 2026 al 5 junio 2026.xlsx` |
| Períodos afectados | Mayo 2026 + Junio 2026 (ambos ausentes — última data es Abril 2026) |
| Loader | `surgical_loader.py:load_falabella()` |
| Punto de ruptura | La ruta es correcta (`01_Raw/FALABELLA/`). El loader simplemente no fue re-ejecutado. |
| Acción requerida | 1. Ejecutar `SurgicalLoader().load_marketplace('FALABELLA')`. 2. Ejecutar clasificación + cierre. |
| Riesgo | Los 1,008 rows actuales serán reemplazados. Debe verificarse post-carga que `_reload_falabella.py` backup de ventas sea compatible. |
| Impacto esperado | Recuperación de ~2 meses ($~1M en RN aproximadamente). |

---

## RIPLEY

| Ítem | Detalle |
|---|---|
| Archivos pendientes | Ninguno — no existen archivos de Junio 2026 en `01_Raw/RIPLEY/Resumen financiero/`. Los archivos existentes (46 XLSX con IDs 000312-2815 a 000378-2815) no contienen data posterior a Mayo 2026. |
| Períodos afectados | Junio 2026 |
| Loader | `surgical_loader.py:load_ripley()` |
| Punto de ruptura | No hay archivos fuente para Junio 2026. La última liquidación procesada es 2026-05-26. |
| Acción requerida | Obtener archivo de Resumen Financiero de RIPLEY para Junio 2026 y colocarlo en `01_Raw/RIPLEY/Resumen financiero/`. Luego ejecutar `SurgicalLoader().load_marketplace('RIPLEY')`. |
| Impacto esperado | 0 hasta obtener el archivo fuente. |

---

## Resumen de Carga

| MP | Archivos a cargar | Períodos | Loader | Ruta funciona | Acción |
|---|---|---|---|---|---|
| ML | 19+ | Jun 2026 | `load_facturacion()` + `load_poscobro()` | ❌ Ruta rota | Corregir DIR_FACTURACION + recargar |
| PARIS | 4 | May+Jun 2026 | `load_paris()` | ✅ | Recargar |
| FALABELLA | 2 | May+Jun 2026 | `load_falabella()` | ✅ | Recargar |
| RIPLEY | 0 | — | `load_ripley()` | ✅ | Esperar archivo fuente |

---

## Pipeline Post-Carga

Después de cargar cada MP, ejecutar en orden:

```python
from engine.v4.marketplace_auditor import MarketplaceAuditorEngine
engine = MarketplaceAuditorEngine()
engine.run_classification()          # Reclasifica todo
# Luego por cada período de cada MP:
engine.run_financial_closing(mp, ini, fin)  # Recalcula cierres
engine.run_audit()                   # Regenera alertas
```

O usar `reset_and_close.py` que ya ejecuta clasificación + cierres + auditoría para todos los MPs.

---

## Veredicto

| Certificación | Resultado |
|---|---|
| **Data Freshness Remediation** | **PASS CONDITIONAL** — El camino de remediación es conocido y ejecutable. 3/4 MPs tienen archivos listos. 1 bug de ruta necesita corrección (DIR_FACTURACION). RIPLEY requiere archivo externo. |
