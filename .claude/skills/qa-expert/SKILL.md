---
name: qa-expert
description: Establish world-class QA testing processes with Google Testing Standards, OWASP security testing, test case writing, bug tracking P0-P4, quality metrics, and autonomous LLM execution.
metadata:
  author: daymade
  source: https://github.com/daymade/claude-code-skills/tree/main/qa-expert
---

# QA Expert

Google Testing Standards + OWASP security testing. AAA pattern (Arrange-Act-Assert).

## Key Capabilities
1. QA Project Initialization: `python scripts/init_qa_project.py <project-name>`
2. Test Case Writing: AAA pattern, TC-[CATEGORY]-[NUMBER] format
3. Test Execution: Ground Truth Principle (test case docs = authoritative source)
4. Bug Reporting: P0 (24h fix) → P4 (optional)
5. Quality Gates: 100% execution, ≥80% pass rate, 0 P0 bugs, ≥80% coverage, 90% OWASP
6. OWASP Coverage: A01-A07, target 90% (9/10 threats)

## Autonomous Execution
Master prompt enables LLM-driven auto-execution, auto-tracking, auto-bug-filing.
