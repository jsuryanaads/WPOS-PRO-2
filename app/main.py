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
from .ui.themes import THEMES, apply_theme, current_theme, set_theme


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

    def change_theme(key, menu, window):
        set_theme(key)
        apply_theme(app, key)
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
        apply_theme(app, current_theme())
        refresh_ui(window)
        add_application_footer(window)
        apply_global_ui(app, window)
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
