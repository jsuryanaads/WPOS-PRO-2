"""Presentation-only Headerbar refinement for WPOS PRO 2.

Header contract:
    KIRI   = active page title + dynamic hint
    TENGAH = store name + store address from Pengaturan Toko
    KANAN  = logged-in username + Indonesian date
"""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout

from ..database import SessionLocal
from ..services.settings import get_settings


_MONTHS = (
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
)


def _store_settings(window):
    try:
        with SessionLocal() as session:
            settings = get_settings(session)
        store_name = str(settings.get("store_name") or "TOKO SEMBAKO").strip() or "TOKO SEMBAKO"
        store_address = str(settings.get("store_address") or "").strip()
        return store_name, store_address
    except Exception:
        return "TOKO SEMBAKO", ""


def _format_date(value):
    """Return an Indonesian date without weekday."""
    return f"{value.day} {_MONTHS[value.month - 1]} {value.year}"


def _update_headerbar(window):
    if not hasattr(window, "_wpos_store_name_label"):
        return

    store_name, store_address = _store_settings(window)
    window._wpos_store_name_label.setText(store_name)
    window._wpos_store_address_label.setText(store_address or "Alamat toko belum diatur")
    window._wpos_store_address_label.setVisible(bool(store_address))
    window._wpos_date_label.setText(_format_date(datetime.now()))


def apply_headerbar(window):
    """Apply the fixed three-zone Headerbar without changing business logic."""
    topbar = window.findChild(QFrame, "modernTopbar")
    if topbar is None or topbar.layout() is None:
        return
    if getattr(window, "_wpos_headerbar_v218", False):
        _update_headerbar(window)
        return

    layout = topbar.layout()
    if layout.count() < 3:
        return

    center_item = layout.itemAt(1)
    date_item = layout.itemAt(2)
    center_widget = center_item.widget() if center_item else None
    date_label = date_item.widget() if date_item else None
    if center_widget is None or date_label is None:
        return

    # CENTER: store name + address.
    center_widget.setParent(None)
    store_host = QFrame()
    store_host.setObjectName("modernStoreHost")
    store_host.setFrameShape(QFrame.NoFrame)
    store_host.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    store_host.setStyleSheet("background: transparent; border: none;")
    store_layout = QVBoxLayout(store_host)
    store_layout.setContentsMargins(0, 0, 0, 0)
    store_layout.setSpacing(0)

    store_name = center_widget
    store_name.setObjectName("modernStoreName")
    store_name.setAlignment(Qt.AlignCenter)
    store_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    store_name.setToolTip("Nama toko dari Pengaturan Toko")
    store_layout.addWidget(store_name)

    address = QLabel()
    address.setObjectName("modernStoreAddress")
    address.setAlignment(Qt.AlignCenter)
    address.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    address.setToolTip("Alamat toko dari Pengaturan Toko")
    store_layout.addWidget(address)

    layout.removeItem(center_item)
    layout.insertWidget(1, store_host, 1)

    window._wpos_store_name_label = store_name
    window._wpos_store_address_label = address

    # RIGHT: username + automatic Indonesian date.
    date_label.setParent(None)
    right_host = QFrame()
    right_host.setObjectName("modernHeaderAccount")
    right_host.setFrameShape(QFrame.NoFrame)
    right_host.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
    right_host.setStyleSheet("background: transparent; border: none;")
    right_layout = QVBoxLayout(right_host)
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.setSpacing(0)

    username = QLabel(str(getattr(window.user, "username", "")))
    username.setObjectName("modernHeaderUsername")
    username.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    username.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
    right_layout.addWidget(username)
    right_layout.addWidget(date_label)

    layout.removeItem(date_item)
    layout.addWidget(right_host, 0)

    window._wpos_header_username_label = username
    window._wpos_date_label = date_label
    date_label.setObjectName("modernDate")
    date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    date_label.setToolTip("Tanggal otomatis")

    _update_headerbar(window)
    window._wpos_headerbar_v218 = True

    if hasattr(window, "modern_stack") and not getattr(window, "_wpos_headerbar_signal", False):
        window.modern_stack.currentChanged.connect(lambda _index: _update_headerbar(window))
        window._wpos_headerbar_signal = True
