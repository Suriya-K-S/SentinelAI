"""
SentinelAI
NTFY Notification Service
"""
import platform
import getpass
import requests
from datetime import datetime


class NtfyNotifier:

    def __init__(
        self,
        server="https://ntfy.sh",
        topic="SentinelAI"
    ):
        self.computer = platform.node()
        self.username = getpass.getuser()
        self.server = server.rstrip("/")
        self.topic = topic

    # -------------------------------------------------

    @property
    def url(self):

        return f"{self.server}/{self.topic}"

    # -------------------------------------------------

    def send(
        self,
        title,
        message,
        priority="default",
        tags=None,
        actions=None
    ):

        headers = {

            "Title": title,

            "Priority": str(priority),

            "Markdown": "yes",

            "Timestamp": str(int(datetime.now().timestamp()))

        }

        if tags:

            if isinstance(tags, list):

                headers["Tags"] = ",".join(tags)

            else:

                headers["Tags"] = str(tags)

        if actions:

            headers["Actions"] = actions

        try:

            response = requests.post(

                self.url,

                data=message.encode("utf-8"),

                headers=headers,

                timeout=10

            )

            response.raise_for_status()

            print(f"[NTFY] Notification Sent : {title}")

            return True

        except Exception as e:

            print(f"[NTFY ERROR] {e}")

            return False

    # -------------------------------------------------

    def info(self, title, message):

        return self.send(

            title,

            message,

            priority="default",

            tags=["information"]

        )

    # -------------------------------------------------

    def warning(self, title, message):

        return self.send(

            title,

            message,

            priority="high",

            tags=["warning"]

        )

    # -------------------------------------------------

    def critical(self, title, message):

        return self.send(

            title,

            message,

            priority="urgent",

            tags=["rotating_light"]

        )

    # -------------------------------------------------

    def send_event(
        self,
        event_type,
        title,
        description,
        severity="INFO",
        device=None
    ):

        icons = {
            "INFO": "ℹ",
            "WARNING": "⚠",
            "ERROR": "❌",
            "CRITICAL": "🚨"
        }

        icon = icons.get(severity, "ℹ")

        message = (
            f"{icon} SentinelAI Alert\n\n"
            f"Event      : {event_type}\n"
            f"Title      : {title}\n"
            f"Severity   : {severity}\n"
            f"User       : {self.username}\n"
            f"Computer   : {self.computer}\n"
            f"Time       : {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n"
        )

        if device:

            message += f"Device     : {device}\n"

        message += f"\nDescription:\n{description}"

        priority = {
            "INFO": "default",
            "WARNING": "high",
            "ERROR": "urgent",
            "CRITICAL": "max"
        }.get(severity, "default")

        tags = {
            "INFO": ["information"],
            "WARNING": ["warning"],
            "ERROR": ["x"],
            "CRITICAL": ["rotating_light"]
        }.get(severity, ["information"])

        return self.send(
            title=f"{icon} {title}",
            message=message,
            priority=priority,
            tags=tags
        )
# ---------------------------------------------------------

notifier = NtfyNotifier()


# ---------------------------------------------------------

if __name__ == "__main__":

    notifier.info(

        "SentinelAI",

        "Notification Test Successful."

    )