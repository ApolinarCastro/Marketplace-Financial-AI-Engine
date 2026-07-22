---
name: excel-automation
description: Create, parse, and control Excel files. Professional formatting with openpyxl, complex xlsm parsing with stdlib zipfile+xml for investment bank financial models. Use when creating formatted Excel reports or parsing complex financial models.
metadata:
  author: daymade
  source: https://github.com/daymade/claude-code-skills/tree/main/excel-automation
---

# Excel Automation

Three capabilities: Create (openpyxl), Parse (zipfile+xml), Control (AppleScript).

## Tool Selection
- Simple file (<1MB, no VBA) → openpyxl or pandas
- Complex xlsm (>1MB, VBA macros) → zipfile + xml.etree.ElementTree
- True .xls (BIFF format) → xlrd

## Key Patterns
- Investment banking color convention: Blue=input, Black=calculated, Green=cross-ref
- Sheet name resolution via workbook.xml → _rels/workbook.xml.rels
- Cell extraction via sharedStrings.xml + sheet XML
- Fix corrupted DefinedNames by removing "Formula removed" entries
