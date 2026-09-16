from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFrame, QSizePolicy
from ..config import APP_NAME
from ..database import SessionLocal
from ..services.auth import change_password, is_default_admin_password, login
from .branding import LOGO_PATH
from .global_ui import add_application_footer


class ChangePasswordDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Wajib Ganti Password")
        self.setFixedSize(430, 300)
        self.setModal(True)

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(10)

        title = QLabel("Keamanan Akun Administrator")
        title.setObjectName("loginTitle")
        root.addWidget(title)
        message = QLabel(
            "Password administrator masih menggunakan password awal yang diketahui umum.\n"
            "Buat password baru minimal 8 karakter untuk melanjutkan."
        )
        message.setWordWrap(True)
        root.addWidget(message)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password baru (minimal 8 karakter)")
        root.addWidget(self.password)

        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.Password)
        self.confirm.setPlaceholderText("Ulangi password baru")
        root.addWidget(self.confirm)

        buttons = QHBoxLayout()
        cancel = QPushButton("Keluar")
        cancel.clicked.connect(self.reject)
        save = QPushButton("Simpan Password")
        save.setDefault(True)
        save.clicked.connect(self.handle_save)
        buttons.addWidget(cancel)
        buttons.addWidget(save)
        root.addLayout(buttons)
        self.password.setFocus()

    def handle_save(self):
        password = self.password.text()
        confirmation = self.confirm.text()
        if len(password) < 8:
            QMessageBox.warning(self, "Password", "Password minimal 8 karakter.")
            return
        if password != confirmation:
            QMessageBox.warning(self, "Password", "Konfirmasi password tidak sama.")
            return
        try:
            with SessionLocal() as session:
                user = session.get(type(self.user), self.user.id)
                if user is None or not is_default_admin_password(user):
                    QMessageBox.critical(self, "Password", "Status akun berubah. Silakan login kembali.")
                    self.reject()
                    return
                change_password(session, user, password)
        except Exception as exc:
            QMessageBox.critical(self, "Password", f"Password gagal disimpan: {exc}")
            return
        QMessageBox.information(self, "Password", "Password administrator berhasil diperbarui.")
        self.accept()


class LoginWindow(QDialog):
    def __init__(self, on_success):
        super().__init__()
        self.on_success = on_success
        self.setWindowTitle(f"{APP_NAME} - Login")
        self.setFixedSize(430, 590)
        self.setModal(True)
        self.setObjectName("loginWindow")
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 24, 32, 22)
        root.setSpacing(0)
        root.addStretch(1)
        card = QFrame()
        card.setObjectName("loginCard")
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 24, 30, 24)
        card_layout.setSpacing(10)
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        logo.setMinimumHeight(82)
        logo.setObjectName("loginLogo")
        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH))
            if not pixmap.isNull():
                logo.setPixmap(pixmap.scaled(92, 92, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        card_layout.addWidget(logo)
        title = QLabel(APP_NAME)
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        subtitle = QLabel("Point of Sale")
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)
        welcome = QLabel("Silakan masuk untuk melanjutkan")
        welcome.setObjectName("loginWelcome")
        welcome.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(welcome)
        mode = QLabel("Offline  •  Database Lokal")
        mode.setObjectName("loginMode")
        mode.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(mode)
        card_layout.addSpacing(6)
        user_label = QLabel("USERNAME")
        user_label.setObjectName("loginFieldLabel")
        card_layout.addWidget(user_label)
        self.username = QLineEdit()
        self.username.setObjectName("loginInput")
        self.username.setPlaceholderText("👤  Masukkan username")
        self.username.setMinimumHeight(44)
        self.username.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.username)
        password_label = QLabel("PASSWORD")
        password_label.setObjectName("loginFieldLabel")
        card_layout.addWidget(password_label)
        password_row = QHBoxLayout()
        password_row.setSpacing(6)
        self.password = QLineEdit()
        self.password.setObjectName("loginInput")
        self.password.setPlaceholderText("🔒  Masukkan password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(44)
        self.password.returnPressed.connect(self.handle_login)
        password_row.addWidget(self.password, 1)
        self.show_password = QPushButton("Lihat")
        self.show_password.setObjectName("loginSecondaryButton")
        self.show_password.setCheckable(True)
        self.show_password.setMinimumHeight(44)
        self.show_password.setToolTip("Tampilkan / sembunyikan password")
        self.show_password.toggled.connect(self.toggle_password)
        password_row.addWidget(self.show_password)
        card_layout.addLayout(password_row)
        card_layout.addSpacing(8)
        self.login_button = QPushButton("MASUK")
        self.login_button.setObjectName("loginPrimaryButton")
        self.login_button.setMinimumHeight(46)
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_button)
        root.addWidget(card)
        root.addStretch(1)
        add_application_footer(self)
        self.username.setFocus()

    def toggle_password(self, visible):
        self.password.setEchoMode(QLineEdit.Normal if visible else QLineEdit.Password)
        self.show_password.setText("Sembunyikan" if visible else "Lihat")

    def handle_login(self):
        username = self.username.text().strip()
        password = self.password.text()
        if not username or not password:
            QMessageBox.warning(self, "Login", "Username dan password wajib diisi.")
            return
        self.login_button.setEnabled(False)
        try:
            with SessionLocal() as session:
                user = login(session, username, password)
                if user and is_default_admin_password(user):
                    change_dialog = ChangePasswordDialog(user, self)
                    if change_dialog.exec() != QDialog.Accepted:
                        return
                    user = login(session, username, password)
                    if user is None:
                        QMessageBox.warning(self, "Login", "Password awal sudah tidak berlaku. Silakan login kembali.")
                        self.password.clear()
                        self.password.setFocus()
                        return
            if user:
                self.on_success(user)
                self.close()
            else:
                QMessageBox.warning(self, "Login", "Username atau password salah")
                self.password.clear()
                self.password.setFocus()
        finally:
            self.login_button.setEnabled(True)
