"""
SentinelAI Configuration Manager
"""

import json
from pathlib import Path

from core.constants import CONFIG_FILE

DEFAULT_CONFIG = {
    "app_name": "SentinelAI",
    "version": "1.0.0",
    "ntfy_topic": "Suriya-Laptop",
    "offline_queue": True,
    "capture_webcam": True,
    "capture_screenshot": False,
    "usb_monitor": True,
    "wifi_monitor": True,
    "debug": False
}


class ConfigManager:

    def __init__(self):
        self.path = Path(CONFIG_FILE)

        if not self.path.exists():
            self.save(DEFAULT_CONFIG)

        self.data = self.load()

    def load(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def save(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)


config = ConfigManager()