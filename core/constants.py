"""
Global constants used throughout SentinelAI.
"""

from pathlib import Path

APP_NAME = "SentinelAI"

DATABASE_NAME = "sentinel.db"

LOG_FOLDER = "logs"
REPORT_FOLDER = "reports"
SCREENSHOT_FOLDER = "screenshots"
WEBCAM_FOLDER = "webcam"

DEFAULT_TIME_FORMAT = "%d-%m-%Y %I:%M:%S %p"

CONFIG_FILE = "config/config.json"

EVENT_LOGIN = "LOGIN"
EVENT_LOGOUT = "LOGOUT"
EVENT_LOCK = "LOCK"
EVENT_UNLOCK = "UNLOCK"
EVENT_USB = "USB"
EVENT_WIFI = "WIFI"
EVENT_SYSTEM = "SYSTEM"

ROOT = Path(__file__).resolve().parent.parent