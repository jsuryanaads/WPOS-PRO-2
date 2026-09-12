from pathlib import Path


GLOBAL_UI = Path(__file__).resolve().parents[1] / "app" / "ui" / "global_ui.py"


def test_global_ui_does_not_enable_clear_buttons():
    source = GLOBAL_UI.read_text(encoding="utf-8")
    # The global UI must never enable the clear button. Explicitly disabling
    # it is intentional and is part of the shared input UX contract.
    assert "setClearButtonEnabled(True)" not in source
    assert "setClearButtonEnabled(False)" in source


def test_global_ui_keeps_input_geometry_normalization():
    source = GLOBAL_UI.read_text(encoding="utf-8")
    assert "QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit" in source
    assert "setMinimumHeight(max(widget.minimumHeight(), 32))" in source
