---
dashboard_schema_version: 1.0
type: dashboard
---
# Documentary Dashboard

Breakdown of documents by DTE type and Chain Type integrations.

## Documents by TipoDTE
```dataview
TABLE length(rows) AS "Total", certification_status
FROM "Evidence"
GROUP BY document_type
```

## Chain Type Integrations
```dataview
TABLE length(rows) AS "Total Documents", marketplace
FROM "Evidence"
GROUP BY chain_type
```
