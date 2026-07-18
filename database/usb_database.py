import sqlite3
from pathlib import Path
from datetime import datetime


class USBDatabase:
    def __init__(self, db_path="database/sentinel.db"):
        self.db_path = Path(db_path)
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS trusted_usb(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE,
            device_name TEXT,
            vendor TEXT,
            first_added TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usb_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            device_name TEXT,
            action TEXT,
            timestamp TEXT
        )
        """)

        self.connection.commit()

    # -----------------------------
    # Trusted USB
    # -----------------------------

    def add_trusted_device(self, device_id, device_name, vendor="Unknown"):
        self.cursor.execute("""
        INSERT OR IGNORE INTO trusted_usb
        (device_id, device_name, vendor, first_added)
        VALUES (?,?,?,?)
        """, (
            device_id,
            device_name,
            vendor,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        self.connection.commit()

    def remove_trusted_device(self, device_id):
        self.cursor.execute(
            "DELETE FROM trusted_usb WHERE device_id=?",
            (device_id,)
        )
        self.connection.commit()

    def is_trusted(self, device_id):
        self.cursor.execute(
            "SELECT * FROM trusted_usb WHERE device_id=?",
            (device_id,)
        )
        return self.cursor.fetchone() is not None

    def get_trusted_devices(self):
        self.cursor.execute("""
        SELECT device_id,device_name,vendor,first_added
        FROM trusted_usb
        ORDER BY device_name
        """)
        return self.cursor.fetchall()

    # -----------------------------
    # History
    # -----------------------------

    def add_history(self, device_id, device_name, action):
        self.cursor.execute("""
        INSERT INTO usb_history
        (device_id,device_name,action,timestamp)
        VALUES (?,?,?,?)
        """, (
            device_id,
            device_name,
            action,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        self.connection.commit()

    def get_history(self, limit=100):
        self.cursor.execute("""
        SELECT *
        FROM usb_history
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        return self.cursor.fetchall()

    def clear_history(self):
        self.cursor.execute("DELETE FROM usb_history")
        self.connection.commit()

    def close(self):
        self.connection.close()


if __name__ == "__main__":

    db = USBDatabase()

    db.add_trusted_device(
        "USB\\VID_TEST123",
        "Pendrive",
        "SanDisk"
    )

    print("\nTrusted Devices\n")

    for device in db.get_trusted_devices():
        print(device)

    db.add_history(
        "USB\\VID_TEST123",
        "Pendrive",
        "Inserted"
    )

    print("\nHistory\n")

    for item in db.get_history():
        print(item)

    db.close()