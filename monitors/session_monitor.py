"""
SentinelAI
Session Monitor

Monitors Windows user session state.
"""

import ctypes
import getpass
import platform
import threading
import time

from engines.event_manager import event_manager


class SessionMonitor:

    def __init__(self, interval=2):

        self.interval = interval

        self.running = False

        self.thread = None

        self.last_locked = None

    # -----------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.monitor,
            daemon=True
        )

        self.thread.start()

        print("[SESSION] Monitor Started")

    # -----------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        print("[SESSION] Monitor Stopped")

    # -----------------------------------------------------

    def workstation_locked(self):

        user32 = ctypes.windll.User32

        hDesktop = user32.OpenInputDesktop(
            0,
            False,
            0x0100
        )

        if hDesktop == 0:
            return True

        user32.CloseDesktop(hDesktop)

        return False

    # -----------------------------------------------------

    def add_event(self, level, message):

        print(f"[{level}] {message}")

        try:

            event_manager.record(
                event_type="SESSION",
                title=level,
                description=message,
                username=getpass.getuser(),
                computer_name=platform.node(),
                status=level
            )

        except Exception as e:

            print("Event Manager Error:", e)

    # -----------------------------------------------------

    def monitor(self):

        self.last_locked = self.workstation_locked()

        while self.running:

            try:

                locked = self.workstation_locked()

                if locked != self.last_locked:

                    if locked:

                        self.add_event(
                            "WARNING",
                            "Workstation Locked"
                        )

                    else:

                        self.add_event(
                            "INFO",
                            "Workstation Unlocked"
                        )

                    self.last_locked = locked

                time.sleep(self.interval)

            except Exception as e:

                print("Session Monitor Error:", e)

                time.sleep(self.interval)


# ---------------------------------------------------------

if __name__ == "__main__":

    monitor = SessionMonitor()

    monitor.start()

    print("Monitoring session... Press Ctrl+C to stop.")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        monitor.stop()