"""
Windows Monitor
"""

import getpass
import platform
from datetime import datetime

from engines.event_manager import event_manager


class WindowsMonitor:

    def start(self):

        event_manager.record(
            event_type="SYSTEM",
            title="Windows Monitor Started",
            description="Monitoring service initialized",
            username=getpass.getuser(),
            computer_name=platform.node(),
            status="RUNNING",
            extra_data={
                "started_at": datetime.now().isoformat()
            },
        )

        print("[OK] Windows Monitor Started")

    def stop(self):
        pass