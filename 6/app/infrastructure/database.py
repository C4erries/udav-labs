import sqlite3
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "insurance.db"
SQL_DIR = ROOT_DIR / "sql"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        schema_sql = (SQL_DIR / "schema.sql").read_text(encoding="utf-8")
        connection.executescript(schema_sql)

        clients_count = connection.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
        if clients_count == 0:
            seed_sql = (SQL_DIR / "seed.sql").read_text(encoding="utf-8")
            connection.executescript(seed_sql)

