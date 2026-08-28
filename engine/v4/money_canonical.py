"""
CanonicalMoney — Single precise financial authority.
All CLP amounts are integers; aggregate before rounding.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

def canonical_clp(value) -> int:
    """Convert any numeric to canonical CLP integer (half-up)."""
    if value is None:
        return 0
    try:
        # handle NaN
        if isinstance(value, float) and (value != value):
            return 0
    except:
        pass
    # use Decimal to avoid binary float error
    try:
        d = Decimal(str(value))
    except:
        return 0
    if d.is_nan():
        return 0
    return int(d.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def canonical_sum(values: Iterable) -> int:
    """Aggregate list of amounts as canonical CLP int."""
    total = sum(Decimal(str(v)) for v in values if v is not None)
    return int(total.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def canonical_sum_sql_result(sql_total) -> int:
    """Convert SQL SUM result (float) to canonical int."""
    if sql_total is None:
        return 0
    return canonical_clp(sql_total)
