"""Record failures from a B2B SaaS agent step without hiding the exception."""
import traceback
from collections.abc import Callable
from typing import TypeVar

import infrai


T = TypeVar("T")


def track_step(step: Callable[[], T]) -> T:
    """Run an agent step, record its exception, then preserve normal control flow."""
    try:
        return step()
    except Exception:
        infrai.errors.capture(traceback.format_exc())
        raise


def call_customer_system() -> str:
    """Replace this function with one tool call from your agent loop."""
    raise ValueError("Customer record needs a required identifier")


if __name__ == "__main__":
    try:
        track_step(call_customer_system)
    except ValueError:
        print("Agent exception recorded in Infrai.")
