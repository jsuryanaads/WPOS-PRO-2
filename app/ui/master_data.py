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
from ..models import Category, Unit, Supplier, Customer


class SimpleMaster(QWidget):
    """Consistent, read-only master-data page used by category/unit/supplier/customer."""

    def __init__(self, model, title, fields):
        super().__init__()
        self.model = model
        self.fields = fields
        self.setWindowTitle(title)

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
        form.setVerticalSpacing(10)
        self.inputs = []
        for field in fields:
            edit = QLineEdit()
            edit.setPlaceholderText(f"Masukkan {field.lower()}")
            edit.returnPressed.connect(self.save)
            self.inputs.append(edit)
            form.addRow(QLabel(field), edit)

        actions = QHBoxLayout()
        save_button = QPushButton("Simpan")
        save_button.setObjectName("primary")
        save_button.clicked.connect(self.save)
        clear_button = QPushButton("Bersihkan")
        clear_button.setObjectName("secondary")
        clear_button.clicked.connect(self.clear_form)
        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("secondary")
        refresh_button.clicked.connect(self.refresh)
        actions.addWidget(save_button)
        actions.addWidget(clear_button)
        actions.addWidget(refresh_button)
        actions.addStretch()
        form.addRow(actions)
        root.addWidget(form_box)

        table_card = QFrame()
        table_card.setObjectName("masterTableCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(12, 12, 12, 12)
        table_layout.setSpacing(8)
        table_title = QLabel("Data Tersimpan")
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
        table_layout.addWidget(self.table, 1)
        root.addWidget(table_card, 1)

        self._apply_local_style()
        self.refresh()

    @staticmethod
    def _subtitle(title):
        return {
            "Kategori": "Kelompokkan produk agar pencarian dan laporan lebih rapi.",
            "Satuan": "Kelola satuan barang yang digunakan pada produk.",
            "Supplier": "Kelola data pemasok untuk transaksi pembelian.",
            "Pelanggan": "Kelola data pelanggan untuk riwayat transaksi.",
        }.get(title, "Kelola data master WPOS PRO.")

    def _apply_local_style(self):
        self.setStyleSheet(self.styleSheet() + """
            QFrame#masterFormCard, QFrame#masterTableCard {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            QLabel#sectionTitle {
                color: #334155;
                font-size: 13px;
                font-weight: 800;
                padding: 2px 4px;
            }
            QPushButton#primary {
                background: #2563eb;
                color: #ffffff;
                border: 0;
                min-height: 38px;
                border-radius: 9px;
                padding: 7px 16px;
                font-weight: 800;
            }
            QPushButton#secondary {
                background: #f1f5f9;
                color: #334155;
                border: 1px solid #e2e8f0;
                min-height: 38px;
                border-radius: 9px;
                padding: 7px 14px;
                font-weight: 700;
            }
            QPushButton#secondary:hover { background: #e2e8f0; }
        """)

    def save(self):
        vals = [field.text().strip() for field in self.inputs]
        if not vals or not vals[0]:
            QMessageBox.warning(self, "Validasi", f"{self.fields[0]} wajib diisi.")
            self.inputs[0].setFocus()
            return
        try:
            with SessionLocal() as session:
                obj = self.model(**{field.lower(): value for field, value in zip(self.fields, vals)})
                session.add(obj)
                session.commit()
            self.clear_form()
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, "Gagal menyimpan", str(exc))

    def clear_form(self):
        for field in self.inputs:
            field.clear()
        if self.inputs:
            self.inputs[0].setFocus()

    def refresh(self):
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
