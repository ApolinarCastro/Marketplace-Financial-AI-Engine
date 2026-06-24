---
name: stack-detector
description: Detect technology stacks (frameworks, languages, databases, tools) in a project by scanning file structures, extensions, and dependencies. Based on Citstack signatures.
---

# Stack Detector

Detect the technology stack of any project/directory by matching file patterns, extensions, and package dependencies against a library of 300+ signatures.

## How it works

1. **Scan Directory**: List the files and directories in the target path.
2. **Match Signatures**: Load the `signatures.json` file and compare its patterns against the discovered items.
3. **Analyze Dependencies**: If a `package.json`, `requirements.txt`, or similar is found, check for specific dependency matches.
4. **Report Results**: Provide a categorized list of detected technologies (Frameworks, Databases, Tools, etc.) with their names and logos.

## Core Data

The signatures are stored in: `.agents/skills/stack-detector/signatures.json`

## Usage

When asked to "scan this project", "identify the stack", or "audit технологий":
- Load `.agents/skills/stack-detector/signatures.json`.
- List files in the target directory (absolute path).
- Report matches in a table format.

Example Output:
| Ubicación | Tecnología | Categoría |
| :--- | :--- | :--- |
| `package.json` | FastAPI | Framework |
| `*.py` | Python | Language |
| `database/` | SQLite | Database |
