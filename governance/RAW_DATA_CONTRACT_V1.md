---
id: RAW_DATA_CONTRACT_V1
version: 1.0.0
fecha: 2026-07-27
estado: CERTIFICADO
owner: Data Architect & Raw Storage Guardian
ultima_revision: 2026-07-27
dependencias:
  - RAW_OFFICIAL_SPECIFICATION_V1
  - DATA_CONTRACT_REGISTRY_V1
---

# CONTRATO CANÓNICO DE DATOS RAW V1

## Propósito
Establecer el esquema de metadatos obligatorio y determinista que debe cumplir cada archivo almacenado en la capa `01_Raw/` antes de su ingesta o normalización.

---

## 1. Esquema JSON Canónico del Registro RAW (`RAWFileRecord`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RAWFileRecord",
  "type": "object",
  "required": [
    "file_id",
    "content_hash",
    "relative_path",
    "file_name",
    "extension",
    "marketplace",
    "source_domain",
    "report_type",
    "period",
    "period_source",
    "size_bytes",
    "modified_at",
    "discovered_at",
    "integrity_status",
    "registry_status",
    "processing_status"
  ],
  "properties": {
    "file_id": { "type": "string", "example": "RAW-a1b2c3d4e5f6" },
    "content_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "relative_path": { "type": "string", "example": "01_Raw/ML/2026-03/ventas_ml.csv" },
    "file_name": { "type": "string", "example": "ventas_ml.csv" },
    "extension": { "type": "string", "example": ".csv" },
    "marketplace": { "type": "string", "enum": ["ML", "PARIS", "RIPLEY", "FALABELLA", "SHOPIFY", "SAP", "DTE", "BANCO", "UNKNOWN"] },
    "source_domain": { "type": "string" },
    "report_type": { "type": "string" },
    "period": { "type": "string", "example": "2026-03" },
    "period_source": { "type": "string", "enum": ["PATH", "FILENAME", "METADATA", "UNKNOWN"] },
    "size_bytes": { "type": "integer", "minimum": 0 },
    "modified_at": { "type": "string", "format": "date-time" },
    "discovered_at": { "type": "string", "format": "date-time" },
    "integrity_status": { "type": "string", "enum": ["VALID", "INVALID", "EMPTY", "UNREADABLE", "UNSUPPORTED"] },
    "registry_status": { "type": "string", "enum": ["NEW", "REGISTERED", "DUPLICATE", "CHANGED", "MISSING"] },
    "processing_status": { "type": "string", "enum": ["NOT_PROCESSED", "PROCESSING", "PROCESSED", "FAILED"] },
    "duplicate_type": { "type": "string" },
    "duplicate_of": { "type": ["string", "null"] },
    "execution_id": { "type": ["string", "null"] },
    "evidence_id": { "type": ["string", "null"] }
  }
}
```

---

## Nodos en Grafos de Gobierno

### Knowledge Graph Nodes
- `Node:RAW_DATA_CONTRACT_V1` (Tipo: `Contrato_Datos_RAW`)

### Execution Graph Nodes
- `ExecNode:RAW_CONTRACT_VALIDATOR` (Handler: `engine/v4/ingestion/raw_file_indexer.py`)
