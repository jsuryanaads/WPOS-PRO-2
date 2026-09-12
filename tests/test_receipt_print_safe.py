from decimal import Decimal
from pathlib import Path

from app.services.receipt_polish import add_html_top_safe_area, add_raw_top_safe_area, format_quantity


def test_quantity_display_removes_cosmetic_zero():
    assert format_quantity(Decimal("5.0")) == "5"
    assert format_quantity(Decimal("10")) == "10"
    assert format_quantity(Decimal("2.5")) == "2.5"
    assert format_quantity(Decimal("0.25")) == "0.25"


def test_html_top_safe_area_preserves_48mm_width():
    html = "<style>body { width:48mm; font-size:9pt; margin:0; padding:0; }</style>"
    result = add_html_top_safe_area(html, padding_mm=2)
    assert "width:48mm" in result
    assert "padding-top:2mm" in result


def test_raw_top_safe_area_adds_two_blank_lines_after_init():
    init = b"\x1b@"
    payload = init + b"\x1ba\x01TOKO SAPNI\n"
    result = add_raw_top_safe_area(payload, init, blank_lines=2)
    assert result == init + b"\n\n" + payload[len(init):]


def test_version_is_291():
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    main = Path("app/main.py").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.9.1"' in config
    assert '#define MyAppVersion "2.9.1"' in installer
    assert "Versi aplikasi: **2.9.1**" in readme
    assert "## 2.9.1 — Receipt Print-Safe Refinement" in changelog
    assert "add_raw_top_safe_area" in main
