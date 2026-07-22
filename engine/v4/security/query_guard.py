"""QueryGuard — Read-only SQL Auditor for Financial Engine.

Detects dangerous SQL patterns without blocking execution.
Mode: AUDIT ONLY — generates evidence, does NOT modify queries.
"""
from __future__ import annotations
import re
import sqlglot
from sqlglot import exp
from typing import Any
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    """Severity levels for detected issues."""
    CRITICAL = "CRITICAL"   # Mutations, DDL, unrestricted access
    HIGH = "HIGH"           # N+1 patterns, missing filters
    MEDIUM = "MEDIUM"       # Redundant SELECT *, PII exposure
    LOW = "LOW"             # Style, optimization hints
    INFO = "INFO"           # Informational


class IssueType(Enum):
    """Types of SQL issues detected."""
    # Mutations (CRITICAL)
    MUTATION_INSERT = "mutation_insert"
    MUTATION_UPDATE = "mutation_update"
    MUTATION_DELETE = "mutation_delete"
    MUTATION_DDL = "mutation_ddl"  # DROP, ALTER, CREATE, TRUNCATE
    
    # Access violations (CRITICAL)
    UNAUTHORIZED_TABLE = "unauthorized_table"
    PII_COLUMN_EXPOSURE = "pii_column_exposure"
    
    # Performance (HIGH/MEDIUM)
    N_PLUS_ONE = "n_plus_one"
    MISSING_FILTER = "missing_filter"
    SELECT_STAR = "select_star"
    REDUNDANT_JOIN = "redundant_join"
    CARTESIAN_PRODUCT = "cartesian_product"
    
    # Style/Quality (LOW/INFO)
    UNUSED_INDEX_HINT = "unused_index_hint"
    SUBOPTIMAL_ORDER_BY = "suboptimal_order_by"


# PII column patterns (case-insensitive)
PII_PATTERNS = [
    r".*_ssn$", r".*_social_security$", r".*_password$", r".*_passwd$",
    r".*_secret$", r".*_token$", r".*_api_key$", r".*_credit_card$",
    r".*_card_number$", r".*_cvv$", r".*_iban$", r".*_rut$", r".*_dni$",
    r".*_email$", r".*_phone$", r".*_address$", r".*_salary$", r".*_income$",
    # Broader patterns for common PII
    r".*password.*", r".*passwd.*", r".*secret.*", r".*token.*",
    r".*credit.?card.*", r".*card.?number.*", r".*cvv.*",
]


# Allowed tables for financial queries (whitelist)
ALLOWED_TABLES = {
    "marketplace_ledger_v1",
    "marketplace_ledger_clasificado_v1",
    "marketplace_cierre_financiero_v1",
    "marketplace_auditoria_v1",
    "marketplace_correcciones_v1",
    "dte_truth_v1",
    "ventas_marketplace",
    "transaction_ledger",
    "order_reconciliation",
    "exceptions",
    "financial_reconciliation",
    "liberaciones",
    "retiros",
    "bank_statement",
    "cargos_no_clasificados",
    "inconsistencias_financieras",
    "pipeline_log",
    "tabla_mapeo",
    "ai_suggestions_log",
    "file_registry",
}


@dataclass
class QueryIssue:
    """A single detected issue in a SQL query."""
    issue_type: IssueType
    severity: Severity
    message: str
    location: str | None = None  # SQL snippet or line reference
    suggestion: str | None = None


@dataclass
class QueryAuditResult:
    """Result of auditing a SQL query."""
    original_sql: str
    parsed_ast: Any = None
    issues: list[QueryIssue] = field(default_factory=list)
    tables_accessed: set[str] = field(default_factory=set)
    columns_selected: list[str] = field(default_factory=list)
    has_mutations: bool = False
    is_read_only: bool = True
    
    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.CRITICAL)
    
    @property
    def high_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.HIGH)
    
    @property
    def summary(self) -> str:
        if self.critical_count > 0:
            return f"❌ {self.critical_count} CRITICAL, {self.high_count} HIGH"
        elif self.high_count > 0:
            return f"⚠️ {self.high_count} HIGH"
        elif self.issues:
            return f"ℹ️ {len(self.issues)} issues (MEDIUM/LOW)"
        return "✅ Clean"


class QueryGuard:
    """Read-only SQL auditor for financial queries.
    
    Does NOT block execution. Only generates evidence for review.
    """
    
    def __init__(
        self,
        allowed_tables: set[str] | None = None,
        pii_columns: list[str] | None = None,
        dialect: str = "duckdb",
    ):
        self.allowed_tables = allowed_tables or ALLOWED_TABLES
        self.pii_patterns = pii_columns or PII_PATTERNS
        self.dialect = dialect
    
    def audit(self, sql: str) -> QueryAuditResult:
        """Audit a SQL query and return detected issues."""
        result = QueryAuditResult(original_sql=sql)
        
        try:
            # Parse SQL with sqlglot
            ast = sqlglot.parse_one(sql, dialect=self.dialect)
            result.parsed_ast = ast
            
            # Run all checks
            self._check_mutations(ast, result)
            self._check_table_access(ast, result)
            self._check_pii_exposure(ast, result)
            self._check_n_plus_one(ast, result)
            self._check_missing_filters(ast, result)
            self._check_select_star(ast, result)
            self._check_redundant_joins(ast, result)
            self._check_cartesian_product(ast, result)
            
        except sqlglot.errors.ParseError as e:
            result.issues.append(QueryIssue(
                issue_type=IssueType.MUTATION_DDL,
                severity=Severity.INFO,
                message=f"Could not parse SQL: {e}",
                suggestion="Review query syntax manually",
            ))
        except Exception as e:
            # Unexpected errors - log but don't mask
            result.issues.append(QueryIssue(
                issue_type=IssueType.MUTATION_DDL,
                severity=Severity.INFO,
                message=f"Unexpected error during audit: {e}",
                suggestion="Review query manually",
            ))
        
        return result
    
    def _check_mutations(self, ast: exp.Expression, result: QueryAuditResult):
        """Detect INSERT, UPDATE, DELETE, DDL statements."""
        mutation_types = {
            exp.Insert: (IssueType.MUTATION_INSERT, "INSERT statement detected"),
            exp.Update: (IssueType.MUTATION_UPDATE, "UPDATE statement detected"),
            exp.Delete: (IssueType.MUTATION_DELETE, "DELETE statement detected"),
            exp.Create: (IssueType.MUTATION_DDL, "CREATE statement detected"),
            exp.Drop: (IssueType.MUTATION_DDL, "DROP statement detected"),
            exp.Alter: (IssueType.MUTATION_DDL, "ALTER statement detected"),
        }
        
        # Handle TruncateTable which may be named differently in sqlglot versions
        truncate_type = getattr(exp, 'TruncateTable', getattr(exp, 'Truncate', None))
        if truncate_type:
            mutation_types[truncate_type] = (IssueType.MUTATION_DDL, "TRUNCATE statement detected")
        
        for node_type, (issue_type, msg) in mutation_types.items():
            for node in ast.find_all(node_type):
                result.has_mutations = True
                result.is_read_only = False
                result.issues.append(QueryIssue(
                    issue_type=issue_type,
                    severity=Severity.CRITICAL,
                    message=msg,
                    location=node.sql(dialect=self.dialect)[:100],
                    suggestion="Financial queries must be read-only. Use SELECT only.",
                ))
    
    def _check_table_access(self, ast: exp.Expression, result: QueryAuditResult):
        """Check all accessed tables against whitelist."""
        for table in ast.find_all(exp.Table):
            table_name = table.name.lower()
            result.tables_accessed.add(table_name)
            
            if table_name not in self.allowed_tables:
                result.issues.append(QueryIssue(
                    issue_type=IssueType.UNAUTHORIZED_TABLE,
                    severity=Severity.CRITICAL,
                    message=f"Access to unauthorized table: {table_name}",
                    location=table.sql(dialect=self.dialect),
                    suggestion=f"Allowed tables: {', '.join(sorted(self.allowed_tables))}",
                ))
    
    def _check_pii_exposure(self, ast: exp.Expression, result: QueryAuditResult):
        """Detect SELECT of PII columns."""
        for column in ast.find_all(exp.Column):
            col_name = column.name.lower()
            for pattern in self.pii_patterns:
                if re.match(pattern, col_name, re.IGNORECASE):
                    result.issues.append(QueryIssue(
                        issue_type=IssueType.PII_COLUMN_EXPOSURE,
                        severity=Severity.CRITICAL,
                        message=f"Potential PII column exposed: {col_name}",
                        location=column.sql(dialect=self.dialect),
                        suggestion="Explicitly list safe columns instead of SELECT *",
                    ))
                    break
            
            # Track all selected columns
            result.columns_selected.append(col_name)
    
    def _check_n_plus_one(self, ast: exp.Expression, result: QueryAuditResult):
        """Detect potential N+1 query patterns (multiple similar queries in loop context).
        
        Heuristic: Multiple queries with same structure but different parameters
        are typically run in application loops. We flag correlated subqueries
        that could be JOINs.
        """
        # Check for correlated subqueries that could be JOINs
        for subquery in ast.find_all(exp.Subquery):
            parent = subquery.parent
            if isinstance(parent, (exp.Where, exp.Join)):
                # Check if it references outer query columns
                outer_refs = list(subquery.find_all(exp.Column, lambda c: c.table and c.table != subquery.alias))
                if outer_refs:
                    result.issues.append(QueryIssue(
                        issue_type=IssueType.N_PLUS_ONE,
                        severity=Severity.HIGH,
                        message="Correlated subquery detected - consider JOIN instead",
                        location=subquery.sql(dialect=self.dialect)[:150],
                        suggestion="Rewrite as JOIN or use LATERAL JOIN for better performance",
                    ))
    
    def _check_missing_filters(self, ast: exp.Expression, result: QueryAuditResult):
        """Detect queries without WHERE filters on large tables."""
        # Only check SELECT statements
        if not isinstance(ast, exp.Select):
            return
        
        # Get FROM table
        from_tables = list(ast.find_all(exp.Table))
        if not from_tables:
            return
        
        # Check for WHERE clause
        where_clause = ast.args.get("where")
        if where_clause is None:
            for table in from_tables:
                if table.name.lower() in self.allowed_tables:
                    result.issues.append(QueryIssue(
                        issue_type=IssueType.MISSING_FILTER,
                        severity=Severity.HIGH,
                        message=f"Full table scan on {table.name} - no WHERE filter",
                        location=table.sql(dialect=self.dialect),
                        suggestion="Add WHERE filter (period, marketplace, financial_group)",
                    ))
    
    def _check_select_star(self, ast: exp.Expression, result: QueryAuditResult):
        """Detect SELECT * patterns."""
        for star in ast.find_all(exp.Star):
            result.issues.append(QueryIssue(
                issue_type=IssueType.SELECT_STAR,
                severity=Severity.MEDIUM,
                message="SELECT * used - explicit columns preferred",
                location=star.sql(dialect=self.dialect),
                suggestion="List explicit columns for better performance and auditability",
            ))
    
    def _check_redundant_joins(self, ast: exp.Expression, result: QueryAuditResult):
        """Detect redundant self-joins or duplicate joins."""
        joins = list(ast.find_all(exp.Join))
        join_tables = []
        
        for join in joins:
            table_name = join.this.name.lower() if isinstance(join.this, exp.Table) else str(join.this)
            if table_name in join_tables:
                result.issues.append(QueryIssue(
                    issue_type=IssueType.REDUNDANT_JOIN,
                    severity=Severity.MEDIUM,
                    message=f"Duplicate JOIN to {table_name}",
                    location=join.sql(dialect=self.dialect)[:150],
                    suggestion="Remove duplicate JOIN or use CTE",
                ))
            join_tables.append(table_name)
    
    def _check_cartesian_product(self, ast: exp.Expression, result: QueryAuditResult):
        """Detect missing JOIN conditions (Cartesian products)."""
        joins = list(ast.find_all(exp.Join))
        for join in joins:
            if join.args.get("on") is None:
                result.issues.append(QueryIssue(
                    issue_type=IssueType.CARTESIAN_PRODUCT,
                    severity=Severity.HIGH,
                    message="JOIN without ON condition - Cartesian product",
                    location=join.sql(dialect=self.dialect)[:150],
                    suggestion="Add ON clause with join condition",
                ))


# Convenience function for direct use
def audit_query(sql: str, **kwargs) -> QueryAuditResult:
    """Audit a single SQL query."""
    guard = QueryGuard(**kwargs)
    return guard.audit(sql)


# Batch audit for multiple queries
def audit_queries(sql_list: list[str], **kwargs) -> list[QueryAuditResult]:
    """Audit multiple SQL queries."""
    guard = QueryGuard(**kwargs)
    return [guard.audit(sql) for sql in sql_list]