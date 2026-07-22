---
name: product-analysis
description: Multi-path parallel product analysis with cross-model test-time compute scaling. Spawns parallel agents to explore product from multiple perspectives, then synthesizes findings into actionable optimization plans.
metadata:
  author: daymade
  source: https://github.com/daymade/claude-code-skills/tree/main/product-analysis
---

# Product Analysis

Multi-agent product audit combining Claude Code agent teams + Codex CLI.

## Scope Modes
- `full`: UX + API + Architecture + Docs
- `ux`: Frontend navigation, information density, user journey
- `api`: Backend API coverage, endpoint health, error handling
- `arch`: Module structure, dependency graph, code duplication
- `compare X Y`: Self-audit + competitive benchmarking

## Parallel Agents
- Agent A: Frontend Navigation & Information Density
- Agent B: User Journey & Empty State
- Agent C: Backend API & Health
- Agent D: Architecture & Module Structure
- Agent E: Documentation & Config Consistency

## Synthesis
Cross-validate findings across agents. Quantify metrics. P0/P1/P2 priorities.

## Execution
```
/product-analysis full
```
