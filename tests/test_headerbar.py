from datetime import datetime

from app.ui.headerbar import _format_date, _user_display_name


def test_headerbar_formats_indonesian_date_without_weekday():
    assert _format_date(datetime(2026, 9, 12)) == "12 September 2026"


def test_headerbar_uses_user_name_not_username():
    class User:
        name = "Kasir Toko"
        username = "kasir"

    class Window:
        user = User()

    assert _user_display_name(Window()) == "Kasir Toko"


def test_headerbar_name_fallback_does_not_expose_username():
    class User:
        name = ""
        username = "kasir"

    class Window:
        user = User()

    assert _user_display_name(Window()) == "Pengguna"


def test_headerbar_contract_uses_store_identity_and_user_name_date_zones():
    from pathlib import Path

    source = Path("app/ui/headerbar.py").read_text(encoding="utf-8")
    # The current Headerbar implementation deliberately reuses the existing
    # topbar labels rather than introducing separate user/date widgets.
    assert "store_name" in source
    assert "store_address" in source
    assert "_wpos_store_label" in source
    assert "_wpos_user_date_label" in source
    assert "_MONTHS" in source
    assert "logged-in user name" in source
    assert "setObjectName(\"modernHeaderUserName\")" in source
