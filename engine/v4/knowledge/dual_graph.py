"""Dual Graph Architecture Module — Executable representation of Knowledge Graph and Execution Graph.

Fulfills Phase 0 & Phase 1 specifications in DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md.
Provides deterministic, in-memory graph structures, node/edge registries, traversal paths,
and cross-graph audit functions without third-party graph engines.
"""
from __future__ import annotations
from typing import Any, Literal
from dataclasses import dataclass, field
import datetime
import json

DomainType = Literal["KNOWLEDGE", "EXECUTION"]


@dataclass
class GraphNode:
    node_id: str
    node_type: str
    domain: DomainType
    owner: str
    estado: str
    version: str = "1.0.0"
    path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "domain": self.domain,
            "owner": self.owner,
            "estado": self.estado,
            "version": self.version,
            "path": self.path,
            "metadata": self.metadata,
        }


@dataclass
class GraphEdge:
    edge_id: str
    source_id: str
    target_id: str
    relation_type: str
    cardinality: str = "1:1"
    audit_notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type,
            "cardinality": self.cardinality,
            "audit_notes": self.audit_notes,
        }


class DualGraphRegistry:
    """Executable Dual Graph Registry for Knowledge & Execution Graph nodes and edges."""

    OFFICIAL_RELATIONS = {
        "IMPLEMENTA", "DEPENDE_DE", "RESPONDE", "USA", "CERTIFICA",
        "ORIGINA", "DERIVA_DE", "REEMPLAZA", "VALIDA", "RESUELVE",
        "BLOQUEA", "CONTRADICE", "AFECTA", "PRODUCE", "CONSUME",
        "EJECUTA", "FALLA_EN", "EVIDENCIA", "PERTENECE_A", "TRANSFORMA",
        "RECONCILIA", "EXPONE", "MIDE", "CUMPLE", "VIOLA", "TRAZA",
        "SOPORTA", "RESPONDIDA_POR", "IMPLEMENTADA_POR", "EVIDENCIADA_POR",
        "DOCUMENTA", "UTILIZA", "GENERA", "REFERENCIA", "DESTINO_DE"
    }

    def __init__(self):
        self._nodes: dict[str, GraphNode] = {}
        self._edges: dict[str, GraphEdge] = {}
        self._build_default_graph()

    def add_node(self, node: GraphNode) -> None:
        if node.node_id in self._nodes:
            raise ValueError(f"Duplicate node_id: {node.node_id}")
        self._nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        if edge.edge_id in self._edges:
            raise ValueError(f"Duplicate edge_id: {edge.edge_id}")
        if edge.source_id not in self._nodes:
            raise ValueError(f"Source node {edge.source_id} does not exist")
        if edge.target_id not in self._nodes:
            raise ValueError(f"Target node {edge.target_id} does not exist")
        if edge.relation_type not in self.OFFICIAL_RELATIONS:
            raise ValueError(f"Unofficial relation type: {edge.relation_type}")
        self._edges[edge.edge_id] = edge

    def get_node(self, node_id: str) -> GraphNode | None:
        return self._nodes.get(node_id)

    def get_out_edges(self, node_id: str) -> list[GraphEdge]:
        return [e for e in self._edges.values() if e.source_id == node_id]

    def get_in_edges(self, node_id: str) -> list[GraphEdge]:
        return [e for e in self._edges.values() if e.target_id == node_id]

    def list_nodes(self, domain: DomainType | None = None) -> list[GraphNode]:
        if domain:
            return [n for n in self._nodes.values() if n.domain == domain]
        return list(self._nodes.values())

    def list_edges(self) -> list[GraphEdge]:
        return list(self._edges.values())

    def trace_question_path(self, question_id: str) -> dict[str, Any]:
        """Returns the full cross-graph path for a Financial Copilot Question."""
        if question_id not in self._nodes:
            raise ValueError(f"Unknown question node: {question_id}")
        
        out_edges = self.get_out_edges(question_id)
        path = [question_id]
        visited_edges = []
        
        curr_id = question_id
        while True:
            edges = self.get_out_edges(curr_id)
            if not edges:
                break
            e = edges[0]
            visited_edges.append(e.to_dict())
            curr_id = e.target_id
            path.append(curr_id)
            if len(path) > 20:  # Safety against cycles
                break
                
        return {
            "question_id": question_id,
            "path_nodes": path,
            "edges": visited_edges,
            "is_complete": len(path) >= 4,
        }

    def audit_orphan_nodes(self) -> list[str]:
        """Returns node_ids of nodes that have neither incoming nor outgoing edges."""
        connected_nodes = set()
        for e in self._edges.values():
            connected_nodes.add(e.source_id)
            connected_nodes.add(e.target_id)
        return [nid for nid in self._nodes if nid not in connected_nodes]

    def audit_cycles(self) -> list[list[str]]:
        """Simple DFS cycle detection."""
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(curr: str, path: list[str]):
            visited.add(curr)
            rec_stack.add(curr)
            path.append(curr)

            for e in self.get_out_edges(curr):
                nxt = e.target_id
                if nxt not in visited:
                    dfs(nxt, path.copy())
                elif nxt in rec_stack:
                    cycle_start = path.index(nxt)
                    cycles.append(path[cycle_start:] + [nxt])

            rec_stack.remove(curr)

        for nid in list(self._nodes.keys()):
            if nid not in visited:
                dfs(nid, [])

        return cycles

    def export_json(self) -> str:
        return json.dumps({
            "nodes": [n.to_dict() for n in self._nodes.values()],
            "edges": [e.to_dict() for e in self._edges.values()],
            "metadata": {
                "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "total_nodes": len(self._nodes),
                "total_edges": len(self._edges),
                "knowledge_nodes": len(self.list_nodes("KNOWLEDGE")),
                "execution_nodes": len(self.list_nodes("EXECUTION")),
            }
        }, indent=2)

    def _build_default_graph(self) -> None:
        """Constructs the certified Phase 1 Dual Graph nodes and edges."""
        # 1. Knowledge Graph Nodes
        k_nodes = [
            GraphNode("DOC-001", "Documento", "KNOWLEDGE", "PMO", "CERTIFICADO", path="governance/EXECUTION_PLAN_PHASE_0_FOUNDATION_V3.md"),
            GraphNode("DOC-002", "Documento", "KNOWLEDGE", "Chief Architect", "CERTIFICADO", path="governance/ARCHITECTURE_REGISTRY_V1.md"),
            GraphNode("DOC-003", "Documento", "KNOWLEDGE", "Data Architect", "CERTIFICADO", path="governance/DATA_CONTRACT_REGISTRY_V1.md"),
            GraphNode("DOC-004", "Documento", "KNOWLEDGE", "Evidence Guardian", "CERTIFICADO", path="governance/EVIDENCE_REGISTRY_V1.md"),
            GraphNode("DOC-005", "Documento", "KNOWLEDGE", "Knowledge Eng", "CERTIFICADO", path="governance/KNOWLEDGE_OS_SPECIFICATION.md"),
            GraphNode("DOC-006", "Documento", "KNOWLEDGE", "Graph Architect", "CERTIFICADO", path="governance/DUAL_GRAPH_ARCHITECTURE_MODEL_V1.md"),
            GraphNode("DOC-007", "Documento", "KNOWLEDGE", "AI Architect", "CERTIFICADO", path="governance/SYSTEM_INTELLIGENCE_SPECIFICATION_V1.md"),
            GraphNode("DOC-008", "Documento", "KNOWLEDGE", "PMO Lead", "CERTIFICADO", path="governance/PMO_REGISTRY_V1.md"),
            GraphNode("DOC-009", "Documento", "KNOWLEDGE", "QA Manager", "CERTIFICADO", path="governance/MATURITY_REGISTRY_V1.md"),
            GraphNode("DOC-010", "Documento", "KNOWLEDGE", "Technical Debt Lead", "CERTIFICADO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),
            
            # Data Contracts
            GraphNode("CTR-001", "Contrato_Datos", "KNOWLEDGE", "Data Eng", "CERTIFICADO"),
            GraphNode("CTR-002", "Contrato_Datos", "KNOWLEDGE", "Data Eng", "CERTIFICADO"),
            GraphNode("CTR-003", "Contrato_Datos", "KNOWLEDGE", "DTE Lead", "VALIDADO"),
            GraphNode("CTR-004", "Contrato_Datos", "KNOWLEDGE", "SAP Lead", "ESPECIFICADO"),
            GraphNode("CTR-005", "Contrato_Datos", "KNOWLEDGE", "Settlement Lead", "CERTIFICADO"),
            GraphNode("CTR-006", "Contrato_Datos", "KNOWLEDGE", "Treasury Lead", "VALIDADO"),
            GraphNode("CTR-007", "Contrato_Datos", "KNOWLEDGE", "Bank Lead", "ESPECIFICADO"),
            GraphNode("CTR-008", "Contrato_Datos", "KNOWLEDGE", "Truth Guardian", "CERTIFICADO"),
            GraphNode("CTR-009", "Contrato_Datos", "KNOWLEDGE", "Evidence Guardian", "CERTIFICADO"),
            GraphNode("CTR-010", "Contrato_Datos", "KNOWLEDGE", "Knowledge Eng", "CERTIFICADO"),
            GraphNode("CTR-011", "Contrato_Datos", "KNOWLEDGE", "Copilot Architect", "CERTIFICADO"),

            # Capabilities
            GraphNode("CAP-TD-001", "Capacidad", "KNOWLEDGE", "QA Lead", "CERTIFICADO"),
            GraphNode("CAP-TD-002", "Capacidad", "KNOWLEDGE", "API Lead", "CERTIFICADO"),
            GraphNode("CAP-TD-003", "Capacidad", "KNOWLEDGE", "UX Lead", "CERTIFICADO"),
            GraphNode("CAP-TD-004", "Capacidad", "KNOWLEDGE", "Knowledge Eng", "CERTIFICADO"),
            GraphNode("CAP-TD-005", "Capacidad", "KNOWLEDGE", "Data Eng", "CERTIFICADO"),
            GraphNode("CAP-TD-006", "Capacidad", "KNOWLEDGE", "Copilot Architect", "CERTIFICADO"),
            GraphNode("CAP-TD-007", "Capacidad", "KNOWLEDGE", "Graph Architect", "CERTIFICADO"),
            GraphNode("CAP-TD-008", "Capacidad", "KNOWLEDGE", "Data Eng", "CERTIFICADO"),
            GraphNode("CAP-F2-001", "Capacidad", "KNOWLEDGE", "Financial Eng", "CERTIFICADO"),

            # Evidences
            GraphNode("EVID-TD-001", "Evidencia", "KNOWLEDGE", "QA Lead", "CERTIFICADO", path="evidence/fase_1b/CAP-TD-001.json"),
            GraphNode("EVID-TD-002", "Evidencia", "KNOWLEDGE", "API Lead", "CERTIFICADO", path="evidence/fase_1b/CAP-TD-002.json"),
            GraphNode("EVID-TD-003", "Evidencia", "KNOWLEDGE", "UX Lead", "CERTIFICADO", path="evidence/fase_1b/CAP-TD-003.json"),
            GraphNode("EVID-TD-004", "Evidencia", "KNOWLEDGE", "Knowledge Eng", "CERTIFICADO", path="evidence/fase_1b/CAP-TD-004.json"),
            GraphNode("EVID-TD-005", "Evidencia", "KNOWLEDGE", "Data Eng", "CERTIFICADO", path="evidence/fase_1b/CAP-TD-005.json"),
            GraphNode("EVID-TD-006", "Evidencia", "KNOWLEDGE", "Copilot Architect", "CERTIFICADO", path="evidence/fase_1b/CAP-TD-006.json"),
            GraphNode("EVID-TD-007", "Evidencia", "KNOWLEDGE", "Graph Architect", "CERTIFICADO", path="evidence/fase_1b/CAP-TD-007.json"),
            GraphNode("EVID-TD-008", "Evidencia", "KNOWLEDGE", "Data Eng", "CERTIFICADO", path="evidence/fase_1b/CAP-TD-008.json"),
            GraphNode("EVID-F2-001", "Evidencia", "KNOWLEDGE", "Financial Lead", "CERTIFICADO", path="evidence/fase_2/CAP-F2-001.json"),

            # Financial Questions Q-001 to Q-010
            GraphNode("Q-001", "Pregunta_Financiera", "KNOWLEDGE", "Data Eng", "CERTIFICADO", metadata={"label": "¿Qué vendí?"}),
            GraphNode("Q-002", "Pregunta_Financiera", "KNOWLEDGE", "Cost Analyst", "CERTIFICADO", metadata={"label": "¿Qué me cobraron?"}),
            GraphNode("Q-003", "Pregunta_Financiera", "KNOWLEDGE", "Treasury Lead", "CERTIFICADO", metadata={"label": "¿Qué me pagaron?"}),
            GraphNode("Q-004", "Pregunta_Financiera", "KNOWLEDGE", "Controller", "VALIDADO", metadata={"label": "¿Qué falta por cobrar?"}),
            GraphNode("Q-005", "Pregunta_Financiera", "KNOWLEDGE", "Truth Guardian", "CERTIFICADO", metadata={"label": "¿Qué devoluciones existen?"}),
            GraphNode("Q-006", "Pregunta_Financiera", "KNOWLEDGE", "DTE Lead", "VALIDADO", metadata={"label": "¿Qué XML o DTE respalda la operación?"}),
            GraphNode("Q-007", "Pregunta_Financiera", "KNOWLEDGE", "SAP Lead", "ESPECIFICADO", metadata={"label": "¿Qué registro SAP respalda la operación?"}),
            GraphNode("Q-008", "Pregunta_Financiera", "KNOWLEDGE", "Bank Lead", "ESPECIFICADO", metadata={"label": "¿Qué movimiento bancario respalda el pago?"}),
            GraphNode("Q-009", "Pregunta_Financiera", "KNOWLEDGE", "Truth Guardian", "CERTIFICADO", metadata={"label": "¿Qué cargo no explicado existe?"}),
            GraphNode("Q-010", "Pregunta_Financiera", "KNOWLEDGE", "Controller", "CERTIFICADO", metadata={"label": "¿Cuál es el margen financiero real?"}),

            # Technical Debts TD-001 to TD-008
            GraphNode("TD-001", "Deuda_Técnica", "KNOWLEDGE", "QA Lead", "RESUELTO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),
            GraphNode("TD-002", "Deuda_Técnica", "KNOWLEDGE", "API Lead", "RESUELTO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),
            GraphNode("TD-003", "Deuda_Técnica", "KNOWLEDGE", "UX Lead", "RESUELTO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),
            GraphNode("TD-004", "Deuda_Técnica", "KNOWLEDGE", "Knowledge Eng", "RESUELTO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),
            GraphNode("TD-005", "Deuda_Técnica", "KNOWLEDGE", "Data Eng", "RESUELTO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),
            GraphNode("TD-006", "Deuda_Técnica", "KNOWLEDGE", "Copilot Architect", "RESUELTO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),
            GraphNode("TD-007", "Deuda_Técnica", "KNOWLEDGE", "Graph Architect", "RESUELTO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),
            GraphNode("TD-008", "Deuda_Técnica", "KNOWLEDGE", "Data Eng", "RESUELTO", path="governance/TECHNICAL_DEBT_REGISTRY_V1.md"),

            # Lineages LIN-001 to LIN-012
            GraphNode("LIN-001", "Linaje", "KNOWLEDGE", "Data Eng", "CERTIFICADO"),
            GraphNode("LIN-002", "Linaje", "KNOWLEDGE", "Data Eng", "CERTIFICADO"),
            GraphNode("LIN-003", "Linaje", "KNOWLEDGE", "DTE Lead", "VALIDADO"),
            GraphNode("LIN-004", "Linaje", "KNOWLEDGE", "SAP Lead", "ESPECIFICADO"),
            GraphNode("LIN-005", "Linaje", "KNOWLEDGE", "Settlement Lead", "CERTIFICADO"),
            GraphNode("LIN-006", "Linaje", "KNOWLEDGE", "Treasury Lead", "VALIDADO"),
            GraphNode("LIN-007", "Linaje", "KNOWLEDGE", "Bank Lead", "ESPECIFICADO"),
            GraphNode("LIN-008", "Linaje", "KNOWLEDGE", "Truth Guardian", "CERTIFICADO"),
            GraphNode("LIN-009", "Linaje", "KNOWLEDGE", "Evidence Guardian", "CERTIFICADO"),
            GraphNode("LIN-010", "Linaje", "KNOWLEDGE", "Knowledge Eng", "CERTIFICADO"),
            GraphNode("LIN-011", "Linaje", "KNOWLEDGE", "Copilot Architect", "CERTIFICADO"),
            GraphNode("LIN-012", "Linaje", "KNOWLEDGE", "Graph Architect", "CERTIFICADO"),

            # PMO & Maturity Nodes
            GraphNode("PMO-F1-01", "PMO", "KNOWLEDGE", "PMO Lead", "CERTIFICADO"),
            GraphNode("MAT-001", "Maturity", "KNOWLEDGE", "QA Lead", "CERTIFICADO"),
        ]

        for n in k_nodes:
            self.add_node(n)

        # 2. Execution Graph Nodes
        e_nodes = [
            GraphNode("EXEC_API_COPILOT", "Endpoint", "EXECUTION", "Backend Eng", "CERTIFICADO", path="api/api.py", metadata={"url": "/api/v4/copilot/ask"}),
            GraphNode("EXEC_COPILOT_ENGINE", "Handler", "EXECUTION", "Copilot Arch", "CERTIFICADO", path="engine/v4/copilot/copilot_engine.py"),
            GraphNode("EXEC_FINANCIAL_ENGINE", "Servicio", "EXECUTION", "Engine Lead", "CERTIFICADO", path="engine/v4/domain/financial_engine.py"),
            GraphNode("EXEC_SURGICAL_LOADER", "Pipeline", "EXECUTION", "Data Eng", "CERTIFICADO", path="engine/v4/surgical_loader.py"),
            GraphNode("EXEC_RAW_INDEXER", "Pipeline", "EXECUTION", "Data Eng", "CERTIFICADO", path="engine/v4/ingestion/raw_file_indexer.py"),
            GraphNode("EXEC_DUCKDB_MAIN", "Tabla_DuckDB", "EXECUTION", "DB Arch", "CERTIFICADO", path="data/db/meli_financial_v4.db"),
            GraphNode("EXEC_VALIDATE_HARNESS", "Harness", "EXECUTION", "QA Lead", "CERTIFICADO", path="tools/validate_fase_1b.py"),
            GraphNode("EXEC_DUAL_GRAPH_ENGINE", "Servicio", "EXECUTION", "Graph Arch", "CERTIFICADO", path="engine/v4/knowledge/dual_graph.py"),
            GraphNode("EXEC_PYTEST_SUITE", "Prueba_Integración", "EXECUTION", "QA Lead", "CERTIFICADO", path="tests/"),
        ]

        for n in e_nodes:
            self.add_node(n)

        # 3. Cross-Graph & Internal Edges
        edges = [
            # Documents -> PMO / Caps / Maturity
            GraphEdge("E-DOC-001", "DOC-001", "PMO-F1-01", "PERTENECE_A", "1:1"),
            GraphEdge("E-DOC-002", "DOC-002", "CAP-TD-001", "DOCUMENTA", "1:1"),
            GraphEdge("E-DOC-003", "DOC-003", "CTR-001", "DOCUMENTA", "1:1"),
            GraphEdge("E-DOC-004", "DOC-004", "EVID-TD-001", "DOCUMENTA", "1:1"),
            GraphEdge("E-DOC-005", "DOC-005", "CAP-TD-004", "DOCUMENTA", "1:1"),
            GraphEdge("E-DOC-006", "DOC-006", "CAP-TD-007", "DOCUMENTA", "1:1"),
            GraphEdge("E-DOC-007", "DOC-007", "CAP-TD-006", "DOCUMENTA", "1:1"),
            GraphEdge("E-DOC-008", "DOC-008", "PMO-F1-01", "DOCUMENTA", "1:1"),
            GraphEdge("E-DOC-009", "DOC-009", "MAT-001", "DOCUMENTA", "1:1"),
            GraphEdge("E-DOC-010", "DOC-010", "TD-001", "DOCUMENTA", "1:1"),

            # Contracts -> Lineage
            GraphEdge("E-CTR-001", "CTR-001", "LIN-001", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-002", "CTR-002", "LIN-002", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-003", "CTR-003", "LIN-003", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-004", "CTR-004", "LIN-004", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-005", "CTR-005", "LIN-005", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-006", "CTR-006", "LIN-006", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-007", "CTR-007", "LIN-007", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-009", "CTR-009", "LIN-009", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-010", "CTR-010", "LIN-010", "PERTENECE_A", "1:1"),
            GraphEdge("E-CTR-011", "CTR-011", "LIN-011", "PERTENECE_A", "1:1"),

            # Lineage -> Caps
            GraphEdge("E-LIN-001", "LIN-001", "CAP-TD-008", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-002", "LIN-002", "CAP-TD-008", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-003", "LIN-003", "CAP-TD-003", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-004", "LIN-004", "CAP-TD-004", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-005", "LIN-005", "CAP-TD-005", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-006", "LIN-006", "CAP-TD-005", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-007", "LIN-007", "CAP-TD-005", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-008", "LIN-008", "CAP-TD-005", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-009", "LIN-009", "CAP-TD-005", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-010", "LIN-010", "CAP-TD-005", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-011", "LIN-011", "CAP-TD-006", "SOPORTA", "1:1"),
            GraphEdge("E-LIN-012", "LIN-012", "CAP-TD-007", "SOPORTA", "1:1"),

            # Evidences -> Capabilities
            GraphEdge("E-EVID-001", "EVID-TD-001", "CAP-TD-001", "CERTIFICA", "1:1"),
            GraphEdge("E-EVID-002", "EVID-TD-002", "CAP-TD-002", "CERTIFICA", "1:1"),
            GraphEdge("E-EVID-003", "EVID-TD-003", "CAP-TD-003", "CERTIFICA", "1:1"),
            GraphEdge("E-EVID-004", "EVID-TD-004", "CAP-TD-004", "CERTIFICA", "1:1"),
            GraphEdge("E-EVID-006", "EVID-TD-006", "CAP-TD-006", "CERTIFICA", "1:1"),
            GraphEdge("E-EVID-008", "EVID-TD-008", "CAP-TD-008", "CERTIFICA", "1:1"),

            # Execution Pipeline and Harness
            GraphEdge("E-EXEC-001", "EXEC_SURGICAL_LOADER", "EXEC_DUCKDB_MAIN", "TRANSFORMA", "1:1"),
            GraphEdge("E-EXEC-002", "EXEC_VALIDATE_HARNESS", "EXEC_PYTEST_SUITE", "VALIDA", "1:1"),
            GraphEdge("E-EXEC-003", "EXEC_RAW_INDEXER", "CAP-TD-008", "IMPLEMENTA", "1:1"),

            # Questions -> Execution & Knowledge
            GraphEdge("E-001", "Q-001", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-002", "Q-002", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-003", "Q-003", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-004", "Q-004", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-005", "Q-005", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-006", "Q-006", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-007", "Q-007", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-008", "Q-008", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-009", "Q-009", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),
            GraphEdge("E-010", "Q-010", "EXEC_API_COPILOT", "RESPONDIDA_POR", "1:1"),

            # Execution chain
            GraphEdge("E-011", "EXEC_API_COPILOT", "EXEC_COPILOT_ENGINE", "IMPLEMENTADA_POR", "1:1"),
            GraphEdge("E-012", "EXEC_COPILOT_ENGINE", "EXEC_FINANCIAL_ENGINE", "USA", "1:N"),
            GraphEdge("E-013", "EXEC_FINANCIAL_ENGINE", "EXEC_DUCKDB_MAIN", "CONSUME", "1:N"),
            GraphEdge("E-014", "EXEC_DUCKDB_MAIN", "CTR-008", "CUMPLE", "1:1"),
            GraphEdge("E-015", "CTR-008", "EVID-TD-005", "EVIDENCIADA_POR", "1:1"),
            GraphEdge("E-016", "EVID-TD-005", "CAP-TD-005", "CERTIFICA", "1:1"),

            # Technical Debt resolution
            GraphEdge("E-017", "TD-001", "CAP-TD-001", "RESUELVE", "1:1"),
            GraphEdge("E-018", "TD-002", "CAP-TD-002", "RESUELVE", "1:1"),
            GraphEdge("E-019", "TD-003", "CAP-TD-003", "RESUELVE", "1:1"),
            GraphEdge("E-020", "TD-004", "CAP-TD-004", "RESUELVE", "1:1"),
            GraphEdge("E-021", "TD-005", "CAP-TD-005", "RESUELVE", "1:1"),
            GraphEdge("E-022", "TD-006", "CAP-TD-006", "RESUELVE", "1:1"),
            GraphEdge("E-023", "TD-007", "CAP-TD-007", "RESUELVE", "1:1"),
            GraphEdge("E-027", "TD-008", "CAP-TD-008", "RESUELVE", "1:1"),

            # Executable Graph Engine connections
            GraphEdge("E-024", "CAP-TD-007", "EVID-TD-007", "PRODUCE", "1:1"),
            GraphEdge("E-025", "EVID-TD-007", "EXEC_DUAL_GRAPH_ENGINE", "CERTIFICA", "1:1"),
            GraphEdge("E-026", "EXEC_DUAL_GRAPH_ENGINE", "EXEC_PYTEST_SUITE", "VALIDA", "1:N"),
            GraphEdge("E-028", "EVID-F2-001", "CAP-F2-001", "CERTIFICA", "1:1"),
        ]

        for e in edges:
            self.add_edge(e)
