ROLES = ("ADMIN", "KASIR")

# UI permission policy. Keep business-service validation independent from the UI.
ROLE_PERMISSIONS = {
    "ADMIN": {"*"},
    "KASIR": {
        "dashboard", "cashier", "customer",
    },
}


def can_access(role, feature):
    role = str(role).upper().strip()
    feature = str(feature).lower().strip()
    permissions = ROLE_PERMISSIONS.get(role, set())
    return "*" in permissions or feature in permissions
