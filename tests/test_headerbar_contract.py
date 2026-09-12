from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEADERBAR = ROOT / "app" / "ui" / "headerbar.py"
DASHBOARD_WELCOME = ROOT / "app" / "ui" / "dashboard_welcome.py"


def test_headerbar_does_not_reparent_existing_widgets():
    source = HEADERBAR.read_text(encoding="utf-8")
    assert "setParent(None)" not in source
    assert "layout.removeItem" not in source
    assert "_wpos_store_label" in source
    assert "_wpos_user_date_label" in source


def test_headerbar_has_three_equal_zones_for_true_center_alignment():
    source = HEADERBAR.read_text(encoding="utf-8")
    assert "layout.setStretch(0, 1)" in source
    assert "layout.setStretch(1, 1)" in source
    assert "layout.setStretch(2, 1)" in source
    assert "store_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)" in source


def test_headerbar_uses_display_name_and_indonesian_date():
    source = HEADERBAR.read_text(encoding="utf-8")
    assert "getattr(user, \"name\", \"\")" in source
    assert 'return name or "Pengguna"' in source
    assert "_MONTHS" in source
    assert "_format_date(datetime.now())" in source


def test_dashboard_welcome_does_not_overwrite_global_header_context():
    source = DASHBOARD_WELCOME.read_text(encoding="utf-8")
    assert "context.setText" not in source
    assert "hint.setText" not in source
    assert "wposDashboardMetricsDate" in source
