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
    """Atomically replace the active database, with Windows lock handling."""
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
    active_stash = destination.with_suffix(".restore.active")
    try:
        # Build and validate the replacement while no handle is open on temp.
        with closing(sqlite3.connect(source)) as src, closing(sqlite3.connect(temp)) as dst:
            src.backup(dst)
            integrity = dst.execute("PRAGMA integrity_check").fetchone()
            if not integrity or integrity[0] != "ok":
                raise ValueError("Backup gagal disalin dengan benar")

        # On Windows, replacing an existing file can fail with WinError 5
        # even when SQLite has no open handle. Stash the active file first,
        # then atomically move the prepared database into its final location.
        if destination.exists() and os.name == "nt":
            for attempt in range(10):
                try:
                    os.replace(destination, active_stash)
                    break
                except PermissionError:
                    if attempt == 9:
                        raise
                    time.sleep(min(0.1 * (2 ** attempt), 1.0))

        try:
            _replace_database(temp, destination)
        except Exception:
            # Restore the active database if the second move failed.
            if active_stash.exists() and not destination.exists():
                _replace_database(active_stash, destination)
            raise
        else:
            if active_stash.exists():
                active_stash.unlink()

        for suffix in ("-wal", "-shm"):
            sidecar = Path(str(destination) + suffix)
            if sidecar.exists():
                sidecar.unlink()
    finally:
        if temp.exists():
            temp.unlink()
        if active_stash.exists() and not destination.exists():
            _replace_database(active_stash, destination)

    return safety_backup
