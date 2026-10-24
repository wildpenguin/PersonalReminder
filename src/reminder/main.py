import asyncio
from reminder.services.notification import ScreenNotification


async def main():
    notif = ScreenNotification()
    await notif.notify("Almost time!", "Prepare to leave for school")

if __name__ == "__main__":
    asyncio.run(main())