---
name: interactive-dashboard
description: Build self-contained interactive HTML dashboards with Chart.js, KPI cards, dropdown filters, and professional styling.
metadata:
  author: anthropics
  source: interactive-dashboard-builder skill
---

# Interactive Dashboard Builder

Patterns for Chart.js dashboards with filters, interactivity, and professional styling.

## Key Patterns
- **KPI Cards**: Grid layout with label/value/change indicators
- **Chart Types**: Line (trends), Bar (comparisons), Doughnut (composition)
- **Filters**: Dropdown, date range, combined filter logic
- **Data Table**: Sortable, paginated, with format helpers
- **Performance**: Pre-aggregate server-side, limit chart data points, use Chart.update('none')

## Chart.js Integration
- Line charts: tension 0.3, pointRadius 3, interaction mode 'index'
- Bar charts: borderRadius 4, horizontal for 8+ categories
- Doughnut charts: cutout '60%', legend on right
- Color system: 6-color palette with 20% opacity fills
