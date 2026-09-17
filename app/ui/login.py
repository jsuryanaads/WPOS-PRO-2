from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QRadialGradient
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QFrame, QSizePolicy
from ..config import APP_NAME
from ..database import SessionLocal
from ..services.auth import login
from ..services.auth import change_password, is_default_admin_password
from .branding import LOGO_PATH, resource_path
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
        message = QLabel("Password administrator masih menggunakan password awal yang diketahui umum.\nBuat password baru minimal 8 karakter untuk melanjutkan.")
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
        self.setModal(True)
        self.setObjectName("loginWindow")
        self.setWindowFlag(Qt.FramelessWindowHint, True)

        # Qt may emit resizeEvent during window-state changes. Initialize all
        # attributes used by the responsive handler before showing fullscreen.
        self._login_card = None
        self._login_logo = None
        self._login_logo_pixmap = QPixmap()
        self._card_layout = None

        self._login_background = resource_path("assets/branding/login_background.png")
        self._login_background_pixmap = QPixmap(str(self._login_background)) if self._login_background.exists() else QPixmap()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        topbar = QHBoxLayout()
        topbar.setContentsMargins(16, 12, 16, 0)
        topbar.addStretch(1)
        self.exit_button = QPushButton("×")
        self.exit_button.setObjectName("loginExitButton")
        self.exit_button.setFixedSize(44, 44)
        self.exit_button.setToolTip("Keluar dari WPOS PRO 2")
        self.exit_button.setStyleSheet("""
            QPushButton#loginExitButton {
                background: rgba(8, 24, 50, 180);
                color: #e6f3ff;
                border: 1px solid rgba(120, 190, 255, 150);
                border-radius: 12px;
                font-size: 28px;
                font-weight: 300;
                padding: 0;
            }
            QPushButton#loginExitButton:hover {
                background: rgba(35, 112, 185, 220);
                border: 1px solid rgba(170, 220, 255, 220);
            }
            QPushButton#loginExitButton:pressed {
                background: rgba(15, 70, 125, 230);
            }
        """)
        self.exit_button.clicked.connect(self.close)
        topbar.addWidget(self.exit_button)
        root.addLayout(topbar)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Glass surface: translucent enough to reveal the blue artwork while
        # retaining strong contrast for the interactive login controls.
        card.setStyleSheet("""
            QFrame#loginCard {
                background: rgba(18, 39, 70, 188);
                border: 1px solid rgba(135, 197, 255, 145);
                border-radius: 20px;
            }
        """)
        self._login_card = card
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 28, 32, 28)
        card_layout.setSpacing(9)
        self._card_layout = card_layout

        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        logo.setMinimumHeight(92)
        logo.setObjectName("loginLogo")
        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH))
            if not pixmap.isNull():
                self._login_logo_pixmap = pixmap
                logo.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self._login_logo = logo
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
        mode = QLabel("●  Offline  •  Database Lokal")
        mode.setObjectName("loginMode")
        mode.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(mode)
        card_layout.addSpacing(5)
        user_label = QLabel("USERNAME")
        user_label.setObjectName("loginFieldLabel")
        card_layout.addWidget(user_label)
        self.username = QLineEdit()
        self.username.setObjectName("loginInput")
        self.username.setPlaceholderText("👤  Masukkan username")
        self.username.setMinimumHeight(48)
        self.username.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.username)
        password_label = QLabel("PASSWORD")
        password_label.setObjectName("loginFieldLabel")
        card_layout.addWidget(password_label)
        password_row = QHBoxLayout()
        password_row.setSpacing(10)
        self.password = QLineEdit()
        self.password.setObjectName("loginInput")
        self.password.setPlaceholderText("🔒  Masukkan password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumHeight(48)
        self.password.returnPressed.connect(self.handle_login)
        password_row.addWidget(self.password, 1)
        self.show_password = QPushButton("Lihat")
        self.show_password.setObjectName("loginSecondaryButton")
        self.show_password.setCheckable(True)
        self.show_password.setMinimumHeight(48)
        self.show_password.setToolTip("Tampilkan / sembunyikan password")
        self.show_password.toggled.connect(self.toggle_password)
        password_row.addWidget(self.show_password)
        card_layout.addLayout(password_row)
        card_layout.addSpacing(7)
        self.login_button = QPushButton("MASUK")
        self.login_button.setObjectName("loginPrimaryButton")
        self.login_button.setMinimumHeight(50)
        self.login_button.setDefault(True)
        self.login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_button)

        center_row = QHBoxLayout()
        center_row.setContentsMargins(0, 0, 0, 0)
        center_row.addStretch(1)
        center_row.addWidget(card, 0, Qt.AlignVCenter)
        center_row.addStretch(1)
        root.addLayout(center_row, 1)
        add_application_footer(self)
        self._apply_responsive_layout()
        self.username.setFocus()

    def _apply_responsive_layout(self):
        card = getattr(self, "_login_card", None)
        card_layout = getattr(self, "_card_layout", None)
        logo = getattr(self, "_login_logo", None)
        logo_pixmap = getattr(self, "_login_logo_pixmap", QPixmap())
        if card is None or card_layout is None or logo is None:
            return

        width = max(1, self.width())
        height = max(1, self.height())
        scale = min(width / 1440.0, height / 900.0)
        card_width = int(max(380, min(520, width * 0.35)))
        card.setFixedWidth(card_width)
        horizontal = int(max(28, min(38, card_width * 0.07)))
        vertical = int(max(20, min(30, 28 * scale)))
        card_layout.setContentsMargins(horizontal, vertical, horizontal, vertical)
        card_layout.setSpacing(int(max(7, min(11, 9 * scale))))
        logo_size = int(max(70, min(100, 100 * scale)))
        logo.setMinimumHeight(logo_size)
        if not logo_pixmap.isNull():
            logo.setPixmap(logo_pixmap.scaled(
                logo_size, logo_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        control_height = int(max(44, min(50, 48 * scale)))
        self.username.setMinimumHeight(control_height)
        self.password.setMinimumHeight(control_height)
        self.show_password.setMinimumHeight(control_height)
        self.login_button.setMinimumHeight(int(max(46, min(52, 50 * scale))))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_responsive_layout()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        rect = self.rect()
        if not self._login_background_pixmap.isNull():
            scaled = self._login_background_pixmap.scaled(rect.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            x = (rect.width() - scaled.width()) // 2
            y = (rect.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            gradient = QLinearGradient(QPointF(0, 0), QPointF(rect.width(), rect.height()))
            gradient.setColorAt(0.0, QColor("#0b1220"))
            gradient.setColorAt(0.55, QColor("#111c2e"))
            gradient.setColorAt(1.0, QColor("#162a3d"))
            painter.fillRect(rect, gradient)
            glow = QRadialGradient(QPointF(rect.width() * 0.18, rect.height() * 0.18), max(rect.width(), rect.height()) * 0.55)
            glow.setColorAt(0.0, QColor(70, 150, 220, 55))
            glow.setColorAt(0.55, QColor(35, 100, 170, 20))
            glow.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.fillRect(rect, glow)
        super().paintEvent(event)

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
