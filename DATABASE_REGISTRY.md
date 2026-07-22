# DATABASE_REGISTRY

| Nombre | Uso | Estado | Último uso | Responsable | Destino |
|---|---|---|---|---|---|
| data/db/meli_financial_v4.db | Single Source of Truth V4 | ACTIVA | Actual | Baseline V4 | CONSERVAR (CORE) |
| marketplaces_auditor.db | Antigua BD auditoría | OBSOLETE (0 bytes) | Pre-V4 | Legacy ETL | ELIMINAR |
| marketplace_ledger.db | Antigua BD ledger | OBSOLETE (0 bytes) | Pre-V4 | Legacy ETL | ELIMINAR |
| marketplace_financials.db | BD V3 | OBSOLETE (0 bytes) | V3 | Legacy ETL | ELIMINAR |
| marketplace_v4.db | Pre-baseline V4 dev | OBSOLETE (0 bytes) | Dev P22 | Dev | ELIMINAR |
| marketplace_v4.duckdb | Dev artefacto | OBSOLETE | Dev P22 | DuckDB | ELIMINAR |
| db.sqlite3 | SQLite artefacto | OBSOLETE (0 bytes) | V1 | Dev | ELIMINAR |
| database.sqlite | SQLite artefacto | OBSOLETE (0 bytes) | V1 | Dev | ELIMINAR |
| database.duckdb | DuckDB artefacto | OBSOLETE | V2 | Dev | ELIMINAR |

*Certificación*: Todas las bases obsoletas de 0 bytes o de artefactos intermedios previos a la Baseline V4 pueden ser eliminadas de forma segura. La única base operativa y que debe preservarse intacta es data/db/meli_financial_v4.db.
