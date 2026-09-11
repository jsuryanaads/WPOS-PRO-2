import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from .config import APP_NAME, APP_VERSION
from .database import init_db
from .ui.login import LoginWindow
from .ui.modern_main_window import ModernMainWindow
from .ui.user_management import UserManagementDialog
from .ui.branding import ICON_PATH
from .ui.global_ui import add_application_footer, apply_global_ui
from .ui.polish import apply_ui_polish
from .ui.ux2026 import apply_ux2026
from .ui.dashboard_welcome import apply_dashboard_welcome
from .ui.form_layouts import apply_hybrid_form_layouts
from .ui.cashier_structure import apply_cashier_structure
from .ui.themes import THEMES, apply_theme, current_theme, set_theme
from .services import printer as printer_service
from .services.receipt_display import format_receipt_html_qty


# Keep receipt calculations/database values untouched while normalizing the
# cosmetic quantity representation used by the Qt/HTML receipt path.
_original_receipt_html = printer_service.receipt_html


def _receipt_html_with_integer_qty(sale, items, settings):
    html = _original_receipt_html(sale, items, settings)
    return format_receipt_html_qty(html)


printer_service.receipt_html = _receipt_html_with_integer_qty


def main():
    init_db()
    app = QApplication(sys.argv)
    if ICON_PATH.exists():
        app.setWindowIcon(QIcon(str(ICON_PATH)))
    apply_theme(app, current_theme())
    apply_global_ui(app)
    holder = {}

    def refresh_ui(window):
        apply_ui_polish(window)
        apply_ux2026(window)
        apply_global_ui(app, window)
        apply_dashboard_welcome(window)
        apply_hybrid_form_layouts(window)
        apply_cashier_structure(window)
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
        def logout_callback(window):
            holder.pop("main", None)
            window.close()
            login_window = LoginWindow(success)
            holder["login"] = login_window
            apply_global_ui(app, login_window)
            login_window.show()

        window = ModernMainWindow(user, logout_callback=logout_callback)
        window.setStyleSheet("")
        window._wpos_active_theme = current_theme()
        apply_theme(app, current_theme())
        refresh_ui(window)
        add_application_footer(window)
        apply_global_ui(app, window)
        apply_dashboard_welcome(window)
        apply_hybrid_form_layouts(window)
        apply_cashier_structure(window)
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
    login.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
