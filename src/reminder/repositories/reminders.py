import json
from datetime import timezone
import sqlite3
import logging

from reminder.models.schema import Reminder, ReminderCreate
from reminder.services.database import Database

class ReminderRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_reminders(self) -> list[Reminder]:
        rows = self.db.execute(
            "SELECT id, due, data, repeat, enabled FROM reminders r WHERE r.enabled = 1"
        ).fetchall()
        return [self._to_model(row) for row in rows]
    
    def add_reminder(self, reminder: ReminderCreate) -> Reminder:
        data = json.dumps({
            "title": reminder.title, 
            "message": reminder.message, 
            "priority": reminder.priority
        })
        due = reminder.due.astimezone(timezone.utc).isoformat()
        try:
            cursor = self.db.execute("INSERT INTO reminders (due, repeat, data, enabled) VALUES (?, ?, ?, ?)", 
                (due, reminder.repeat, data, reminder.enabled))
            return Reminder(id=cursor.lastrowid, **reminder.model_dump())
        except sqlite3.Error as e:
            logging.exception("Unexpected database error %s", e)
            self.db.close()
            raise

    def _to_model(self, row) -> Reminder:
        return Reminder(
            id=row["id"],
            due=row["due"],
            repeat=row["repeat"],
            enabled=row["enabled"],
            **json.loads(row["data"]),
        )