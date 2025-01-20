import logging
import sys
from datetime import datetime
import time

class LocalTimeFormatter(logging.Formatter):
    """Custom formatter to display server local time."""
    def formatTime(self, record, datefmt=None):
        local_time = time.localtime(record.created)
        if datefmt:
            return time.strftime(datefmt, local_time)
        return time.strftime('%Y-%m-%d %H:%M:%S', local_time)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

formatter = LocalTimeFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)