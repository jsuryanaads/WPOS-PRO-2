"""Presentation-only receipt formatting helpers."""

import re

from .receipt_polish import format_quantity


_QTY_RE = re.compile(r">([0-9]+(?:\.[0-9]+)?)\s+x\s+")


def format_receipt_html_qty(html: str) -> str:
    """Render receipt quantities without cosmetic decimal zeros.

    This changes only receipt presentation; transaction/database values remain
    Decimal and are not modified.
    """
    return _QTY_RE.sub(lambda match: f">{format_quantity(match.group(1))} x ", html)
