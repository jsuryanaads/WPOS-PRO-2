from pathlib import Path
from datetime import datetime
from contextlib import closing
import os
import sqlite3
import time
from ..config import DATA_DIR, BACKUP_DIR

REQUIRED_TABLES = {
    "users",
    "products",
    "sales",
    "sale_items",
    "purchases",
    "purchase_items",
    "stock_movements",
    "cash_movements",
    "settings",
}


def _database_path():
    return DATA_DIR / "wpos.db"


def backup_database():
    source = _database_path()
    if not source.exists():
        raise FileNotFoundError("Database belum ada")
    destination = BACKUP_DIR / f"wpos_{datetime.now():%Y%m%d_%H%M%S_%f}.db"
    with closing(sqlite3.connect(source)) as src, closing(sqlite3.connect(destination)) as dst:
        src.backup(dst)
    return destination


def _validate_backup(source):
    """Validate SQLite integrity and the minimum WPOS schema before restore."""
    try:
        with closing(sqlite3.connect(source)) as connection:
            integrity = connection.execute("PRAGMA integrity_check").fetchone()
            if not integrity or integrity[0] != "ok":
                raise ValueError("Backup database rusak: integrity_check gagal")
            rows = connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            tables = {row[0] for row in rows}
    except sqlite3.DatabaseError as exc:
        raise ValueError("File backup bukan database SQLite yang valid") from exc

    missing = REQUIRED_TABLES - tables
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"Backup tidak kompatibel: tabel wajib tidak ditemukan ({names})")


def _restore_into_database(source, destination):
    """Restore directly into the existing SQLite file, avoiding Windows rename locks."""
    attempts = 10 if os.name == "nt" else 1
    delay = 0.1
    for attempt in range(attempts):
        try:
            with closing(sqlite3.connect(source)) as src, closing(sqlite3.connect(destination)) as dst:
                src.backup(dst)
                integrity = dst.execute("PRAGMA integrity_check").fetchone()
                if not integrity or integrity[0] != "ok":
                    raise ValueError("Backup gagal disalin dengan benar")
            return
        except (PermissionError, sqlite3.OperationalError):
            if attempt == attempts - 1:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 1.0)


def restore_database(path):
    source = Path(path)
    destination = _database_path()
    if not source.exists():
        raise FileNotFoundError("Backup tidak ditemukan")
    if source.resolve() == destination.resolve():
        raise ValueError("File backup sama dengan database aktif")

    _validate_backup(source)

    # Always preserve the currently active database before replacing/restoring it.
    safety_backup = backup_database() if destination.exists() else None
    temp = destination.with_suffix(".restore.tmp")
    try:
        if destination.exists():
            # Do not rename the active DB on Windows: another process may hold
            # a valid SQLite handle. SQLite Backup API can update the existing
            # database without requiring an OS-level rename/delete.
            _restore_into_database(source, destination)
        else:
            with closing(sqlite3.connect(source)) as src, closing(sqlite3.connect(temp)) as dst:
                src.backup(dst)
                integrity = dst.execute("PRAGMA integrity_check").fetchone()
                if not integrity or integrity[0] != "ok":
                    raise ValueError("Backup gagal disalin dengan benar")
            os.replace(temp, destination)

        for suffix in ("-wal", "-shm"):
            sidecar = Path(str(destination) + suffix)
            if sidecar.exists():
                sidecar.unlink()
    finally:
        if temp.exists():
            temp.unlink()

    return safety_backup
