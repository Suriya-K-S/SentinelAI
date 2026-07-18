"""
SentinelAI
System Utility Functions
"""

import getpass
import os
import platform
import socket
import uuid

import psutil


# ---------------------------------------------------------
# System Information
# ---------------------------------------------------------

def username():
    """Return current logged-in username."""
    return getpass.getuser()


def computer_name():
    """Return computer hostname."""
    return socket.gethostname()


def operating_system():
    """Return operating system."""
    return platform.system()


def os_version():
    """Return OS version."""
    return platform.version()


def architecture():
    """Return CPU architecture."""
    return platform.machine()


def processor():
    """Return processor name."""
    return platform.processor()


# ---------------------------------------------------------
# Memory Information
# ---------------------------------------------------------

def total_ram():
    """Return total RAM in GB."""
    memory = psutil.virtual_memory()
    return round(memory.total / (1024 ** 3), 2)


def available_ram():
    """Return available RAM in GB."""
    memory = psutil.virtual_memory()
    return round(memory.available / (1024 ** 3), 2)


def ram_usage():
    """Return RAM usage percentage."""
    return psutil.virtual_memory().percent


# ---------------------------------------------------------
# CPU Information
# ---------------------------------------------------------

def cpu_usage():
    """Return CPU usage percentage."""
    return psutil.cpu_percent(interval=1)


def cpu_count():
    """Return logical CPU count."""
    return psutil.cpu_count(logical=True)


# ---------------------------------------------------------
# Disk Information
# ---------------------------------------------------------

def disk_usage(path="C:\\"):
    """Return disk usage percentage."""
    return psutil.disk_usage(path).percent


def free_disk(path="C:\\"):
    """Return free disk space in GB."""
    usage = psutil.disk_usage(path)
    return round(usage.free / (1024 ** 3), 2)


# ---------------------------------------------------------
# Network Information
# ---------------------------------------------------------

def ip_address():

    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "Unknown"


def mac_address():

    mac = uuid.getnode()

    return ":".join(
        ("%012X" % mac)[i:i + 2]
        for i in range(0, 12, 2)
    )


# ---------------------------------------------------------
# Battery
# ---------------------------------------------------------

def battery_info():

    battery = psutil.sensors_battery()

    if battery is None:
        return None

    return {
        "percent": battery.percent,
        "plugged": battery.power_plugged,
        "seconds_left": battery.secsleft
    }


# ---------------------------------------------------------

if __name__ == "__main__":

    print("User:", username())
    print("Computer:", computer_name())
    print("OS:", operating_system())
    print("Version:", os_version())
    print("Architecture:", architecture())
    print("Processor:", processor())
    print("CPU:", cpu_usage(), "%")
    print("RAM:", ram_usage(), "%")
    print("Disk:", disk_usage(), "%")
    print("IP:", ip_address())
    print("MAC:", mac_address())
    print("Battery:", battery_info())