---
name: baseline-ui
description: Quickly deslop UI code by fixing spacing, hierarchy, typography, and small layout issues. Use when the interface needs a fast cleanup or polish pass.
metadata:
  author: ibelick
  source: https://raw.githubusercontent.com/ibelick/ui-skills/main/skills/baseline-ui/SKILL.md
  registry: https://www.ui-skills.com/skills/ibelick/baseline-ui
---

# Baseline UI

Enforces an opinionated UI baseline to prevent AI-generated interface slop.

## Focus Areas
- **Spacing**: Consistent padding/margin scale, no random values
- **Hierarchy**: Clear visual weight through size + weight + color, not just size
- **Typography**: text-balance for headings, text-pretty for body, tabular-nums for data
- **Layout**: Fixed z-index scale, size-* for square elements
- **Animation**: Compositor props only (transform, opacity), never layout properties
- **Performance**: No blur/backdrop-filter on large surfaces, no will-change outside animation
- **Design**: No gradients unless requested, no purple/multicolor gradients, no glow effects
