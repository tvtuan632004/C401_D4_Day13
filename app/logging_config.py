from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import structlog
from structlog.contextvars import merge_contextvars

from .pii import scrub_text

LOG_PATH = Path(os.getenv("LOG_PATH", "data/logs.jsonl"))


import json


class DummyLogger:
    """Dummy logger that accepts keyword arguments without doing anything."""
    def msg(self, message=None, **kw):
        pass
    
    def debug(self, message=None, **kw):
        pass
    
    def info(self, message=None, **kw):
        pass
    
    def warning(self, message=None, **kw):
        pass
    
    def error(self, message=None, **kw):
        pass
    
    def critical(self, message=None, **kw):
        pass


class DummyLoggerFactory:
    """Factory that returns a dummy logger."""
    def __call__(self, *args, **kwargs):
        return DummyLogger()


class JsonlFileProcessor:
    def __call__(self, logger: Any, method_name: str, event_dict: dict[str, Any]) -> dict[str, Any]:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event_dict) + "\n")
        return event_dict


def scrub_event(_: Any, __: str, event_dict: dict[str, Any]) -> dict[str, Any]:
    # scrub payload
    payload = event_dict.get("payload")
    if isinstance(payload, dict):
        event_dict["payload"] = {
            k: scrub_text(v) if isinstance(v, str) else v for k, v in payload.items()
        }

    # scrub event name
    if "event" in event_dict and isinstance(event_dict["event"], str):
        event_dict["event"] = scrub_text(event_dict["event"])

    for key, value in event_dict.items():
        if isinstance(value, str):
            event_dict[key] = scrub_text(value)

    return event_dict


def configure_logging() -> None:
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    )

    structlog.configure(
        processors=[
            merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="ts"),

            scrub_event,

            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,

            JsonlFileProcessor(),
        ],
        context_class=dict,
        logger_factory=DummyLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger() -> structlog.typing.FilteringBoundLogger:
    return structlog.get_logger()