"""Presentation-only Headerbar refinement for WPOS PRO 2."""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from ..database import SessionLocal
from ..services.settings import get_settings


_MONTHS = (
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
)
_WEEKDAYS = (
    "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu",
)


def _store_name(window):
    try:
        with SessionLocal() as session:
            settings = get_settings(session)
        return str(settings.get("store_name") or "TOKO SEMBAKO").strip() or "TOKO SEMBAKO"
    except Exception:
        return "TOKO SEMBAKO"


def _update_headerbar(window):
    if not hasattr(window, "_wpos_store_name_label"):
        return
    now = datetime.now()
    window._wpos_store_name_label.setText(_store_name(window))
    window._wpos_date_label.setText(
        f"{now.day} {_MONTHS[now.month - 1]} {now.year}\n{_WEEKDAYS[now.weekday()]}"
    )


def apply_headerbar(window):
    """Use Context | Store Name | Welcome + Date as the fixed header structure."""
    topbar = window.findChild(__import__("PySide6.QtWidgets", fromlist=["QFrame"]).QFrame, "modernTopbar")
    if topbar is None or topbar.layout() is None:
        return
    if getattr(window, "_wpos_headerbar_v278", False):
        _update_headerbar(window)
        return

    layout = topbar.layout()
    if layout.count() < 3:
        return

    welcome_item = layout.itemAt(1)
    date_item = layout.itemAt(2)
    welcome = welcome_item.widget() if welcome_item else None
    date_label = date_item.widget() if date_item else None
    if welcome is None or date_label is None:
        return

    welcome.setObjectName("modernStoreName")
    welcome.setText(_store_name(window))
    welcome.setAlignment(Qt.AlignCenter)
    welcome.setToolTip("Nama toko dari Pengaturan Toko")
    window._wpos_store_name_label = welcome

    date_label.setObjectName("modernDate")
    date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    window._wpos_date_label = date_label

    _update_headerbar(window)
    window._wpos_headerbar_v278 = True

    if hasattr(window, "modern_stack") and not getattr(window, "_wpos_headerbar_signal", False):
        window.modern_stack.currentChanged.connect(lambda _index: _update_headerbar(window))
        window._wpos_headerbar_signal = True
