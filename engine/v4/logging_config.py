"""
Meli Financial Auditor v3.5 — Logging Module

Structured logging with levels: INFO, WARNING, ERROR, CRITICAL.
All engine events go through this module.
"""
import logging
import sys
from pathlib import Path
from datetime import datetime

LOG_DIR = Path(__file__).parent.parent.parent / "00_Config" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

_LOG_FILE = LOG_DIR / f"meli_auditor_{datetime.now().strftime('%Y%m%d')}.log"

_EVENTS = [
    "file_processed",
    "rows_inserted",
    "rows_reconciled",
    "exceptions_detected",
    "errors_detected",
]


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure root meli logger with console + file handlers."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger = logging.getLogger("meli")

    if logger.handlers:
        return logger  # already configured

    logger.setLevel(log_level)
    fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a child logger under the meli namespace."""
    return logging.getLogger(f"meli.{name}")


def log_event(logger: logging.Logger, event: str, **kwargs):
    """Log a structured engine event."""
    if event not in _EVENTS:
        logger.warning(f"Unknown event type: {event}")
    details = " | ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"EVENT={event} | {details}")
