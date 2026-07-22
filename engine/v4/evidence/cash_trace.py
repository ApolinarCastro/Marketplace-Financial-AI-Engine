from engine.v4.evidence.contracts import CashTraceStatus


class CashTrace:
    """CashTrace — Structural gap.

    No settlement/pago/banco data exists in the database.
    This component exists only as a design contract for future implementation.
    All fields return NO_DISPONIBLE.
    """

    def __init__(self):
        pass

    def trace(self, order_id: str) -> CashTraceStatus:
        return CashTraceStatus(
            cash_status=f"NO_DISPONIBLE — no cash source data for order {order_id}",
        )
