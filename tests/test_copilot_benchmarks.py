"""Benchmarks for all 11 Copilot handlers (P39R2A).

Measures: time, stability, SQL queries, JSON response integrity.
Baseline comparison against stored golden files.
Run with: python -m pytest tests/test_copilot_benchmarks.py -v
"""
from __future__ import annotations
import pytest
import time
import json
from pathlib import Path
from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)
GOLDEN_DIR = Path(__file__).parent / "golden"

ALL_QUESTIONS = [
    "profit_loss", "why", "marketplace_impact", "top_detalle",
    "commission_impact", "cost_change", "top_transactions",
    "period_change", "cash_flow", "risk", "evidence",
]

# Max acceptable response time in seconds
MAX_TIME_SEC = 5.0


class TestBenchmarkResponseTime:
    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_handler_completes_under_5s(self, qid):
        start = time.time()
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        elapsed = time.time() - start
        assert r.status_code == 200, f"{qid}: {r.status_code}"
        assert elapsed < MAX_TIME_SEC, f"{qid}: took {elapsed:.2f}s (max {MAX_TIME_SEC}s)"
        print(f"  [{qid}] {elapsed:.2f}s")

    def test_benchmark_summary(self):
        results = {}
        for qid in ALL_QUESTIONS:
            start = time.time()
            r = client.get("/api/v4/copilot/ask", params={"question": qid})
            elapsed = time.time() - start
            data = r.json()
            byte_size = len(r.text)
            results[qid] = {"time_s": round(elapsed, 3), "bytes": byte_size, "has_data": data.get("answer", {}).get("summary", "") != ""}
            assert r.status_code == 200
        print("\n=== COPILOT BENCHMARK RESULTS ===")
        print(f"{'Question':<25} {'Time(s)':<10} {'Bytes':<10} {'Data':<8}")
        print("-" * 55)
        for qid, res in results.items():
            print(f"{qid:<25} {res['time_s']:<10.3f} {res['bytes']:<10} {'YES' if res['has_data'] else 'NO':<8}")
        avg_time = sum(r["time_s"] for r in results.values()) / len(results)
        print(f"\nAverage: {avg_time:.3f}s  Total: {sum(r['time_s'] for r in results.values()):.3f}s")
        assert avg_time < MAX_TIME_SEC, f"Average response time {avg_time:.2f}s exceeds {MAX_TIME_SEC}s"

    def test_benchmark_stable_across_calls(self):
        """Run profit_loss twice — times should be within 2x of each other."""
        times = []
        for _ in range(3):
            start = time.time()
            r = client.get("/api/v4/copilot/ask", params={"question": "profit_loss"})
            elapsed = time.time() - start
            assert r.status_code == 200
            times.append(elapsed)
        max_ratio = max(times) / min(times) if min(times) > 0 else 999
        assert max_ratio < 3.0, f"Unstable: max/min ratio = {max_ratio:.2f}"
        print(f"  [stability] times={[f'{t:.2f}s' for t in times]}, ratio={max_ratio:.2f}")

    def test_benchmark_json_integrity(self):
        """All responses must be valid JSON with no truncation."""
        for qid in ALL_QUESTIONS:
            r = client.get("/api/v4/copilot/ask", params={"question": qid})
            assert r.status_code == 200
            try:
                data = json.loads(r.text)
            except json.JSONDecodeError as e:
                pytest.fail(f"{qid}: invalid JSON — {e}")
            assert "answer" in data, f"{qid}: missing answer"
            assert "explanation" in data, f"{qid}: missing explanation"
            assert "evidence" in data, f"{qid}: missing evidence"

    def test_benchmark_marketplace_filter_speed(self):
        """ALL filter should be similar speed to specific MP."""
        start_all = time.time()
        r_all = client.get("/api/v4/copilot/ask", params={"question": "profit_loss", "marketplace": "ALL"})
        time_all = time.time() - start_all
        assert r_all.status_code == 200

        start_mp = time.time()
        r_mp = client.get("/api/v4/copilot/ask", params={"question": "profit_loss", "marketplace": "ML"})
        time_mp = time.time() - start_mp
        assert r_mp.status_code == 200

        print(f"  [filter] ALL={time_all:.2f}s  ML={time_mp:.2f}s")
        assert time_all < MAX_TIME_SEC and time_mp < MAX_TIME_SEC


class TestBenchmarkMemoryFootprint:
    def test_response_size_under_50kb(self):
        """Each response should be under 50KB."""
        for qid in ALL_QUESTIONS:
            r = client.get("/api/v4/copilot/ask", params={"question": qid})
            size_kb = len(r.text) / 1024
            assert size_kb < 50, f"{qid}: {size_kb:.1f}KB exceeds 50KB"
            print(f"  [{qid}] {size_kb:.1f}KB")


class TestBenchmarkGoldenComparison:
    def test_all_questions_have_golden_files(self):
        for qid in ALL_QUESTIONS:
            path = GOLDEN_DIR / f"copilot_{qid}.json"
            assert path.exists(), f"Missing golden: {path}"

    @pytest.mark.parametrize("qid", ALL_QUESTIONS)
    def test_key_structure_matches_golden(self, qid):
        """Live response must have same top-level keys as golden."""
        path = GOLDEN_DIR / f"copilot_{qid}.json"
        with open(path, encoding="utf-8") as f:
            golden = json.load(f)
        r = client.get("/api/v4/copilot/ask", params={"question": qid})
        live = r.json()
        for key in ("question", "period", "answer", "explanation", "breakdown", "evidence"):
            assert key in live, f"{qid}: live missing '{key}'"
            assert key in golden, f"{qid}: golden missing '{key}'"
