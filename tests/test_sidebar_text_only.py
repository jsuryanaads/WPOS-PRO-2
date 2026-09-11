from pathlib import Path


def test_sidebar_navigation_renders_text_only():
    source = Path("app/ui/modern_main_window.py").read_text(encoding="utf-8")

    assert 'for _icon, title, index in entries:' in source
    assert 'item = QListWidgetItem(title)' in source
    assert 'QListWidgetItem(f"  {icon}   {title}")' not in source


def test_sidebar_keeps_navigation_indexes():
    source = Path("app/ui/modern_main_window.py").read_text(encoding="utf-8")

    assert 'item.setData(Qt.UserRole, index)' in source
    assert 'self._nav_indexes.append(index)' in source
