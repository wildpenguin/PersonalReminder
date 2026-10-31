from pydantic import BaseModel, AwareDatetime
from typing import Literal

class ReminderCreate(BaseModel):
    due: AwareDatetime
    repeat: bool = False
    title: str
    message: str
    priority: Literal["low", "normal", "high"] = "normal"
    enabled: bool = True

class Reminder(ReminderCreate):
    id: int