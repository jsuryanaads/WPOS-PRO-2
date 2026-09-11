from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QCheckBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from ..database import SessionLocal
from ..services.users import ROLES, list_users, create_user, set_user_active, reset_password


class UserManagementDialog(QDialog):
    def __init__(self, actor, parent=None):
        super().__init__(parent)
        self.actor = actor
        self.selected_user_id = None
        self.setWindowTitle("WPOS PRO - Manajemen User")
        self.resize(760, 520)
        root = QVBoxLayout(self)

        form = QFormLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password / password baru")
        self.password.setEchoMode(QLineEdit.Password)
        self.role = QComboBox()
        self.role.addItems(ROLES)
        self.active = QCheckBox("Aktif")
        self.active.setChecked(True)
        form.addRow("Username", self.username)
        form.addRow("Password", self.password)
        form.addRow("Role", self.role)
        form.addRow("Status", self.active)
        root.addLayout(form)

        buttons = QHBoxLayout()
        for text, slot in [
            ("Tambah User", self.add_user),
            ("Reset Password", self.do_reset_password),
            ("Aktif/Nonaktif", self.toggle_active),
            ("Bersihkan", self.clear_form),
        ]:
            b = QPushButton(text)
            b.clicked.connect(slot)
            buttons.addWidget(b)
        root.addLayout(buttons)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Status"])
        self.table.cellClicked.connect(self.select_user)
        root.addWidget(self.table)
        self.refresh()

    def refresh(self):
        with SessionLocal() as s:
            rows = list_users(s)
            data = [(u.id, u.username, u.role, "AKTIF" if u.active else "NONAKTIF") for u in rows]
        self.table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))

    def select_user(self, row, _column):
        self.selected_user_id = int(self.table.item(row, 0).text())
        self.username.setText(self.table.item(row, 1).text())
        self.role.setCurrentText(self.table.item(row, 2).text())
        self.active.setChecked(self.table.item(row, 3).text() == "AKTIF")
        self.password.clear()

    def add_user(self):
        try:
            with SessionLocal() as s:
                create_user(s, self.username.text(), self.password.text(), self.role.currentText())
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
        try:
            with SessionLocal() as s:
                set_user_active(s, self.selected_user_id, self.active.isChecked(), self.actor.id)
            self.refresh()
        except Exception as exc:
            QMessageBox.warning(self, "User", str(exc))

    def clear_form(self):
        self.selected_user_id = None
        self.username.clear()
        self.password.clear()
        self.role.setCurrentText("TEKNISI")
        self.active.setChecked(True)
