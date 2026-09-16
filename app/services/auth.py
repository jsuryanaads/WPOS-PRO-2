import hashlib
import hmac
import os
from ..models import User

ITERATIONS = 210_000
DEFAULT_ADMIN_PASSWORD = "admin123"


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password tidak boleh kosong")
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations))
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def is_default_admin_password(user: User) -> bool:
    """Return True only for the legacy bootstrap admin credential."""
    return (
        str(user.username).lower() == "admin"
        and str(user.role).upper() == "ADMIN"
        and verify_password(DEFAULT_ADMIN_PASSWORD, user.password_hash)
    )


def change_password(session, user: User, new_password: str) -> None:
    """Replace a user's password using the application's password hashing policy."""
    if len(new_password) < 8:
        raise ValueError("Password minimal 8 karakter")
    user.password_hash = hash_password(new_password)
    session.commit()


def ensure_default_admin(session):
    admin = session.query(User).filter_by(username="admin").first()
    if not admin:
        session.add(
            User(
                username="admin",
                name="Administrator",
                password_hash=hash_password(DEFAULT_ADMIN_PASSWORD),
                role="ADMIN",
                active=True,
            )
        )
        session.commit()
    elif not admin.name:
        admin.name = "Administrator"
        session.commit()


def login(session, username: str, password: str):
    user = session.query(User).filter_by(username=username, active=True).first()
    return user if user and verify_password(password, user.password_hash) else None
