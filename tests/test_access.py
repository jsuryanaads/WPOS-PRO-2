from app.services.access import can_access


def test_admin_has_full_access():
    assert can_access("ADMIN", "cashier")
    assert can_access("ADMIN", "users")
    assert can_access("ADMIN", "backup")


def test_pengelola_operational_access():
    assert can_access("PENGELOLA", "cashier")
    assert can_access("PENGELOLA", "purchase")
    assert can_access("PENGELOLA", "cash")
    assert not can_access("PENGELOLA", "users")


def test_teknisi_is_restricted():
    assert can_access("TEKNISI", "products")
    assert can_access("TEKNISI", "stock")
    assert can_access("TEKNISI", "reports")
    assert not can_access("TEKNISI", "cashier")
    assert not can_access("TEKNISI", "purchase")
    assert not can_access("TEKNISI", "backup")


def test_unknown_role_is_denied():
    assert not can_access("UNKNOWN", "dashboard")
