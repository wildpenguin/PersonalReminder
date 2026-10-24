from desktop_notifier import DesktopNotifier, Urgency, Button, DEFAULT_SOUND

class ScreenNotification:
    def __init__(self):
        self.notifier = DesktopNotifier(app_name="Personal Reminder")

    async def notify(self, title: str, message: str, ):
        await self.notifier.send(
            title=title,
            message=message,
            urgency=Urgency.Normal,
            buttons=[
                Button(
                    title="Dismiss",
                    on_pressed=lambda: print("Dismissed")
                )
            ],
            sound=DEFAULT_SOUND
        )