from engine.v4.evidence.contracts import EvidenceLink
from engine.v4.domain.financial_engine import FinancialEngine


class EvidenceLinkRegistry:
    def __init__(self, fe: FinancialEngine):
        self.fe = fe

    VALID_TYPES = ("id_orden", "id_transaccion", "folio_xml", "archivo_origen")

    def _lookup(self, id_type: str, value: str) -> list[dict]:
        kwargs = {"limit": 1000}
        if id_type in ("id_orden", "id_transaccion"):
            kwargs["order_id"] = value
        elif id_type == "folio_xml":
            kwargs["folio_xml"] = value
        elif id_type == "archivo_origen":
            kwargs["archivo_origen"] = value
        else:
            return []
        result = self.fe.query_ledger(**kwargs)
        return result.get("data", [])

    def resolve(self, identifier: str, id_type: str = "id_orden") -> list[EvidenceLink]:
        if id_type not in self.VALID_TYPES:
            return []
        records = self._lookup(id_type, identifier)
        links = []
        for row in records:
            confidence = "CERTIFICADO"
            if not row.get("folio_xml"):
                confidence = "PARCIAL"
            links.append(EvidenceLink(
                source_identifier=identifier,
                source_type=id_type,
                target_identifier=row.get("id_transaccion"),
                target_type="id_transaccion",
                engine_used="FinancialEngine",
                method_used="query_ledger()",
                confidence=confidence,
                marketplace=row.get("marketplace"),
                periodo=row.get("periodo"),
                financial_group=row.get("financial_group"),
                detalle=row.get("detalle"),
                monto=row.get("monto"),
                folio_xml=row.get("folio_xml"),
                archivo_origen=row.get("archivo_origen"),
            ))
        return links
