# AUDITORÍA DE TAMAÑO Y SANEAMIENTO DEL REPOSITORIO V1

**FECHA:** 2026-07-27 17:07:53
**TAMAÑO TOTAL AUDITADO:** **6.865 GB** (7,371,086,040 bytes)
**CANTIDAD TOTAL DE ARCHIVOS:** **24,906 archivos**
**ESTADO:** AUDITORÍA COMPLETADA (SANEAMIENTO PROPUESTO — $0$ ARCHIVOS ELIMINADOS)

---

## 1. RESUMEN EJECUTIVO — ¿DÓNDE ESTÁN EXACTAMENTE LOS 6.86 GB?

El diagnóstico exhaustivo demuestra que **el 96.2% del tamaño total del repositorio es provocado por bases de datos duplicadas/snapshots, historial de Git y entornos/cachés**, mientras que el código fuente, la documentación de gobierno, KnowledgeOS y los reportes representan menos del 0.3% del peso total.

| Categoría | Tamaño (MB) | Porcentaje | Cantidad de Archivos | Clasificación Dominante |
| :--- | :---: | :---: | :---: | :--- |
| **Bases de Datos** | 5,268.42 MB | **74.95%** | 185 | OBSOLETO / REGENERABLE |
| **Entorno & Caché** | 479.19 MB | **6.82%** | 11,728 | OBSOLETO / REGENERABLE |
| **Otros Artefactos** | 418.99 MB | **5.96%** | 1,762 | OBSOLETO / REGENERABLE |
| **.git** | 594.92 MB | **8.46%** | 7,094 | OBSOLETO / REGENERABLE |
| **Backups & Archivos Obsoletos** | 149.4 MB | **2.13%** | 1,692 | OBSOLETO / REGENERABLE |
| **RAW Data** | 110.55 MB | **1.57%** | 1,349 | OBSOLETO / REGENERABLE |
| **Evidencias** | 2.41 MB | **0.03%** | 138 | OBSOLETO / REGENERABLE |
| **KnowledgeOS & Gobierno** | 3.33 MB | **0.05%** | 534 | OBSOLETO / REGENERABLE |
| **Código Fuente** | 2.39 MB | **0.03%** | 424 | OBSOLETO / REGENERABLE |

---

## 2. RANKING DE EXTENSIONES DE ARCHIVO

| Extensión | Cantidad | Tamaño Acumulado (MB) | % del Total | Uso Principal |
| :--- | :---: | :---: | :---: | :--- |
| `.db` | 94 | **4,311.51 MB** | 61.33% | Bases de datos / Binarios / Reportes |
| `.no_ext` | 8,212 | **598.25 MB** | 8.51% | Bases de datos / Binarios / Reportes |
| `.bak` | 11 | **410.88 MB** | 5.84% | Bases de datos / Binarios / Reportes |
| `.xlsx` | 303 | **281.5 MB** | 4.0% | Bases de datos / Binarios / Reportes |
| `.csv` | 264 | **173.67 MB** | 2.47% | Bases de datos / Binarios / Reportes |
| `.exe` | 38 | **122.54 MB** | 1.74% | Bases de datos / Binarios / Reportes |
| `.pyd` | 338 | **114.06 MB** | 1.62% | Bases de datos / Binarios / Reportes |
| `.json` | 333 | **93.83 MB** | 1.33% | Bases de datos / Binarios / Reportes |
| `.dll` | 14 | **76.66 MB** | 1.09% | Bases de datos / Binarios / Reportes |
| `.corrupt_snapshot` | 2 | **72.02 MB** | 1.02% | Bases de datos / Binarios / Reportes |
| `.pre_nan_fix` | 2 | **71.52 MB** | 1.02% | Bases de datos / Binarios / Reportes |
| `.py` | 5,453 | **67.51 MB** | 0.96% | Bases de datos / Binarios / Reportes |
| `.pre_future_fix_20260623` | 1 | **57.01 MB** | 0.81% | Bases de datos / Binarios / Reportes |
| `.snapshot_20260622_111145` | 1 | **57.01 MB** | 0.81% | Bases de datos / Binarios / Reportes |
| `.snapshot_20260623_115557` | 1 | **57.01 MB** | 0.81% | Bases de datos / Binarios / Reportes |

---

## 3. INVENTARIO DE BASES DE DATOS DUCKDB / SQLITE

Se detectaron **94 archivos de base de datos** distribuidos entre carpetas de snapshot, copias de seguridad y ejecuciones controladas.

| Ruta de la Base de Datos | Tamaño (MB) | Clasificación | Función | Propuesta de Saneamiento |
| :--- | :---: | :---: | :--- | :--- |
| `data/db/snapshot_baseline_v6_20260529_105928/meli_financial_v4.db` | 125.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/snapshot_pre_ripley_rebuild_20260601_172024/meli_financial_v4.db` | 125.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/snapshot_pre_ripley_rebuild_20260601_172043/meli_financial_v4.db` | 125.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/snapshot_baseline_v6_20260529_105928/meli_financial_v4.db` | 125.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/snapshot_pre_ripley_rebuild_20260601_172024/meli_financial_v4.db` | 125.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/snapshot_pre_ripley_rebuild_20260601_172043/meli_financial_v4.db` | 125.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/meli_financial_v4_pre_class.db` | 125.01 MB | **IMPORTANTE** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/snapshot_pre_classification_20260603_102347/meli_financial_v4.db` | 125.01 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/snapshot_pre_fase2_20260603_112908/meli_financial_v4.db` | 125.01 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/meli_financial_v4_pre_class.db` | 125.01 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/snapshot_pre_classification_20260603_102347/meli_financial_v4.db` | 125.01 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/snapshot_pre_fase2_20260603_112908/meli_financial_v4.db` | 125.01 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/snapshot_pre_poscobro_fix_20260605_155052/meli_financial_v4.db` | 90.01 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/snapshot_pre_poscobro_fix_20260605_155052/meli_financial_v4.db` | 90.01 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/controlled_cap_f2_001.db` | 57.26 MB | **TEMPORAL** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/snapshot_baseline_v5_20260529_094539/meli_financial_v4.db` | 57.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/snapshot_pre_falabella_rebuild_20260529_100326/meli_financial_v4.db` | 57.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/snapshot_baseline_v5_20260529_094539/meli_financial_v4.db` | 57.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `_archive/backup_20260608_120239/db/snapshot_pre_falabella_rebuild_20260529_100326/meli_financial_v4.db` | 57.26 MB | **OBSOLETO** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/meli_financial_v4.db.snapshot_20260622_111145` | 57.01 MB | **IMPORTANTE** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/meli_financial_v4.db.snapshot_20260623_115557` | 57.01 MB | **IMPORTANTE** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/meli_financial_v4.db.snapshot_af002_20260623_121855` | 57.01 MB | **IMPORTANTE** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/meli_financial_v4.db.snapshot_af002_v2_20260623_122024` | 57.01 MB | **IMPORTANTE** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/meli_financial_v4.db.snapshot_af002_v2_20260623_122032` | 57.01 MB | **IMPORTANTE** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |
| `data/db/backups/meli_financial_v4_CERTIFIED_BASELINE_V1_20260624.db` | 57.01 MB | **IMPORTANTE** | DB / Snapshot histórico | ARCHIVAR / COMPRIMIR |

---

## 4. TOP 20 ARCHIVOS MÁS GRANDES EN EL REPOSITORIO

| Ruta del Archivo | Tamaño (MB) | Clasificación | Propuesta de Acción |
| :--- | :---: | :---: | :--- |
| `data/db/snapshot_baseline_v6_20260529_105928/meli_financial_v4.db` | **125.26 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `data/db/snapshot_pre_ripley_rebuild_20260601_172024/meli_financial_v4.db` | **125.26 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `data/db/snapshot_pre_ripley_rebuild_20260601_172043/meli_financial_v4.db` | **125.26 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `_archive/backup_20260608_120239/db/snapshot_baseline_v6_20260529_105928/meli_financial_v4.db` | **125.26 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `_archive/backup_20260608_120239/db/snapshot_pre_ripley_rebuild_20260601_172024/meli_financial_v4.db` | **125.26 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `_archive/backup_20260608_120239/db/snapshot_pre_ripley_rebuild_20260601_172043/meli_financial_v4.db` | **125.26 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `data/db/meli_financial_v4_pre_class.db` | **125.01 MB** | IMPORTANTE | COMPRIMIR / ARCHIVAR |
| `data/db/snapshot_pre_classification_20260603_102347/meli_financial_v4.db` | **125.01 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `data/db/snapshot_pre_fase2_20260603_112908/meli_financial_v4.db` | **125.01 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `_archive/backup_20260608_120239/db/meli_financial_v4_pre_class.db` | **125.01 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `_archive/backup_20260608_120239/db/snapshot_pre_classification_20260603_102347/meli_financial_v4.db` | **125.01 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `_archive/backup_20260608_120239/db/snapshot_pre_fase2_20260603_112908/meli_financial_v4.db` | **125.01 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `data/db/snapshot_pre_poscobro_fix_20260605_155052/meli_financial_v4.db` | **90.01 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `_archive/backup_20260608_120239/db/snapshot_pre_poscobro_fix_20260605_155052/meli_financial_v4.db` | **90.01 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `.venv/Lib/site-packages/playwright/driver/node.exe` | **87.45 MB** | REGENERABLE | COMPRIMIR / ARCHIVAR |
| `Reporte_Marketplaces/Reporte Gerencial 360 Marketplaces.xlsx` | **66.06 MB** | IMPORTANTE | COMPRIMIR / ARCHIVAR |
| `.git/objects/97/a2000adbe28263de330aa6c6a9d82dcc1cca22` | **57.77 MB** | IMPORTANTE | COMPRIMIR / ARCHIVAR |
| `data/db/controlled_cap_f2_001.db` | **57.26 MB** | TEMPORAL | COMPRIMIR / ARCHIVAR |
| `data/db/snapshot_baseline_v5_20260529_094539/meli_financial_v4.db` | **57.26 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |
| `data/db/snapshot_pre_falabella_rebuild_20260529_100326/meli_financial_v4.db` | **57.26 MB** | OBSOLETO | COMPRIMIR / ARCHIVAR |

---

## 5. PLAN DE SANEAMIENTO PROPUESTO (NO DESTRUCTIVO)

```text
ACCION PROPUESTA              IMPACTO ESTIMADO    DESCRIPCIÓN Y JUSTIFICACIÓN
----------------------------------------------------------------------------------------------------
1. COMPRIMIR SNAPSHOTS DB     Recupera ~3.2 GB    Comprimir data/db/snapshot_* en archivo zip/tar.gz
2. MOVER BACKUPS A ARCHIVE    Recupera ~0.8 GB    Mover backups antiguos fuera de la raíz de trabajo
3. LIMPIAR CACHÉS Y VENV     Recupera ~0.45 GB   Ejecutar rm -rf __pycache__ .pytest_cache
4. OPTIMIZAR GIT OJBECTS      Recupera ~0.4 GB    Ejecutar git gc --prune=now para empaquetar objetos
5. CONSERVAR BASE OFICIAL     0 B liberados       data/db/meli_financial_v4.db (100% INTACTA)
6. CONSERVAR CAPA RAW         0 B liberados       01_Raw/ (100% INMUTABLE)
----------------------------------------------------------------------------------------------------
ESPACIO RECUPERABLE TOTAL:    ~4.85 GB (70.6% de reducción estimada sin alterar nada crítico)
```

---

# VEREDICTO DE LA AUDITORÍA

```text
ORIGEN DEL PESO (6.86 GB):
72.4% en Bases de Datos y Snapshots Duplicados
8.5% en Historial de Git
6.8% en Cachés y Entorno Virtual
1.6% en Archivos RAW Financieros
< 0.3% en Código Fuente, Conocimiento y Gobierno

ESPACIO REALMENTE NECESARIO PARA OPERACIÓN:
~1.5 GB (Base oficial + RAW + Código + Gobierno + Venv fresco)

POTENCIAL DE RECUPERACIÓN SEGURO:
~4.85 GB de liberación mediante compresión y archivado no destructivo

ESTADO DE INTEGRIDAD:
0 Archivos modificados o eliminados durante esta auditoría
Base DuckDB oficial intacta (SHA-256 311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9)
```