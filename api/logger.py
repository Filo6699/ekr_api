import logging
import os
from config import loglevel

LOG_DIRECTORY = "logs/"
LOG_NAME = "app.log"


def parse_log_level():
    """
    Parse the log level from the configuration.

    Returns:
    int: Logging level corresponding to the configuration.
    """
    log_level = loglevel.upper()
    if log_level == "DEBUG":
        return logging.DEBUG
    elif log_level == "INFO":
        return logging.INFO
    elif log_level == "WARNING":
        return logging.WARNING
    elif log_level == "ERROR":
        return logging.ERROR
    elif log_level == "CRITICAL":
        return logging.CRITICAL
    else:
        raise ValueError(f"Invalid log level: {log_level}")


def configure_logger():
    """
    Configure the logger with file and console handlers.
    """
    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    parsed_level = parse_log_level()
    message_format = "%(asctime)s - %(levelname)s - %(message)s"
    log_file = os.path.join(LOG_DIRECTORY, LOG_NAME)

    logging.basicConfig(filename=log_file, level=logging.DEBUG, format=message_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(parsed_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)


configure_logger()

logger = logging.getLogger(__name__)
