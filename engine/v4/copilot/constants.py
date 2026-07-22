"""Centralized constants for CopilotEngine — Single source of truth for financial groups, marketplaces, and thresholds."""

FINANCIAL_GROUPS = {
    "INGRESOS": "ingresos",
    "DEVOLUCIONES": "devoluciones",
    "COMISIONES": "comisiones",
    "COSTOS_OPERACIONALES": "costos_operacionales",
    "COSTOS_COMERCIALES": "costos_comerciales",
    "AJUSTES": "ajustes",
    "RECUPERACIONES": "recuperaciones_y_bonificaciones",
    "TESORERIA": "tesoreria",
    "FLUJO_CAJA": "flujo_de_caja",
}

COMMISSION_GROUPS = ["comisiones", "costos_comerciales"]

COST_COMPONENTS = ["total_costos_operacionales", "total_costos_comerciales", "total_ajustes"]

MARKETPLACES = ["ml", "ripley", "paris", "falabella"]

CIERRE_TABLE = "marketplace_cierre_financiero_v1"
LEDGER_TABLE = "marketplace_ledger_v1"
DTE_TABLE = "dte_truth_v1"
AUDIT_TABLE = "marketplace_auditoria_v1"

CANONICAL_MP_NAMES = {
    "ml": "Mercado Libre",
    "ripley": "Ripley",
    "paris": "Paris",
    "falabella": "Falabella",
}
