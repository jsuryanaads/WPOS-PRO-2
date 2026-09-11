from app.services.access import can_access


def test_admin_has_full_access():
    assert can_access("ADMIN", "cashier")
    assert can_access("ADMIN", "users")
    assert can_access("ADMIN", "backup")


def test_kasir_has_operational_access_only():
    assert can_access("KASIR", "dashboard")
    assert can_access("KASIR", "cashier")
    assert can_access("KASIR", "customer")
    assert not can_access("KASIR", "users")
    assert not can_access("KASIR", "backup")
    assert not can_access("KASIR", "settings")
    assert not can_access("KASIR", "purchase")


def test_removed_roles_are_denied():
    assert not can_access("PENGELOLA", "dashboard")
    assert not can_access("TEKNISI", "products")
    assert not can_access("PENGELOLA", "users")
    assert not can_access("TEKNISI", "cashier")


def test_unknown_role_is_denied():
    assert not can_access("UNKNOWN", "dashboard")
