---
dashboard_schema_version: 1.0
type: dashboard
---
# Executive Dashboard

Overview of the certification process across all audited documents.

## High-Level Status
```dataview
TABLE length(rows) AS "Total Documents"
FROM "Evidence"
GROUP BY certification_status
```

## Evidence Level Overview
```dataview
TABLE length(rows) AS "Total"
FROM "Evidence"
GROUP BY evidence_level
```

## Recent Activity
```dataview
TABLE marketplace, document_type, folio, certification_status
FROM "Evidence"
SORT file.ctime DESC
LIMIT 10
```
