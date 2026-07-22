# GOVERNANCE LAYER V1

## Architecture
The Governance Layer establishes an immutable framework that regulates modifications to the Marketplace Financial AI Engine. It acts as an overarching control mechanism separating operational code from core financial structures, ledgers, and taxonomies.

## Marketplace Registry
All marketplaces are officially registered with a designated status. The registry defines ownership, baseline documentation, and regression guards.
- **RIPLEY**: `FROZEN`
- **MERCADO_LIBRE**: `CERTIFIED`
- **PARIS**: `CERTIFIED`
- **FALABELLA**: `DEVELOPMENT`
- **FUTURE_MARKETPLACES**: `DEVELOPMENT`
*See `MARKETPLACE_REGISTRY.json` for details.*

## Skills Registry
Specific permissions and modifiable targets are strictly scoped by the executing agent's skill profile.
- **UI_ENHANCEMENT**: Permitted to modify styles, layouts, badges, and filters. Protected against ledger, taxonomy, loaders, and the financial engine.
- **REPORTING & VISUALIZATION**: Read-only.
- **DATA_IMPORT / FINANCIAL_ENGINE / TAXONOMY_ENGINE / LEDGER_ENGINE**: High restrictions, blocked from external modification without explicit governance bypass.
- **GOVERNANCE_ENGINE**: Authorized exclusively to maintain governance records.
*See `SKILLS_REGISTRY.json` for details.*

## Policy Engine
Mandatory operational rules locked inside the AI Engine:
- `FINANCIAL_STRUCTURE_LOCK = TRUE`
- `LEDGER_LOCK = TRUE`
- `LOADER_LOCK = TRUE`
- `KPI_ENGINE_LOCK = TRUE`
- `TAXONOMY_LOCK = TRUE`
- `EXECUTIVE_LOCK = TRUE`
- `AI_LAYER_LOCK = TRUE`
- `UI_SCOPE_LIMITATION = TRUE`

## Protected Components
The following components are strictly immutable and require explicit authorization to modify:
- `surgical_loader.py`
- `financial_closing.py`
- `marketplace_auditor.py`
- `marketplace_ledger`
- `financial taxonomy`
- `truth_type engine`
- `executive_dashboard`
- `dashboard financial structure`
- `ai operational layer`
- `ripley baseline`
- `ripley regression guard`
- `single financial truth`

## Change Control
All modifications must be logged in `CHANGE_LOG.md`. All directives authorizing these changes must be logged in `APPROVAL_LOG.md`.

## Deployment Gates
Mandatory sequential validation required prior to deployment. If any gate fails, deployment is blocked (`DEPLOYMENT_BLOCKED`).
1. **Governance Guard**
2. **Regression Guard**
3. **Marketplace Guard**
4. **UI Guard**
5. **Data Integrity Guard**

## Compliance Matrix
- **No Code Modification Before Governance**: COMPLIANT
- **No UI Redesign Without Authorization**: COMPLIANT
- **No Financial Engine Changes**: COMPLIANT
- **No Taxonomy Changes**: COMPLIANT
- **No Loader Changes**: COMPLIANT
- **All Changes Require Registration**: COMPLIANT
- **All Changes Require Traceability**: COMPLIANT
