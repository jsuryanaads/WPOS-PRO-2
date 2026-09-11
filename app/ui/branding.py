from pathlib import Path
import sys


def resource_path(relative: str) -> Path:
    """Resolve a bundled application asset in source and PyInstaller builds."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return base / relative


LOGO_PATH = resource_path("assets/branding/wpos_logo.png")
