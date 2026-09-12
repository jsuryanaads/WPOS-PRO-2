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
    sidebar or legacy/compatibility navigation calls.
    """
    if not hasattr(window, "nav_list") or not hasattr(window, "_nav_items"):
        return

    role = getattr(window.user, "role", "")

    for index, item in window._nav_items.items():
        window.nav_list.setItemHidden(item, not can_access(role, PAGE_FEATURES.get(index, "")))

    # Hide section headings that have no visible child page.
    section_has_visible_page = {}
    for item in window.nav_list.findItems("", 0):
        section = item.data(256 + 1)  # Qt.UserRole + 1
        if section == "section":
            section_has_visible_page[item.data(256 + 2)] = False

    for index, item in window._nav_items.items():
        if can_access(role, PAGE_FEATURES.get(index, "")):
            for row in range(window.nav_list.count()):
                header = window.nav_list.item(row)
                if header.data(256 + 1) == "section":
                    entries = [
                        entry_index
                        for entry_index, nav_item in window._nav_items.items()
                        if nav_item.data(256 + 2) == header.data(256 + 2)
                    ]
                    if index in entries:
                        section_has_visible_page[header.data(256 + 2)] = True

    for row in range(window.nav_list.count()):
        header = window.nav_list.item(row)
        if header.data(256 + 1) == "section":
            window.nav_list.setItemHidden(
                header, not section_has_visible_page.get(header.data(256 + 2), False)
            )

    # Guard both modern navigation entry points. This is intentionally
    # installed on the instance so legacy callers cannot bypass the policy.
    original_select = window._select_navigation
    if not getattr(window, "_wpos_role_select_guard", False):
        def guarded_select(page_index):
            if not page_allowed(window.user, page_index):
                return False
            return original_select(page_index)

        window._select_navigation = guarded_select
        window._wpos_role_select_guard = True

    original_navigate = window._navigate
    if not getattr(window, "_wpos_role_navigate_guard", False):
        def guarded_navigate(current, previous):
            if current is None:
                return original_navigate(current, previous)
            index = current.data(256)
            if not isinstance(index, int) or not page_allowed(window.user, index):
                return False
            return original_navigate(current, previous)

        window._navigate = guarded_navigate
        window._wpos_role_navigate_guard = True
