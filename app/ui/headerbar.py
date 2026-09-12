"""Presentation-only Headerbar refinement for WPOS PRO 2."""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from ..database import SessionLocal
from ..services.settings import get_settings


_MONTHS = (
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
)
_WEEKDAYS = (
    "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu",
)


def _store_settings(window):
    try:
        with SessionLocal() as session:
            settings = get_settings(session)
        return (
            str(settings.get("store_name") or "TOKO SEMBAKO").strip() or "TOKO SEMBAKO",
            str(settings.get("store_address") or "").strip(),
        )
    except Exception:
        return "TOKO SEMBAKO", ""


def _update_headerbar(window):
    if not hasattr(window, "_wpos_store_name_label"):
        return
    now = datetime.now()
    store_name, store_address = _store_settings(window)
    window._wpos_store_name_label.setText(store_name)
    window._wpos_store_address_label.setText(store_address)
    window._wpos_store_address_label.setVisible(bool(store_address))
    window._wpos_date_label.setText(
        f"{now.day} {_MONTHS[now.month - 1]} {now.year}"
    )


def apply_headerbar(window):
    """Use Context | Store Name + Address | Date as the fixed header structure."""
    topbar = window.findChild(QFrame, "modernTopbar")
    if topbar is None or topbar.layout() is None:
        return
    if getattr(window, "_wpos_headerbar_v279", False):
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

    # Replace the old single-line welcome label with a centered store identity block.
    welcome.setObjectName("modernStoreName")
    welcome.setText(_store_settings(window)[0])
    welcome.setAlignment(Qt.AlignCenter)
    welcome.setToolTip("Nama toko dari Pengaturan Toko")

    store_host = QWidgetHeaderHost(welcome)
    store_layout = store_host.layout()
    store_layout.addWidget(welcome)
    address = QLabel()
    address.setObjectName("modernStoreAddress")
    address.setAlignment(Qt.AlignCenter)
    address.setToolTip("Alamat toko dari Pengaturan Toko")
    store_layout.addWidget(address)
    layout.insertWidget(1, store_host, 1)
    layout.removeItem(welcome_item)
    window._wpos_store_name_label = welcome
    window._wpos_store_address_label = address

    date_label.setObjectName("modernDate")
    date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    window._wpos_date_label = date_label

    _update_headerbar(window)
    window._wpos_headerbar_v279 = True

    if hasattr(window, "modern_stack") and not getattr(window, "_wpos_headerbar_signal", False):
        window.modern_stack.currentChanged.connect(lambda _index: _update_headerbar(window))
        window._wpos_headerbar_signal = True


class QWidgetHeaderHost(QFrame):
    """Transparent host used only to stack store name and address in the center zone."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("modernStoreHost")
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")
        self.setSizePolicy(__import__("PySide6.QtWidgets", fromlist=["QSizePolicy"]).QSizePolicy.Expanding, __import__("PySide6.QtWidgets", fromlist=["QSizePolicy"]).QSizePolicy.Preferred)
        box = QVBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(0)
