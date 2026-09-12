from pathlib import Path

from app.services.access import can_access
from app.ui.access_control import PAGE_FEATURES, QUICK_ACTION_PAGES


KASIR_ALLOWED_PAGES = {0, 1, 13}


def test_page_feature_mapping_covers_all_pages():
    assert set(PAGE_FEATURES) == set(range(14))


def test_kasir_navigation_policy_matches_access_service():
    for page_index, feature in PAGE_FEATURES.items():
        expected = page_index in KASIR_ALLOWED_PAGES
        assert can_access("KASIR", feature) is expected


def test_admin_navigation_policy_is_full_access():
    assert all(can_access("ADMIN", feature) for feature in PAGE_FEATURES.values())


def test_kasir_quick_actions_are_limited_to_allowed_pages():
    assert QUICK_ACTION_PAGES["+ Transaksi Baru"] == 1
    assert QUICK_ACTION_PAGES["+ Produk"] == 2
    assert QUICK_ACTION_PAGES["Stok & Mutasi"] == 3
    assert QUICK_ACTION_PAGES["Laporan"] == 6
    assert all(not can_access("KASIR", PAGE_FEATURES[index]) for index in (2, 3, 6))


def test_main_applies_role_access_layer():
    source = Path("app/main.py").read_text(encoding="utf-8")
    assert "from .ui.access_control import apply_role_access" in source
    assert "apply_role_access(window)" in source


def test_role_access_uses_valid_qlistwidgetitem_visibility_api():
    source = Path("app/ui/access_control.py").read_text(encoding="utf-8")
    assert "item.setHidden(not allowed)" in source
    assert "item.setHidden(not section_visible.get(current_section, False))" in source
    assert "setItemHidden" not in source


def test_role_access_has_runtime_navigation_guard():
    source = Path("app/ui/access_control.py").read_text(encoding="utf-8")
    assert "window._select_navigation = guarded_select" in source
    assert "page_allowed(window.user, page_index)" in source
    assert "button.setVisible(page_allowed(window.user, target_page))" in source
