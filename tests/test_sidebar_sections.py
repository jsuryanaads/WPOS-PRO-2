from pathlib import Path


def test_sidebar_keeps_four_sections_and_text_only_navigation():
    source = Path("app/ui/modern_main_window.py").read_text(encoding="utf-8")

    for section in ("OPERASIONAL", "KEUANGAN", "DATA MASTER", "SYSTEM"):
        assert f'("{section}"' in source

    assert 'header_widget.setObjectName("modernNavSection")' in source
    assert 'header_widget.setProperty("section", section)' in source
    assert 'item = QListWidgetItem(title)' in source
    assert 'item.setData(Qt.UserRole, index)' in source


def test_sidebar_section_palette_is_theme_aware():
    source = Path("app/ui/theme_shell.py").read_text(encoding="utf-8")

    assert 'QLabel#modernNavSection' in source
    assert '[section="KEUANGAN"]' in source
    assert '[section="DATA MASTER"]' in source
    assert '[section="SYSTEM"]' in source
    assert 'background:{p[\'shell_alt\']}' in source
    assert 'background:{p[\'surface_alt\']}' in source
