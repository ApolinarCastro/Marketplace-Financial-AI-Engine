---
name: fixing-accessibility
description: Audit and fix HTML accessibility issues including ARIA labels, keyboard navigation, focus management, color contrast, and form errors. Use when adding interactive controls, forms, dialogs, or reviewing WCAG compliance.
metadata:
  author: ibelick
  source: https://raw.githubusercontent.com/ibelick/ui-skills/main/skills/fixing-accessibility/SKILL.md
  registry: https://www.ui-skills.com/skills/ibelick/fixing-accessibility
---

# Fixing Accessibility

Priority order: accessible names → keyboard access → focus/dialogs → semantics → forms/errors → announcements → contrast/states → media/motion → tool boundaries.

## Key Rules
1. Every interactive control needs an accessible name
2. All interactive elements must be reachable by Tab
3. Modals must trap focus while open
4. Prefer native elements (button, a, input) over role-based hacks
5. Errors must be linked to fields using aria-describedby
6. Ensure sufficient contrast for text and icons
7. Respect prefers-reduced-motion for non-essential motion
