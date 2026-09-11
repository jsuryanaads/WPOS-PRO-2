import pytest
from PySide6.QtWidgets import QApplication, QStackedWidget, QWidget

from app.ui.premium_cashier import apply_premium_cashier


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication([])
    return app


class CashierHarness:
    def __init__(self):
        self.modern_stack = QStackedWidget()
        self.modern_stack.addWidget(QWidget())
        self.modern_stack.addWidget(QWidget())
        self.barcode = None
        self.qty = None
        self.cart_table = None
        self.discount = None
        self.method = None
        self.paid = None
        self.total_label = None
        self.change_label = None

    def _prepare_table(self, table):
        table.setColumnCount(5)

    def add_barcode(self):
        pass

    def refresh_cart(self):
        return 0

    def payment_method_changed(self, _method):
        pass

    def update_change(self):
        pass

    def clear_cart(self):
        pass

    def checkout(self):
        pass


def test_premium_cashier_replaces_blank_legacy_page(qapp):
    harness = CashierHarness()
    old_page = harness.modern_stack.widget(1)

    apply_premium_cashier(harness)
    qapp.processEvents()

    page = harness.modern_stack.widget(1)
    assert page is not old_page
    assert page.objectName() == "premiumCashierPage"
    assert page.layout() is not None
    assert harness.barcode is not None
    assert harness.barcode.objectName() == "premiumBarcode"
    assert harness.cart_table is not None
    assert harness.paid is not None


def test_modern_page_surface_rules_are_present(qapp):
    from app.ui.ux2026 import apply_ux2026

    class TabsStub:
        def setCurrentIndex(self, _index):
            pass

    window = QWidget()
    window.tabs = TabsStub()
    apply_ux2026(window)
    assert window.styleSheet() is not None


def test_dark_and_light_themes_are_exposed():
    from app.ui.themes import THEMES

    assert list(THEMES) == ["DARK", "LIGHT"]
    assert THEMES["DARK"]["label"] == "Dark Mode"
    assert THEMES["LIGHT"]["label"] == "Light Mode"


def test_light_theme_sidebar_uses_light_palette():
    from app.ui.theme_shell import THEME_PALETTES, theme_shell_stylesheet

    light = THEME_PALETTES["LIGHT"]
    stylesheet = theme_shell_stylesheet("LIGHT")

    assert light["shell"] == "#f7f9fb"
    assert light["sidebar_text"] == "#435465"
    assert "QFrame#modernSidebar { background:#f7f9fb; color:#435465;" in stylesheet
    assert "QListWidget#modernNav { background:#f7f9fb; color:#435465;" in stylesheet
