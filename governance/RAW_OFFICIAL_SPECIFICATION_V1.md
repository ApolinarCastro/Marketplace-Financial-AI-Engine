---
id: RAW_OFFICIAL_SPECIFICATION_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Senior Data Engineer & Raw Storage Guardian
ultima_revision: 2026-07-27
dependencias:
  - EXECUTION_PLAN_PHASE_0_FOUNDATION_V3
  - DATA_CONTRACT_REGISTRY_V1
  - RAW_DATA_CONTRACT_V1
---

# ESPECIFICACIÓN OFICIAL DE LA CAPA RAW V1

## Declaración de Inmutabilidad
```text
REGLA NÚMERO 1 DE LA CAPA RAW:
LA CAPA RAW ES 100% INMUTABLE.
NINGÚN PROCESO DE INGESTA, INDEXACIÓN O LIMPIEZA PUEDE MODIFICAR, MOVER O ELIMINAR UN ARCHIVO RAW.
RAW_MUTATIONS = 0 EN TODO MOMENTO.
```

---

## 1. Estructura Oficial de Directorios RAW (`01_Raw/`)

```text
01_Raw/
├── FALABELLA/                  # Cartolas y liquidaciones Falabella (CSV / XLSX / XML)
├── ML/                         # Reportes de ventas, liberaciones y poscobro Mercado Libre (CSV / JSON)
├── PARIS/                      # Liquidaciones y cartolas Paris (XLSX / XML)
├── RIPLEY/                     # Liquidaciones, comisiones y DTEs Ripley (XLSX / XML)
└── SHOPIFY/                    # Exportaciones de ventas directas Shopify (CSV)
```

---

## 2. Clasificación Oficial del Inventario (1,349 Archivos)

```text
====================================================================================================
CLASIFICACIÓN CANÓNICA               CANTIDAD ARCHIVOS   ESTADO DE INTEGRIDAD
====================================================================================================
RAW_FINANCIERO_AUTORIZADO            1,341 Archivos      VALID (Hashes SHA-256 calculados por streaming)
RAW_TÉCNICO_NO_AUTORIZADO            2 Archivos (.py/.json) VALID (Archivos auxiliares de soporte)
REFERENCIA                           6 Archivos (.md/.dat) SUPPORTED (Documentación o esquemas)
CUARENTENA                           0 Archivos          PASS
DESCONOCIDO                          0 Archivos          PASS
TOTAL ARCHIVOS INDEXADOS             1,349 Archivos      INMUTABILIDAD GARANTIZADA
====================================================================================================
```

---

## 3. Reglas de Conservación e Integridad

1. **Streaming SHA-256**: Identidad primaria determinista derivada del hash SHA-256 del contenido (`open(f, 'rb')`).
2. **Path Normalization**: Rutas relativas guardadas con separador Unix `/` independientemente del sistema operativo.
3. **Idempotencia de Lectura**: Re-ejecutar el indexador produce `new_files = 0`, `changed_files = 0`, `missing_files = 0`.
4. **Cero Mutaciones**: Ningún archivo RAW se modifica, mueve o elimina (`RAW_MUTATIONS = 0`).

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:RAW_OFFICIAL_SPECIFICATION_V1` (Tipo: `Especificacion_Capa_RAW`)

### Execution Graph Nodes
- `ExecNode:RAW_FILE_INDEXER_SERVICE` (Servicio: `engine/v4/ingestion/raw_file_indexer.py`)
