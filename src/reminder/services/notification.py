import asyncio
from desktop_notifier import DesktopNotifier, Urgency, Button, DEFAULT_SOUND

URGENCY = {"low": Urgency.Low, "normal": Urgency.Normal, "high": Urgency.Critical}

class ScreenNotification:
    def __init__(self):
        self.notifier = DesktopNotifier(app_name="Personal Reminder")

    async def notify(self, title: str, message: str, priority: str) -> bool:

        identifier = await self.notifier.send(
            title=title,
            message=message,
            urgency= URGENCY[priority],
            buttons=[
                Button(
                    title="Dismiss",
                    on_pressed=lambda: print("Dismissed")
                )
            ],
            sound=DEFAULT_SOUND
        )
        for _ in range(10):
            if identifier in await self.notifier.get_current_notifications():
                return True
            await asyncio.sleep(0.1)
        return False