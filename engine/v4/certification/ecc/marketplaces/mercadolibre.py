from ..ecc_payload import ECCPayload
from .base_marketplace import BaseMarketplacePlugin

class MercadoLibrePlugin(BaseMarketplacePlugin):
    def enrich_payload(self, payload: ECCPayload) -> ECCPayload:
        if payload.document_type == "33":
            payload.chain_type = "DIRECT_LINK"
        elif payload.document_type in ["43", "61"]:
            payload.chain_type = "DOCUMENT_CHAIN"
        else:
            payload.chain_type = "DOCUMENT_CHAIN"
        return payload
