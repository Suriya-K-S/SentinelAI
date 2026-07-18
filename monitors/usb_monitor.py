"""
USB Monitor
"""

import wmi

from engines.event_manager import event_manager


class USBMonitor:

    def start(self):

        c = wmi.WMI()

        print("\n[USB] Scanning connected USB devices...\n")

        for device in c.Win32_USBHub():

            device_name = device.Name or "Unknown USB Device"

            print(f"[USB] {device_name}")

            event_manager.record(
                event_type="USB",
                title="USB Device Detected",
                description=device_name,
                status="CONNECTED",
                extra_data={
                    "device_id": device.DeviceID
                },
            )

    def stop(self):
        pass