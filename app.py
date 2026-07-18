"""
=====================================================
SentinelAI
Main Application
=====================================================
"""

import time
import traceback

from core.logger import log
from database.database import database
from monitors.monitor_manager import MonitorManager


class SentinelAI:

    def __init__(self):

        self.monitor_manager = MonitorManager()

        self.running = False

    # -------------------------------------------------

    def start(self):

        log.info("SentinelAI Starting...")

        print("=" * 60)
        print("        SentinelAI Security Monitor")
        print("=" * 60)

        self.running = True

        try:

            self.monitor_manager.start()

            print()
            print("SentinelAI Started Successfully")
            print("Press CTRL + C to Exit")
            print()

            while self.running:

                time.sleep(1)

        except KeyboardInterrupt:

            print()

            print("Stopping SentinelAI...")

            self.stop()

        except Exception as e:

            print()

            print("Application Error")

            print(e)

            traceback.print_exc()

            self.stop()

    # -------------------------------------------------

    def stop(self):

        self.running = False

        try:

            self.monitor_manager.stop()

        except Exception:

            pass

        try:

            database.connection.commit()

        except Exception:

            pass

        try:

            database.connection.close()

        except Exception:

            pass

        log.info("SentinelAI Stopped")

        print("Application Closed")


# =====================================================

def main():

    app = SentinelAI()

    app.start()


# =====================================================

if __name__ == "__main__":

    main()