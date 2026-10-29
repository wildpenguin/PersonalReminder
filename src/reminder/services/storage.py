from pathlib import Path
import sqlite3
import json

DB_PATH = Path(__file__).resolve().parent / "db/reminders.db"

class Storage:
    def __init__(self):
        self.db = sqlite3.connect(DB_PATH)

    def run_migrations(self):
        
