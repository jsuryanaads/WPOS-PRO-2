from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from ..database import SessionLocal
from ..services.users import (
    ROLES, list_users, create_user, update_user, set_user_active,
    reset_password, delete_user,
)


class UserManagementDialog(QDialog):
    def __init__(self, actor, parent=None):
        super().__init__(parent)
        self.actor = actor
        self.selected_user_id = None
        self.setWindowTitle("WPOS PRO - Manajemen User")
        self.resize(900, 560)
        root = QVBoxLayout(self)

        form = QFormLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("Nama lengkap user")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username login")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password / password baru")
        self.password.setEchoMode(QLineEdit.Password)
        self.role = QComboBox()
        self.role.addItems(ROLES)
        self.active = QCheckBox("Aktif")
        self.active.setChecked(True)
        form.addRow("Nama", self.name)
        form.addRow("Username", self.username)
        form.addRow("Password", self.password)
        form.addRow("Role", self.role)
        form.addRow("Status", self.active)
        root.addLayout(form)

        buttons = QHBoxLayout()
        for text, slot in [
            ("Tambah User", self.add_user),
            ("Simpan Perubahan", self.save_user),
            ("Reset Password", self.do_reset_password),
            ("Aktif/Nonaktif", self.toggle_active),
            ("Hapus User", self.delete_selected),
            ("Reset Form", self.clear_form),
        ]:
            b = QPushButton(text)
            b.clicked.connect(slot)
            buttons.addWidget(b)
        root.addLayout(buttons)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Nama", "Username", "Role", "Status"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.cellClicked.connect(self.select_user)
        root.addWidget(self.table)
        self.refresh()

    def refresh(self):
        with SessionLocal() as s:
            rows = list_users(s)
            data = [
                (u.id, u.name or u.username, u.username, u.role, "AKTIF" if u.active else "NONAKTIF")
                for u in rows
            ]
        self.table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if c == 0:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(r, c, item)
        self.table.resizeColumnsToContents()
        if self.table.columnCount() >= 5:
            self.table.setColumnWidth(1, max(160, self.table.columnWidth(1)))
            self.table.setColumnWidth(2, max(130, self.table.columnWidth(2)))
            self.table.setColumnWidth(4, max(90, self.table.columnWidth(4)))

    def select_user(self, row, _column):
        self.selected_user_id = int(self.table.item(row, 0).text())
        self.name.setText(self.table.item(row, 1).text())
        self.username.setText(self.table.item(row, 2).text())
        self.username.setEnabled(False)
        self.role.setCurrentText(self.table.item(row, 3).text())
        self.active.setChecked(self.table.item(row, 4).text() == "AKTIF")
        self.password.clear()

    def add_user(self):
        try:
            with SessionLocal() as s:
                create_user(
                    s,
                    self.username.text(),
                    self.password.text(),
                    self.role.currentText(),
                    self.name.text(),
                )
            self.clear_form()
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def save_user(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "User", "Pilih user terlebih dahulu")
            return
        try:
            with SessionLocal() as s:
                update_user(
                    s,
                    self.selected_user_id,
                    self.name.text(),
                    self.role.currentText(),
                    self.active.isChecked(),
                    self.actor.id,
                )
            self.clear_form()
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def do_reset_password(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "User", "Pilih user terlebih dahulu")
            return
        try:
            with SessionLocal() as s:
                reset_password(s, self.selected_user_id, self.password.text())
            self.password.clear()
            QMessageBox.information(self, "User", "Password berhasil direset.")
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def toggle_active(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "User", "Pilih user terlebih dahulu")
            return
        target_active = not self.active.isChecked()
        try:
            with SessionLocal() as s:
                set_user_active(s, self.selected_user_id, target_active, self.actor.id)
            self.active.setChecked(target_active)
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def delete_selected(self):
        if not self.selected_user_id:
            QMessageBox.warning(self, "User", "Pilih user yang akan dihapus terlebih dahulu")
            return
        username = self.username.text().strip()
        answer = QMessageBox.question(
            self,
            "Hapus User",
            f"Hapus user '{username}' secara permanen?\n\nData akun tidak dapat dikembalikan.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        try:
            with SessionLocal() as s:
                delete_user(s, self.selected_user_id, self.actor.id)
            self.clear_form()
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def clear_form(self):
        self.selected_user_id = None
        self.name.clear()
        self.username.clear()
        self.username.setEnabled(True)
        self.password.clear()
        self.role.setCurrentText("KASIR")
        self.active.setChecked(True)
