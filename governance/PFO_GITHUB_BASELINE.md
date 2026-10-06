# PROJECT FINISH ONE — GitHub Baseline

## Repository

Repository:
https://github.com/ApolinarCastro/Marketplace-Financial-AI-Engine

Branch:
main

Baseline SHA:
e2ff733e25ede8d8074cbce51aa5bf5f9cbcd3b7

Status:
BASELINE_PUBLISHED

## Purpose

This commit is the official GitHub code baseline for PROJECT FINISH ONE.

It does NOT certify the financial END-TO-END flow.

The objective after this baseline is:

SOURCE DATA
→ INGESTION
→ NORMALIZATION
→ LEDGER
→ RECONCILIATION
→ CLASIFICACIÓN
→ RESULTADO FINANCIERO
→ EVIDENCIA

with:

EXPECTED RESULT = ACTUAL RESULT

## Validation State

Loop Control suite:

53 / 55 PASS

Known pending failures:

1. test_no_forbidden_coordination_tokens
   - adapter.py contains reserved token "handoff"

2. test_kernel_contains_no_financial_logic
   - policy.py references official DB outside protected-resource list

These failures are NOT closed by this baseline record.

## Sensitive Data Exclusions

Excluded from Git tracking:

- 01_Raw/
- data/db/
- production databases
- database backups
- database snapshots
- real marketplace exports
- real DTE/XML financial data
- sensitive evidence folders
- virtual environments
- runtime temporary files

## Source of Truth Boundary

GitHub is the source of truth for versioned application code and governance artifacts.

GitHub is NOT the source of truth for:

- production financial data
- RAW marketplace files
- production DuckDB databases
- confidential DTE/XML
- runtime evidence containing sensitive data

## Next Project Phase

Next checkpoint:

PROJECT FINISH ONE — PHASE 1 BASELINE EXECUTION

Required outputs:

- repository boots
- DB initializes
- Golden Dataset identified
- first reproducible E2E blocker
- 00_BASELINE_REPORT.md

No architecture expansion is authorized before the first END-TO-END CERTIFIED PASS.
