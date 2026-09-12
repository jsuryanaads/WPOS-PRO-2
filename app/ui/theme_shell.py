"""Theme-driven presentation layer for the WPOS PRO 2 shell."""

THEME_PALETTES = {
    "DARK": {
        "shell":"#15181e","shell_alt":"#242a33","shell_hover":"#303946","accent":"#396fae","content":"#20242b","surface":"#242a33","surface_alt":"#292f38","border":"#39414c","text":"#e6eaf0","muted":"#aab3c0","inverse":"#ffffff","selected":"#396fae","selected_text":"#ffffff","input":"#292f38","input_border":"#414956","table_alt":"#292f38","header":"#303946","focus":"#6ea8fe","danger":"#9d4f55","success":"#52715c","sidebar_text":"#aab3c0","sidebar_inverse":"#ffffff"
    },
    "LIGHT": {
        "shell":"#f7f9fb","shell_alt":"#e8eef4","shell_hover":"#d8e5ef","accent":"#2b78b8","content":"#f4f6f8","surface":"#ffffff","surface_alt":"#eef2f5","border":"#c8d1d9","text":"#263442","muted":"#667583","inverse":"#263442","selected":"#2b78b8","selected_text":"#ffffff","input":"#ffffff","input_border":"#c8d1d9","table_alt":"#f1f4f7","header":"#e2e8ed","focus":"#2b78b8","danger":"#b34f4f","success":"#39734a","sidebar_text":"#435465","sidebar_inverse":"#16324f"
    },
}


def theme_shell_stylesheet(theme_key: str) -> str:
    p = THEME_PALETTES.get(theme_key, THEME_PALETTES["DARK"])
    return f"""
/* WPOS PRO 2 — active theme: {theme_key} */
QFrame#modernSidebar {{ background:{p['shell']}; color:{p['sidebar_text']}; border:0; min-width:230px; max-width:230px; }}
QFrame#modernBrand {{ background:{p['shell_alt']}; border:1px solid {p['shell_hover']}; border-radius:14px; }}
QLabel#modernBrandLogo {{ min-width:42px; max-width:42px; min-height:42px; max-height:42px; }}
QLabel#modernBrandName {{ color:{p['sidebar_inverse']}; font-size:18px; font-weight:900; }}
QLabel#modernBrandVersion {{ color:{p['muted']}; font-size:9px; font-weight:700; }}
QListWidget#modernNav {{ background:{p['shell']}; color:{p['sidebar_text']}; border:0; outline:none; padding:0; }}
QListWidget#modernNav::item {{ background:transparent; color:{p['sidebar_text']}; padding:5px 10px; margin:1px 2px; border:1px solid transparent; border-radius:8px; font-size:11px; min-height:20px; }}
QListWidget#modernNav::item:hover {{ background:{p['shell_hover']}; color:{p['sidebar_inverse']}; }}
QListWidget#modernNav::item:selected {{ background:{p['selected']}; color:{p['selected_text']}; font-weight:800; border:1px solid {p['selected']}; }}
QListWidget#modernNav::item:disabled {{ background:{p['shell_alt']}; color:{p['sidebar_inverse']}; padding:4px 10px; margin:5px 2px 2px; border:1px solid {p['shell_hover']}; border-radius:7px; font-size:9px; font-weight:900; }}
QListWidget#modernNav::item:disabled:hover {{ background:{p['shell_alt']}; color:{p['sidebar_inverse']}; }}
QFrame#modernAccount {{ background:{p['shell_alt']}; border:1px solid {p['shell_hover']}; border-radius:12px; }}
QLabel#modernUser {{ color:{p['sidebar_inverse']}; font-weight:800; }}
QLabel#modernRole {{ color:{p['muted']}; font-size:10px; }}
QPushButton#modernLogout {{ background:{p['shell_hover']}; color:{p['sidebar_inverse']}; border:1px solid {p['shell_hover']}; border-radius:8px; padding:7px; margin-top:5px; }}
QPushButton#modernLogout:hover {{ background:{p['accent']}; color:{p['selected_text']}; }}
QFrame#modernContent {{ background:{p['content']}; color:{p['text']}; }}
QFrame#modernTopbar {{ background:{p['surface']}; border:1px solid {p['border']}; border-radius:12px; min-height:58px; max-height:64px; }}
QLabel#modernContext {{ color:{p['text']}; font-size:17px; font-weight:900; }}
QLabel#modernHint {{ color:{p['muted']}; font-size:10px; }}
QFrame#modernStoreHost, QFrame#modernHeaderAccount {{ background:transparent; border:0; }}
QLabel#modernStoreName {{ color:{p['text']}; font-size:15px; font-weight:900; padding:0 12px; }}
QLabel#modernStoreAddress {{ color:{p['muted']}; font-size:9px; padding:0 12px; }}
QLabel#modernHeaderUsername {{ color:{p['text']}; font-size:10px; font-weight:800; }}
QLabel#modernDate {{ color:{p['muted']}; font-size:10px; font-weight:700; padding-left:12px; min-width:108px; }}
QStackedWidget#modernStack {{ background:transparent; border:0; }}
QWidget#modernStack > QWidget {{ background:{p['content']}; color:{p['text']}; }}
QLabel#pageTitle {{ color:{p['text']}; }}
QLabel#pageSubtitle {{ color:{p['muted']}; }}
QFrame#card {{ background:{p['surface']}; border:1px solid {p['border']}; }}
QLabel#cardTitle {{ color:{p['muted']}; }}
QLabel#cardValue {{ color:{p['text']}; }}
QLabel#total {{ background:{p['accent']}; color:{p['inverse']}; }}
QGroupBox {{ background:{p['surface']}; border:1px solid {p['border']}; color:{p['text']}; }}
QGroupBox::title {{ background:{p['surface']}; color:{p['text']}; }}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {{ background:{p['input']}; color:{p['text']}; border:1px solid {p['input_border']}; }}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {{ border:1px solid {p['focus']}; }}
QPushButton {{ background:{p['accent']}; color:{p['inverse']}; border-color:{p['accent']}; }}
QPushButton:hover {{ background:{p['shell_hover']}; border-color:{p['shell_hover']}; }}
QPushButton#primary, QPushButton#dashboardPrimary, QPushButton#premiumAdd, QPushButton#premiumCheckout {{ background:{p['accent']}; color:{p['inverse']}; }}
QPushButton#danger {{ background:{p['danger']}; color:{p['inverse']}; }}
QPushButton#dashboardSecondary, QPushButton#secondary, QPushButton#dashboardGhost, QPushButton#premiumClear {{ background:{p['surface_alt']}; color:{p['text']}; border-color:{p['border']}; }}
QTableWidget {{ background:{p['surface']}; color:{p['text']}; border:1px solid {p['border']}; gridline-color:{p['border']}; alternate-background-color:{p['table_alt']}; selection-background-color:{p['selected']}; selection-color:{p['selected_text']}; }}
QHeaderView::section {{ background:{p['header']}; color:{p['text']}; border:0; border-bottom:1px solid {p['border']}; }}
QToolTip {{ background:{p['shell']}; color:{p['sidebar_inverse']}; border:1px solid {p['border']}; padding:6px 8px; }}
QFrame#masterHeader {{ background:transparent; border:0; }}
QFrame#masterFormCard, QFrame#masterTableCard {{ background:{p['surface']}; color:{p['text']}; border:1px solid {p['border']}; border-radius:12px; }}
QLabel#sectionTitle {{ color:{p['text']}; font-size:13px; font-weight:800; }}
QFrame#premiumCashierPage, QFrame#premiumScanCard, QFrame#premiumCartCard, QFrame#premiumPayCard, QFrame#premiumChangeBox, QFrame#premiumTotalBox, QFrame#premiumTransactionControls {{ background:{p['surface']}; color:{p['text']}; border:1px solid {p['border']}; border-radius:12px; }}
QFrame#premiumCartCard {{ min-width:0px; }}
QFrame#premiumPayCard {{ min-width:290px; max-width:330px; }}
QTableWidget#premiumCartTable {{ min-width:0px; }}
QLabel#premiumSectionTitle {{ color:{p['text']}; font-weight:900; }}
QLabel#premiumControlsTitle {{ color:{p['text']}; font-size:12px; font-weight:900; }}
QLabel#premiumMuted, QLabel#premiumFieldCaption, QLabel#premiumPayLabel, QLabel#premiumTotalCaption, QLabel#premiumChangeCaption {{ color:{p['muted']}; }}
QLineEdit#premiumBarcode, QDoubleSpinBox#premiumQty, QDoubleSpinBox#premiumMoneyInput, QComboBox#premiumMethod {{ background:{p['input']}; color:{p['text']}; border:1px solid {p['input_border']}; }}
QLabel#premiumTotal, QLabel#premiumChange {{ color:{p['text']}; font-size:24px; font-weight:900; }}
QFrame#premiumTransactionControls QPushButton {{ min-height:36px; font-weight:800; }}
QFrame#premiumTransactionControls QPushButton#premiumCheckout {{ min-width:180px; }}
QFrame#applicationFooter {{ background:{p['surface_alt']}; border-top:1px solid {p['border']}; }}
QLabel#applicationFooterLabel {{ color:{p['muted']}; }}
"""


def apply_theme_shell(widget, theme_key: str) -> None:
    marker = "/* WPOS PRO 2 — active theme:"
    current = widget.styleSheet()
    if marker in current:
        current = current[:current.index(marker)]
    widget.setStyleSheet(current + theme_shell_stylesheet(theme_key))
