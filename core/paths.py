"""
Project path management.
"""

from pathlib import Path
import sys

# Supports both normal execution and interactive environments
if "__file__" in globals():
    ROOT = Path(__file__).resolve().parent.parent
else:
    ROOT = Path(sys.argv[0]).resolve().parent

LOGS = ROOT / "logs"
DATABASE = ROOT / "database"
REPORTS = ROOT / "reports"
SCREENSHOTS = ROOT / "screenshots"
WEBCAM = ROOT / "webcam"
CONFIG = ROOT / "config"

ALL_FOLDERS = [
    LOGS,
    DATABASE,
    REPORTS,
    SCREENSHOTS,
    WEBCAM,
    CONFIG,
]


def create_directories():
    """Create required directories if they don't exist."""
    for folder in ALL_FOLDERS:
        folder.mkdir(parents=True, exist_ok=True)