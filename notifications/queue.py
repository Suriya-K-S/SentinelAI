"""
SentinelAI
Notification Queue
"""

import queue
import threading
import time

from notifications.ntfy import notifier


class NotificationQueue:

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
            target=self.process,
            daemon=True
        )

        self.worker.start()

        print("[QUEUE] Notification Queue Started")

    # -------------------------------------------------

    def stop(self):

        self.running = False

        if self.worker:

            self.worker.join(timeout=2)

        print("[QUEUE] Notification Queue Stopped")

    # -------------------------------------------------

    def send(
        self,
        title,
        message,
        priority="default",
        tags=None
    ):

        self.queue.put({

            "title": title,

            "message": message,

            "priority": priority,

            "tags": tags

        })

    # -------------------------------------------------

    def process(self):

        while self.running:

            try:

                if self.queue.empty():

                    time.sleep(0.5)

                    continue

                event = self.queue.get()

                notifier.send(

                    title=event["title"],

                    message=event["message"],

                    priority=event["priority"],

                    tags=event["tags"]

                )

                self.queue.task_done()

            except Exception as e:

                print("[QUEUE ERROR]", e)

                time.sleep(1)


# ---------------------------------------------------------

notification_queue = NotificationQueue()


# ---------------------------------------------------------

if __name__ == "__main__":

    notification_queue.start()

    notification_queue.send(

        title="SentinelAI",

        message="Queue Working Successfully",

        priority="default",

        tags=["white_check_mark"]

    )

    try:

        while True:

            time.sleep(1)

    except KeyboardInterrupt:

        notification_queue.stop()