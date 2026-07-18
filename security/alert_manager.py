"""
Central Alert Manager
"""

from datetime import datetime


class AlertManager:

    def __init__(self):

        self.alert_count = 0

        self.callbacks = []

    # -----------------------------------

    def register_callback(self, callback):

        self.callbacks.append(callback)

    # -----------------------------------

    def create_alert(self,
                     level,
                     title,
                     message):

        self.alert_count += 1

        alert = {

            "id": self.alert_count,

            "level": level,

            "title": title,

            "message": message,

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }

        print()

        print("=" * 60)

        print(f"[{level}] {title}")

        print(message)

        print(alert["time"])

        print("=" * 60)

        print()

        for callback in self.callbacks:

            try:

                callback(alert)

            except Exception:

                pass

        return alert

    # -----------------------------------

    def info(self, title, message):

        return self.create_alert(
            "INFO",
            title,
            message
        )

    # -----------------------------------

    def warning(self, title, message):

        return self.create_alert(
            "WARNING",
            title,
            message
        )

    # -----------------------------------

    def critical(self, title, message):

        return self.create_alert(
            "CRITICAL",
            title,
            message
        )

    # -----------------------------------

    def alert(self, title, message):

        return self.create_alert(
            "ALERT",
            title,
            message
        )