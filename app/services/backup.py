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


def _replace_database(source, destination):
    """Replace the active database, tolerating short-lived Windows file locks."""
    attempts = 10 if os.name == "nt" else 1
    delay = 0.1
    last_error = None

    for attempt in range(attempts):
        try:
            os.replace(source, destination)
            return
        except PermissionError as exc:
            last_error = exc
            if attempt == attempts - 1:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 1.0)

    if last_error is not None:
        raise last_error


def restore_database(path):
    source = Path(path)
    destination = _database_path()
    if not source.exists():
        raise FileNotFoundError("Backup tidak ditemukan")
    if source.resolve() == destination.resolve():
        raise ValueError("File backup sama dengan database aktif")

    _validate_backup(source)

    # Always preserve the currently active database before replacing it.
    safety_backup = backup_database() if destination.exists() else None
    temp = destination.with_suffix(".restore.tmp")
    try:
        # sqlite3.Connection is a transaction context manager, not a close
        # context manager. Use closing() so Windows releases the temp file
        # handle before replacement.
        with closing(sqlite3.connect(source)) as src, closing(sqlite3.connect(temp)) as dst:
            src.backup(dst)
            integrity = dst.execute("PRAGMA integrity_check").fetchone()
            if not integrity or integrity[0] != "ok":
                raise ValueError("Backup gagal disalin dengan benar")

        # Both SQLite handles above are explicitly closed before replacement.
        # Windows can still report WinError 5/32 briefly while antivirus,
        # indexing, or another process releases a newly-created file handle.
        _replace_database(temp, destination)

        for suffix in ("-wal", "-shm"):
            sidecar = Path(str(destination) + suffix)
            if sidecar.exists():
                sidecar.unlink()
    except Exception:
        # Keep the original database untouched if replacement did not happen.
        # If replacement already happened, the safety backup remains available.
        raise
    finally:
        if temp.exists():
            temp.unlink()

    return safety_backup
