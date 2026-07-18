"""
SentinelAI
Helper Functions
"""

import hashlib
import json
import os
import socket
import uuid
from datetime import datetime


# ---------------------------------------------------------
# Time Helpers
# ---------------------------------------------------------

def current_time():
    """Return current timestamp."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def current_date():
    """Return current date."""

    return datetime.now().strftime("%Y-%m-%d")


# ---------------------------------------------------------
# File Helpers
# ---------------------------------------------------------

def ensure_directory(path):

    os.makedirs(path, exist_ok=True)

    return path


def file_exists(path):

    return os.path.isfile(path)


def folder_exists(path):

    return os.path.isdir(path)


# ---------------------------------------------------------
# JSON Helpers
# ---------------------------------------------------------

def save_json(data, filename):

    with open(filename, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=4)


def load_json(filename):

    if not os.path.exists(filename):

        return {}

    with open(filename, "r", encoding="utf-8") as f:

        return json.load(f)


# ---------------------------------------------------------
# Hash Helpers
# ---------------------------------------------------------

def sha256(text):

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def md5(text):

    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


# ---------------------------------------------------------
# System Helpers
# ---------------------------------------------------------

def computer_name():

    return socket.gethostname()


def mac_address():

    mac = uuid.getnode()

    return ":".join(

        ("%012X" % mac)[i:i+2]

        for i in range(0, 12, 2)

    )


# ---------------------------------------------------------

if __name__ == "__main__":

    print(current_time())

    print(current_date())

    print(computer_name())

    print(mac_address())

    print(sha256("SentinelAI"))