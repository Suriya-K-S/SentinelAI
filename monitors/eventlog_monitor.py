"""
SentinelAI
Windows Event Log Monitor
"""

import threading
import time

import win32con
import win32evtlog

from engines.event_manager import event_manager


class EventLogMonitor:

    def __init__(self, interval=10):

        self.interval = interval

        self.running = False
        self.thread = None

        self.server = "localhost"
        self.log_type = "System"

        # Stores the newest processed record
        self.last_record = 0

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

        print("[EVENTLOG] Monitor Started")

    # -------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=2)

        print("[EVENTLOG] Monitor Stopped")

    # -------------------------------------------------

    def add_event(
        self,
        level,
        source,
        event_id,
        message
    ):

        print(
            f"[EVENTLOG] [{level}] "
            f"{source} | Event ID: {event_id}"
        )

        try:

            event_manager.record(
                event_type="EVENTLOG",
                title=level,
                description=message,
                status=level,
                extra_data={
                    "source": source,
                    "event_id": event_id
                }
            )

        except Exception as e:

            print("Event Manager Error:", e)

    # -------------------------------------------------

    def monitor(self):

        try:

            handle = win32evtlog.OpenEventLog(
                self.server,
                self.log_type
            )

        except Exception as e:

            print("Unable to open Windows Event Log:", e)
            return

        # ---------------------------------------------
        # Ignore all old events already present
        # ---------------------------------------------

        try:

            flags = (
                win32evtlog.EVENTLOG_BACKWARDS_READ
                | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            )

            events = win32evtlog.ReadEventLog(
                handle,
                flags,
                0
            )

            if events:
                self.last_record = events[0].RecordNumber

        except Exception:
            pass

        # ---------------------------------------------
        # Start monitoring only NEW events
        # ---------------------------------------------

        flags = (
            win32evtlog.EVENTLOG_FORWARDS_READ
            | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        )

        try:

            while self.running:

                try:

                    events = win32evtlog.ReadEventLog(
                        handle,
                        flags,
                        0
                    )

                    if not events:

                        time.sleep(self.interval)
                        continue

                    for event in events:

                        record = event.RecordNumber

                        if record <= self.last_record:
                            continue

                        self.last_record = record

                        event_id = event.EventID & 0xFFFF
                        source = event.SourceName

                        if event.EventType == win32con.EVENTLOG_ERROR_TYPE:

                            level = "ERROR"

                        elif event.EventType == win32con.EVENTLOG_WARNING_TYPE:

                            level = "WARNING"

                        else:
                            continue

                        message = (
                            f"{source} generated "
                            f"Event ID {event_id}"
                        )

                        self.add_event(
                            level,
                            source,
                            event_id,
                            message
                        )

                except Exception as e:

                    print("ReadEventLog Error:", e)

                time.sleep(self.interval)

        finally:

            try:

                win32evtlog.CloseEventLog(handle)

            except Exception:

                pass


# -------------------------------------------------

if __name__ == "__main__":

    monitor = EventLogMonitor()

    monitor.start()

    print()
    print("Monitoring Windows Event Logs...")
    print("Press CTRL + C to stop.")

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        print()

        print("Stopping Event Log Monitor...")

        monitor.stop()

        print("Stopped.")