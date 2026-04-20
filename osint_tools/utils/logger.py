"""Logging configuration for OSINT Tools."""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional


def get_logger(
    name: str = "osint_tools",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Create and return a configured logger.

    Attaches a ``StreamHandler`` (stderr) and optionally a
    ``RotatingFileHandler`` when *log_file* is provided.  Calling this
    function multiple times with the same *name* returns the same logger
    without adding duplicate handlers.

    Args:
        name: Logger name.
        level: Log level string (e.g. ``"DEBUG"``, ``"INFO"``).  Falls back
            to the ``OSINT_LOG_LEVEL`` environment variable, then ``"INFO"``.
        log_file: Path to the log file.  Falls back to the ``OSINT_LOG_FILE``
            environment variable.  When ``None`` / empty no file handler is
            attached.

    Returns:
        A :class:`logging.Logger` instance.
    """
    logger = logging.getLogger(name)

    # Only configure once
    if logger.handlers:
        return logger

    resolved_level = level or os.environ.get("OSINT_LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, resolved_level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # Optional file handler
    resolved_file = log_file or os.environ.get("OSINT_LOG_FILE", "")
    if resolved_file:
        file_handler = RotatingFileHandler(
            resolved_file,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger


# Default logger used throughout the package
logger = get_logger()
