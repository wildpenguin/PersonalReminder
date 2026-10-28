import os
import sys
import plistlib
import subprocess
from pathlib import Path

LABEL = "com.daily.reminder"
PLIST = Path.home() / "Library/LaunchAgents" / f"{LABEL}.plist"
SCRIPT = Path(__file__).resolve().parent / "src/reminder/reminder.py"

def install():
    if not SCRIPT:
        sys.exit(f"Not found: {SCRIPT}")

    config = {
        "Label": LABEL,
        "ProgramArguments": [sys.executable, str(SCRIPT)],
        "StartInterval": 300,
        "RunAtLoad": True,
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

if "--install" in sys.argv:
    install()
elif "--uninstall" in sys.argv:
    uninstall()