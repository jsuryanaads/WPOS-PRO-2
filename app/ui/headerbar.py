"""Presentation-only Headerbar refinement for WPOS PRO 2.

Header contract:
    KIRI   = active page title + dynamic hint
    TENGAH = store name + store address from Pengaturan Toko
    KANAN  = logged-in user name + Indonesian date

The implementation deliberately updates the existing topbar labels in place.
It does not detach/reparent Qt widgets, which keeps QObject ownership stable
and avoids introducing lifetime-sensitive UI mutations during refresh.
"""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel

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


def _user_display_name(window):
    """Return the logged-in user's display name, never the login username."""
    user = getattr(window, "user", None)
    name = str(getattr(user, "name", "") or "").strip()
    return name or "Pengguna"


def _update_headerbar(window):
    """Refresh header values without changing Qt widget ownership."""
    store_label = getattr(window, "_wpos_store_label", None)
    user_date_label = getattr(window, "_wpos_user_date_label", None)
    if store_label is None or user_date_label is None:
        return

    store_name, store_address = _store_settings(window)
    store_label.setText(store_name if not store_address else f"{store_name}\n{store_address}")
    user_date_label.setText(f"{_user_display_name(window)}\n{_format_date(datetime.now())}")


def apply_headerbar(window):
    """Apply the fixed three-zone Headerbar using existing widgets only."""
    topbar = window.findChild(QFrame, "modernTopbar")
    if topbar is None or topbar.layout() is None:
        return

    if getattr(window, "_wpos_headerbar_v219", False):
        _update_headerbar(window)
        return

    layout = topbar.layout()
    if layout.count() < 3:
        return

    center_item = layout.itemAt(1)
    date_item = layout.itemAt(2)
    store_label = center_item.widget() if center_item else None
    user_date_label = date_item.widget() if date_item else None
    if store_label is None or user_date_label is None:
        return

    # Keep the existing QLabel objects in their original layouts. This is
    # intentionally safer than setParent()/layout removal/reinsertion.
    store_label.setObjectName("modernStoreName")
    store_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
    store_label.setWordWrap(True)
    store_label.setToolTip("Nama dan alamat toko dari Pengaturan Toko")

    user_date_label.setObjectName("modernHeaderUserName")
    user_date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    user_date_label.setWordWrap(True)
    user_date_label.setToolTip("Nama pengguna yang sedang login dan tanggal otomatis")

    window._wpos_store_label = store_label
    window._wpos_user_date_label = user_date_label
    window._wpos_headerbar_v219 = True

    _update_headerbar(window)

    if hasattr(window, "modern_stack") and not getattr(window, "_wpos_headerbar_signal", False):
        window.modern_stack.currentChanged.connect(lambda _index: _update_headerbar(window))
        window._wpos_headerbar_signal = True
