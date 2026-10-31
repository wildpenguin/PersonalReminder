from contextlib import asynccontextmanager

from fastapi import FastAPI

from reminder.models.schema import Reminder, ReminderCreate
from reminder.repositories.reminders import ReminderRepository
from reminder.services.database import Database

db = Database()
repo = ReminderRepository(db)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.run_migrations()
    yield
    db.close()

app = FastAPI(lifespan=lifespan)

@app.get("/reminders")
async def list_reminders() -> list[Reminder]:
    return repo.get_reminders()

@app.post("/reminders", status_code=201)
async def create(reminder: ReminderCreate) -> Reminder:
    return repo.add_reminder(reminder)
