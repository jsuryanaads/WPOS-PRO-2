from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import DATABASE_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _migrate_users_name():
    """Add the optional user display name to existing SQLite databases."""
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return
    columns = {column["name"] for column in inspector.get_columns("users")}
    if "name" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR(150)"))


def _migrate_legacy_user_roles():
    """Normalize the removed legacy TEKNISI role to the supported KASIR role."""
    with engine.begin() as connection:
        connection.execute(text("UPDATE users SET role = 'KASIR' WHERE UPPER(role) = 'TEKNISI'"))


def init_db():
    from . import models
    Base.metadata.create_all(engine)
    _migrate_users_name()
    _migrate_legacy_user_roles()
    from .services.auth import ensure_default_admin
    with SessionLocal() as session:
        ensure_default_admin(session)
