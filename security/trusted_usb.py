"""
SentinelAI
Trusted USB Manager
"""

from database.usb_database import USBDatabase


class TrustedUSBManager:
    """
    Manages trusted USB devices.
    """

    def __init__(self):
        self.db = USBDatabase()

    # --------------------------
    # Register Device
    # --------------------------

    def register_device(self, device_id, device_name, vendor="Unknown"):
        """
        Add a USB device to the trusted list.
        """
        self.db.add_trusted_device(
            device_id=device_id,
            device_name=device_name,
            vendor=vendor
        )

    # --------------------------
    # Remove Device
    # --------------------------

    def remove_device(self, device_id):
        self.db.remove_trusted_device(device_id)

    # --------------------------
    # Check Device
    # --------------------------

    def is_trusted(self, device_id):
        return self.db.is_trusted(device_id)

    # --------------------------
    # Handle Connection
    # --------------------------

    def verify_device(self, device_id, device_name, vendor="Unknown"):
        """
        Returns:
            trusted : bool
            level   : INFO / ALERT
            message : text
        """

        trusted = self.is_trusted(device_id)

        if trusted:

            self.db.add_history(
                device_id,
                device_name,
                "Trusted USB Connected"
            )

            return {
                "trusted": True,
                "level": "INFO",
                "message": f"Trusted USB Connected : {device_name}"
            }

        else:

            self.db.add_history(
                device_id,
                device_name,
                "Unknown USB Connected"
            )

            return {
                "trusted": False,
                "level": "ALERT",
                "message": f"UNKNOWN USB DETECTED : {device_name}"
            }

    # --------------------------
    # Device Removed
    # --------------------------

    def device_removed(self, device_id, device_name):

        self.db.add_history(
            device_id,
            device_name,
            "USB Removed"
        )

        return {
            "level": "INFO",
            "message": f"USB Removed : {device_name}"
        }

    # --------------------------
    # List Trusted
    # --------------------------

    def trusted_devices(self):
        return self.db.get_trusted_devices()

    # --------------------------
    # History
    # --------------------------

    def history(self):
        return self.db.get_history()

    # --------------------------
    # Close
    # --------------------------

    def close(self):
        self.db.close()


# --------------------------------------------------
# Testing
# --------------------------------------------------

if __name__ == "__main__":

    manager = TrustedUSBManager()

    manager.register_device(
        "USB\\VID_0781",
        "SanDisk Cruzer",
        "SanDisk"
    )

    print()

    print(manager.verify_device(
        "USB\\VID_0781",
        "SanDisk Cruzer"
    ))

    print()

    print(manager.verify_device(
        "USB\\VID_UNKNOWN",
        "Random Pendrive"
    ))

    print()

    print(manager.history())

    manager.close()