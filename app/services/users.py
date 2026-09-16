from .auth import hash_password
from ..models import User

ROLES = ("ADMIN", "KASIR")


def list_users(session):
    return session.query(User).order_by(User.name, User.username).all()


def _validate_name(name):
    return str(name or "").strip()


def create_user(session, username, password, role="KASIR", name=""):
    username = str(username).strip()
    name = _validate_name(name)
    role = str(role).strip().upper()
    if not username or not password:
        raise ValueError("Username dan password wajib diisi")
    if not name:
        raise ValueError("Nama user wajib diisi")
    if role not in ROLES:
        raise ValueError("Role tidak valid")
    if session.query(User).filter_by(username=username).first():
        raise ValueError("Username sudah digunakan")
    user = User(username=username, name=name, password_hash=hash_password(password), role=role, active=True)
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise


def update_user(session, user_id, name, role, active, actor_user_id=None):
    user = session.get(User, int(user_id))
    if not user:
        raise ValueError("User tidak ditemukan")
    name = _validate_name(name)
    role = str(role).strip().upper()
    if not name:
        raise ValueError("Nama user wajib diisi")
    if role not in ROLES:
        raise ValueError("Role tidak valid")
    if actor_user_id is not None and user.id == int(actor_user_id):
        if not active:
            raise ValueError("Administrator tidak boleh menonaktifkan akun sendiri")
        if user.role == "ADMIN" and role != "ADMIN":
            raise ValueError("Role akun yang sedang digunakan tidak boleh diturunkan. Logout lalu gunakan akun Administrator lain untuk mengubah role ini.")
    if user.role == "ADMIN" and not active:
        active_admins = session.query(User).filter_by(role="ADMIN", active=True).count()
        if active_admins <= 1:
            raise ValueError("Minimal satu Administrator aktif harus tersedia")
    if user.role == "ADMIN" and role != "ADMIN":
        active_admins = session.query(User).filter_by(role="ADMIN", active=True).count()
        if user.active and active_admins <= 1:
            raise ValueError("Minimal satu Administrator aktif harus tersedia")
    user.name = name
    user.role = role
    user.active = bool(active)
    try:
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise


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
    try:
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise


def reset_password(session, user_id, new_password):
    if not new_password:
        raise ValueError("Password baru wajib diisi")
    user = session.get(User, int(user_id))
    if not user:
        raise ValueError("User tidak ditemukan")
    user.password_hash = hash_password(new_password)
    try:
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise


def delete_user(session, user_id, actor_user_id=None):
    user = session.get(User, int(user_id))
    if not user:
        raise ValueError("User tidak ditemukan")
    if actor_user_id is not None and user.id == int(actor_user_id):
        raise ValueError("Akun yang sedang digunakan tidak boleh dihapus")
    if user.role == "ADMIN" and user.active:
        active_admins = session.query(User).filter_by(role="ADMIN", active=True).count()
        if active_admins <= 1:
            raise ValueError("Administrator aktif terakhir tidak boleh dihapus")
    try:
        session.delete(user)
        session.commit()
    except Exception:
        session.rollback()
        raise
