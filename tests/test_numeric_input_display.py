from pathlib import Path


def test_numeric_display_is_compacted_without_value_scaling():
    source = Path("app/ui/ux2026.py").read_text(encoding="utf-8")

    assert "_compact_numeric_display" in source
    assert "QTimer.singleShot(0, compact)" in source
    assert "text = f\"{value:.{decimals}f}\".rstrip(\"0\").rstrip(\".\")" in source
    assert "never multiplied or converted to thousands" in source


def test_numeric_input_keeps_fractional_precision():
    source = Path("app/ui/main_window.py").read_text(encoding="utf-8")

    # Existing quantity fields retain 3-decimal precision; only presentation
    # is compacted by ux2026.py.
    assert "self.qty.setDecimals(3)" in source
    assert "x.setDecimals(3)" in source
