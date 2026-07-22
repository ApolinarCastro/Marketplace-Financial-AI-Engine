---
name: ui-designer
description: Extract design systems from reference UI images and generate implementation-ready UI design prompts. Use when users provide UI screenshots/mockups and want to create consistent designs or build MVP UIs.
metadata:
  author: daymade
  source: https://github.com/daymade/claude-code-skills/tree/main/ui-designer
---

# UI Designer

Systematic extraction of design systems from reference UI images.

## Workflow
1. **Gather Inputs**: Reference images directory + project idea file
2. **Extract Design System**: Color palette, typography, components, spacing, animations
3. **Generate MVP PRD**: Elevator pitch → problem → audience → features → UX
4. **Compose UI Prompt**: Design system + PRD → implementation-ready prompt
5. **Implement UI**: React + Tailwind CSS + Lucide icons, multiple variations

## Key Deliverables
- Design system markdown (colors, typography, components, spacing)
- Structured PRD with UX considerations
- Implementation prompt for React/Tailwind
