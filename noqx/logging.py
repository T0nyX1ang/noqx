"""Logging utility for the site."""

import inspect
import logging

from loguru import logger


class LoguruHandler(logging.Handler):  # pragma: no cover
    """Emit standard logging to loguru logger."""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logger.remove()
