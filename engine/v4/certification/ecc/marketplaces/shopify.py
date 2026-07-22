from ..ecc_payload import ECCPayload
from .base_marketplace import BaseMarketplacePlugin

class ShopifyPlugin(BaseMarketplacePlugin):
    def enrich_payload(self, payload: ECCPayload) -> ECCPayload:
        payload.chain_type = "PAYMENT_CHAIN"
        return payload
