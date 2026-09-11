from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..database import SessionLocal
from ..models import Category, Unit, Supplier, Customer, Product, Purchase


class SimpleMaster(QWidget):
    """Unified CRUD master-data page for category/unit/supplier/customer."""

    def __init__(self, model, title, fields):
        super().__init__()
        self.model = model
        self.fields = fields
        self.setWindowTitle(title)
        self.setProperty("wposMasterPage", True)
        self.selected_id = None

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 18)
        root.setSpacing(12)

        header = QFrame()
        header.setObjectName("masterHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 4)
        title_label = QLabel(title)
        title_label.setObjectName("pageTitle")
        subtitle = QLabel(self._subtitle(title))
        subtitle.setObjectName("pageSubtitle")
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle)
        root.addWidget(header)

        form_box = QFrame()
        form_box.setObjectName("masterFormCard")
        form = QFormLayout(form_box)
        form.setContentsMargins(16, 14, 16, 14)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(8)
        form.setRowWrapPolicy(QFormLayout.DontWrapRows)
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.inputs = []
        for field in fields:
            edit = QLineEdit()
            edit.setPlaceholderText(f"Masukkan {field.lower()}")
            edit.returnPressed.connect(self.save)
            self.inputs.append(edit)
            form.addRow(QLabel(field), edit)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        self.save_button = QPushButton("Simpan Baru")
        self.save_button.setObjectName("primary")
        self.save_button.clicked.connect(self.save)
        self.edit_button = QPushButton("Edit Terpilih")
        self.edit_button.setObjectName("secondary")
        self.edit_button.clicked.connect(self.edit_selected)
        self.delete_button = QPushButton("Hapus Terpilih")
        self.delete_button.setObjectName("danger")
        self.delete_button.clicked.connect(self.delete_selected)
        clear_button = QPushButton("Bersihkan")
        clear_button.setObjectName("secondary")
        clear_button.clicked.connect(self.clear_form)
        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("secondary")
        refresh_button.clicked.connect(self.refresh)
        for button in (self.save_button, self.edit_button, self.delete_button, clear_button, refresh_button):
            actions.addWidget(button)
        actions.addStretch()
        form.addRow(actions)
        root.addWidget(form_box)

        table_card = QFrame()
        table_card.setObjectName("masterTableCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(12, 12, 12, 12)
        table_layout.setSpacing(8)
        table_title = QLabel("Data Tersimpan — klik baris untuk memilih")
        table_title.setObjectName("sectionTitle")
        table_layout.addWidget(table_title)

        self.table = QTableWidget(0, len(fields) + 1)
        self.table.setObjectName("masterTable")
        self.table.setHorizontalHeaderLabels(fields + ["ID"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSortingEnabled(False)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setFocusPolicy(Qt.StrongFocus)
        self.table.cellClicked.connect(self.select_row)
        table_layout.addWidget(self.table, 1)
        root.addWidget(table_card, 1)

        self._set_edit_mode(False)
        self.refresh()

    @staticmethod
    def _subtitle(title):
        return {
            "Kategori": "Kelompokkan produk agar pencarian dan laporan lebih rapi.",
            "Satuan": "Kelola satuan barang yang digunakan pada produk.",
            "Supplier": "Kelola data pemasok untuk transaksi pembelian.",
            "Pelanggan": "Kelola data pelanggan untuk riwayat transaksi.",
        }.get(title, "Kelola data master WPOS PRO.")

    def _set_edit_mode(self, editing):
        self.save_button.setText("Simpan Perubahan" if editing else "Simpan Baru")
        self.edit_button.setEnabled(bool(self.selected_id))
        self.delete_button.setEnabled(bool(self.selected_id))

    def select_row(self, row, _column=0):
        item = self.table.item(row, len(self.fields))
        if item is None:
            return
        try:
            self.selected_id = int(item.text())
        except ValueError:
            self.selected_id = None
            return
        for index, _field in enumerate(self.fields):
            cell = self.table.item(row, index)
            self.inputs[index].setText(cell.text() if cell else "")
        self._set_edit_mode(True)
        self.inputs[0].setFocus()

    def edit_selected(self):
        if not self.selected_id:
            QMessageBox.information(self, "Edit", "Pilih data yang ingin diedit dari tabel terlebih dahulu.")
            return
        self.inputs[0].setFocus()

    def save(self):
        vals = [field.text().strip() for field in self.inputs]
        if not vals or not vals[0]:
            QMessageBox.warning(self, "Validasi", f"{self.fields[0]} wajib diisi.")
            self.inputs[0].setFocus()
            return
        try:
            with SessionLocal() as session:
                obj = session.get(self.model, self.selected_id) if self.selected_id else None
                if obj is None:
                    obj = self.model(**{field.lower(): value for field, value in zip(self.fields, vals)})
                    session.add(obj)
                else:
                    for field, value in zip(self.fields, vals):
                        setattr(obj, field.lower(), value)
                session.commit()
            self.clear_form()
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, "Gagal menyimpan", str(exc))

    def _dependency_message(self, session, obj):
        if isinstance(obj, Category):
            count = session.query(Product).filter_by(category_id=obj.id).count()
            if count:
                return f"Kategori masih dipakai oleh {count} produk. Hapus ditolak agar histori produk tidak rusak."
        elif isinstance(obj, Unit):
            count = session.query(Product).filter_by(unit_id=obj.id).count()
            if count:
                return f"Satuan masih dipakai oleh {count} produk. Hapus ditolak agar histori produk tidak rusak."
        elif isinstance(obj, Supplier):
            count = session.query(Purchase).filter_by(supplier_id=obj.id).count()
            if count:
                return f"Supplier masih dipakai oleh {count} transaksi pembelian. Hapus ditolak agar histori transaksi tidak rusak."
        return None

    def delete_selected(self):
        if not self.selected_id:
            QMessageBox.information(self, "Hapus", "Pilih data yang ingin dihapus dari tabel terlebih dahulu.")
            return
        try:
            with SessionLocal() as session:
                obj = session.get(self.model, self.selected_id)
                if obj is None:
                    self.clear_form()
                    self.refresh()
                    return
                dependency = self._dependency_message(session, obj)
                if dependency:
                    QMessageBox.warning(self, "Tidak dapat dihapus", dependency)
                    return
                name = getattr(obj, "name", str(self.selected_id))
                answer = QMessageBox.question(
                    self,
                    "Konfirmasi Hapus",
                    f"Hapus {self.windowTitle()} '{name}'?\n\nTindakan ini tidak dapat dibatalkan.",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )
                if answer != QMessageBox.Yes:
                    return
                session.delete(obj)
                session.commit()
            self.clear_form()
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, "Gagal menghapus", str(exc))

    def clear_form(self):
        self.selected_id = None
        for field in self.inputs:
            field.clear()
        self._set_edit_mode(False)
        if self.inputs:
            self.inputs[0].setFocus()

    def refresh(self):
        self.selected_id = None
        self._set_edit_mode(False)
        with SessionLocal() as session:
            rows = session.query(self.model).order_by(self.model.id.desc()).all()
        self.table.setRowCount(len(rows))
        for row_index, obj in enumerate(rows):
            for col_index, field in enumerate(self.fields):
                self.table.setItem(
                    row_index,
                    col_index,
                    QTableWidgetItem(str(getattr(obj, field.lower(), ""))),
                )
            self.table.setItem(row_index, len(self.fields), QTableWidgetItem(str(obj.id)))
        self.table.resizeRowsToContents()


def category_page():
    return SimpleMaster(Category, "Kategori", ["Name"])


def unit_page():
    return SimpleMaster(Unit, "Satuan", ["Name"])


def supplier_page():
    return SimpleMaster(Supplier, "Supplier", ["Name", "Phone", "Address"])


def customer_page():
    return SimpleMaster(Customer, "Pelanggan", ["Name", "Phone", "Address"])
