---
dashboard_schema_version: 1.0
type: dashboard
---
# Marketplace Dashboard

Stratification of evidence by integration origin.

## Document Volumes by Marketplace
```dataview
TABLE length(rows) AS "Total Documents"
FROM "Evidence"
GROUP BY marketplace
```

## Success Rate by Marketplace
```dataview
TABLE length(rows) AS "Total", certification_status
FROM "Evidence"
GROUP BY marketplace
```
