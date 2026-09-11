from app.database import Base, SessionLocal, engine
from app.models import User
from app.services.users import create_user, set_user_active, reset_password
from app.services.auth import verify_password


def setup_function():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_create_user_hashes_password_and_role():
    with SessionLocal() as s:
        u = create_user(s, "kasir", "Rahasia123", "TEKNISI")
        assert u.role == "TEKNISI"
        assert u.password_hash != "Rahasia123"
        assert verify_password("Rahasia123", u.password_hash)


def test_last_admin_cannot_be_disabled():
    with SessionLocal() as s:
        admin = User(username="admin", password_hash="x", role="ADMIN", active=True)
        s.add(admin); s.commit()
        try:
            set_user_active(s, admin.id, False)
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert "Minimal satu Administrator" in str(exc)


def test_self_deactivation_is_blocked():
    with SessionLocal() as s:
        admin = User(username="admin", password_hash="x", role="ADMIN", active=True)
        other = User(username="other", password_hash="x", role="TEKNISI", active=True)
        s.add_all([admin, other]); s.commit()
        try:
            set_user_active(s, admin.id, False, actor_user_id=admin.id)
            assert False, "Expected ValueError"
        except ValueError as exc:
            assert "akun sendiri" in str(exc)


def test_reset_password_changes_hash():
    with SessionLocal() as s:
        u = create_user(s, "kasir", "lama", "TEKNISI")
        old_hash = u.password_hash
        reset_password(s, u.id, "baru")
        assert u.password_hash != old_hash
        assert verify_password("baru", u.password_hash)
        assert not verify_password("lama", u.password_hash)
