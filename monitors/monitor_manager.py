"""
SentinelAI
Monitor Manager
"""

import time

from monitors.login_monitor import LoginMonitor
from monitors.windows_monitor import WindowsMonitor
from monitors.usb_monitor import USBMonitor
from monitors.usb_live_monitor import USBLiveMonitor
from monitors.network_monitor import NetworkMonitor
from monitors.power_monitor import PowerMonitor
from monitors.session_monitor import SessionMonitor
from monitors.eventlog_monitor import EventLogMonitor


class MonitorManager:

    def __init__(self):

        self.monitors = []

        self.running = False

    # ------------------------------------------------

    def initialize(self):

        self.monitors = [

            WindowsMonitor(),
            LoginMonitor(),
            USBMonitor(),
            USBLiveMonitor(),
            NetworkMonitor(),
            PowerMonitor(),
            SessionMonitor(),
            EventLogMonitor(),

        ]

    # ------------------------------------------------

    def start(self):

        if self.running:
            return

        self.initialize()

        print("=" * 60)
        print("Starting SentinelAI Monitors")
        print("=" * 60)

        self.running = True

        for monitor in self.monitors:

            try:
                monitor.start()

                print(f"[OK] {monitor.__class__.__name__}")

            except Exception as e:

                print(f"[FAILED] {monitor.__class__.__name__}")

                print(e)

        print()
        print("SentinelAI is now monitoring your system.")

    # ------------------------------------------------

    def stop(self):

        if not self.running:
            return

        self.running = False

        print()
        print("Stopping monitors...")

        for monitor in self.monitors:

            try:

                monitor.stop()

            except Exception:

                pass

        print("All monitors stopped.")

    # ------------------------------------------------

    def run(self):

        self.start()

        try:

            while self.running:

                time.sleep(1)

        except KeyboardInterrupt:

            self.stop()


if __name__ == "__main__":

    manager = MonitorManager()

    manager.run()