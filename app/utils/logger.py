import logging

class TerminalColor:
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: TerminalColor.CYAN,
        logging.INFO: TerminalColor.GREEN,
        logging.WARNING: TerminalColor.YELLOW,
        logging.ERROR: TerminalColor.RED,
        logging.CRITICAL: TerminalColor.RED + TerminalColor.WHITE
    }

    def format(self, record):
        level_color = self.COLORS.get(record.levelno, TerminalColor.RESET)
        reset_color = TerminalColor.RESET
        message = super().format(record)
        return f"{level_color}{message}{reset_color}"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)