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
QLabel#loginFooter { font-size: 11px; }
QLineEdit#loginInput { min-height: 30px; padding: 6px 12px; border-radius: 9px; }
QPushButton#loginPrimaryButton { min-height: 30px; border-radius: 10px; font-size: 14px; font-weight: 800; }
QPushButton#loginSecondaryButton { min-width: 58px; min-height: 30px; border-radius: 9px; font-weight: 700; }
"""

THEMES = {
    "MODERN_BLUE": {
        "label": "Modern Blue",
        "stylesheet": COMMON + """
QWidget, QMainWindow, QDialog { background: #edf0f3; color: #263442; }
QMenuBar { background: #dfe4e9; color: #263442; border-bottom: 1px solid #c6cdd4; }
QMenuBar::item:selected, QMenu::item:selected { background: #d3e2ef; color: #145a96; }
QMenu { background: #f4f6f8; color: #263442; border: 1px solid #c6cdd4; }
QToolBar { background: #dfe4e9; border: 0; spacing: 6px; }
QTabWidget::pane { border: 0; background: #edf0f3; }
QTabBar { background: #dfe4e9; }
QTabBar::tab { background: #dfe4e9; color: #526070; padding: 10px 16px; border: 0; }
QTabBar::tab:hover { background: #e9edf1; color: #145a96; }
QTabBar::tab:selected { background: #edf0f3; color: #145a96; border-bottom: 3px solid #2673b8; }
QPushButton { background: #3b78a8; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
QPushButton:hover { background: #2f638e; }
QPushButton:disabled { background: #b8c1ca; color: #eef1f3; }
QPushButton#primary { background: #2673b8; }
QPushButton#danger { background: #b54747; }
QToolBar QPushButton#danger { background: #2673b8; color: white; }
QToolBar QPushButton#danger:hover { background: #1f5f99; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #f8f9fa; color: #172033; border: 1px solid #c5cdd5; border-radius: 6px; padding: 6px; }
QTableWidget, QListWidget { background: #f8f9fa; color: #172033; border: 1px solid #c5cdd5; border-radius: 8px; alternate-background-color: #eef1f4; }
QHeaderView::section { background: #d8e1e9; color: #17324d; padding: 8px; border: 0; font-weight: 700; }
QGroupBox { background: #e5e9ed; border: 1px solid #c6cdd4; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #edf0f3; color: #315a7d; }
QFrame#brandStrip { background: #2673b8; }
QLabel#brandName, QLabel#brandVersion { color: white; }
QLabel#cardTitle { color: #687787; }
QLabel#cardValue { color: #102a43; }
QFrame#card { background: #f8f9fa; border: 1px solid #cbd3db; }
QLabel#total { background: #245d88; color: white; }
QFrame#loginCard { background: #e5e9ed; border: 1px solid #c6cdd4; }
QLabel#loginTitle { color: #172033; }
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #5f6f7e; }
QPushButton#loginPrimaryButton { background: #2673b8; color: #ffffff; }
QPushButton#loginPrimaryButton:hover { background: #1f5f99; }
QPushButton#loginSecondaryButton { background: #d8e5f0; color: #145a96; }
QPushButton#loginSecondaryButton:hover { background: #cbddea; }
""",
    },
    "KEMERDEKAAN": {
        "label": "Kemerdekaan",
        "stylesheet": COMMON + """
QWidget, QMainWindow, QDialog { background: #e8e7e8; color: #30282a; }
QMenuBar { background: #5f2024; color: #fff4f4; border-bottom: 2px solid #a9323a; }
QMenuBar::item:selected { background: #7c292e; color: #ffffff; }
QMenu { background: #6b2429; color: #ffffff; border: 1px solid #a53a40; }
QMenu::item:selected { background: #96343a; color: #ffffff; }
QToolBar { background: #5f2024; border: 0; spacing: 6px; }
QTabWidget::pane { border: 0; background: #e8e7e8; }
QTabBar { background: #74272c; }
QTabBar::tab { background: #74272c; color: #f9dddd; padding: 10px 16px; border: 0; }
QTabBar::tab:hover { background: #8b3035; color: white; }
QTabBar::tab:selected { background: #ded9da; color: #7f1d1d; border-bottom: 3px solid #c43f3f; }
QPushButton { background: #a52f37; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 700; }
QPushButton:hover { background: #8f252d; }
QPushButton:disabled { background: #a99395; color: #eee7e7; }
QPushButton#primary { background: #b9343b; }
QPushButton#danger { background: #721b21; }
QToolBar QPushButton#danger { background: #b9343b; color: white; }
QToolBar QPushButton#danger:hover { background: #8f252d; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #f1edef; color: #30282a; border: 1px solid #c9b8ba; border-radius: 6px; padding: 6px; }
QTableWidget, QListWidget { background: #f1edef; color: #30282a; border: 1px solid #c9b8ba; border-radius: 8px; alternate-background-color: #e7e0e2; }
QHeaderView::section { background: #a9323a; color: white; padding: 8px; border: 0; font-weight: 700; }
QGroupBox { background: #ded9da; border: 1px solid #c7b6b8; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #e8e7e8; color: #7f1d1d; }
QFrame#brandStrip { background: #9f292f; }
QLabel#brandName, QLabel#brandVersion { color: white; }
QLabel#cardTitle { color: #76585b; }
QLabel#cardValue { color: #5f2025; }
QFrame#card { background: #ded9da; border: 1px solid #c7b6b8; }
QLabel#total { background: #8f252c; color: white; }
QFrame#loginCard { background: #ded9da; border: 1px solid #c7b6b8; }
QLabel#loginTitle { color: #701b20; }
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #70575a; }
QPushButton#loginPrimaryButton { background: #a52f37; color: white; }
QPushButton#loginPrimaryButton:hover { background: #8f252d; }
QPushButton#loginSecondaryButton { background: #d5c9cb; color: #7f1d1d; }
QPushButton#loginSecondaryButton:hover { background: #cbbabd; }
""",
    },
    "KEAGAMAAN": {
        "label": "Keagamaan",
        "stylesheet": COMMON + """
QWidget, QMainWindow, QDialog { background: #e6ebe7; color: #26362d; }
QMenuBar { background: #294638; color: #f2f6f3; border-bottom: 2px solid #66816d; }
QMenuBar::item:selected { background: #3b5b46; color: white; }
QMenu { background: #304f3c; color: white; border: 1px solid #587561; }
QMenu::item:selected { background: #496b54; color: white; }
QToolBar { background: #294638; border: 0; spacing: 6px; }
QTabWidget::pane { border: 0; background: #e6ebe7; }
QTabBar { background: #365641; }
QTabBar::tab { background: #365641; color: #e0ebe3; padding: 10px 16px; border: 0; }
QTabBar::tab:hover { background: #476650; color: white; }
QTabBar::tab:selected { background: #dfe5e1; color: #294638; border-bottom: 3px solid #66856f; }
QPushButton { background: #52715c; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 600; }
QPushButton:hover { background: #3f5e49; }
QPushButton:disabled { background: #9eafa2; color: #edf2ee; }
QPushButton#primary { background: #496c55; }
QPushButton#danger { background: #805050; }
QToolBar QPushButton#danger { background: #496c55; color: white; }
QToolBar QPushButton#danger:hover { background: #3f5e49; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #eef2ef; color: #203027; border: 1px solid #b7c6ba; border-radius: 6px; padding: 6px; }
QTableWidget, QListWidget { background: #eef2ef; color: #203027; border: 1px solid #b7c6ba; border-radius: 8px; alternate-background-color: #e0e7e1; }
QHeaderView::section { background: #587963; color: white; padding: 8px; border: 0; font-weight: 700; }
QGroupBox { background: #dce3de; border: 1px solid #b7c6ba; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #e6ebe7; color: #294638; }
QFrame#brandStrip { background: #496b54; }
QLabel#brandName, QLabel#brandVersion { color: white; }
QLabel#cardTitle { color: #58705f; }
QLabel#cardValue { color: #294638; }
QFrame#card { background: #dce3de; border: 1px solid #b7c6ba; }
QLabel#total { background: #496c55; color: white; }
QFrame#loginCard { background: #dce3de; border: 1px solid #b7c6ba; }
QLabel#loginTitle { color: #294638; }
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #58705f; }
QPushButton#loginPrimaryButton { background: #496c55; color: white; }
QPushButton#loginPrimaryButton:hover { background: #3f5e49; }
QPushButton#loginSecondaryButton { background: #cedbd1; color: #294638; }
QPushButton#loginSecondaryButton:hover { background: #c0d0c4; }
""",
    },
    "DARK": {
        "label": "Dark Mode",
        "stylesheet": COMMON + """
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
QToolBar QPushButton#danger:hover { background: #4b83c3; }
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
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel, QLabel#loginFooter { color: #aab3c0; }
QPushButton#loginPrimaryButton { background: #396fae; color: white; }
QPushButton#loginPrimaryButton:hover { background: #4b83c3; }
QPushButton#loginSecondaryButton { background: #303946; color: #dbeafe; }
QPushButton#loginSecondaryButton:hover { background: #3a4555; }
QLineEdit#loginInput { background: #292f38; color: #e6eaf0; border: 1px solid #414956; }
""",
    },
}


def current_theme():
    with SessionLocal() as session:
        return get_setting(session, "ui_theme", "MODERN_BLUE")


def set_theme(theme_key):
    if theme_key not in THEMES:
        raise ValueError("Tema tidak tersedia")
    with SessionLocal() as session:
        set_setting(session, "ui_theme", theme_key)


def apply_theme(app, theme_key):
    theme = THEMES.get(theme_key, THEMES["MODERN_BLUE"])
    app.setStyleSheet(theme["stylesheet"])
    return theme["label"]
