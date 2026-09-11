from pathlib import Path


def test_sidebar_keeps_four_sections_and_text_only_navigation():
    source = Path("app/ui/modern_main_window.py").read_text(encoding="utf-8")

    for section in ("OPERASIONAL", "KEUANGAN", "DATA MASTER", "SYSTEM"):
        assert f'("{section}"' in source

    assert 'header = QListWidgetItem(section)' in source
    assert 'header.setFlags(Qt.NoItemFlags)' in source
    assert 'header.setSizeHint(QSize(0, 25))' in source
    assert 'item = QListWidgetItem(title)' in source
    assert 'item.setData(Qt.UserRole, index)' in source
    assert 'item.setSizeHint(QSize(0, 30))' in source
    assert 'self._nav_items[index] = item' in source


def test_sidebar_has_compact_fixed_width_layout():
    source = Path("app/ui/modern_main_window.py").read_text(encoding="utf-8")
    assert 'sidebar.setFixedWidth(230)' in source
    assert 'self.nav_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)' in source
    assert 'self.nav_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)' in source


def test_sidebar_section_palette_is_theme_aware():
    source = Path("app/ui/theme_shell.py").read_text(encoding="utf-8")

    assert 'QListWidget#modernNav::item:disabled' in source
    assert 'color:{p[\'sidebar_inverse\']}' in source
    assert 'background:{p[\'shell_alt\']}' in source
    assert 'background:{p[\'selected\']}' in source
