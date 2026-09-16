from pathlib import Path


def test_cashier_structure_module_is_presentation_only():
    source = Path("app/ui/cashier_structure.py").read_text(encoding="utf-8")
    assert "premiumCartCard" in source
    assert "premiumPayCard" in source
    assert "premiumTransactionControls" in source


def test_payment_label_contract_is_installed():
    source = Path("app/ui/cashier_structure.py").read_text(encoding="utf-8")
    assert "_install_payment_label_contract" in source
    assert "window.update_change = update_change_with_contract" in source
    assert 'removeprefix("TOTAL ")' in source
    assert 'removeprefix("Kembalian: ")' in source


def test_version_is_current_release():
    from app.config import APP_VERSION
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert f'APP_VERSION = "{APP_VERSION}"' in config
    assert f'#define MyAppVersion "{APP_VERSION}"' in installer
    assert f"Versi aplikasi: **{APP_VERSION}**" in readme
    assert f"## {APP_VERSION} —" in changelog
