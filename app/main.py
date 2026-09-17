import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QIcon
from .config import APP_NAME, APP_VERSION
from .database import init_db, SessionLocal
from .ui.login import LoginWindow
from .ui.modern_main_window import ModernMainWindow
from .ui.main_window import MainWindow
from .ui import main_window as main_window_module
from .ui.purchase_multi import (
    purchase_page as multi_item_purchase_page,
    load_purchase_options as multi_item_load_purchase_options,
    add_purchase_item as multi_item_add_purchase_item,
    clear_purchase_items as multi_item_clear_purchase_items,
    save_purchase as multi_item_save_purchase,
)
from .ui.product_status import apply_product_status_patch
from .ui.user_management import UserManagementDialog
from .ui.branding import ICON_PATH
from .ui.global_ui import add_application_footer, apply_global_ui
from .ui.polish import apply_ui_polish
from .ui.ux2026 import apply_ux2026
from .ui.dashboard_welcome import apply_dashboard_welcome
from .ui.form_layouts import apply_hybrid_form_layouts
from .ui.cashier_structure import apply_cashier_structure
from .ui.headerbar import apply_headerbar
from .ui.product_display import apply_product_table_display
from .ui.access_control import apply_role_access
from .ui.responsive_realtime import apply_responsive_realtime
from .ui.themes import THEMES, apply_theme, current_theme, set_theme
from .services import printer as printer_service
from .services.receipt_display import format_receipt_html_qty
from .services.receipt_polish import add_html_top_safe_area, add_raw_top_safe_area
from .services.settings import get_settings

_original_receipt_html = printer_service.receipt_html
_original_escpos_receipt_bytes = printer_service._escpos_receipt_bytes
_original_print_receipt = printer_service.print_receipt


def _receipt_html_with_integer_qty(sale, items, settings):
    html = _original_receipt_html(sale, items, settings)
    html = format_receipt_html_qty(html)
    return add_html_top_safe_area(html, padding_mm=2)


def _escpos_receipt_bytes_with_safe_area(*args, **kwargs):
    data = _original_escpos_receipt_bytes(*args, **kwargs)
    return add_raw_top_safe_area(data, printer_service.CMD_INIT, blank_lines=2)


def _safe_print_receipt(parent, sale, items):
    """Keep a committed sale successful when the printer layer raises."""
    try:
        return _original_print_receipt(parent, sale, items)
    except Exception:
        return False


def _refresh_printer_controls(window):
    """Refresh printer lists in-place; never create a second Printer page."""
    with SessionLocal() as session:
        settings = get_settings(session)

    for attr, key in (("printer_combo", "printer_name"), ("report_printer_combo", "report_printer_name")):
        combo = getattr(window, attr, None)
        if combo is None:
            continue
        selected = settings.get(key, "")
        combo.blockSignals(True)
        combo.clear()
        combo.addItem("Printer default / pilih saat cetak", "")
        for name in printer_service.available_printers():
            combo.addItem(name, name)
        index = combo.findData(selected)
        if index >= 0:
            combo.setCurrentIndex(index)
        combo.blockSignals(False)


main_window_module.MainWindow.refresh_printer_page = _refresh_printer_controls
printer_service.receipt_html = _receipt_html_with_integer_qty
printer_service._escpos_receipt_bytes = _escpos_receipt_bytes_with_safe_area
main_window_module.print_receipt = _safe_print_receipt
apply_product_status_patch(MainWindow)

MainWindow.purchase_page = multi_item_purchase_page
MainWindow.load_purchase_options = multi_item_load_purchase_options
MainWindow.add_purchase_item = multi_item_add_purchase_item
MainWindow.clear_purchase_items = multi_item_clear_purchase_items
MainWindow.save_purchase = multi_item_save_purchase


def main():
    init_db()
    app = QApplication(sys.argv)
    if ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(ICON_PATH)))
    apply_theme(app, current_theme())
    apply_global_ui(app)
    holder = {}

    def refresh_ui(window):
        """Apply window-level presentation once per layer."""
        apply_ui_polish(window)
        apply_ux2026(window)
        apply_global_ui(app, window)
        apply_dashboard_welcome(window)
        apply_hybrid_form_layouts(window)
        apply_cashier_structure(window)
        apply_headerbar(window)
        apply_product_table_display(window)
        apply_role_access(window)
        add_application_footer(window)
        apply_global_ui(app, window)
        apply_responsive_realtime(window)

        for object_name in ("modernUser", "modernRole"):
            label = window.findChild(QWidget, object_name)
            if label is not None:
                label.hide()

        account = window.findChild(QWidget, "modernAccount")
        if account is not None:
            account.adjustSize()

        paid = getattr(window, "paid", None)
        if paid is not None and hasattr(window, "update_change") and not getattr(window, "_wpos_paid_change_live", False):
            paid.valueChanged.connect(lambda _value: window.update_change())
            window._wpos_paid_change_live = True
            window.update_change()

    def change_theme(key, menu, window):
        set_theme(key)
        apply_theme(app, key)
        window._wpos_active_theme = key
        refresh_ui(window)
        for action in menu.actions():
            action.setChecked(action.text() == THEMES[key]["label"])

    def success(user):
        printer_service.set_current_cashier(user)

        def logout_callback(window):
            holder.pop("main", None)
            window.close()
            login_window = LoginWindow(success)
            holder["login"] = login_window
            apply_global_ui(app, login_window)
            login_window.showFullScreen()

        window = ModernMainWindow(user, logout_callback=logout_callback)
        window.setStyleSheet("")
        window._wpos_active_theme = current_theme()
        apply_theme(app, current_theme())
        refresh_ui(window)
        holder["main"] = window

        theme_menu = window.menuBar().addMenu("Tema")
        selected = current_theme()
        for key, info in THEMES.items():
            action = theme_menu.addAction(info["label"])
            action.setCheckable(True)
            action.setChecked(key == selected)
            action.triggered.connect(lambda checked=False, k=key: change_theme(k, theme_menu, window))

        if str(user.role).upper() == "ADMIN":
            menu = window.menuBar().addMenu("Administrasi")
            action = menu.addAction("Manajemen User")
            action.triggered.connect(lambda: UserManagementDialog(user, window).exec())

        window.show()

    login = LoginWindow(success)
    holder["login"] = login
    apply_global_ui(app, login)
    login.showFullScreen()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
