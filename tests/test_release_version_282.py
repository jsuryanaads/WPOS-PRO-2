from pathlib import Path
import re

from app.config import APP_NAME, APP_VERSION


ROOT = Path(__file__).resolve().parents[1]


def test_release_version_is_consistent():
    installer = (ROOT / "installer.iss").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    escaped_version = re.escape(APP_VERSION)
    assert re.fullmatch(r"\d+\.\d+\.\d+", APP_VERSION)
    assert f'#define MyAppVersion "{APP_VERSION}"' in installer
    assert f"Nama aplikasi: **{APP_NAME}**" in readme
    assert f"Versi aplikasi: **{APP_VERSION}**" in readme
    assert f"## Perubahan terbaru {APP_VERSION}" in readme
    assert f"## {APP_VERSION} —" in changelog
    assert re.search(rf"APP_VERSION\s*=\s*[\"']{escaped_version}[\"']", (ROOT / "app" / "config.py").read_text(encoding="utf-8"))
