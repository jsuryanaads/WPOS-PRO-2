from PySide6.QtWidgets import (
    QDialog, QFrame, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFileDialog, QMessageBox, QInputDialog
)

from ..database import SessionLocal, engine
from ..services.excel import export_products, import_products
from ..services.reset import reset_all_business_data, reset_transactions_and_stock


COMPLEX_POPUPS = {
    2: ("Data Produk", "Form Produk", "Kelola data produk tanpa memenuhi halaman tabel."),
    4: ("Data Pembelian", "Form Pembelian", "Input pembelian melalui dialog agar tabel tetap mendapat ruang maksimal."),
}

MASTER_POPUPS = {"Supplier": "Form Supplier", "Pelanggan": "Form Pelanggan"}


class _PopupController:
    def __init__(self, page, form_box, title, description, buttons=None, width=720, height=520):
        self.page = page
        self.form_box = form_box
        self.dialog = QDialog(page.window())
        self.dialog.setWindowTitle(title)
        self.dialog.setModal(True)
        self.dialog.resize(width, height)
        self.dialog.setMinimumSize(width, height)
        root = QVBoxLayout(self.dialog)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(10)
        heading = QLabel(title)
        heading.setObjectName("popupTitle")
        root.addWidget(heading)
        hint = QLabel(description)
        hint.setObjectName("popupHint")
        hint.setWordWrap(True)
        root.addWidget(hint)
        form_box.setParent(self.dialog)
        form_box.show()
        root.addWidget(form_box, 1)
        actions = QHBoxLayout()
        actions.setSpacing(8)
        for button in buttons or []:
            button.setParent(self.dialog)
            button.show()
            actions.addWidget(button)
        actions.addStretch()
        close = QPushButton("Tutup")
        close.setObjectName("secondary")
        close.clicked.connect(self.dialog.reject)
        actions.addWidget(close)
        root.addLayout(actions)
        self.dialog.setProperty("wposPopup", True)

    def open(self):
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
        return self.dialog


def _remove_widget_from_layout(layout, target):
    if layout is None:
        return False
    for index in range(layout.count() - 1, -1, -1):
        item = layout.itemAt(index)
        if item.widget() is target:
            layout.takeAt(index)
            return True
        child = item.layout()
        if child is not None and _remove_widget_from_layout(child, target):
            return True
    return False


def _find_groupbox(page, title):
    for box in page.findChildren(QGroupBox):
        if box.title() == title:
            return box
    return None


def _attach_product_excel(page):
    if getattr(page, "_wpos_excel_actions", False):
        return
    actions = QHBoxLayout()
    export_button = QPushButton("Export Excel")
    export_button.setObjectName("secondary")
    import_button = QPushButton("Import Excel")
    import_button.setObjectName("secondary")
    template_button = QPushButton("Template Excel")
    template_button.setObjectName("secondary")
    export_button.clicked.connect(lambda: _export_product_excel(page))
    import_button.clicked.connect(lambda: _import_product_excel(page))
    template_button.clicked.connect(lambda: _export_product_excel(page, template=True))
    actions.addWidget(export_button)
    actions.addWidget(import_button)
    actions.addWidget(template_button)
    actions.addStretch()
    page.layout().insertLayout(2, actions)
    page._wpos_excel_actions = True


def _export_product_excel(page, template=False):
    filename, _ = QFileDialog.getSaveFileName(
        page, "Export Produk ke Excel", "produk_template.xlsx" if template else "produk.xlsx", "Excel (*.xlsx)"
    )
    if not filename:
        return
    try:
        with SessionLocal() as session:
            path = export_products(session, filename)
        QMessageBox.information(page, "Export Excel", f"File berhasil dibuat:\n{path}")
    except Exception as exc:
        QMessageBox.critical(page, "Export gagal", str(exc))


def _import_product_excel(page):
    filename, _ = QFileDialog.getOpenFileName(page, "Import Produk dari Excel", "", "Excel (*.xlsx)")
    if not filename:
        return
    choice = QMessageBox.question(
        page,
        "Mode Import",
        "Pilih mode import.\n\nYES = Tambah produk baru saja\nNO = Update data berdasarkan Barcode",
        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
        QMessageBox.Yes,
    )
    if choice == QMessageBox.Cancel:
        return
    mode = "add" if choice == QMessageBox.Yes else "update"
    try:
        with SessionLocal() as session:
            result = import_products(session, filename, mode=mode)
        page.load_product_options()
        page.load_products()
        if hasattr(page, "clear_product_form"):
            page.clear_product_form()
        QMessageBox.information(
            page, "Import Excel berhasil",
            f"Produk baru: {result['created']}\nProduk diperbarui: {result['updated']}\n\nStok berjalan tidak diubah saat update Barcode."
        )
    except Exception as exc:
        QMessageBox.critical(page, "Import dibatalkan", str(exc))


def _popup_complex_page(page, title, dialog_title, description):
    if getattr(page, "_wpos_form_layout_mode", None) == "popup":
        if title == "Data Produk":
            _attach_product_excel(page)
        return
    form_box = _find_groupbox(page, title)
    if form_box is None:
        return
    buttons = [button for button in page.findChildren(QPushButton) if button.parent() is page]
    for button in buttons:
        _remove_widget_from_layout(page.layout(), button)
        button.hide()
    _remove_widget_from_layout(page.layout(), form_box)
    controller = _PopupController(
        page, form_box, dialog_title, description, buttons=buttons,
        width=760 if title == "Data Produk" else 680,
        height=560 if title == "Data Produk" else 440,
    )
    page._wpos_form_popup = controller
    trigger_text = "＋ Tambah / Edit Produk" if title == "Data Produk" else "＋ Pembelian Baru"
    trigger = QPushButton(trigger_text)
    trigger.setObjectName("formPopupTrigger")
    trigger.clicked.connect(controller.open)
    page.layout().insertWidget(1, trigger)
    page._wpos_form_layout_mode = "popup"
    if title == "Data Produk":
        _attach_product_excel(page)


def _popup_master_page(page, title, dialog_title):
    if getattr(page, "_wpos_form_layout_mode", None) == "popup":
        return
    form_box = page.findChild(QFrame, "masterFormCard")
    if form_box is None:
        return
    _remove_widget_from_layout(page.layout(), form_box)
    controller = _PopupController(
        page, form_box, dialog_title,
        "Form lengkap dibuka sebagai popup agar tabel data tetap menjadi fokus utama.",
        width=620, height=390,
    )
    page._wpos_form_popup = controller
    trigger = QPushButton("＋ Tambah / Edit " + title)
    trigger.setObjectName("formPopupTrigger")
    trigger.clicked.connect(controller.open)
    page.layout().insertWidget(1, trigger)
    page._wpos_form_layout_mode = "popup"


def _inline_simple_master(page):
    if getattr(page, "_wpos_form_layout_mode", None) == "inline":
        return
    form_box = page.findChild(QFrame, "masterFormCard")
    if form_box is None or form_box.layout() is None:
        return
    form_layout = form_box.layout()
    edit = form_box.findChild(QLineEdit)
    label = next((item for item in form_box.findChildren(QLabel) if item.text() == "Name"), None)
    buttons = list(form_box.findChildren(QPushButton))
    if edit is None or label is None or not buttons:
        return
    _remove_widget_from_layout(page.layout(), form_box)
    _remove_widget_from_layout(form_layout, label)
    _remove_widget_from_layout(form_layout, edit)
    inline = QFrame()
    inline.setObjectName("masterInlineCard")
    layout = QHBoxLayout(inline)
    layout.setContentsMargins(16, 10, 16, 10)
    layout.setSpacing(10)
    for widget in (label, edit):
        widget.setParent(inline)
        widget.show()
    layout.addWidget(label)
    layout.addWidget(edit, 1)
    for button in buttons:
        _remove_widget_from_layout(form_layout, button)
        button.setParent(inline)
        button.show()
        layout.addWidget(button)
    page.layout().insertWidget(1, inline)
    form_box.deleteLater()
    page._wpos_form_layout_mode = "inline"


def _attach_reset_controls(window):
    page = window.modern_stack.widget(9) if getattr(window, "modern_stack", None) and window.modern_stack.count() > 9 else None
    if page is None or getattr(page, "_wpos_reset_actions", False):
        return
    box = page.findChild(QGroupBox, "")
    if box is None:
        boxes = page.findChildren(QGroupBox)
        box = next((item for item in boxes if item.title() == "Database"), None)
    if box is None or box.layout() is None:
        return

    separator = QLabel("RESET DATA")
    separator.setObjectName("sectionTitle")
    warning = QLabel(
        "Fitur ini menghapus data secara permanen. Akun pengguna dan pengaturan toko tetap dipertahankan."
    )
    warning.setWordWrap(True)
    warning.setObjectName("pageSubtitle")
    tx_button = QPushButton("RESET TRANSAKSI & STOK")
    tx_button.setObjectName("secondary")
    all_button = QPushButton("RESET SEMUA DATA BISNIS")
    all_button.setObjectName("danger")
    tx_button.clicked.connect(lambda: _reset_transactions(window))
    all_button.clicked.connect(lambda: _reset_all_business(window))
    box.layout().addWidget(separator)
    box.layout().addWidget(warning)
    box.layout().addWidget(tx_button)
    box.layout().addWidget(all_button)
    page._wpos_reset_actions = True


def _confirm_reset(parent, title, message):
    first = QMessageBox.question(
        parent, title, message + "\n\nTindakan ini tidak dapat dibatalkan. Lanjutkan?",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
    )
    if first != QMessageBox.Yes:
        return False
    text, ok = QInputDialog.getText(parent, "Konfirmasi Reset", "Ketik RESET untuk mengonfirmasi:")
    return ok and text.strip() == "RESET"


def _reset_transactions(window):
    if not _confirm_reset(
        window, "Reset Transaksi & Stok",
        "Penjualan, pembelian, mutasi stok dan mutasi kas akan dihapus. Master Produk tetap ada dan stoknya menjadi 0."
    ):
        return
    try:
        engine.dispose()
        with SessionLocal() as session:
            result = reset_transactions_and_stock(session)
        QMessageBox.information(
            window, "Reset Berhasil",
            "Transaksi dan stok berhasil direset.\n\nTutup dan jalankan kembali aplikasi agar seluruh halaman memuat data baru."
        )
    except Exception as exc:
        QMessageBox.critical(window, "Reset Gagal", str(exc))


def _reset_all_business(window):
    if not _confirm_reset(
        window, "Reset Semua Data Bisnis",
        "SEMUA produk, kategori, satuan, supplier, pelanggan, penjualan, pembelian, mutasi stok dan mutasi kas akan dihapus."
    ):
        return
    try:
        engine.dispose()
        with SessionLocal() as session:
            result = reset_all_business_data(session)
        QMessageBox.information(
            window, "Reset Berhasil",
            "Semua data bisnis berhasil direset. Akun pengguna dan pengaturan toko tetap ada.\n\nTutup dan jalankan kembali aplikasi."
        )
    except Exception as exc:
        QMessageBox.critical(window, "Reset Gagal", str(exc))


def _remove_widget_from_layout(layout, target):
    if layout is None:
        return False
    for index in range(layout.count() - 1, -1, -1):
        item = layout.itemAt(index)
        if item.widget() is target:
            layout.takeAt(index)
            return True
        child = item.layout()
        if child is not None and _remove_widget_from_layout(child, target):
            return True
    return False


def apply_hybrid_form_layouts(window):
    """Apply approved presentation-only form layouts, Excel actions and reset controls."""
    stack = getattr(window, "modern_stack", None)
    if stack is None:
        return
    for index, (title, dialog_title, description) in COMPLEX_POPUPS.items():
        if index < stack.count():
            _popup_complex_page(stack.widget(index), title, dialog_title, description)
    for index in (10, 11, 12, 13):
        if index >= stack.count():
            continue
        page = stack.widget(index)
        title = page.windowTitle()
        if title in MASTER_POPUPS:
            _popup_master_page(page, title, MASTER_POPUPS[title])
        elif title in ("Kategori", "Satuan"):
            _inline_simple_master(page)
    _attach_reset_controls(window)
    window.setProperty("wposHybridForms", True)
