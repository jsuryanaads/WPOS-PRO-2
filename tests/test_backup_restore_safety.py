import sqlite3

import pytest


REQUIRED_TABLES = (
    "users", "categories", "units", "products", "suppliers", "customers",
    "sales", "sale_items", "purchases", "purchase_items",
    "stock_movements", "cash_movements", "settings",
)


def _make_db(path):
    with sqlite3.connect(path) as db:
        for table in REQUIRED_TABLES:
            db.execute(f"CREATE TABLE {table} (id INTEGER PRIMARY KEY)")
        db.commit()


def test_restore_rejects_invalid_backup(tmp_path, monkeypatch):
    from app.services import backup

    active = tmp_path / "wpos.db"
    invalid = tmp_path / "invalid.db"
    active.write_bytes(b"active")
    invalid.write_bytes(b"not sqlite")
    monkeypatch.setattr(backup, "DATA_DIR", tmp_path)
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path / "backups")
    backup.BACKUP_DIR.mkdir()

    with pytest.raises(ValueError, match="SQLite"):
        backup.restore_database(invalid)

    assert active.read_bytes() == b"active"


def test_restore_creates_safety_backup(tmp_path, monkeypatch):
    from app.services import backup

    active = tmp_path / "wpos.db"
    source = tmp_path / "good.db"
    backup_dir = tmp_path / "backups"
    backup_dir.mkdir()
    _make_db(active)
    _make_db(source)
    monkeypatch.setattr(backup, "DATA_DIR", tmp_path)
    monkeypatch.setattr(backup, "BACKUP_DIR", backup_dir)

    safety = backup.restore_database(source)

    assert safety is not None
    assert safety.exists()
    with sqlite3.connect(active) as db:
        tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert set(REQUIRED_TABLES) == tables
    assert safety.parent == backup_dir


def test_restore_rejects_incompatible_sqlite(tmp_path, monkeypatch):
    from app.services import backup

    active = tmp_path / "wpos.db"
    source = tmp_path / "wrong.db"
    _make_db(active)
    with sqlite3.connect(source) as db:
        db.execute("CREATE TABLE unrelated (id INTEGER PRIMARY KEY)")
        db.commit()
    monkeypatch.setattr(backup, "DATA_DIR", tmp_path)
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path / "backups")
    backup.BACKUP_DIR.mkdir()

    with pytest.raises(ValueError, match="tidak ditemukan"):
        backup.restore_database(source)


def test_restore_rejects_backup_missing_master_table(tmp_path, monkeypatch):
    from app.services import backup

    active = tmp_path / "wpos.db"
    source = tmp_path / "missing-master.db"
    _make_db(active)
    _make_db(source)
    with sqlite3.connect(source) as db:
        db.execute("DROP TABLE customers")
        db.commit()
    monkeypatch.setattr(backup, "DATA_DIR", tmp_path)
    monkeypatch.setattr(backup, "BACKUP_DIR", tmp_path / "backups")
    backup.BACKUP_DIR.mkdir()

    with pytest.raises(ValueError, match="customers"):
        backup.restore_database(source)
