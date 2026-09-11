import hashlib
import hmac
import os
from ..models import User

ITERATIONS = 210_000

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

def ensure_default_admin(session):
    if not session.query(User).filter_by(username="admin").first():
        session.add(User(username="admin", password_hash=hash_password("admin123"), role="ADMIN", active=True))
        session.commit()

def login(session, username: str, password: str):
    user = session.query(User).filter_by(username=username, active=True).first()
    return user if user and verify_password(password, user.password_hash) else None
