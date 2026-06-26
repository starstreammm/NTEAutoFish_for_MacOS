import logging
import sys

from typing import Literal


class Logger:
    _log = None
    _level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    @classmethod
    def init(cls):
        # Get logger
        logger = logging.getLogger("main")
        logger.setLevel(logging.DEBUG)

        # Stderr handler
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        stderr_handler.setFormatter(
            logging.Formatter("{levelname:^7} : {message}", style="{")
        )
        logger.addHandler(stderr_handler)

        # Stdout handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(getattr(logging, cls._level))
        stdout_handler.setFormatter(
            logging.Formatter("{levelname:^7} : {message}", style="{")
        )
        logger.addHandler(stdout_handler)

        cls._log = logger

    @classmethod
    def info(cls, msg: str):
        if cls._log is None:
            print("Logger not initialized.")
            return
        cls._log.info(msg)

    @classmethod
    def warning(cls, msg: str):
        if cls._log is None:
            print("Logger not initialized.")
            return
        cls._log.warning(msg)

    @classmethod
    def error(cls, msg: str):
        if cls._log is None:
            print("Logger not initialized.")
            return
        cls._log.error(msg)

    @classmethod
    def debug(cls, msg: str):
        if cls._log is None:
            print("Logger not initialized.")
            return
        cls._log.debug(msg)
