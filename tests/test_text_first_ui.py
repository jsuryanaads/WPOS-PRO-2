from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def test_sidebar_has_no_navigation_icons():
    source = (REPO / "app/ui/modern_main_window.py").read_text(encoding="utf-8")
    assert 'QListWidgetItem(title)' in source
    assert 'QListWidgetItem(f"  {icon}' not in source


def test_dashboard_does_not_create_metric_icon_labels():
    source = (REPO / "app/ui/modern_main_window.py").read_text(encoding="utf-8")
    assert 'dashboardMetricIcon' not in source
    assert 'icons = {' not in source


def test_modern_shell_removes_cosmetic_symbol_prefixes():
    source = (REPO / "app/ui/modern_main_window.py").read_text(encoding="utf-8")
    assert 'def _remove_cosmetic_prefixes(self):' in source
    for prefix in ('"+ "', '"↻ "', '"↥ "', '"⚙ "', '"● "'):
        assert prefix in source


def test_brand_logo_remains_identity_element():
    source = (REPO / "app/ui/modern_main_window.py").read_text(encoding="utf-8")
    assert 'LOGO_PATH.exists()' in source
    assert 'modernBrandLogo' in source
