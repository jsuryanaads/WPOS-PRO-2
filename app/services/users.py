from .auth import hash_password
from ..models import User

ROLES = ("ADMIN", "PENGELOLA", "TEKNISI")


def list_users(session):
    return session.query(User).order_by(User.username).all()


def create_user(session, username, password, role="TEKNISI"):
    username = str(username).strip()
    role = str(role).strip().upper()
    if not username or not password:
        raise ValueError("Username dan password wajib diisi")
    if role not in ROLES:
        raise ValueError("Role tidak valid")
    if session.query(User).filter_by(username=username).first():
        raise ValueError("Username sudah digunakan")
    user = User(username=username, password_hash=hash_password(password), role=role, active=True)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def set_user_active(session, user_id, active, actor_user_id=None):
    user = session.get(User, int(user_id))
    if not user:
        raise ValueError("User tidak ditemukan")
    if actor_user_id is not None and user.id == int(actor_user_id) and not active:
        raise ValueError("Administrator tidak boleh menonaktifkan akun sendiri")
    if user.role == "ADMIN" and not active:
        active_admins = session.query(User).filter_by(role="ADMIN", active=True).count()
        if active_admins <= 1:
            raise ValueError("Minimal satu Administrator aktif harus tersedia")
    user.active = bool(active)
    session.commit()
    session.refresh(user)
    return user


def reset_password(session, user_id, new_password):
    if not new_password:
        raise ValueError("Password baru wajib diisi")
    user = session.get(User, int(user_id))
    if not user:
        raise ValueError("User tidak ditemukan")
    user.password_hash = hash_password(new_password)
    session.commit()
    session.refresh(user)
    return user
