import json
from datetime import timezone, datetime
import sqlite3
import logging

from reminder.models.schema import Reminder, ReminderCreate, ReminderLog
from reminder.services.database import Database

class ReminderRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_reminders(self) -> list[Reminder]:
        rows = self.db.execute(
            "SELECT id, due, data, repeat, enabled " \
            "FROM reminders r WHERE r.enabled = 1"
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
    
    def get_reminders_to_show(self) -> list[Reminder]:
        rows = self.db.execute(
            """
            SELECT r.id, r.due, r.data, r.repeat, r.enabled FROM reminders r
            WHERE r.enabled = 1
            AND r.due <= :now
            AND (r.repeat = 0 OR time(r.due) <= time(:now))
            AND NOT EXISTS (
                SELECT 1 FROM reminders_log rl
                WHERE rl.reminder_id = r.id
                    AND (r.repeat = 0 OR date(rl.date) = date(:now))
            )
            """,
            {"now": datetime.now(timezone.utc).isoformat()},
        ).fetchall()
        return [self._to_model(row) for row in rows]


    def log_success(self, reminder: Reminder) -> ReminderLog:
        cursor = self.db.execute("INSERT INTO reminders_log (reminder_id, date) VALUES (?, ?)",
                (reminder.id, datetime.now(timezone.utc)))
        return ReminderLog(id=cursor.lastrowid, reminder_id=reminder.id, date=datetime.now(timezone.utc))

    def _to_model(self, row) -> Reminder:
        return Reminder(
            id=row["id"],
            due=row["due"],
            repeat=row["repeat"],
            enabled=row["enabled"],
            **json.loads(row["data"]),
        )