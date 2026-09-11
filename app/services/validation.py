from decimal import Decimal, InvalidOperation


def decimal_value(value, label, *, non_negative=False):
    """Convert input to a finite Decimal with consistent domain validation."""
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"{label} tidak valid")
    if not result.is_finite():
        raise ValueError(f"{label} tidak valid")
    if non_negative and result < 0:
        raise ValueError(f"{label} tidak boleh negatif")
    return result
