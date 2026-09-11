from ..database import SessionLocal
from ..services.settings import get_setting, set_setting

COMMON = """
QWidget { font-family: 'Segoe UI'; }
QLabel#pageTitle { font-size: 24px; font-weight: 800; }
QLabel#pageSubtitle { font-size: 13px; }
QFrame#card { border-radius: 10px; }
QLabel#cardTitle { font-size: 11px; font-weight: 700; }
QLabel#cardValue { font-size: 22px; font-weight: 800; }
QFrame#brandStrip { border-radius: 11px; }
QLabel#brandName { font-size: 18px; font-weight: 800; background: transparent; }
QLabel#brandVersion { font-size: 11px; background: transparent; }
QLabel#total { border-radius: 8px; padding: 10px 14px; font-size: 18px; font-weight: 800; }
QLabel#accountUser { font-weight: 700; }
QPushButton#logoutButton { min-height: 30px; min-width: 64px; border-radius: 7px; padding: 6px 12px; font-weight: 700; }
QFrame#loginCard { border-radius: 18px; }
QLabel#loginTitle { font-size: 27px; font-weight: 800; }
QLabel#loginVersion { font-size: 12px; }
QLabel#loginWelcome { font-size: 13px; }
QLabel#loginFieldLabel { font-size: 11px; font-weight: 800; }
QLineEdit#loginInput { min-height: 30px; padding: 6px 12px; border-radius: 9px; }
QPushButton#loginPrimaryButton { min-height: 30px; border-radius: 10px; font-size: 14px; font-weight: 800; }
QPushButton#loginSecondaryButton { min-width: 58px; min-height: 30px; border-radius: 9px; font-weight: 700; }
QFrame#applicationFooter { min-height: 30px; max-height: 30px; }
QLabel#applicationFooterLabel { font-size: 10px; font-weight: 600; }
"""

DARK = COMMON + """
QWidget, QMainWindow, QDialog { background: #20242b; color: #e6eaf0; }
QMenuBar { background: #15181e; color: #e6eaf0; border-bottom: 1px solid #343b46; }
QMenuBar::item:selected, QMenu::item:selected { background: #2c3542; color: white; }
QMenu { background: #242a33; color: #e6eaf0; border: 1px solid #3a424f; }
QToolBar { background: #15181e; border: 0; spacing: 6px; }
QTabWidget::pane { border: 0; background: #20242b; }
QTabBar { background: #15181e; }
QTabBar::tab { background: #15181e; color: #aab3c0; padding: 10px 16px; border: 0; }
QTabBar::tab:hover { background: #282e38; color: white; }
QTabBar::tab:selected { background: #242a33; color: white; border-bottom: 3px solid #6ea8fe; }
QPushButton { background: #315f9f; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
QPushButton:hover { background: #3d73bd; }
QPushButton:disabled { background: #505966; color: #c5cad2; }
QPushButton#primary { background: #396fae; }
QPushButton#danger { background: #9d4f55; }
QToolBar QPushButton#danger { background: #396fae; color: white; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #292f38; color: #e6eaf0; border: 1px solid #414956; border-radius: 6px; padding: 6px; }
QTableWidget, QListWidget { background: #242a33; color: #e6eaf0; border: 1px solid #39414c; border-radius: 8px; alternate-background-color: #292f38; }
QHeaderView::section { background: #303946; color: #e6eaf0; padding: 8px; border: 0; font-weight: 700; }
QGroupBox { background: #292f38; border: 1px solid #39414c; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #20242b; color: #cbd5e1; }
QFrame#brandStrip { background: #293f5e; }
QLabel#brandName, QLabel#brandVersion { color: #f4f7fb; }
QLabel#cardTitle { color: #aab3c0; }
QLabel#cardValue { color: #f4f7fb; }
QFrame#card { background: #242a33; border: 1px solid #39414c; }
QLabel#total { background: #315f9f; color: white; }
QTableWidget::item:selected { background: #334e70; color: white; }
QFrame#loginCard { background: #292f38; border: 1px solid #39414c; }
QLabel#loginTitle { color: #f8fafc; }
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel { color: #aab3c0; }
QPushButton#loginPrimaryButton { background: #396fae; color: white; }
QPushButton#loginPrimaryButton:hover { background: #4b83c3; }
QPushButton#loginSecondaryButton { background: #303946; color: #dbeafe; }
QPushButton#loginSecondaryButton:hover { background: #3a4555; }
QLineEdit#loginInput { background: #292f38; color: #e6eaf0; border: 1px solid #414956; }
QFrame#applicationFooter { background: #1a1e24; border-top: 1px solid #343b46; }
QLabel#applicationFooterLabel { color: #aab3c0; }
"""

LIGHT = COMMON + """
QWidget, QMainWindow, QDialog { background: #f4f6f8; color: #263442; }
QMenuBar { background: #ffffff; color: #263442; border-bottom: 1px solid #d7dde3; }
QMenuBar::item:selected, QMenu::item:selected { background: #e8f1f8; color: #155d91; }
QMenu { background: #ffffff; color: #263442; border: 1px solid #d7dde3; }
QToolBar { background: #ffffff; border: 0; spacing: 6px; }
QTabWidget::pane { border: 0; background: #f4f6f8; }
QTabBar { background: #ffffff; }
QTabBar::tab { background: #ffffff; color: #5b6875; padding: 10px 16px; border: 0; }
QTabBar::tab:hover { background: #eef4f8; color: #155d91; }
QTabBar::tab:selected { background: #f4f6f8; color: #155d91; border-bottom: 3px solid #2b78b8; }
QPushButton { background: #2b78b8; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
QPushButton:hover { background: #21679f; }
QPushButton:disabled { background: #b9c3cc; color: #f5f7f9; }
QPushButton#primary { background: #2b78b8; }
QPushButton#danger { background: #b34f4f; }
QToolBar QPushButton#danger { background: #2b78b8; color: white; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #ffffff; color: #263442; border: 1px solid #c8d1d9; border-radius: 6px; padding: 6px; }
QTableWidget, QListWidget { background: #ffffff; color: #263442; border: 1px solid #c8d1d9; border-radius: 8px; alternate-background-color: #f1f4f7; }
QHeaderView::section { background: #e2e8ed; color: #263f55; padding: 8px; border: 0; font-weight: 700; }
QGroupBox { background: #eef2f5; border: 1px solid #c8d1d9; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #f4f6f8; color: #315a7d; }
QFrame#brandStrip { background: #2b78b8; }
QLabel#brandName, QLabel#brandVersion { color: white; }
QLabel#cardTitle { color: #667583; }
QLabel#cardValue { color: #163b59; }
QFrame#card { background: #ffffff; border: 1px solid #ccd5dc; }
QLabel#total { background: #23689e; color: white; }
QTableWidget::item:selected { background: #cfe4f3; color: #173c58; }
QFrame#loginCard { background: #eef2f5; border: 1px solid #c8d1d9; }
QLabel#loginTitle { color: #173c58; }
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel { color: #61707e; }
QPushButton#loginPrimaryButton { background: #2b78b8; color: white; }
QPushButton#loginPrimaryButton:hover { background: #21679f; }
QPushButton#loginSecondaryButton { background: #dce9f2; color: #155d91; }
QPushButton#loginSecondaryButton:hover { background: #cfdfeb; }
QLineEdit#loginInput { background: #ffffff; color: #263442; border: 1px solid #c8d1d9; }
QFrame#applicationFooter { background: #e6ebef; border-top: 1px solid #c8d1d9; }
QLabel#applicationFooterLabel { color: #5b6875; }
"""

THEMES = {
    "DARK": {"label": "Dark Mode", "stylesheet": DARK},
    "LIGHT": {"label": "Light Mode", "stylesheet": LIGHT},
}


def current_theme():
    with SessionLocal() as session:
        saved = get_setting(session, "ui_theme", "DARK")
        if saved not in THEMES:
            saved = "DARK"
            set_setting(session, "ui_theme", saved)
        return saved


def set_theme(theme_key):
    if theme_key not in THEMES:
        raise ValueError("Tema tidak tersedia")
    with SessionLocal() as session:
        set_setting(session, "ui_theme", theme_key)


def apply_theme(app, theme_key):
    theme = THEMES.get(theme_key, THEMES["DARK"])
    app.setStyleSheet(theme["stylesheet"])
    return theme["label"]
