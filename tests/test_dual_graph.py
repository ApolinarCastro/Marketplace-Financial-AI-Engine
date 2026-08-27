"""Tests for Phase 1.b CAP-TD-007 — Executable Dual Graph Architecture & Node Connection."""
from __future__ import annotations
import pytest
import json
from engine.v4.knowledge.dual_graph import DualGraphRegistry, GraphNode, GraphEdge


@pytest.fixture
def graph():
    return DualGraphRegistry()


class TestDualGraphStructure:
    def test_graph_initialization_has_nodes_and_edges(self, graph):
        nodes = graph.list_nodes()
        edges = graph.list_edges()
        assert len(nodes) > 30
        assert len(edges) > 20

    def test_knowledge_and_execution_domain_split(self, graph):
        k_nodes = graph.list_nodes("KNOWLEDGE")
        e_nodes = graph.list_nodes("EXECUTION")
        assert len(k_nodes) > 0
        assert len(e_nodes) > 0
        assert len(k_nodes) + len(e_nodes) == len(graph.list_nodes())

    def test_node_ids_unique(self, graph):
        nodes = graph.list_nodes()
        node_ids = [n.node_id for n in nodes]
        assert len(node_ids) == len(set(node_ids))

    def test_no_orphan_nodes(self, graph):
        orphans = graph.audit_orphan_nodes()
        assert orphans == [], f"Orphan nodes detected in Dual Graph: {orphans}"

    def test_no_invalid_cycles(self, graph):
        cycles = graph.audit_cycles()
        assert cycles == [], f"Cycles detected in Dual Graph: {cycles}"


class TestFinancialQuestionCrossGraphPaths:
    @pytest.mark.parametrize("qid", [f"Q-{i:03d}" for i in range(1, 11)])
    def test_each_question_has_valid_cross_graph_path(self, graph, qid):
        res = graph.trace_question_path(qid)
        assert res["question_id"] == qid
        assert len(res["path_nodes"]) >= 4
        assert res["is_complete"] is True
        assert len(res["edges"]) >= 3


class TestDualGraphExportAndIntegrity:
    def test_export_json_valid_and_parseable(self, graph):
        raw_json = graph.export_json()
        parsed = json.loads(raw_json)
        assert "nodes" in parsed
        assert "edges" in parsed
        assert "metadata" in parsed
        assert parsed["metadata"]["total_nodes"] == len(graph.list_nodes())

    def test_unofficial_relation_type_raises_value_error(self, graph):
        node1 = GraphNode("TEST-N1", "Documento", "KNOWLEDGE", "QA", "CERTIFICADO")
        node2 = GraphNode("TEST-N2", "Documento", "KNOWLEDGE", "QA", "CERTIFICADO")
        graph.add_node(node1)
        graph.add_node(node2)
        
        with pytest.raises(ValueError, match="Unofficial relation type"):
            graph.add_edge(GraphEdge("E-BAD", "TEST-N1", "TEST-N2", "UNOFFICIAL_RELATION"))
