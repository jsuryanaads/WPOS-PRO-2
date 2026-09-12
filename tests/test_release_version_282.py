from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_release_version_is_consistent():
    config = (ROOT / "app" / "config.py").read_text(encoding="utf-8")
    installer = (ROOT / "installer.iss").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert re.search(r'APP_VERSION\s*=\s*["\']2\.8\.2["\']', config)
    assert '#define MyAppVersion "2.8.2"' in installer
    assert "Versi aplikasi: **2.8.2**" in readme
    assert "## Perubahan terbaru 2.8.2" in readme
    assert "## 2.8.2 — Headerbar Stabilization" in changelog
