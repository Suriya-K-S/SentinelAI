"""
Login Monitor
"""

import getpass
import platform
from datetime import datetime

from engines.event_manager import event_manager


class LoginMonitor:

    def start(self):

        username = getpass.getuser()
        computer_name = platform.node()

        event_manager.record(
            event_type="LOGIN",
            title="User Logged In",
            description=f"{username} logged into Windows",
            username=username,
            computer_name=computer_name,
            status="SUCCESS",
            extra_data={
                "login_time": datetime.now().isoformat()
            },
        )

        print(f"[OK] User Logged In: {username}")

    def stop(self):
        pass