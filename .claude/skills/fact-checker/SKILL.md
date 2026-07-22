---
name: fact-checker
description: Verify factual claims in documents using web search and official sources, then propose corrections with user confirmation. Use for fact-checking AI model specs, technical docs, statistics, and general claims.
metadata:
  author: daymade
  source: https://github.com/daymade/claude-code-skills/tree/main/fact-checker
---

# Fact Checker

Verify factual claims against authoritative sources.

## Workflow
1. **Identify factual claims**: Technical specs, version numbers, stats, benchmarks
2. **Search authoritative sources**: Official docs, API references, GitHub releases
3. **Compare claims vs sources**: ✅ Accurate / ❌ Incorrect / ⚠️ Outdated / ❓ Unverifiable
4. **Generate correction report**: With source links and rationale
5. **Apply corrections**: Only after user approval

## Search Strategy
- Use model names + specification + current year
- Prefer official sources (product pages > API docs > blogs > third-party)
- Include temporal context in corrections ("As of June 2026")
