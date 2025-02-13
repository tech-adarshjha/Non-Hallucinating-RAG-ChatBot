# logger.py
import logging
import os
from datetime import datetime
from logging import Logger
from typing import Optional

from config.log import logLevel


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class LoggerFactory:
    def __init__(self,
                 name: str = 'MyApp',
                 log_file: Optional[str] = 'app.log',
                 level: int = logging.INFO,
                 fmt: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                 datefmt: Optional[str] = '%Y-%m-%d %H:%M:%S') -> None:
        """
        Initialize a LoggerFactory instance.

        Args:
            name (str): Name of the logger.
            log_file (Optional[str]): File to which logs should be written. If None, logs are only output to console.
            level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
            fmt (str): Format for log messages.
            datefmt (Optional[str]): Date format for log messages.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(fmt, datefmt)

        # Console handler (always attached)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(CustomFormatter())
        self.logger.addHandler(console_handler)

        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file, mode='a')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Prevent logging messages from being propagated to the root logger
        self.logger.propagate = False

    def get_logger(self) -> Logger:
        """
        Returns the configured logger instance.

        Returns:
            logging.Logger: Configured logger instance.
        """
        return self.logger


# Create a logger instance for the entire application
cwd = os.getcwd()
name = "Humm.chat"
log_file_name = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
Log_PATH = os.path.join(cwd, "logs", log_file_name)


logger_factory = LoggerFactory(
    name=name, log_file=None, level=logLevel)
logger = logger_factory.get_logger()

# Log messages
# logger.debug("Debug level message")
# logger.info("Info level message")
# logger.warning("Warning level message")
# logger.error("Error level message")
