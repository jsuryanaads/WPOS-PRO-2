from pathlib import Path


def test_global_ui_owns_clear_button_policy():
    global_ui = Path("app/ui/global_ui.py").read_text(encoding="utf-8")
    ux2026 = Path("app/ui/ux2026.py").read_text(encoding="utf-8")

    assert "setClearButtonEnabled(False)" in global_ui
    assert "setClearButtonEnabled(True)" not in global_ui
    assert "setClearButtonEnabled(True)" not in ux2026
    assert "Clear buttons are controlled exclusively by global_ui.py" in ux2026


def test_ui_layers_have_separated_responsibilities():
    global_ui = Path("app/ui/global_ui.py").read_text(encoding="utf-8")
    ux2026 = Path("app/ui/ux2026.py").read_text(encoding="utf-8")
    theme_shell = Path("app/ui/theme_shell.py").read_text(encoding="utf-8")

    assert "theme_shell" in global_ui
    assert "Geometry and colors belong to global_ui.py and theme_shell.py" in ux2026
    assert "THEME_PALETTES" in theme_shell


def test_ui_entrypoint_keeps_ui_application_order_centralized():
    main = Path("app/main.py").read_text(encoding="utf-8")

    assert "apply_ui_polish(window)" in main
    assert "apply_ux2026(window)" in main
    assert "apply_global_ui(app, window)" in main
    assert "apply_theme(app, current_theme())" in main
