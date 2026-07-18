"""
SentinelAI
Event Engine
"""

import threading
import queue
import time

from engines.event_manager import event_manager


class EventEngine:

    def __init__(self):

        self.queue = queue.Queue()

        self.running = False

        self.worker = None

    # -------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.worker = threading.Thread(
            target=self.process_events,
            daemon=True
        )

        self.worker.start()

        print("[EVENT ENGINE] Started")

    # -------------------------------------------------

    def stop(self):

        self.running = False

        if self.worker:

            self.worker.join(timeout=2)

        print("[EVENT ENGINE] Stopped")

    # -------------------------------------------------

    def push(self, **event):

        """
        Add an event to the processing queue.

        Example:

        engine.push(
            event_type="USB",
            title="USB Connected",
            description="SanDisk USB"
        )
        """

        self.queue.put(event)

    # -------------------------------------------------

    def process_events(self):

        while self.running:

            try:

                if self.queue.empty():

                    time.sleep(0.2)

                    continue

                event = self.queue.get()

                event_manager.record(**event)

                self.queue.task_done()

            except Exception as e:

                print("[EVENT ENGINE ERROR]", e)

                time.sleep(1)


# ---------------------------------------------------------

event_engine = EventEngine()


# ---------------------------------------------------------

if __name__ == "__main__":

    event_engine.start()

    event_engine.push(
        event_type="SYSTEM",
        title="Engine Test",
        description="Event Engine Working",
        status="INFO"
    )

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        event_engine.stop()