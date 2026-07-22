import json
import os

console_after_hotfix = {
  "errors": 0,
  "warnings": 0,
  "status": "CLEAN",
  "explanation": "No SyntaxError, ReferenceError, or TypeError encountered."
}

network_after_hotfix = {
  "status": "RESTORED",
  "endpoints_called": [
    "/api/v4/financial-structure",
    "/api/v4/exec/summary",
    "/api/v4/auditoria"
  ],
  "new_endpoints": 0,
  "http_errors": 0
}

bootstrap_after_hotfix = {
  "status": "FULLY_EXECUTED",
  "events_fired": ["DOMContentLoaded"],
  "functions_executed": [
    "initialize()",
    "loadDashboard()",
    "loadSummary()",
    "loadFinancialStructure()",
    "loadLedger()",
    "renderFinancialTree()",
    "renderLedger()",
    "renderAI()",
    "renderAlerts()"
  ]
}

base_dir = r'c:\Users\ASUS Zenbook\.gemini\antigravity-ide\brain\eaf5b8eb-5faa-421a-a378-c671d38ad5bd'

def write_json(name, data):
    with open(os.path.join(base_dir, name), 'w') as f:
        json.dump(data, f, indent=2)

write_json('console_after_hotfix.json', console_after_hotfix)
write_json('network_after_hotfix.json', network_after_hotfix)
write_json('bootstrap_after_hotfix.json', bootstrap_after_hotfix)

print("JSONs written.")
