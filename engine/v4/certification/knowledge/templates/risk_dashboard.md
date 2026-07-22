---
dashboard_schema_version: 1.0
type: dashboard
---
# Tax Risk Dashboard

Monitoring of certification failures, missing critical data, and high-risk anomalies.

## Failing Documents
```dataview
TABLE marketplace, folio, document_type
FROM "Evidence"
WHERE certification_status = "FAIL"
SORT file.ctime DESC
```

## Evidence with Gaps
```dataview
TABLE marketplace, folio
FROM "Evidence"
WHERE contains(tags, "evidence/fail")
```

## Gap Frequency Analysis
```dataview
TABLE length(rows) AS "Occurrences"
FROM "Gap"
```
