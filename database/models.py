"""
Database Models
"""

from dataclasses import dataclass


@dataclass
class Event:

    event_type: str

    title: str

    description: str

    event_time: str

    username: str = ""

    computer_name: str = ""

    status: str = ""

    extra_data: str = ""