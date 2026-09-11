from pathlib import Path
from datetime import datetime
import os
import sqlite3
from ..config import DATA_DIR, BACKUP_DIR


def _database_path():
    return DATA_DIR / "wpos.db"


def backup_database():
    source = _database_path()
    if not source.exists():
        raise FileNotFoundError("Database belum ada")
    destination = BACKUP_DIR / f"wpos_{datetime.now():%Y%m%d_%H%M%S_%f}.db"
    with sqlite3.connect(source) as src, sqlite3.connect(destination) as dst:
        src.backup(dst)
    return destination


def restore_database(path):
    source = Path(path)
    destination = _database_path()
    if not source.exists():
        raise FileNotFoundError("Backup tidak ditemukan")
    if source.resolve() == destination.resolve():
        raise ValueError("File backup sama dengan database aktif")
    temp = destination.with_suffix(".restore.tmp")
    try:
        with sqlite3.connect(source) as src, sqlite3.connect(temp) as dst:
            src.backup(dst)
        os.replace(temp, destination)
        for suffix in ("-wal", "-shm"):
            sidecar = Path(str(destination) + suffix)
            if sidecar.exists():
                sidecar.unlink()
    finally:
        if temp.exists():
            temp.unlink()
