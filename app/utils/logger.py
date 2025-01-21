import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
