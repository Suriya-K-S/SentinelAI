"""
SentinelAI Logging System
"""

from pathlib import Path
from datetime import datetime
from loguru import logger

from core.paths import LOGS, create_directories

# Create required folders
create_directories()

LOG_FILE = LOGS / f"sentinel_{datetime.now().strftime('%Y%m%d')}.log"

# Remove default logger
logger.remove()

# Console output
logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO",
    format="<green>{time:DD-MM-YYYY HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "{message}",
)

# File output
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

# Export
log = logger