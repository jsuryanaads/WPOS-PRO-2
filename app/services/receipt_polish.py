"""Print-safe formatting helpers for WPOS PRO 2 thermal receipts."""

from decimal import Decimal


def format_quantity(value):
    """Display integral Decimal quantities without a misleading .0 suffix."""
    quantity = Decimal(str(value))
    if quantity == quantity.to_integral_value():
        return f"{quantity.to_integral_value():f}"
    return format(quantity.normalize(), "f").rstrip("0").rstrip(".")


def add_html_top_safe_area(html, padding_mm=2):
    """Add a small print-safe top area without changing receipt width."""
    marker = "body { width:48mm;"
    replacement = f"body {{ width:48mm; padding-top:{padding_mm}mm;"
    if marker in html:
        return html.replace(marker, replacement, 1)
    return html


def add_raw_top_safe_area(data, init_command, blank_lines=2):
    """Insert blank feed lines immediately after ESC/POS initialization."""
    if not data.startswith(init_command):
        return data
    return init_command + (b"\n" * max(0, int(blank_lines))) + data[len(init_command):]
