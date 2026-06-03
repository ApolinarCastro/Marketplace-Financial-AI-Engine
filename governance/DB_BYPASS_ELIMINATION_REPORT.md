# DB BYPASS ELIMINATION REPORT

**Sprint**: B1.1 — Phase A1
**Date**: 2026-05-30
**Regime**: IMPLEMENTATION

---

## Summary

Eliminated all 4 instances of direct `duckdb.connect()` that bypassed the `DatabaseV4` singleton. All database access now flows through `DatabaseV4.get()`.

## Files Modified

| # | File | Before | After | Risk Before |
|---|---|---|---|---|
| 1 | `_reload_falabella.py` | `duckdb.connect(hardcoded_path)` + raw `fetchall()`/`fetchone()` | `DatabaseV4.get()` + `db.execute()`/`db.insert_df()` | 🔴 HIGH — hardcoded path, direct WRITE (DELETE/INSERT) |
| 2 | `engine/v4/surgical_recovery_flow.py` | `duckdb.connect()` × 2, `DELETE FROM marketplace_ledger_clasificado_v1` | `DatabaseV4.get()` + `db.execute()`, `db.query()` | 🔴 HIGH — dual connections, destructive DELETE |
| 3 | `engine/v4/run_full_closing.py` | `duckdb.connect()` + `conn.execute().df()` | `DatabaseV4.get()` + `db.query()` | 🟡 MEDIUM — bypassed singleton for READ |
| 4 | `engine/v4/surgical_xml_justifier.py` | `self.conn = duckdb.connect()` in `__init__`, `self.conn.close()` | `self.db = DatabaseV4.get()`, lifecycle managed by singleton | 🟡 MEDIUM — second connection for WRITE |

## Changes by File

### 1. `_reload_falabella.py`
- Removed `import duckdb`
- Added `from engine.v4.database import DatabaseV4`
- Changed `conn = duckdb.connect(...)` to `db = DatabaseV4.get()`
- Replaced `conn.execute(...)` → `db.execute(...)` (all 9 occurrences)
- Replaced raw DataFrame SQL injection `INSERT INTO ventas_marketplace SELECT * FROM df_backup` → `db.insert_df(df_backup, "ventas_marketplace")`
- Removed `import duckdb`

### 2. `engine/v4/surgical_recovery_flow.py`
- Removed `import duckdb` and `ROOT`/`DB_PATH` constants
- Added `from engine.v4.database import DatabaseV4`
- Replaced first `conn = duckdb.connect()` → `db = DatabaseV4.get()`
- Replaced `conn.execute("DELETE...")` → `db.execute("DELETE...")`
- Removed `conn.close()` (first occurrence)
- Replaced second `conn = duckdb.connect()` + `conn.execute(...).df()` → `db.query(...)`
- Removed `conn.close()` (second occurrence)

### 3. `engine/v4/run_full_closing.py`
- Removed `import duckdb` and `ROOT`/`DB_PATH` constants
- Added `from engine.v4.database import DatabaseV4`
- Replaced `conn = duckdb.connect()` → `db = DatabaseV4.get()`
- Replaced `conn.execute(...).df()` → `db.query(...)`
- Removed `conn.close()`

### 4. `engine/v4/surgical_xml_justifier.py`
- Removed `import duckdb` and `DB_PATH` constant
- Added `from engine.v4.database import DatabaseV4`
- Changed `self.conn = duckdb.connect(...)` → `self.db = DatabaseV4.get()`
- Replaced all `self.conn.execute(...)` → `self.db.execute(...)` (4 occurrences)
- Removed `self.conn.close()` from `run()` method

## Verification

- **14/14 regression tests**: PASS
- **DatabaseV4 singleton**: all 4 files now use `DatabaseV4.get()` exclusively
- **No `import duckdb` or `duckdb.connect()` remains** in any of the 4 target files (confirmed via grep)

## Residual Risk

- `database/duckdb_manager.py` connects to `database/reconciliation.db` (separate legacy DB, not `meli_financial_v4.db`) — **out of scope**
- `_generate_v6.py` and `_explore_snapshot.py` connect to snapshot DBs with `duckdb.connect()` — **READ only, out of scope**
