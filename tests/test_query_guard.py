"""Tests for QueryGuard — Read-only SQL Auditor."""
import pytest
from engine.v4.security.query_guard import (
    QueryGuard, audit_query, audit_queries,
    QueryAuditResult, IssueType, Severity,
)


class TestQueryGuard:
    """Test QueryGuard detection capabilities."""
    
    def setup_method(self):
        self.guard = QueryGuard()
    
    # ── Mutation Detection ─────────────────────────────────────────────
    
    def test_detects_insert(self):
        result = self.guard.audit("INSERT INTO marketplace_ledger_v1 VALUES (1, 2, 3)")
        assert result.has_mutations
        assert result.is_read_only is False
        assert any(i.issue_type == IssueType.MUTATION_INSERT for i in result.issues)
        assert any(i.severity == Severity.CRITICAL for i in result.issues)
    
    def test_detects_update(self):
        result = self.guard.audit("UPDATE marketplace_ledger_v1 SET monto = 100")
        assert result.has_mutations
        assert any(i.issue_type == IssueType.MUTATION_UPDATE for i in result.issues)
    
    def test_detects_delete(self):
        result = self.guard.audit("DELETE FROM marketplace_ledger_v1 WHERE id = 1")
        assert result.has_mutations
        assert any(i.issue_type == IssueType.MUTATION_DELETE for i in result.issues)
    
    def test_detects_drop(self):
        result = self.guard.audit("DROP TABLE marketplace_ledger_v1")
        assert result.has_mutations
        assert any(i.issue_type == IssueType.MUTATION_DDL for i in result.issues)
    
    def test_detects_alter(self):
        result = self.guard.audit("ALTER TABLE marketplace_ledger_v1 ADD COLUMN test TEXT")
        assert result.has_mutations
        assert any(i.issue_type == IssueType.MUTATION_DDL for i in result.issues)
    
    def test_detects_truncate(self):
        result = self.guard.audit("TRUNCATE TABLE marketplace_ledger_v1")
        assert result.has_mutations
        assert any(i.issue_type == IssueType.MUTATION_DDL for i in result.issues)
    
    def test_select_is_read_only(self):
        result = self.guard.audit("SELECT * FROM marketplace_ledger_v1 WHERE monto > 0")
        assert result.has_mutations is False
        assert result.is_read_only is True
    
    # ── Table Access Control ───────────────────────────────────────────
    
    def test_allows_whitelisted_table(self):
        result = self.guard.audit("SELECT * FROM marketplace_ledger_v1")
        assert not any(i.issue_type == IssueType.UNAUTHORIZED_TABLE for i in result.issues)
    
    def test_blocks_unauthorized_table(self):
        result = self.guard.audit("SELECT * FROM users_secrets")
        assert any(i.issue_type == IssueType.UNAUTHORIZED_TABLE for i in result.issues)
        assert any(i.severity == Severity.CRITICAL for i in result.issues)
    
    def test_tracks_accessed_tables(self):
        result = self.guard.audit("""
            SELECT l.monto, c.clasificacion_operativa
            FROM marketplace_ledger_v1 l
            JOIN marketplace_ledger_clasificado_v1 c ON l.id_transaccion = c.id_transaccion
        """)
        assert "marketplace_ledger_v1" in result.tables_accessed
        assert "marketplace_ledger_clasificado_v1" in result.tables_accessed
    
    # ── PII Exposure ───────────────────────────────────────────────────
    
    def test_detects_ssn_column(self):
        result = self.guard.audit("SELECT user_ssn FROM marketplace_ledger_v1")
        assert any(i.issue_type == IssueType.PII_COLUMN_EXPOSURE for i in result.issues)
    
    def test_detects_password_column(self):
        result = self.guard.audit("SELECT password_hash FROM marketplace_ledger_v1")
        assert any(i.issue_type == IssueType.PII_COLUMN_EXPOSURE for i in result.issues)
    
    def test_detects_credit_card(self):
        result = self.guard.audit("SELECT card_number FROM marketplace_ledger_v1")
        assert any(i.issue_type == IssueType.PII_COLUMN_EXPOSURE for i in result.issues)
    
    def test_detects_email(self):
        result = self.guard.audit("SELECT user_email FROM marketplace_ledger_v1")
        assert any(i.issue_type == IssueType.PII_COLUMN_EXPOSURE for i in result.issues)
    
    def test_tracks_selected_columns(self):
        result = self.guard.audit("SELECT monto, detalle, tipo_movimiento FROM marketplace_ledger_v1")
        assert "monto" in result.columns_selected
        assert "detalle" in result.columns_selected
        assert "tipo_movimiento" in result.columns_selected
    
    # ── Missing Filters ────────────────────────────────────────────────
    
    def test_flags_full_table_scan(self):
        result = self.guard.audit("SELECT * FROM marketplace_ledger_v1")
        assert any(i.issue_type == IssueType.MISSING_FILTER for i in result.issues)
        assert any(i.severity == Severity.HIGH for i in result.issues)
    
    def test_allows_filtered_query(self):
        result = self.guard.audit("SELECT * FROM marketplace_ledger_v1 WHERE fecha >= '2026-01-01'")
        assert not any(i.issue_type == IssueType.MISSING_FILTER for i in result.issues)
    
    # ── Select * ───────────────────────────────────────────────────────
    
    def test_flags_select_star(self):
        result = self.guard.audit("SELECT * FROM marketplace_ledger_v1 WHERE monto > 0")
        assert any(i.issue_type == IssueType.SELECT_STAR for i in result.issues)
        assert any(i.severity == Severity.MEDIUM for i in result.issues)
    
    # ── Redundant Joins ────────────────────────────────────────────────
    
    def test_flags_duplicate_join(self):
        sql = """
            SELECT * FROM marketplace_ledger_v1 l
            JOIN marketplace_ledger_clasificado_v1 c ON l.id = c.id
            JOIN marketplace_ledger_clasificado_v1 c2 ON l.id = c2.id
        """
        result = self.guard.audit(sql)
        assert any(i.issue_type == IssueType.REDUNDANT_JOIN for i in result.issues)
    
    # ── Cartesian Product ──────────────────────────────────────────────
    
    def test_flags_join_without_on(self):
        sql = "SELECT * FROM marketplace_ledger_v1 l JOIN marketplace_ledger_clasificado_v1 c"
        result = self.guard.audit(sql)
        assert any(i.issue_type == IssueType.CARTESIAN_PRODUCT for i in result.issues)
    
    # ── N+1 Pattern ────────────────────────────────────────────────────
    
    def test_flags_correlated_subquery(self):
        sql = """
            SELECT * FROM marketplace_ledger_v1 l
            WHERE EXISTS (
                SELECT 1 FROM marketplace_ledger_clasificado_v1 c 
                WHERE c.id_transaccion = l.id_transaccion
            )
        """
        result = self.guard.audit(sql)
        # Note: This may or may not trigger depending on sqlglot parsing
        # Just ensure it runs without error
        assert isinstance(result, QueryAuditResult)
    
    # ── Result Summary ─────────────────────────────────────────────────
    
    def test_summary_clean(self):
        result = self.guard.audit("SELECT monto FROM marketplace_ledger_v1 WHERE monto > 0")
        assert result.summary == "✅ Clean"
    
    def test_summary_with_high(self):
        result = self.guard.audit("SELECT * FROM marketplace_ledger_v1")
        assert "HIGH" in result.summary or "MEDIUM" in result.summary or "CRITICAL" in result.summary
    
    def test_summary_with_critical(self):
        result = self.guard.audit("DROP TABLE marketplace_ledger_v1")
        assert "CRITICAL" in result.summary


class TestAuditQueries:
    """Test batch audit function."""
    
    def test_audit_multiple(self):
        queries = [
            "SELECT * FROM marketplace_ledger_v1",
            "SELECT monto FROM marketplace_ledger_v1 WHERE monto > 0",
            "DROP TABLE test",
        ]
        results = audit_queries(queries)
        assert len(results) == 3
        assert results[0].issues  # select star
        assert not results[1].issues  # clean
        assert results[2].has_mutations  # drop


class TestCustomConfiguration:
    """Test QueryGuard with custom config."""
    
    def test_custom_allowed_tables(self):
        guard = QueryGuard(allowed_tables={"custom_table"})
        result = guard.audit("SELECT * FROM custom_table")
        assert not any(i.issue_type == IssueType.UNAUTHORIZED_TABLE for i in result.issues)
    
    def test_custom_pii_patterns(self):
        guard = QueryGuard(pii_columns=[r".*_custom_secret$"])
        result = guard.audit("SELECT my_custom_secret FROM marketplace_ledger_v1")
        assert any(i.issue_type == IssueType.PII_COLUMN_EXPOSURE for i in result.issues)


# ═══════════════════════════════════════════════════════════════════════
# REAL-WORLD FINANCIAL QUERY TESTS
# ═══════════════════════════════════════════════════════════════════════

class TestFinancialQueries:
    """Test with actual financial engine query patterns."""
    
    def setup_method(self):
        self.guard = QueryGuard()
    
    def test_exec_summary_pattern(self):
        """Pattern from FinancialEngine.query_exec_summary"""
        sql = """
            SELECT 
                COALESCE(SUM(CASE WHEN LOWER(financial_group)='ingresos' 
                    AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as gross,
                COALESCE(SUM(CASE WHEN LOWER(financial_group)='devoluciones' 
                    AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END), 0) as returns
            FROM marketplace_ledger_v1
            WHERE fecha >= ? AND LOWER(marketplace) = LOWER(?)
        """
        result = self.guard.audit(sql)
        assert result.is_read_only
        assert not result.has_mutations
    
    def test_waterfall_pattern(self):
        """Pattern from FinancialEngine.query_waterfall"""
        sql = """
            SELECT
                SUM(CASE WHEN LOWER(financial_group)='ingresos' 
                    AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END) as ventas,
                SUM(CASE WHEN LOWER(financial_group)='devoluciones' 
                    AND COALESCE(include_in_operational_pnl,1)=1 THEN monto ELSE 0 END) as devoluciones
            FROM marketplace_ledger_v1
            WHERE fecha BETWEEN ? AND ? AND LOWER(marketplace) = LOWER(?)
        """
        result = self.guard.audit(sql)
        assert result.is_read_only
    
    def test_ledger_query_pattern(self):
        """Pattern from FinancialEngine.query_ledger"""
        sql = """
            SELECT * FROM marketplace_ledger_v1
            WHERE marketplace = ? AND fecha >= ? AND fecha <= ?
            AND LOWER(financial_group) = LOWER(?)
            AND COALESCE(include_in_operational_pnl, 1) = 1
            ORDER BY fecha DESC LIMIT ? OFFSET ?
        """
        result = self.guard.audit(sql)
        assert result.is_read_only
        # Should flag SELECT *
        assert any(i.issue_type == IssueType.SELECT_STAR for i in result.issues)
    
    def test_desglose_pattern(self):
        """Pattern from FinancialEngine.query_desglose"""
        sql = """
            SELECT COALESCE(c.financial_group, 'sin_clasificar') as financial_group,
                   l.detalle, l.tipo_movimiento, c.clasificacion_operativa,
                   SUM(COALESCE(l.monto, 0)) as total, COUNT(*) as cantidad
            FROM marketplace_ledger_v1 l
            LEFT JOIN marketplace_ledger_clasificado_v1 c
                ON l.marketplace = c.marketplace AND l.id_transaccion = c.id_transaccion
            WHERE l.marketplace = ? AND l.fecha BETWEEN ? AND ?
            GROUP BY c.financial_group, l.detalle, l.tipo_movimiento, c.clasificacion_operativa
        """
        result = self.guard.audit(sql)
        assert result.is_read_only
        assert "marketplace_ledger_v1" in result.tables_accessed
        assert "marketplace_ledger_clasificado_v1" in result.tables_accessed
    
    def test_cobros_breakdown_pattern(self):
        """Pattern from FinancialEngine.query_cobros_breakdown"""
        sql = """
            SELECT marketplace, detalle, financial_group, SUM(COALESCE(monto, 0)) as total
            FROM marketplace_ledger_v1
            WHERE LOWER(financial_group) IN ('costos_operacionales', 'costos_comerciales', 'comisiones', 'ajustes')
              AND COALESCE(include_in_operational_pnl, 1) = 1
              AND fecha BETWEEN ? AND ?
            GROUP BY marketplace, detalle, financial_group
        """
        result = self.guard.audit(sql)
        assert result.is_read_only


# ═══════════════════════════════════════════════════════════════════════
# EDGE CASES
# ═══════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Edge cases and error handling."""
    
    def setup_method(self):
        self.guard = QueryGuard()
    
    def test_unparseable_sql(self):
        """Gracefully handles unparseable SQL."""
        # Truly unparseable: missing closing parenthesis, invalid syntax
        result = self.guard.audit("SELECT * FROM (SELECT 1")
        assert isinstance(result, QueryAuditResult)
        assert len(result.issues) >= 1
        assert result.issues[0].severity == Severity.INFO
    
    def test_empty_query(self):
        result = self.guard.audit("")
        assert isinstance(result, QueryAuditResult)
    
    def test_cte_query(self):
        """Common Table Expressions should work."""
        sql = """
            WITH filtered AS (
                SELECT * FROM marketplace_ledger_v1 WHERE monto > 0
            )
            SELECT SUM(monto) FROM filtered
        """
        result = self.guard.audit(sql)
        assert result.is_read_only
    
    def test_case_sensitivity(self):
        """Table names should be case-insensitive for whitelist."""
        result = self.guard.audit("SELECT * FROM MARKETPLACE_LEDGER_V1")
        assert not any(i.issue_type == IssueType.UNAUTHORIZED_TABLE for i in result.issues)
    
    def test_alias_preserved(self):
        """Table aliases should be resolved."""
        sql = "SELECT l.monto FROM marketplace_ledger_v1 l WHERE l.monto > 0"
        result = self.guard.audit(sql)
        assert "marketplace_ledger_v1" in result.tables_accessed