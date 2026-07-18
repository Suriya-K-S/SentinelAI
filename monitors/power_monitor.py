"""
SentinelAI
Power Monitor
"""

import threading
import time

import psutil

from engines.event_manager import event_manager


class PowerMonitor:

    def __init__(self, interval=10):

        self.interval = interval

        self.running = False

        self.thread = None

        self.last_percent = None
        self.last_plugged = None

    # -------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.monitor,
            daemon=True
        )

        self.thread.start()

        print("[POWER] Monitor Started")

    # -------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        print("[POWER] Monitor Stopped")

    # -------------------------------------------------

    def add_event(self, level, message):

        print(f"[{level}] {message}")

        try:

            event_manager.record(
                event_type="POWER",
                title=level,
                description=message,
                status=level
            )

        except Exception as e:

            print("Event Manager Error:", e)

    # -------------------------------------------------

    def monitor(self):

        while self.running:

            try:

                battery = psutil.sensors_battery()

                if battery is None:

                    time.sleep(self.interval)
                    continue

                percent = battery.percent
                plugged = battery.power_plugged

                # First Reading

                if self.last_percent is None:

                    self.last_percent = percent
                    self.last_plugged = plugged

                # Charger Connected

                if plugged != self.last_plugged:

                    if plugged:

                        self.add_event(
                            "INFO",
                            "Charger Connected"
                        )

                    else:

                        self.add_event(
                            "WARNING",
                            "Charger Disconnected"
                        )

                    self.last_plugged = plugged

                # Battery Low

                if percent <= 20 and self.last_percent > 20:

                    self.add_event(
                        "WARNING",
                        f"Battery Low ({percent}%)"
                    )

                # Battery Critical

                if percent <= 10 and self.last_percent > 10:

                    self.add_event(
                        "CRITICAL",
                        f"Battery Critical ({percent}%)"
                    )

                # Battery Full

                if percent == 100 and plugged:

                    self.add_event(
                        "INFO",
                        "Battery Fully Charged"
                    )

                self.last_percent = percent

                time.sleep(self.interval)

            except Exception as e:

                print("Power Monitor Error:", e)

                time.sleep(self.interval)


# ---------------------------------------------------------

if __name__ == "__main__":

    monitor = PowerMonitor()

    monitor.start()

    print("Monitoring Power... Press Ctrl+C to stop.")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        monitor.stop()