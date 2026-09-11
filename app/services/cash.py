from decimal import Decimal, InvalidOperation
from ..models import CashMovement


def record_cash_movement(session, movement_type, amount, reference=None, note=None):
    movement_type = str(movement_type).upper().strip()
    if movement_type not in {"IN", "OUT"}:
        raise ValueError("Jenis kas tidak valid")
    try:
        amount = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        raise ValueError("Jumlah kas tidak valid")
    if amount <= 0:
        raise ValueError("Jumlah kas harus lebih dari nol")
    movement = CashMovement(
        movement_type=movement_type,
        amount=amount,
        reference=str(reference).strip() if reference else None,
        note=str(note).strip() if note else None,
    )
    try:
        session.add(movement)
        session.commit()
        session.refresh(movement)
        return movement
    except Exception:
        session.rollback()
        raise
