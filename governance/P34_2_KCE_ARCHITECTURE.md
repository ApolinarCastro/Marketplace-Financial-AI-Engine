# P34.2 — KnowledgeConsolidationEngine (KCE) Architecture

**Date:** 2026-07-09
**Status:** IMPLEMENTED ✅
**Tests:** 23/23 PASS, 0 regression

## Overview

KCE is the first engine in Marketplace Financial that learns automatically from audit findings, governance decisions, RFCs, and certifications — eliminating the manual maintenance burden of hundreds of Markdown files.

## Architecture

```
api/knowledge_api.py         ← FastAPI app (standalone, port 3002)
engine/v4/knowledge/
├── __init__.py              ← Package marker
├── kce.py                   ← KnowledgeConsolidationEngine (orchestrator)
├── audit_scanner.py         ← Reads marketplace_auditoria_v1
├── decision_parser.py       ← Parses governance/*.md (DEC, RFC)
├── knowledge_indexer.py     ← Reads/writes knowledge_index.yaml
└── retention_manager.py     ← File lifecycle transitions
tests/test_knowledge_engine.py  ← 23 tests
```

## Components

### 1. AuditScanner (`audit_scanner.py`)
- Queries `marketplace_auditoria_v1` grouped by marketplace + check_name
- Generates `AuditKnowledgeEntry` with id, summary, status, row_count
- Provides `coverage_summary()` per marketplace

### 2. DecisionParser (`decision_parser.py`)
- Scans `governance/*.md` recursively
- Extracts DEC-XXX, RFC_XXX, and document-level IDs via regex
- Parses status (ACTIVE/SUPERSEDED/CERTIFIED/FAIL/OBSOLETE)
- Extracts summaries from VERDICT/VERDICTO sections
- Tags entries with marketplace names and keywords

### 3. KnowledgeIndexer (`knowledge_indexer.py`)
- Reads and writes `knowledge_index.yaml` with UTF-8 encoding
- `merge()` adds new entries without duplicating existing ones
- `search()` with keyword/type/status filters
- `get()` single-entry lookup

### 4. RetentionManager (`retention_manager.py`)
- Enforces allowed status transitions (ACTIVE→OBSOLETE, etc.)
- Suggests action per entry (KEEP/ARCHIVE/MONITOR)
- Scans file system for governance files

### 5. KCE Orchestrator (`kce.py`)
- `consolidate()`: Scans audits → governance files → taxonomies → merge → coverage analysis
- `_analyze_coverage_gaps()`: Cross-references knowledge IDs against Python source code
- `_find_codebase_references()`: Extracts DEC/RFC/AUDIT/TAXONOMY/CERT references from `engine/v4/*.py`
- `status_report()`: Summarizes type/status distribution

## API Endpoints (standalone)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v4/knowledge` | List/search knowledge entries |
| GET | `/api/v4/knowledge/{id}` | Single entry lookup |
| POST | `/api/v4/knowledge/consolidate` | Run consolidation (dry_run=True by default) |
| GET | `/api/v4/knowledge/status` | Type/status distribution |
| GET | `/api/v4/knowledge/coverage-gaps` | Knowledge not referenced in code |
| GET | `/api/v4/knowledge/audit-coverage` | Per-MP audit summary |
| GET | `/api/v4/knowledge/retention-recs` | Archive recommendations |

## Key Design Decisions

1. **Dry-run by default**: Consolidate endpoint defaults to `dry_run=true`. No file mutation without explicit override.
2. **Standalone API**: `api/knowledge_api.py` creates a separate FastAPI app. Can be mounted via `app.mount()` or run independently.
3. **Zero modifications to Core**: No changes to api.py, database.py, or any existing engine. KCE is a read-only consumer of `marketplace_auditoria_v1`.
4. **Safe YAML writing**: Uses UTF-8 encoding, dedup by ID, preserves existing entries on merge.

## Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `engine/v4/knowledge/__init__.py` | 0 | Package marker |
| `engine/v4/knowledge/kce.py` | 191 | Main orchestrator |
| `engine/v4/knowledge/audit_scanner.py` | 57 | Audit scanner |
| `engine/v4/knowledge/decision_parser.py` | 115 | Governance parser |
| `engine/v4/knowledge/knowledge_indexer.py` | 77 | YAML manager |
| `engine/v4/knowledge/retention_manager.py` | 89 | File lifecycle |
| `api/knowledge_api.py` | 97 | Knowledge API |
| `tests/test_knowledge_engine.py` | 262 | Tests (23) |
