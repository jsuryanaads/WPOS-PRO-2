from ..models import Setting

DEFAULT_SETTINGS = {
    "store_name": "TOKO SEMBAKO",
    "store_address": "",
    "store_phone": "",
    "receipt_footer": "Terima kasih sudah berbelanja",
    "receipt_paper": "58mm",
    "printer_name": "",
}


def get_setting(session, key, default=""):
    row = session.query(Setting).filter_by(key=key).first()
    return row.value if row else default


def get_settings(session):
    wrapper = getattr(session, "session", None)
    actual = wrapper if wrapper is not None else session
    try:
        return {key: get_setting(actual, key, default) for key, default in DEFAULT_SETTINGS.items()}
    finally:
        if wrapper is not None and hasattr(session, "close"):
            session.close()


def set_setting(session, key, value):
    key = str(key).strip()
    if not key:
        raise ValueError("Key pengaturan wajib diisi")
    row = session.query(Setting).filter_by(key=key).first()
    if row:
        row.value = str(value)
    else:
        row = Setting(key=key, value=str(value))
        session.add(row)
    session.commit()
    session.refresh(row)
    return row


def save_settings(session, values):
    try:
        for key, value in values.items():
            key = str(key).strip()
            if not key:
                raise ValueError("Key pengaturan wajib diisi")
            row = session.query(Setting).filter_by(key=key).first()
            if row:
                row.value = str(value)
            else:
                session.add(Setting(key=key, value=str(value)))
        session.commit()
    except Exception:
        session.rollback()
        raise
