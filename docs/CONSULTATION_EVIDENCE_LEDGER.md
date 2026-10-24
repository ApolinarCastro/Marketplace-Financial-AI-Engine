# Consultation Evidence Ledger

This file defines the mandatory evidence format for material technical work in this repository.

The purpose is to prove which persistent project sources, shared knowledge-library sources, ECC references, official documentation, repository evidence, or other sources were actually consulted, what they contributed, and whether they materially influenced the solution.

## Required entry template

```text
TASK_ID:
PROJECT:
TIMESTAMP:

GAP_OR_BLOCKER:

SOURCES_CONSULTED:
  - SOURCE_TYPE:
    SOURCE_REFERENCE:
    NORMALIZED_VIEW_REFERENCE: <optional; MarkItDown or other derived view>
    NORMALIZATION_STATUS: NOT_USED | COMPLETE | PARTIAL | FAILED
    WHY_CONSULTED:
    USEFUL_FINDING:
    APPLIED_TO_SOLUTION: YES | NO
    DECISION_OR_CHANGE_INFLUENCED:
    EVIDENCE_REFERENCE:

RESULT: PASS | FAIL | BLOCKED | NO_MATERIAL_CONTRIBUTION
NEXT_ACTION:
```

## Allowed SOURCE_TYPE values

- PROJECT_STATE
- KNOWLEDGE_LIBRARY
- ECC
- OFFICIAL_DOCS
- REPOSITORY
- OTHER

## Mandatory rules

1. "Library consulted" without an exact source reference and useful finding is invalid evidence.
2. If a source was consulted but did not influence the result, record `APPLIED_TO_SOLUTION: NO`.
3. When a MarkItDown or other derived view is used, record both the authoritative original and the derived reference. PARTIAL/FAILED normalization cannot replace native-source verification for material claims.
4. Do not force irrelevant library consultation. Use the project's consultation router or source-authority policy when available.
5. When a blocker could reasonably benefit from existing technical knowledge, consult the router before inventing a new solution.
6. More sources is not better. Relevance and measurable impact matter.
7. A source recommendation never proves PASS. Project-specific reproducible verification is still required.
8. If a source changes diagnosis, architecture, implementation, testing, or recovery strategy, record exactly what changed.
9. If no source materially contributed, use `RESULT: NO_MATERIAL_CONTRIBUTION`; never manufacture value.
10. Link this ledger entry from the task's evidence or closure artifact whenever the project uses separate evidence files.
11. Periodic reporting should aggregate useful-source contribution without turning source count into a vanity metric.

## Semantic boundary

```text
CONSULTED != USEFUL
USEFUL != APPLIED
APPLIED != VERIFIED
VERIFIED contribution requires evidence
```

## Example

```text
TASK_ID: EXAMPLE-001
PROJECT: Example Project
TIMESTAMP: 2026-10-17T16:00:00-03:00

GAP_OR_BLOCKER:
A browser acquisition path fails after a marketplace markup change.

SOURCES_CONSULTED:
  - SOURCE_TYPE: PROJECT_STATE
    SOURCE_REFERENCE: CURRENT_STATE.md
    WHY_CONSULTED: Confirm certified baseline and current first blocker.
    USEFUL_FINDING: Existing fallback path is certified and must not be replaced without failure evidence.
    APPLIED_TO_SOLUTION: YES
    DECISION_OR_CHANGE_INFLUENCED: Limited diagnosis to failing acquisition branch.
    EVIDENCE_REFERENCE: evidence/example-001/root_cause.json

  - SOURCE_TYPE: KNOWLEDGE_LIBRARY
    SOURCE_REFERENCE: <exact library document and section>
    WHY_CONSULTED: Check established recovery patterns.
    USEFUL_FINDING: <specific finding or NONE>
    APPLIED_TO_SOLUTION: NO
    DECISION_OR_CHANGE_INFLUENCED: None.
    EVIDENCE_REFERENCE: evidence/example-001/consultation.md

RESULT: PASS
NEXT_ACTION: Close task and preserve verified lesson if reusable.
```
