"""Tests for execute_query contract — validates placeholder count, SQL validation, QueryGuard."""
from __future__ import annotations
import pytest
from engine.v4.copilot.copilot_engine import CopilotEngine


@pytest.fixture(scope="module")
def engine():
    return CopilotEngine()


class TestExecuteQuery:
    def test_empty_sql_raises(self, engine):
        with pytest.raises(ValueError, match="Empty SQL"):
            engine.execute_query("")

    def test_whitespace_sql_raises(self, engine):
        with pytest.raises(ValueError, match="Empty SQL"):
            engine.execute_query("   ")

    def test_placeholder_mismatch_raises(self, engine):
        sql = "SELECT * FROM marketplace_ledger_v1 WHERE fecha BETWEEN ? AND ?"
        with pytest.raises(ValueError, match="Parameter mismatch"):
            engine.execute_query(sql, ["2026-01-01"])  # 2 ? but 1 param

    def test_placeholder_mismatch_extra_params_raises(self, engine):
        sql = "SELECT * FROM marketplace_ledger_v1 WHERE fecha = ?"
        with pytest.raises(ValueError, match="Parameter mismatch"):
            engine.execute_query(sql, ["2026-01-01", "extra"])

    def test_valid_query_returns_df(self, engine):
        sql = "SELECT 1 as val"
        df = engine.execute_query(sql)
        assert len(df) == 1
        assert df.iloc[0]["val"] == 1

    def test_valid_query_with_params(self, engine):
        df = engine.execute_query("SELECT ? as val, ? as val2", ["hello", 42])
        assert df.iloc[0]["val"] == "hello"
        assert df.iloc[0]["val2"] == 42

    def test_query_guard_blocks_mutations(self, engine):
        sql = "INSERT INTO marketplace_ledger_v1 (marketplace) VALUES ('x')"
        with pytest.raises(ValueError, match="SQL audit CRITICAL"):
            engine.execute_query(sql)

    def test_query_guard_blocks_ddl(self, engine):
        sql = "DROP TABLE marketplace_ledger_v1"
        with pytest.raises(ValueError, match="SQL audit CRITICAL"):
            engine.execute_query(sql)

    def test_ledger_query_passes_guard(self, engine):
        sql = "SELECT COUNT(*) as n FROM marketplace_ledger_v1 WHERE LOWER(marketplace) = ?"
        df = engine.execute_query(sql, ["ml"])
        assert not df.empty

    def test_cierre_query_passes_guard(self, engine):
        sql = "SELECT COUNT(*) as n FROM marketplace_cierre_financiero_v1 WHERE LOWER(marketplace) NOT IN ('all')"
        df = engine.execute_query(sql)
        assert not df.empty
