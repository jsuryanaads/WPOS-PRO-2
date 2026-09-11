from pathlib import Path


def test_global_ui_disables_clear_button_on_every_line_edit():
    source = Path("app/ui/global_ui.py").read_text(encoding="utf-8")

    assert "for widget in root.findChildren(QLineEdit):" in source
    assert "widget.setClearButtonEnabled(False)" in source
    assert 'widget.setProperty("wposClearButtonDisabled", True)' in source


def test_numeric_spinboxes_also_disable_internal_line_edit_clear_button():
    source = Path("app/ui/global_ui.py").read_text(encoding="utf-8")

    assert "line_edit = widget.lineEdit()" in source
    assert "line_edit.setClearButtonEnabled(False)" in source
