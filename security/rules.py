"""
SentinelAI
Security Rules
"""

from enum import Enum


class AlertLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ALERT = "ALERT"
    CRITICAL = "CRITICAL"


class EventType(Enum):

    USB_INSERT = "USB_INSERT"
    USB_REMOVE = "USB_REMOVE"

    UNKNOWN_USB = "UNKNOWN_USB"

    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"

    LOCK = "LOCK"
    UNLOCK = "UNLOCK"

    SHUTDOWN = "SHUTDOWN"
    RESTART = "RESTART"

    NETWORK_CONNECTED = "NETWORK_CONNECTED"
    NETWORK_DISCONNECTED = "NETWORK_DISCONNECTED"

    WIFI_CHANGED = "WIFI_CHANGED"

    INTERNET_LOST = "INTERNET_LOST"

    SCREENSHOT = "SCREENSHOT"


SECURITY_RULES = {

    EventType.UNKNOWN_USB:
    AlertLevel.ALERT,

    EventType.USB_INSERT:
    AlertLevel.INFO,

    EventType.USB_REMOVE:
    AlertLevel.INFO,

    EventType.LOGIN:
    AlertLevel.INFO,

    EventType.LOGOUT:
    AlertLevel.INFO,

    EventType.LOCK:
    AlertLevel.INFO,

    EventType.UNLOCK:
    AlertLevel.INFO,

    EventType.SHUTDOWN:
    AlertLevel.WARNING,

    EventType.RESTART:
    AlertLevel.WARNING,

    EventType.NETWORK_CONNECTED:
    AlertLevel.INFO,

    EventType.NETWORK_DISCONNECTED:
    AlertLevel.WARNING,

    EventType.WIFI_CHANGED:
    AlertLevel.WARNING,

    EventType.INTERNET_LOST:
    AlertLevel.WARNING
}