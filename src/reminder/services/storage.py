from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "db/reminders.db"

MIGRATIONS = [
    """ CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY,
        due TEXT NOT NULL,
        repeat INTEGER NOT NULL DEFAULT 0,
        data TEXT NOT NULL CHECK (json_valid(data)),
        enabled INTEGER NOT NULL DEFAULT 1
    );
    """,
    """ CREATE TABLE IF NOT EXISTS reminders_log (
        id INTEGER PRIMARY KEY,
        reminder_id INTEGER NOT NULL REFERENCES reminders(id) ON DELETE CASCADE,
        date TEXT NOT NULL 
    );
    """,
]

class Storage:
    def __init__(self, db_path: Path | str = DB_PATH):
        self.db = sqlite3.connect(db_path, autocommit=False)
        self.db.execute("PRAGMA foreign_keys = ON")

    def run_migrations(self) -> int:
        version = self.db.execute("PRAGMA user_version").fetchone()[0]
        pending = MIGRATIONS[version:]
        for number, sql in enumerate(pending, start=version + 1):
            with self.db:
                self.db.execute(sql)
                self.db.execute(f"PRAGMA user_version = {int(number)}")
        return len(pending)

    def close(self):
        self.db.close()

