# Contrato API <-> UI (JSON Schema)

## POST `/api/v4/electronic_certification/validate`
**Request:** `multipart/form-data` (file: XML)
**Response:**
```json
{
  "status": "success",
  "data": {
    "marketplace": "ML",
    "folio": 123456,
    "validation_pipeline": {
      "xml_parsed": true,
      "xsd_valid": true,
      "signature_valid": true,
      "caf_valid": true,
      "iva_consistent": true
    },
    "legal_status": "CERTIFIED",
    "chain_type": "DOCUMENT_CHAIN",
    "evidence_hash": "a1b2c3d4e5f6..."
  }
}
```

## POST `/api/v4/obsidian/export`
**Request:** JSON con `evidence_hash` y `folio`.
**Response:** `{"status": "success", "vault_path": "C:/.../vault/evidence_123456.md"}`
