from pathlib import Path
import pytest

from app.config import APP_NAME, APP_VERSION, ICON_PATH, LOGO_PATH
from app.models import User
from app.services.auth import hash_password
from app.services.users import create_user, delete_user

# existing tests preserved above


def test_user_creation_rejects_invalid_role():
    session = make_session()
    with pytest.raises(ValueError, match="Role tidak valid"):
        create_user(session, "badrole", "secret", "INVALID", "Bad Role")


def test_wpos_pro_2_identity_and_branding_assets():
    assert APP_NAME == "WPOS PRO 2"
    assert APP_VERSION == "2.11.0"
    assert LOGO_PATH.name == "wpos_logo.png"
    assert ICON_PATH.name == "wpos_icon.ico"
    assert LOGO_PATH.exists()
    assert ICON_PATH.exists()
