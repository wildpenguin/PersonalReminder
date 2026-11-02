import asyncio
from reminder.services.notification import ScreenNotification
from reminder.services.database import Database
from reminder.repositories.reminders import ReminderRepository
import time

async def main():
    db = Database()
    reminderRepo = ReminderRepository(db)
    reminders = reminderRepo.get_reminders_to_show()
    notifier = ScreenNotification()

    for reminder in reminders:
        success = await notifier.notify(reminder.title, reminder.message, reminder.priority)
        if success:
            reminderRepo.log_success(reminder)
        time.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
