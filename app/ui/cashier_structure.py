"""Presentation-only structure refinement for the Kasir page."""

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout


def _find_button(window, text):
    for button in window.findChildren(QPushButton):
        if button.text().strip() == text:
            return button
    return None


def apply_cashier_structure(window):
    """Reorganize existing Kasir widgets once per window."""
    if getattr(window, "_wpos_cashier_structure_v277", False):
        return
    page = window.modern_stack.widget(1) if hasattr(window, "modern_stack") else None
    if page is None:
        return
    cart_card = page.findChild(QFrame, "premiumCartCard")
    pay_card = page.findChild(QFrame, "premiumPayCard")
    if cart_card is None or pay_card is None:
        return

    pay_card.setMinimumWidth(290)
    pay_card.setMaximumWidth(330)
    pay_card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    pay_layout = pay_card.layout()
    if pay_layout is not None:
        pay_layout.setSpacing(8)
        for index in range(pay_layout.count() - 1, -1, -1):
            item = pay_layout.itemAt(index)
            if item is not None and item.spacerItem() is not None:
                pay_layout.takeAt(index)

    for label in cart_card.findChildren(QLabel):
        if label.objectName() == "premiumSectionTitle":
            label.setText("Keranjang Transaksi")
            break

    labels = {
        "PARKIR": "PARKIR",
        "PARKIRAN": "TRANSAKSI PARKIR",
        "BATAL": "BATAL TRANSAKSI",
        "RIWAYAT": "RIWAYAT TRANSAKSI",
        "CLEAR": "CLEAR",
    }
    buttons = []
    for key, display in labels.items():
        button = _find_button(window, key)
        if button is not None and button.parentWidget() is pay_card:
            buttons.append((button, display))

    checkout = _find_button(window, "BAYAR & CETAK")
    if checkout is not None and checkout.parentWidget() is pay_card:
        buttons.append((checkout, "BAYAR & CETAK"))

    if not buttons:
        window._wpos_cashier_structure_v277 = True
        return

    for button, display in buttons:
        if pay_layout is not None:
            pay_layout.removeWidget(button)
        button.setText(display)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    controls = QFrame(page)
    controls.setObjectName("premiumTransactionControls")
    controls_layout = QVBoxLayout(controls)
    controls_layout.setContentsMargins(0, 0, 0, 0)
    controls_layout.setSpacing(5)
    title = QLabel("Kontrol Transaksi")
    title.setObjectName("premiumControlsTitle")
    controls_layout.addWidget(title)

    row = QHBoxLayout()
    row.setSpacing(8)
    for button, _display in buttons:
        row.addWidget(button, 1)
    controls_layout.addLayout(row)

    root = page.layout()
    if root is None:
        return
    root.addWidget(controls, 0)
    checkout.setObjectName("premiumCheckout")
    window._wpos_cashier_structure_v277 = True
