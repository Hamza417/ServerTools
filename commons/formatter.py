import logging


class Formatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[92m',  # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m'  # Magenta
    }

    RESET = '\033[0m'

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"


def configure_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(Formatter('%(levelname)s - %(message)s'))
    logging.basicConfig(level=logging.INFO, handlers=[handler])
