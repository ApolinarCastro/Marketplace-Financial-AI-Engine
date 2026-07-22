from ..ecc_payload import ECCPayload

class BaseMarketplacePlugin:
    """Base plugin for marketplace specialization"""
    
    def enrich_payload(self, payload: ECCPayload) -> ECCPayload:
        """
        Applies deterministic rules to classify the chain type.
        Default implementation returns UNKNOWN_CHAIN if no rule matches.
        """
        if not payload.chain_type:
            payload.chain_type = "UNKNOWN_CHAIN"
        return payload
