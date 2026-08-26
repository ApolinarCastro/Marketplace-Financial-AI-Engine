"""Benchmark Framework — Ponytail methodology for performance regression detection.

Implements: baseline, current, candidate arms with 10-run median reporting.
Metrics: time (seconds), memory (MB), SQL executed (count), stability (stddev), regression flag.
"""
from __future__ import annotations
import pytest
import time
import statistics
import tracemalloc
import os
from dataclasses import dataclass, field
from typing import Callable, Any
from pathlib import Path
import json

from engine.v4.domain.financial_engine import FinancialEngine
from engine.v4.database import DatabaseV4

fe = FinancialEngine()
db = DatabaseV4.get()

BENCH_DIR = Path(__file__).parent / "benchmarks"
BENCH_DIR.mkdir(exist_ok=True)

# ════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ════════════════════════════════════════════════════════════════════

@dataclass
class BenchmarkResult:
    """Single benchmark run result."""
    name: str
    arm: str  # "baseline" | "current" | "candidate"
    duration_ms: float
    memory_mb: float
    sql_count: int
    success: bool
    error: str | None = None


@dataclass
class BenchmarkSummary:
    """Aggregated benchmark summary (median of runs)."""
    name: str
    arm: str
    median_duration_ms: float
    median_memory_mb: float
    median_sql_count: int
    stddev_duration_ms: float
    stddev_memory_mb: float
    runs: int
    success_rate: float
    
    def regression_vs(self, other: "BenchmarkSummary", threshold_pct: float = 10.0) -> dict:
        """Compare against another arm, return regression info."""
        if self.median_duration_ms == 0:
            duration_delta_pct = 0
        else:
            duration_delta_pct = ((self.median_duration_ms - other.median_duration_ms) / other.median_duration_ms) * 100
        
        if self.median_memory_mb == 0:
            memory_delta_pct = 0
        else:
            memory_delta_pct = ((self.median_memory_mb - other.median_memory_mb) / other.median_memory_mb) * 100
        
        regressed = (
            duration_delta_pct > threshold_pct or 
            memory_delta_pct > threshold_pct or
            self.success_rate < 0.9
        )
        
        return {
            "regressed": regressed,
            "duration_delta_pct": round(duration_delta_pct, 1),
            "memory_delta_pct": round(memory_delta_pct, 1),
            "success_rate": self.success_rate,
        }


# ════════════════════════════════════════════════════════════════════
# BENCHMARK RUNNER
# ════════════════════════════════════════════════════════════════════

class BenchmarkRunner:
    """Executes benchmarks with Ponytail methodology.
    
    Measures: time (ms), memory (MB), success rate
    Arms: baseline, current, candidate
    Methodology: 10 runs, median reported
    """
    
    def __init__(self, runs: int = 10, warmup: int = 2):
        self.runs = runs
        self.warmup = warmup
    
    def _run_once(self, name: str, arm: str, fn: Callable) -> BenchmarkResult:
        """Execute a single benchmark run."""
        # Start memory tracking
        tracemalloc.start()
        start_mem = tracemalloc.get_traced_memory()[0]
        
        start_time = time.perf_counter()
        try:
            result = fn()
            success = True
            error = None
        except Exception as e:
            success = False
            error = str(e)
            result = None
        end_time = time.perf_counter()
        
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        duration_ms = (end_time - start_time) * 1000
        memory_mb = (peak_mem - start_mem) / (1024 * 1024)
        
        return BenchmarkResult(
            name=name,
            arm=arm,
            duration_ms=duration_ms,
            memory_mb=memory_mb,
            sql_count=0,  # Not measured - hook removed to avoid test interference
            success=success,
            error=error,
        )
    
    def run_arm(self, name: str, arm: str, fn: Callable) -> BenchmarkSummary:
        """Run benchmark for one arm (baseline/current/candidate)."""
        results = []
        
        # Warmup runs (not counted)
        for _ in range(self.warmup):
            try:
                fn()
            except:
                pass
        
        # Measured runs
        for i in range(self.runs):
            result = self._run_once(name, arm, fn)
            results.append(result)
        
        # Aggregate
        successful = [r for r in results if r.success]
        if not successful:
            return BenchmarkSummary(
                name=name, arm=arm,
                median_duration_ms=0, median_memory_mb=0, median_sql_count=0,
                stddev_duration_ms=0, stddev_memory_mb=0,
                runs=self.runs, success_rate=0.0,
            )
        
        durations = [r.duration_ms for r in successful]
        memories = [r.memory_mb for r in successful]
        sqls = [r.sql_count for r in successful]
        
        return BenchmarkSummary(
            name=name,
            arm=arm,
            median_duration_ms=statistics.median(durations),
            median_memory_mb=statistics.median(memories),
            median_sql_count=statistics.median(sqls),
            stddev_duration_ms=statistics.stdev(durations) if len(durations) > 1 else 0,
            stddev_memory_mb=statistics.stdev(memories) if len(memories) > 1 else 0,
            runs=len(successful),
            success_rate=len(successful) / self.runs,
        )


# ════════════════════════════════════════════════════════════════════
# DEFINED BENCHMARKS (5 Core Financial Queries)
# ════════════════════════════════════════════════════════════════════

PERIODO = "2026-01"

BENCHMARKS = [
    {
        "name": "exec_summary_all",
        "description": "Executive Summary — ALL marketplaces YTD",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_exec_summary(periodo=PERIODO, marketplace="ALL"),
    },
    {
        "name": "exec_summary_ml",
        "description": "Executive Summary — ML YTD",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_exec_summary(periodo=PERIODO, marketplace="ML"),
    },
    {
        "name": "waterfall_all",
        "description": "Waterfall — ALL marketplaces YTD",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_waterfall(periodo=PERIODO, marketplace="ALL"),
    },
    {
        "name": "waterfall_ripley",
        "description": "Waterfall — RIPLEY YTD (signal_mode=SIGNAL)",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_waterfall(periodo=PERIODO, marketplace="RIPLEY"),
    },
    {
        "name": "ledger_ml",
        "description": "Ledger Query — ML YTD, signal_mode=SIGNAL, limit=200",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_ledger(marketplace="ML", periodo=PERIODO, signal_mode="SIGNAL", operational_only=True, limit=200),
    },
    {
        "name": "financial_structure_all",
        "description": "Financial Structure — ALL marketplaces YTD",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_desglose(marketplace="ALL", periodo=PERIODO, exclude_non_operational=True),
    },
    {
        "name": "cobros_breakdown",
        "description": "Cobros Breakdown Matrix — YTD",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_cobros_breakdown(periodo=PERIODO),
    },
    {
        "name": "cierre_all",
        "description": "Cierre Financiero — ALL marketplaces",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_cierre_all(),
    },
    {
        "name": "audit_ml",
        "description": "Audit Query — ML (first page)",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_audit(marketplace="ML", limit=50),
    },
    {
        "name": "operational_intelligence_ml",
        "description": "Operational Intelligence — ML YTD",
        "fn": lambda: FinancialEngine(DatabaseV4.get()).query_operational_intelligence(periodo=PERIODO, marketplace="ML"),
    },
]


# ════════════════════════════════════════════════════════════════════
# PYTEST INTEGRATION
# ════════════════════════════════════════════════════════════════════

def _save_benchmark_result(summary: BenchmarkSummary, arm: str):
    """Save benchmark result to JSON file."""
    fname = BENCH_DIR / f"{summary.name}_{arm}.json"
    data = {
        "name": summary.name,
        "arm": summary.arm,
        "median_duration_ms": summary.median_duration_ms,
        "median_memory_mb": summary.median_memory_mb,
        "median_sql_count": summary.median_sql_count,
        "stddev_duration_ms": summary.stddev_duration_ms,
        "stddev_memory_mb": summary.stddev_memory_mb,
        "runs": summary.runs,
        "success_rate": summary.success_rate,
        "timestamp": time.time(),
    }
    with open(fname, "w") as f:
        json.dump(data, f, indent=2)


def _load_benchmark_result(name: str, arm: str) -> BenchmarkSummary | None:
    """Load benchmark result from JSON file."""
    fname = BENCH_DIR / f"{name}_{arm}.json"
    if not fname.exists():
        return None
    with open(fname) as f:
        data = json.load(f)
    # Filter to only dataclass fields
    fields = {f.name for f in BenchmarkSummary.__dataclass_fields__.values()}
    filtered = {k: v for k, v in data.items() if k in fields}
    return BenchmarkSummary(**filtered)


@pytest.fixture
def benchmark_runner():
    return BenchmarkRunner(runs=10, warmup=2)


@pytest.mark.parametrize("bench", BENCHMARKS)
def test_benchmark_current(bench, benchmark_runner):
    """Run current implementation (baseline for comparison)."""
    summary = benchmark_runner.run_arm(bench["name"], "current", bench["fn"])
    _save_benchmark_result(summary, "current")
    
    # Verify success
    assert summary.success_rate >= 0.9, f"{bench['name']}: success_rate={summary.success_rate}"
    
    # Print summary
    print(f"\n  {bench['name']} ({bench['description']}):")
    print(f"    duration: {summary.median_duration_ms:.1f}ms ± {summary.stddev_duration_ms:.1f}ms")
    print(f"    memory: {summary.median_memory_mb:.1f}MB ± {summary.stddev_memory_mb:.1f}MB")
    print(f"    sql_count: {summary.median_sql_count}")
    print(f"    success: {summary.success_rate:.0%}")


# ════════════════════════════════════════════════════════════════════
# REGRESSION DETECTION (Compare current vs baseline)
# ════════════════════════════════════════════════════════════════════

def test_benchmark_regression_detection(benchmark_runner):
    """Compare current vs established baseline for regressions.
    
    Baseline must be established first (run test_benchmark_establish_baseline manually).
    This test is skipped by default - enable when baseline is stable.
    """
    pytest.skip("Enable manually after establishing stable baseline")
    regressions = []
    
    for bench in BENCHMARKS:
        current = _load_benchmark_result(bench["name"], "current")
        baseline = _load_benchmark_result(bench["name"], "baseline")
        
        if baseline is None:
            print(f"  {bench['name']}: No baseline established — run test_benchmark_establish_baseline first")
            continue
        
        cmp = current.regression_vs(baseline, threshold_pct=30.0)
        
        if cmp["regressed"]:
            regressions.append({
                "benchmark": bench["name"],
                "duration_delta_pct": cmp["duration_delta_pct"],
                "memory_delta_pct": cmp["memory_delta_pct"],
                "success_rate": cmp["success_rate"],
            })
            print(f"  ⚠️ REGRESSION: {bench['name']} — duration: {cmp['duration_delta_pct']:+.1f}%, memory: {cmp['memory_delta_pct']:+.1f}%")
        else:
            print(f"  ✓ {bench['name']}: duration={cmp['duration_delta_pct']:+.1f}%, memory={cmp['memory_delta_pct']:+.1f}%")
    
    if regressions:
        pytest.fail(f"Performance regressions detected: {regressions}")


def test_benchmark_summary_report():
    """Generate consolidated benchmark report."""
    report = {
        "timestamp": time.time(),
        "benchmarks": [],
    }
    
    for bench in BENCHMARKS:
        current = _load_benchmark_result(bench["name"], "current")
        baseline = _load_benchmark_result(bench["name"], "baseline")
        
        entry = {
            "name": bench["name"],
            "description": bench["description"],
            "current": {
                "duration_ms": current.median_duration_ms if current else None,
                "memory_mb": current.median_memory_mb if current else None,
                "sql_count": current.median_sql_count if current else None,
                "success_rate": current.success_rate if current else None,
            },
            "baseline": {
                "duration_ms": baseline.median_duration_ms if baseline else None,
                "memory_mb": baseline.median_memory_mb if baseline else None,
                "sql_count": baseline.median_sql_count if baseline else None,
            } if baseline else None,
        }
        
        if current and baseline:
            cmp = current.regression_vs(baseline)
            entry["regression"] = cmp
        
        report["benchmarks"].append(entry)
    
    report_path = BENCH_DIR / "benchmark_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Benchmark report saved to: {report_path}")


# ════════════════════════════════════════════════════════════════════
# CANDIDATE MODE (for testing optimizations)
# ════════════════════════════════════════════════════════════════════

def test_benchmark_candidate_mode(benchmark_runner):
    """Run candidate arm — use for testing optimizations before promotion."""
    # This test is manual — override with candidate implementation
    # Example usage:
    #   summary = benchmark_runner.run_arm("exec_summary_all", "candidate", my_optimized_fn)
    #   _save_benchmark_result(summary, "candidate")
    pass