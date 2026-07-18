"""
SentinelAI Event Manager
"""

from datetime import datetime
import json

from database.database import database
from core.logger import log


class EventManager:
    """
    Handles all system events.
    """

    def record(
        self,
        event_type: str,
        title: str,
        description: str = "",
        username: str = "",
        computer_name: str = "",
        status: str = "",
        extra_data=None,
    ):

        if extra_data is None:
            extra_data = {}

        event_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        database.cursor.execute(
            """
            INSERT INTO events
            (
                event_type,
                title,
                description,
                event_time,
                username,
                computer_name,
                status,
                extra_data
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_type,
                title,
                description,
                event_time,
                username,
                computer_name,
                status,
                json.dumps(extra_data),
            ),
        )

        database.connection.commit()

        log.info(f"[{event_type}] {title}")


event_manager = EventManager()