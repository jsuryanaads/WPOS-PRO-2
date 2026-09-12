from PySide6.QtCore import Qt

from ..services.access import can_access


# Page index -> permission feature. Keep this mapping aligned with
# ModernMainWindow.NAVIGATION/PAGE_TITLES and the existing access policy.
PAGE_FEATURES = {
    0: "dashboard",
    1: "cashier",
    2: "products",
    3: "stock",
    4: "purchase",
    5: "cash",
    6: "reports",
    7: "settings",
    8: "printer",
    9: "backup",
    10: "category",
    11: "unit",
    12: "supplier",
    13: "customer",
}


def page_allowed(user, page_index):
    return can_access(getattr(user, "role", ""), PAGE_FEATURES.get(page_index, ""))


def apply_role_access(window):
    """Apply role-based navigation and runtime page guards.

    The existing access policy remains the single source of truth. This layer
    prevents a non-authorized role from reaching restricted pages through the
    sidebar or compatibility navigation calls.
    """
    if not hasattr(window, "nav_list") or not hasattr(window, "_nav_items"):
        return

    role = getattr(window.user, "role", "")
    section_visible = {}
    current_section = None

    for row in range(window.nav_list.count()):
        item = window.nav_list.item(row)
        item_type = item.data(Qt.UserRole + 1)
        if item_type == "section":
            current_section = item.data(Qt.UserRole + 2)
            section_visible[current_section] = False
            continue
        if item_type != "item":
            continue

        index = item.data(Qt.UserRole)
        allowed = isinstance(index, int) and can_access(role, PAGE_FEATURES.get(index, ""))
        window.nav_list.setItemHidden(item, not allowed)
        if allowed and current_section is not None:
            section_visible[current_section] = True

    current_section = None
    for row in range(window.nav_list.count()):
        item = window.nav_list.item(row)
        if item.data(Qt.UserRole + 1) != "section":
            continue
        current_section = item.data(Qt.UserRole + 2)
        window.nav_list.setItemHidden(item, not section_visible.get(current_section, False))

    # Guard compatibility/legacy programmatic navigation. Sidebar items are
    # hidden above, while this guard prevents direct setCurrentIndex bypasses.
    if not getattr(window, "_wpos_role_select_guard", False):
        original_select = window._select_navigation

        def guarded_select(page_index):
            if not page_allowed(window.user, page_index):
                return False
            return original_select(page_index)

        window._select_navigation = guarded_select
        window._wpos_role_select_guard = True
