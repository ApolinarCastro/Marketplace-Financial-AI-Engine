# Coordination Contract: Codex <-> OpenCode

## Purpose
This directory is the only supported coordination interface between Codex and OpenCode.
No agent may use ad hoc markdown, chat memory, or direct RC1/core edits as a coordination mechanism.

## Scope
Allowed coordination concerns:
- Active execution state
- Capability status
- Blockers
- Evidence references
- Handoff metadata
- Protected-core boundaries

Forbidden coordination concerns:
- Editing financial truth logic through coordination files
- Writing SQL, ETL, ledger, closing, or RC1 core decisions here
- Declaring PASS/CERTIFIED without executable evidence

## Canonical Files
1. `governance/coordination/coordination_registry.json`
   Source of truth for contract metadata, protected paths, and interface inventory.
2. `governance/coordination/coordination_state.json`
   Source of truth for current coordination state and next handoff.
3. `execution_board.json`
   Source of truth for capability-level execution status.
4. `evidence/fase_1b/*summary*.json`
   Source of truth for reproducible validation evidence.
5. `tools/verify_coordination_interface.py`
   Gatekeeper that verifies the interface is structurally valid.

## RC1 Protection
The coordination interface is read/write for orchestration only.
It must not modify or override protected core areas, especially:
- RC1 core
- financial engine
- ETL
- ledger
- closing
- DEC-019 protected logic

## Operating Rule
If Codex and OpenCode disagree, they must update `coordination_state.json` and rerun the verifier.
If a change cannot be expressed through these files, it is not an approved coordination path.
