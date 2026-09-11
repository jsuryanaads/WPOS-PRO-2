"""Presentation-only receipt formatting helpers."""

import re


_QTY_DECIMAL_ZERO_RE = re.compile(r">([0-9]+)\.0+\s+x\s+")


def format_receipt_html_qty(html: str) -> str:
    """Render whole-number quantities without a cosmetic '.0' suffix.

    This changes only receipt presentation; transaction/database values remain
    Decimal and are not modified.
    """
    return _QTY_DECIMAL_ZERO_RE.sub(r">\1 x ", html)
