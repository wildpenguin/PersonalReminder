import os
import sys
import plistlib
import subprocess
from pathlib import Path
from reminder.services.database import Database

LABEL = "com.daily.reminder"
PLIST = Path.home() / "Library/LaunchAgents" / f"{LABEL}.plist"

def install():
    if sys.prefix == sys.base_prefix:
        sys.exit("Run this from the project's venv: uv run python -m reminder.installer --install")

    config = {
        "Label": LABEL,
        "ProgramArguments": [sys.executable, "-m", "reminder.notifier"],
        "StartInterval": 300,
        "RunAtLoad": True,
        "StandardOutPath": str(Path.home() / "Library/Logs/reminder.out"),
        "StandardErrorPath": str(Path.home() / "Library/Logs/reminder.err"),
    }

    PLIST.parent.mkdir(parents=True, exist_ok=True)
    with PLIST.open("wb") as f:
        plistlib.dump(config, f)
    
    uid = os.getuid()
    subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(PLIST)])
    subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(PLIST)], check=True)

def uninstall():
    subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}", str(PLIST)])
    PLIST.unlink(missing_ok=True)

def migrate():
    migrations = Database().run_migrations()
    if migrations > 0:
        print (f"{migrations} migration(s) was executed sucessfuly.")
    else:
        print (f"No new migrations were executed.")


if "--install" in sys.argv:
    install()
elif "--uninstall" in sys.argv:
    uninstall()
elif "--migrate" in sys.argv:
    migrate()