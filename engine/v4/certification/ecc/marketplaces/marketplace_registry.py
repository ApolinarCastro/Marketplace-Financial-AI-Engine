from typing import Dict, Type
from .base_marketplace import BaseMarketplacePlugin
from .mercadolibre import MercadoLibrePlugin
from .paris import ParisPlugin
from .falabella import FalabellaPlugin
from .ripley import RipleyPlugin
from .shopify import ShopifyPlugin

class MarketplaceRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[BaseMarketplacePlugin]] = {
            "MERCADO_LIBRE": MercadoLibrePlugin,
            "PARIS": ParisPlugin,
            "FALABELLA": FalabellaPlugin,
            "RIPLEY": RipleyPlugin,
            "SHOPIFY": ShopifyPlugin
        }

    def get_plugin(self, marketplace_name: str) -> BaseMarketplacePlugin:
        """
        Returns the specific plugin for the marketplace, or BaseMarketplacePlugin as a fallback.
        """
        if not marketplace_name:
            return BaseMarketplacePlugin()
            
        plugin_class = self._registry.get(marketplace_name.upper(), BaseMarketplacePlugin)
        return plugin_class()
