from PySide6.QtWidgets import QDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout


COMPLEX_POPUPS = {
    2: ("Produk", "Form Produk", "Kelola data produk tanpa memenuhi halaman tabel."),
    4: ("Pembelian", "Form Pembelian", "Input pembelian melalui dialog agar tabel tetap mendapat ruang maksimal."),
}

MASTER_POPUPS = {
    "Supplier": "Form Supplier",
    "Pelanggan": "Form Pelanggan",
}


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
    for box in page.findChildren(QFrame):
        title_getter = getattr(box, "title", None)
        if callable(title_getter) and title_getter() == title:
            return box
    return None


def _popup_complex_page(page, title, dialog_title, description):
    if getattr(page, "_wpos_form_layout_mode", None) == "popup":
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
        page,
        form_box,
        dialog_title,
        description,
        buttons=buttons,
        width=760 if title == "Produk" else 680,
        height=560 if title == "Produk" else 440,
    )
    page._wpos_form_popup = controller

    trigger_text = "＋ Tambah / Edit Produk" if title == "Produk" else "＋ Pembelian Baru"
    trigger = QPushButton(trigger_text)
    trigger.setObjectName("formPopupTrigger")
    trigger.clicked.connect(controller.open)
    page.layout().insertWidget(1, trigger)
    page._wpos_form_layout_mode = "popup"


def _popup_master_page(page, title, dialog_title):
    if getattr(page, "_wpos_form_layout_mode", None) == "popup":
        return
    form_box = page.findChild(QFrame, "masterFormCard")
    if form_box is None:
        return

    _remove_widget_from_layout(page.layout(), form_box)
    controller = _PopupController(
        page,
        form_box,
        dialog_title,
        "Form lengkap dibuka sebagai popup agar tabel data tetap menjadi fokus utama.",
        buttons=[],
        width=620,
        height=390,
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


def apply_hybrid_form_layouts(window):
    """Apply the approved hybrid form UX without changing business logic."""
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

    window.setProperty("wposHybridForms", True)
