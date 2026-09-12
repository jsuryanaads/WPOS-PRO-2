from datetime import datetime

from app.ui.headerbar import _format_date


def test_headerbar_formats_indonesian_date_without_weekday():
    assert _format_date(datetime(2026, 9, 12)) == "12 September 2026"


def test_headerbar_contract_uses_store_identity_and_user_date_zones():
    from pathlib import Path

    source = Path("app/ui/headerbar.py").read_text(encoding="utf-8")
    assert "store_name" in source
    assert "store_address" in source
    assert "_wpos_header_username_label" in source
    assert "_wpos_date_label" in source
    assert "_MONTHS" in source
