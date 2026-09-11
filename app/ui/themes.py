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

MODERN_BLUE = COMMON + """
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
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel { color: #5f6f7e; }
QPushButton#loginPrimaryButton { background: #2673b8; color: #ffffff; }
QPushButton#loginPrimaryButton:hover { background: #1f5f99; }
QPushButton#loginSecondaryButton { background: #d8e5f0; color: #145a96; }
QPushButton#loginSecondaryButton:hover { background: #cbddea; }
QFrame#applicationFooter { background: #dfe4e9; border-top: 1px solid #c6cdd4; }
QLabel#applicationFooterLabel { color: #526070; }
"""

PURPLE_PREMIUM = COMMON + """
QWidget, QMainWindow, QDialog { background: #f2eff7; color: #2d2638; }
QMenuBar { background: #3e3157; color: #f8f5ff; border-bottom: 1px solid #6d5a8d; }
QMenuBar::item:selected, QMenu::item:selected { background: #5a4779; color: white; }
QMenu { background: #47385f; color: white; border: 1px solid #725f91; }
QToolBar { background: #3e3157; border: 0; spacing: 6px; }
QTabWidget::pane { border: 0; background: #f2eff7; }
QTabBar { background: #47385f; }
QTabBar::tab { background: #47385f; color: #e8e0f4; padding: 10px 16px; border: 0; }
QTabBar::tab:hover { background: #5a4779; color: white; }
QTabBar::tab:selected { background: #ebe5f2; color: #4b3570; border-bottom: 3px solid #7d5ab0; }
QPushButton { background: #7252a0; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 700; }
QPushButton:hover { background: #60438a; }
QPushButton:disabled { background: #aaa0b7; color: #f3eff7; }
QPushButton#primary { background: #7d5ab0; }
QPushButton#danger { background: #a04f68; }
QToolBar QPushButton#danger { background: #7d5ab0; color: white; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #faf8fc; color: #292333; border: 1px solid #cfc5db; border-radius: 6px; padding: 6px; }
QTableWidget, QListWidget { background: #faf8fc; color: #292333; border: 1px solid #cfc5db; border-radius: 8px; alternate-background-color: #eee9f4; }
QHeaderView::section { background: #725c91; color: white; padding: 8px; border: 0; font-weight: 700; }
QGroupBox { background: #e9e2ef; border: 1px solid #cfc5db; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #f2eff7; color: #4b3570; }
QFrame#brandStrip { background: #68498d; }
QLabel#brandName, QLabel#brandVersion { color: white; }
QLabel#cardTitle { color: #756781; }
QLabel#cardValue { color: #4b3570; }
QFrame#card { background: #faf8fc; border: 1px solid #d1c8dc; }
QLabel#total { background: #68498d; color: white; }
QFrame#loginCard { background: #e9e2ef; border: 1px solid #cfc5db; }
QLabel#loginTitle { color: #4b3570; }
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel { color: #756781; }
QPushButton#loginPrimaryButton { background: #7d5ab0; color: white; }
QPushButton#loginPrimaryButton:hover { background: #60438a; }
QPushButton#loginSecondaryButton { background: #ddd2e8; color: #4b3570; }
QPushButton#loginSecondaryButton:hover { background: #d1c4df; }
QFrame#applicationFooter { background: #e7dfed; border-top: 1px solid #cfc5db; }
QLabel#applicationFooterLabel { color: #665874; }
"""

EMERALD = COMMON + """
QWidget, QMainWindow, QDialog { background: #eef5f1; color: #25372e; }
QMenuBar { background: #244b3a; color: #f3faf6; border-bottom: 1px solid #557764; }
QMenuBar::item:selected, QMenu::item:selected { background: #35664e; color: white; }
QMenu { background: #2c5743; color: white; border: 1px solid #63836f; }
QToolBar { background: #244b3a; border: 0; spacing: 6px; }
QTabWidget::pane { border: 0; background: #eef5f1; }
QTabBar { background: #2c5743; }
QTabBar::tab { background: #2c5743; color: #e1eee6; padding: 10px 16px; border: 0; }
QTabBar::tab:hover { background: #396b53; color: white; }
QTabBar::tab:selected { background: #e2ece6; color: #24513c; border-bottom: 3px solid #4f8b6a; }
QPushButton { background: #3e7c5b; color: white; border: 0; border-radius: 7px; padding: 8px 14px; font-weight: 700; }
QPushButton:hover { background: #32664a; }
QPushButton:disabled { background: #9caf9f; color: #edf3ef; }
QPushButton#primary { background: #428762; }
QPushButton#danger { background: #96565c; }
QToolBar QPushButton#danger { background: #428762; color: white; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background: #f7faf8; color: #203128; border: 1px solid #bdcec2; border-radius: 6px; padding: 6px; }
QTableWidget, QListWidget { background: #f7faf8; color: #203128; border: 1px solid #bdcec2; border-radius: 8px; alternate-background-color: #e6efe9; }
QHeaderView::section { background: #4b765e; color: white; padding: 8px; border: 0; font-weight: 700; }
QGroupBox { background: #e0eae3; border: 1px solid #bdcec2; border-radius: 9px; margin-top: 10px; padding: 12px 8px 8px; font-weight: 700; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; background: #eef5f1; color: #24513c; }
QFrame#brandStrip { background: #397557; }
QLabel#brandName, QLabel#brandVersion { color: white; }
QLabel#cardTitle { color: #5d7567; }
QLabel#cardValue { color: #24513c; }
QFrame#card { background: #f7faf8; border: 1px solid #c5d4ca; }
QLabel#total { background: #397557; color: white; }
QFrame#loginCard { background: #e0eae3; border: 1px solid #bdcec2; }
QLabel#loginTitle { color: #24513c; }
QLabel#loginVersion, QLabel#loginWelcome, QLabel#loginFieldLabel { color: #5d7567; }
QPushButton#loginPrimaryButton { background: #428762; color: white; }
QPushButton#loginPrimaryButton:hover { background: #32664a; }
QPushButton#loginSecondaryButton { background: #d5e4da; color: #24513c; }
QPushButton#loginSecondaryButton:hover { background: #c7dacd; }
QFrame#applicationFooter { background: #dce8e0; border-top: 1px solid #bdcec2; }
QLabel#applicationFooterLabel { color: #50685a; }
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

THEMES = {
    "MODERN_BLUE": {"label": "Modern Blue", "stylesheet": MODERN_BLUE},
    "PURPLE_PREMIUM": {"label": "Purple Premium", "stylesheet": PURPLE_PREMIUM},
    "EMERALD": {"label": "Emerald", "stylesheet": EMERALD},
    "DARK": {"label": "Dark Mode", "stylesheet": DARK},
}


def current_theme():
    with SessionLocal() as session:
        saved = get_setting(session, "ui_theme", "MODERN_BLUE")
        if saved not in THEMES:
            saved = "MODERN_BLUE"
            set_setting(session, "ui_theme", saved)
        return saved


def set_theme(theme_key):
    if theme_key not in THEMES:
        raise ValueError("Tema tidak tersedia")
    with SessionLocal() as session:
        set_setting(session, "ui_theme", theme_key)


def apply_theme(app, theme_key):
    theme = THEMES.get(theme_key, THEMES["MODERN_BLUE"])
    app.setStyleSheet(theme["stylesheet"])
    return theme["label"]
