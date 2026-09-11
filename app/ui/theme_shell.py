"""Theme-driven visual contract for the WPOS PRO V2 modern shell.

The business pages keep their existing logic. This module owns only presentation
colors and shell surfaces so every page follows the active application theme.
"""


THEME_PALETTES = {
    "MODERN_BLUE": {
        "shell": "#16324f", "shell_alt": "#1f4f78", "shell_hover": "#275f8f", "accent": "#2673b8",
        "content": "#edf0f3", "surface": "#f8f9fa", "surface_alt": "#e5e9ed", "border": "#c6cdd4",
        "text": "#263442", "muted": "#687787", "inverse": "#ffffff", "selected": "#2673b8",
        "selected_text": "#ffffff", "input": "#f8f9fa", "input_border": "#c5cdd5", "table_alt": "#eef1f4",
        "header": "#d8e1e9", "focus": "#2673b8", "danger": "#b54747", "success": "#39734a",
    },
    "KEMERDEKAAN": {
        "shell": "#5f2024", "shell_alt": "#74272c", "shell_hover": "#8b3035", "accent": "#b9343b",
        "content": "#e8e7e8", "surface": "#f1edef", "surface_alt": "#ded9da", "border": "#c7b6b8",
        "text": "#30282a", "muted": "#76585b", "inverse": "#ffffff", "selected": "#b9343b",
        "selected_text": "#ffffff", "input": "#f1edef", "input_border": "#c9b8ba", "table_alt": "#e7e0e2",
        "header": "#a9323a", "focus": "#b9343b", "danger": "#721b21", "success": "#416a4c",
    },
    "KEAGAMAAN": {
        "shell": "#294638", "shell_alt": "#365641", "shell_hover": "#476650", "accent": "#496c55",
        "content": "#e6ebe7", "surface": "#eef2ef", "surface_alt": "#dce3de", "border": "#b7c6ba",
        "text": "#26362d", "muted": "#58705f", "inverse": "#ffffff", "selected": "#496c55",
        "selected_text": "#ffffff", "input": "#eef2ef", "input_border": "#b7c6ba", "table_alt": "#e0e7e1",
        "header": "#587963", "focus": "#496c55", "danger": "#805050", "success": "#52715c",
    },
    "DARK": {
        "shell": "#15181e", "shell_alt": "#242a33", "shell_hover": "#303946", "accent": "#396fae",
        "content": "#20242b", "surface": "#242a33", "surface_alt": "#292f38", "border": "#39414c",
        "text": "#e6eaf0", "muted": "#aab3c0", "inverse": "#ffffff", "selected": "#396fae",
        "selected_text": "#ffffff", "input": "#292f38", "input_border": "#414956", "table_alt": "#292f38",
        "header": "#303946", "focus": "#6ea8fe", "danger": "#9d4f55", "success": "#52715c",
    },
}


def theme_shell_stylesheet(theme_key: str) -> str:
    """Return the complete modern-shell and page-component visual layer."""
    p = THEME_PALETTES.get(theme_key, THEME_PALETTES["MODERN_BLUE"])
    return f"""
/* WPOS PRO V2 — active theme: {theme_key} */
QFrame#modernSidebar {{ background: {p['shell']}; color: {p['inverse']}; border: 0; min-width: 230px; max-width: 250px; }}
QFrame#modernBrand {{ background: {p['shell_alt']}; border: 1px solid {p['shell_hover']}; border-radius: 14px; }}
QLabel#modernBrandLogo {{ min-width: 44px; max-width: 44px; min-height: 44px; max-height: 44px; }}
QLabel#modernBrandName {{ color: {p['inverse']}; font-size: 18px; font-weight: 900; }}
QLabel#modernBrandVersion {{ color: {p['muted']}; font-size: 9px; font-weight: 700; }}
QListWidget#modernNav {{ background: {p['shell']}; color: {p['muted']}; border: 0; outline: none; padding: 0; }}
QListWidget#modernNav::item {{ background: transparent; color: {p['muted']}; padding: 9px 8px; margin: 1px 0; border: 0; border-radius: 8px; font-size: 12px; }}
QListWidget#modernNav::item:hover {{ background: {p['shell_hover']}; color: {p['inverse']}; }}
QListWidget#modernNav::item:selected {{ background: {p['selected']}; color: {p['selected_text']}; font-weight: 800; }}
QListWidget#modernNav::item:disabled {{ background: transparent; color: {p['muted']}; padding: 11px 8px 4px; margin-top: 5px; font-size: 9px; font-weight: 900; }}
QFrame#modernAccount {{ background: {p['shell_alt']}; border: 1px solid {p['shell_hover']}; border-radius: 12px; }}
QLabel#modernUser {{ color: {p['inverse']}; font-weight: 800; }}
QLabel#modernRole {{ color: {p['muted']}; font-size: 10px; }}
QPushButton#modernLogout {{ background: {p['shell_hover']}; color: {p['inverse']}; border: 1px solid {p['shell_hover']}; border-radius: 8px; padding: 7px; margin-top: 5px; }}
QPushButton#modernLogout:hover {{ background: {p['accent']}; color: {p['inverse']}; }}

QFrame#modernContent {{ background: {p['content']}; color: {p['text']}; }}
QFrame#modernTopbar {{ background: {p['surface']}; border: 1px solid {p['border']}; border-radius: 12px; }}
QLabel#modernContext {{ color: {p['text']}; font-size: 17px; font-weight: 900; }}
QLabel#modernHint {{ color: {p['muted']}; font-size: 10px; }}
QLabel#modernStatusOffline {{ background: {p['surface_alt']}; color: {p['danger']}; border: 1px solid {p['border']}; border-radius: 999px; padding: 5px 9px; font-size: 9px; font-weight: 900; }}
QLabel#modernStatusLocal {{ background: {p['surface_alt']}; color: {p['success']}; border: 1px solid {p['border']}; border-radius: 999px; padding: 5px 9px; font-size: 9px; font-weight: 900; }}
QStackedWidget#modernStack {{ background: transparent; border: 0; }}
QWidget#modernStack > QWidget {{ background: {p['content']}; color: {p['text']}; }}
QWidget#modernStack QWidget {{ font-size: 11px; }}

QLabel#pageTitle {{ color: {p['text']}; }}
QLabel#pageSubtitle {{ color: {p['muted']}; }}
QFrame#card {{ background: {p['surface']}; border: 1px solid {p['border']}; border-radius: 12px; }}
QLabel#cardTitle {{ color: {p['muted']}; font-size: 10px; font-weight: 800; }}
QLabel#cardValue {{ color: {p['text']}; font-size: 22px; font-weight: 900; }}
QLabel#total {{ background: {p['accent']}; color: {p['inverse']}; }}
QGroupBox {{ background: {p['surface']}; border: 1px solid {p['border']}; border-radius: 12px; color: {p['text']}; }}
QGroupBox::title {{ background: {p['surface']}; color: {p['text']}; }}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {{ background: {p['input']}; color: {p['text']}; border: 1px solid {p['input_border']}; border-radius: 8px; }}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {{ border: 1px solid {p['focus']}; }}
QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QTextEdit:disabled {{ background: {p['surface_alt']}; color: {p['muted']}; }}
QPushButton {{ background: {p['accent']}; color: {p['inverse']}; border-color: {p['accent']}; }}
QPushButton:hover {{ background: {p['shell_hover']}; color: {p['inverse']}; border-color: {p['shell_hover']}; }}
QPushButton#primary, QPushButton#dashboardPrimary {{ background: {p['accent']}; color: {p['inverse']}; border-color: {p['accent']}; }}
QPushButton#danger {{ background: {p['danger']}; color: {p['inverse']}; border-color: {p['danger']}; }}
QPushButton#dashboardSecondary {{ background: {p['surface_alt']}; color: {p['text']}; border-color: {p['border']}; }}
QPushButton#dashboardGhost {{ background: {p['surface']}; color: {p['text']}; border-color: {p['border']}; }}
QTableWidget {{ background: {p['surface']}; color: {p['text']}; border: 1px solid {p['border']}; gridline-color: {p['border']}; alternate-background-color: {p['table_alt']}; selection-background-color: {p['selected']}; selection-color: {p['selected_text']}; }}
QTableWidget::item {{ padding: 7px; }}
QHeaderView::section {{ background: {p['header']}; color: {p['text']}; border: 0; border-bottom: 1px solid {p['border']}; }}
QScrollBar::handle:vertical {{ background: {p['border']}; border-radius: 4px; min-height: 28px; }}
QScrollBar::handle:vertical:hover {{ background: {p['muted']}; }}
QToolTip {{ background: {p['shell']}; color: {p['inverse']}; border: 1px solid {p['border']}; padding: 6px 8px; }}

QFrame#premiumCashierPage, QFrame#premiumScanCard, QFrame#premiumCartCard, QFrame#premiumPayCard, QFrame#premiumChangeBox, QFrame#premiumTotalBox {{ background: {p['surface']}; color: {p['text']}; border: 1px solid {p['border']}; border-radius: 12px; }}
QLabel#premiumPageTitle, QLabel#premiumSectionTitle {{ color: {p['text']}; font-weight: 900; }}
QLabel#premiumPageSubtitle, QLabel#premiumShortcut, QLabel#premiumMuted, QLabel#premiumFieldCaption, QLabel#premiumPayLabel, QLabel#premiumTotalCaption, QLabel#premiumChangeCaption {{ color: {p['muted']}; }}
QLineEdit#premiumBarcode, QDoubleSpinBox#premiumQty, QDoubleSpinBox#premiumMoneyInput, QComboBox#premiumMethod {{ background: {p['input']}; color: {p['text']}; border: 1px solid {p['input_border']}; }}
QLabel#premiumTotal, QLabel#premiumChange {{ color: {p['text']}; font-size: 24px; font-weight: 900; }}
QPushButton#premiumAdd, QPushButton#premiumCheckout {{ background: {p['accent']}; color: {p['inverse']}; border-color: {p['accent']}; }}
QPushButton#premiumClear {{ background: {p['surface_alt']}; color: {p['text']}; border-color: {p['border']}; }}
"""


def apply_theme_shell(widget, theme_key: str) -> None:
    """Append the active theme's visual contract to a window/application."""
    widget.setStyleSheet(widget.styleSheet() + theme_shell_stylesheet(theme_key))
