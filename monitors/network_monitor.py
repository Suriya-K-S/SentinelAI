"""
SentinelAI
Network Monitor
"""

import threading
import time
import socket

from engines.event_manager import event_manager
from notifications.ntfy import notifier


class NetworkMonitor:

    def __init__(self, interval=5):

        self.interval = interval

        self.running = False
        self.thread = None

        self.connected = None
        self.ip_address = None

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

        print("[NETWORK] Monitor Started")

    # -------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread:

            self.thread.join(timeout=2)

        print("[NETWORK] Monitor Stopped")

    # -------------------------------------------------
    def is_connected(self):

        try:

            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=3
            )

            return True

        except OSError:

            return False

    # -------------------------------------------------

    def get_ip_address(self):

        try:

            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
            )

            s.connect(("8.8.8.8", 80))

            ip = s.getsockname()[0]

            s.close()

            return ip

        except Exception:

            return "Unknown"

    # -------------------------------------------------

    def log_event(
        self,
        level,
        title,
        description
    ):

        print(f"[{level}] {title}")

        try:

            event_manager.record(
                event_type="NETWORK",
                title=title,
                description=description,
                status=level
            )

        except Exception as e:

            print(
                "Network Event Error:",
                e
            )

    # -------------------------------------------------
    def is_connected(self):

        try:

            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=3
            )

            return True

        except OSError:

            return False

    # -------------------------------------------------

    def get_ip_address(self):

        try:

            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
            )

            s.connect(("8.8.8.8", 80))

            ip = s.getsockname()[0]

            s.close()

            return ip

        except Exception:

            return "Unknown"

    # -------------------------------------------------

    def log_event(
        self,
        level,
        title,
        description
    ):

        print(f"[{level}] {title}")

        try:

            event_manager.record(
                event_type="NETWORK",
                title=title,
                description=description,
                status=level
            )

        except Exception as e:

            print(
                "Network Event Error:",
                e
            )

    # -------------------------------------------------
    def monitor(self):

        self.connected = self.is_connected()
        self.ip_address = self.get_ip_address()

        while self.running:

            try:

                current_status = self.is_connected()
                current_ip = self.get_ip_address()

                # ---------------------------------------
                # Internet Connected
                # ---------------------------------------

                if current_status and not self.connected:

                    self.log_event(
                        "INFO",
                        "Internet Connected",
                        f"Internet connection restored.\nIP Address: {current_ip}"
                    )

                    notifier.send_event(
                        event_type="NETWORK",
                        title="Internet Connected",
                        description=f"Internet connection restored.\nIP Address: {current_ip}",
                        severity="INFO"
                    )

                # ---------------------------------------
                # Internet Disconnected
                # ---------------------------------------

                elif not current_status and self.connected:

                    self.log_event(
                        "WARNING",
                        "Internet Disconnected",
                        "Internet connection lost."
                    )

                    notifier.send_event(
                        event_type="NETWORK",
                        title="Internet Disconnected",
                        description="Internet connection lost.",
                        severity="WARNING"
                    )

                # ---------------------------------------
                # IP Address Changed
                # ---------------------------------------

                if (
                    current_status
                    and self.connected
                    and current_ip != self.ip_address
                ):

                    self.log_event(
                        "INFO",
                        "IP Address Changed",
                        f"{self.ip_address} → {current_ip}"
                    )

                    notifier.send_event(
                        event_type="NETWORK",
                        title="IP Address Changed",
                        description=f"{self.ip_address} → {current_ip}",
                        severity="INFO"
                    )

                self.connected = current_status
                self.ip_address = current_ip

            except Exception as e:

                print(f"[NETWORK ERROR] {e}")

            time.sleep(self.interval)

    # -------------------------------------------------
# -------------------------------------------------
# Standalone Testing
# -------------------------------------------------

if __name__ == "__main__":

    monitor = NetworkMonitor()

    monitor.start()

    print()
    print("Monitoring Network...")
    print("Connect or disconnect your Internet.")
    print("Press CTRL + C to stop.")

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        print()

        print("Stopping Network Monitor...")

        monitor.stop()

        print("Network Monitor Stopped.")