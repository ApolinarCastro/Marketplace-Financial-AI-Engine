from ..ecc_payload import ECCPayload
from .base_marketplace import BaseMarketplacePlugin

class RipleyPlugin(BaseMarketplacePlugin):
    def enrich_payload(self, payload: ECCPayload) -> ECCPayload:
        payload.chain_type = "SETTLEMENT_CHAIN"
        return payload
