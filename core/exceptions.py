"""
Custom exceptions for SentinelAI.
"""


class SentinelError(Exception):
    """Base exception."""
    pass


class DatabaseError(SentinelError):
    """Database related errors."""
    pass


class ConfigurationError(SentinelError):
    """Configuration related errors."""
    pass


class NotificationError(SentinelError):
    """Notification related errors."""
    pass