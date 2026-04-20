from __future__ import annotations

import os
from typing import Any
import time
from .logging_config import get_logger


# ===== Try import Langfuse =====
try:
    from langfuse import observe, get_client, propagate_attributes
    _LANGFUSE_AVAILABLE = True
except Exception:  # pragma: no cover
    _LANGFUSE_AVAILABLE = False

    # ===== Fallbacks =====
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    def propagate_attributes(*args: Any, **kwargs: Any):
        class _DummyCtx:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        return _DummyCtx()

    def get_client():
        class _DummyClient:
            def flush(self) -> None:
                return None

            def get_current_trace_id(self) -> str | None:
                return None

        return _DummyClient()


def tracing_enabled() -> bool:
    return bool(
        _LANGFUSE_AVAILABLE
        and os.getenv("LANGFUSE_PUBLIC_KEY")
        and os.getenv("LANGFUSE_SECRET_KEY")
        and os.getenv("LANGFUSE_BASE_URL")
    )


def flush_traces() -> None:
    if not tracing_enabled():
        return
    try:
        get_client().flush()
    except Exception:
        pass


def get_current_trace_id() -> str | None:
    if not tracing_enabled():
        return None
    try:
        return get_client().get_current_trace_id()
    except Exception:
        return None
    
def observe(name: str = "span"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()

            result = func(*args, **kwargs)

            latency = (time.perf_counter() - start) * 1000

            log = get_logger()
            log.info(
                "span_latency",
                span=name,
                latency_ms=round(latency, 2)
            )

            return result
        return wrapper
    return decorator