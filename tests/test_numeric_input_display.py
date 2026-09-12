from pathlib import Path


def test_numeric_display_is_compacted_without_value_scaling():
    source = Path("app/ui/ux2026.py").read_text(encoding="utf-8")
    assert "_normalize_numeric_inputs" in source
    assert "spin.setDecimals(0)" in source
    assert "spin.setSingleStep(1)" in source
    assert "prevent locale ambiguity" in source


def test_numeric_input_keeps_fractional_precision():
    source = Path("app/ui/main_window.py").read_text(encoding="utf-8")
    assert "self.qty.setDecimals(3)" in source
    assert "x.setDecimals(3)" in source
