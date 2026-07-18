"""
SentinelAI
USB Live Monitor

Monitors USB insertion/removal in real time.
"""

import time
import threading
import pythoncom
import wmi

from engines.event_manager import event_manager
from security.trusted_usb import TrustedUSBManager
from notifications.ntfy import notifier


class USBLiveMonitor:

    def __init__(self, interval=5):

        self.interval = interval

        self.running = False
        self.thread = None

        self.wmi_obj = None

        self.trusted_manager = TrustedUSBManager()

        self.connected_devices = {}

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

        print("[USB] Live Monitor Started")

    # -------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        self.trusted_manager.close()

        print("[USB] Live Monitor Stopped")

    # -------------------------------------------------

    def get_usb_devices(self):

        devices = {}

        try:

            # Create WMI object inside the monitoring thread
            wmi_obj = wmi.WMI()

            for usb in wmi_obj.Win32_USBHub():

                device_id = getattr(usb, "DeviceID", None)

                if not device_id:
                    continue

                devices[device_id] = {

                    "id": device_id,

                    "name": getattr(
                        usb,
                        "Name",
                        "Unknown USB Device"
                    ),

                    "manufacturer": getattr(
                        usb,
                        "Manufacturer",
                        "Unknown"
                    )

                }

        except Exception as e:

            print(f"[USB ERROR] {e}")

            return {}

        return devices

    # -------------------------------------------------

    def log_event(self, level, message):

        print(f"[{level}] {message}")

        try:

            event_manager.record(
                event_type="USB",
                title=level,
                description=message,
                status=level
            )

        except Exception as e:

            print("Event Manager Error:", e)

    # -------------------------------------------------

    def monitor(self):

        pythoncom.CoInitialize()

        try:

            self.connected_devices = self.get_usb_devices()

            while self.running:

                try:

                    current = self.get_usb_devices()

                    previous_ids = set(self.connected_devices.keys())
                    current_ids = set(current.keys())

                    inserted = current_ids - previous_ids
                    removed = previous_ids - current_ids

                    # ---------------------------------------
                    # USB Inserted
                    # ---------------------------------------

                    for device_id in inserted:

                        device = current[device_id]

                        result = self.trusted_manager.verify_device(
                            device["id"],
                            device["name"],
                            device["manufacturer"]
                        )

                        self.log_event(
                            result["level"],
                            result["message"]
                        )

                        severity = result["level"].upper()

                        if severity not in (
                            "INFO",
                            "WARNING",
                            "ERROR",
                            "CRITICAL"
                        ):
                            severity = "INFO"

                        notifier.send_event(
                            event_type="USB",
                            title="USB Device Inserted",
                            description=result["message"],
                            severity=severity,
                            device=device["name"]
                        )

                    # ---------------------------------------
                    # USB Removed
                    # ---------------------------------------

                    for device_id in removed:

                        device = self.connected_devices[device_id]

                        result = self.trusted_manager.device_removed(
                            device["id"],
                            device["name"]
                        )

                        self.log_event(
                            result["level"],
                            result["message"]
                        )

                        severity = result["level"].upper()

                        if severity not in (
                            "INFO",
                            "WARNING",
                            "ERROR",
                            "CRITICAL"
                        ):
                            severity = "INFO"

                        notifier.send_event(
                            event_type="USB",
                            title="USB Device Removed",
                            description=result["message"],
                            severity=severity,
                            device=device["name"]
                        )

                    self.connected_devices = current

                except Exception as e:

                    print(f"[USB MONITOR ERROR] {e}")

                time.sleep(self.interval)

        finally:

            pythoncom.CoUninitialize()

    # -------------------------------------------------
    # ------------------------------------------------------
# Standalone Testing
# ------------------------------------------------------

if __name__ == "__main__":

    monitor = USBLiveMonitor()

    monitor.start()

    print()
    print("Monitoring USB devices...")
    print("Insert or remove a USB device.")
    print("Press CTRL + C to stop.")

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        print()

        print("Stopping USB Live Monitor...")

        monitor.stop()

        print("USB Live Monitor Stopped.")