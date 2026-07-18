"""
SentinelAI
Time Utility Functions
"""

from datetime import datetime, timedelta


# ---------------------------------------------------------
# Current Time
# ---------------------------------------------------------

def now():
    """Return current datetime."""
    return datetime.now()


def current_date():
    """Return current date."""
    return datetime.now().strftime("%Y-%m-%d")


def current_time():
    """Return current time."""
    return datetime.now().strftime("%H:%M:%S")


def timestamp():
    """Return current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------
# Formatting
# ---------------------------------------------------------

def format_datetime(dt, fmt="%Y-%m-%d %H:%M:%S"):
    """Format datetime object."""
    return dt.strftime(fmt)


def parse_datetime(value, fmt="%Y-%m-%d %H:%M:%S"):
    """Convert string to datetime."""
    return datetime.strptime(value, fmt)


# ---------------------------------------------------------
# Time Difference
# ---------------------------------------------------------

def seconds_between(start, end):
    """Return difference in seconds."""
    return int((end - start).total_seconds())


def minutes_between(start, end):
    """Return difference in minutes."""
    return round(
        (end - start).total_seconds() / 60,
        2
    )


def hours_between(start, end):
    """Return difference in hours."""
    return round(
        (end - start).total_seconds() / 3600,
        2
    )


# ---------------------------------------------------------
# Add Time
# ---------------------------------------------------------

def add_seconds(dt, seconds):
    return dt + timedelta(seconds=seconds)


def add_minutes(dt, minutes):
    return dt + timedelta(minutes=minutes)


def add_hours(dt, hours):
    return dt + timedelta(hours=hours)


def add_days(dt, days):
    return dt + timedelta(days=days)


# ---------------------------------------------------------
# Event Duration
# ---------------------------------------------------------

def elapsed(start_time):
    """
    Return elapsed seconds since start_time.
    """
    return seconds_between(
        start_time,
        datetime.now()
    )


# ---------------------------------------------------------
# Friendly Display
# ---------------------------------------------------------

def readable(dt=None):

    if dt is None:
        dt = datetime.now()

    return dt.strftime("%d-%m-%Y %I:%M:%S %p")


# ---------------------------------------------------------

if __name__ == "__main__":

    start = now()

    print("Current Date :", current_date())
    print("Current Time :", current_time())
    print("Timestamp    :", timestamp())

    later = add_minutes(start, 5)

    print("Later        :", readable(later))

    print(
        "Difference   :",
        minutes_between(start, later),
        "minutes"
    )