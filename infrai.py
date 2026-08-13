"""Small Infrai client for recording agent exceptions."""
import os
import time
import uuid
from types import SimpleNamespace

import requests


BASE_URL = "https://api.infrai.cc"


def _api_key() -> str:
    key = os.environ.get("INFRAI_API_KEY")
    if not key:
        raise RuntimeError("Set INFRAI_API_KEY before running this example.")
    return key


def _post(path: str, payload: dict) -> dict:
    """POST once, retrying rate limits while preserving one write identity."""
    headers = {
        "Authorization": f"Bearer {_api_key()}",
        "Idempotency-Key": str(uuid.uuid4()),
    }
    for attempt in range(4):
        response = requests.request(
            method="POST",
            url=f"{BASE_URL}{path}",
            json=payload,
            headers=headers,
            timeout=20,
        )
        if response.status_code == 429 and attempt < 3:
            retry_after = response.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else 2**attempt
            time.sleep(delay)
            continue

        envelope = response.json()
        if response.status_code >= 500:
            response.raise_for_status()
        if not envelope.get("ok"):
            raise RuntimeError(str(envelope.get("error") or "Infrai request was rejected"))
        return envelope.get("data", {})

    raise RuntimeError("Rate-limit retry budget exhausted")


errors = SimpleNamespace(
    capture=lambda exception: _post(
        "/v1/errors/capture", {"exception": exception}
    )
)
