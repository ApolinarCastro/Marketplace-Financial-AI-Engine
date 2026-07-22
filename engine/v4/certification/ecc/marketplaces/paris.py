from ..ecc_payload import ECCPayload
from .base_marketplace import BaseMarketplacePlugin

class ParisPlugin(BaseMarketplacePlugin):
    def enrich_payload(self, payload: ECCPayload) -> ECCPayload:
        if payload.document_type == "33":
            payload.chain_type = "DIRECT_LINK"
        else:
            payload.chain_type = "DOCUMENT_CHAIN"
        return payload
