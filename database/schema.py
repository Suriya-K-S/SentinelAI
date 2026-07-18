"""
SentinelAI Database Schema
"""

DATABASE_VERSION = 1

CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    event_type TEXT NOT NULL,

    title TEXT NOT NULL,

    description TEXT,

    event_time TEXT NOT NULL,

    username TEXT,

    computer_name TEXT,

    status TEXT,

    extra_data TEXT

);
"""

CREATE_DEVICES_TABLE = """
CREATE TABLE IF NOT EXISTS devices (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    device_type TEXT,

    device_name TEXT,

    serial_number TEXT,

    vendor TEXT,

    product_id TEXT,

    first_seen TEXT,

    last_seen TEXT,

    trusted INTEGER DEFAULT 0

);
"""

CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS settings (

    key TEXT PRIMARY KEY,

    value TEXT

);
"""