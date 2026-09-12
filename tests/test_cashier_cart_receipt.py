from decimal import Decimal
from pathlib import Path
import re


def test_receipt_qty_formatter_removes_zero_suffix_only_for_whole_qty():
    from app.services.receipt_display import format_receipt_html_qty

    html = ">1.0 x 3500< >2.0 x 5000< >1.5 x 2000<"
    result = format_receipt_html_qty(html)
    assert ">1 x 3500<" in result
    assert ">2 x 5000<" in result
    assert ">1.5 x 2000<" in result


def test_cashier_layout_css_keeps_payment_panel_bounded():
    text = Path("app/ui/theme_shell.py").read_text(encoding="utf-8")
    assert "QFrame#premiumPayCard" in text
    assert "max-width:330px" in text
    assert "QFrame#premiumCartCard" in text


def test_version_and_docs_are_synchronized():
    config = Path("app/config.py").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")

    match = re.search(r'^APP_VERSION = [\"\']([^\"\']+)[\"\']$', config, re.MULTILINE)
    assert match, "APP_VERSION tidak ditemukan di app/config.py"
    version = match.group(1)

    assert f"Versi aplikasi: **{version}**" in readme
    assert f"## Perubahan terbaru {version}" in readme
    assert f'#define MyAppVersion "{version}"' in installer
