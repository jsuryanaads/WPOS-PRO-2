ROLES = ("ADMIN", "PENGELOLA", "TEKNISI")

# UI permission policy. Keep business-service validation independent from the UI.
ROLE_PERMISSIONS = {
    "ADMIN": {"*"},
    "PENGELOLA": {
        "dashboard", "cashier", "products", "stock", "purchase", "cash",
        "reports", "settings", "printer", "backup", "category", "unit",
        "supplier", "customer",
    },
    "TEKNISI": {
        "dashboard", "products", "stock", "reports",
    },
}


def can_access(role, feature):
    role = str(role).upper().strip()
    feature = str(feature).lower().strip()
    permissions = ROLE_PERMISSIONS.get(role, set())
    return "*" in permissions or feature in permissions
