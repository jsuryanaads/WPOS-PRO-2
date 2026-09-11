from PySide6.QtWidgets import QApplication, QFormLayout, QGroupBox, QHBoxLayout, QLineEdit, QPushButton, QStackedWidget, QTableWidget, QVBoxLayout, QWidget

from app.ui.form_layouts import apply_hybrid_form_layouts


def _app():
    return QApplication.instance() or QApplication([])


def _master_page(title, fields):
    page = QWidget()
    page.setWindowTitle(title)
    root = QVBoxLayout(page)
    root.addWidget(QWidget())
    box = QGroupBox()
    box.setObjectName("masterFormCard")
    form = QFormLayout(box)
    for field in fields:
        form.addRow(field, QLineEdit())
    actions = QHBoxLayout()
    for text in ("Simpan", "Bersihkan", "Refresh"):
        actions.addWidget(QPushButton(text))
    form.addRow(actions)
    root.addWidget(box)
    root.addWidget(QTableWidget())
    return page


def _complex_page(title):
    page = QWidget()
    root = QVBoxLayout(page)
    root.addWidget(QWidget())
    box = QGroupBox(title)
    form = QFormLayout(box)
    form.addRow("Name", QLineEdit())
    form.addRow("Second", QLineEdit())
    root.addWidget(box)
    actions = QHBoxLayout()
    for text in ("Tambah Produk", "Edit Terpilih", "Form Baru"):
        actions.addWidget(QPushButton(text))
    root.addLayout(actions)
    root.addWidget(QTableWidget())
    return page


def test_hybrid_layouts_use_popup_for_complex_forms_and_master_forms():
    app = _app()
    window = QWidget()
    stack = QStackedWidget(window)
    pages = [QWidget() for _ in range(14)]
    pages[2] = _complex_page("Produk")
    pages[4] = _complex_page("Pembelian")
    pages[10] = _master_page("Kategori", ["Name"])
    pages[11] = _master_page("Satuan", ["Name"])
    pages[12] = _master_page("Supplier", ["Name", "Phone", "Address"])
    pages[13] = _master_page("Pelanggan", ["Name", "Phone", "Address"])
    for page in pages:
        stack.addWidget(page)
    window.modern_stack = stack

    apply_hybrid_form_layouts(window)
    app.processEvents()

    assert pages[2]._wpos_form_layout_mode == "popup"
    assert pages[4]._wpos_form_layout_mode == "popup"
    assert pages[2]._wpos_form_popup.dialog.windowTitle() == "Form Produk"
    assert pages[4]._wpos_form_popup.dialog.windowTitle() == "Form Pembelian"
    assert pages[10]._wpos_form_layout_mode == "inline"
    assert pages[11]._wpos_form_layout_mode == "inline"
    assert pages[12]._wpos_form_layout_mode == "popup"
    assert pages[13]._wpos_form_layout_mode == "popup"
