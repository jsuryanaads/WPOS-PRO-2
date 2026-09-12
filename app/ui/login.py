from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFrame, QSizePolicy
from ..config import APP_NAME
from ..database import SessionLocal
from ..services.auth import login
from .branding import LOGO_PATH
from .global_ui import add_application_footer


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
            if user:
                self.on_success(user)
                self.close()
            else:
                QMessageBox.warning(self, "Login", "Username atau password salah")
                self.password.clear()
                self.password.setFocus()
        finally:
            self.login_button.setEnabled(True)
