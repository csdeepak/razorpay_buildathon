"""An in-process fake of an OpenAI-shaped `/chat/completions` endpoint.

Same approach as `src/tool/fake_razorpay.py`: a `requests.Session`-shaped
object, so `OpenAICompatBackend` runs its real auth, body construction,
response parsing and error mapping against it and only the socket is missing.

Scripted rather than simulated. A fake model that "decides" things would just
be a worse model; what the adapter needs proving is that it can *carry*
whatever a real model returns. So a test queues the turns it wants and this
plays them back, including the ugly ones:

- a tool call whose `arguments` string is **not valid JSON** (the failure mode
  Anthropic's wire format makes impossible and this one does not)
- `arguments` arriving pre-parsed as an object, which some providers do in
  spite of the spec
- 429 / 402 / 400, so `ModelBackendError` classification is exercised

The request each turn was answered with is kept in `.requests`, so tests can
assert on what actually went over the wire -- that the system prompt leads,
that tool results come back as `role: "tool"` keyed by `tool_call_id`, and
that provider pinning is present when asked for.
"""

from __future__ import annotations

import json as _json
from typing import Any


class FakeResponse:
    def __init__(self, status_code: int, payload: Any) -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = _json.dumps(payload)

    def json(self) -> Any:
        return self._payload


def assistant_turn(
    *,
    text: str = "",
    tool_calls: list[dict[str, Any]] | None = None,
    prompt_tokens: int = 100,
    completion_tokens: int = 20,
    provider: str = "FakeProvider",
    finish_reason: str = "stop",
) -> FakeResponse:
    """Build one successful completion in the OpenAI response shape."""
    message: dict[str, Any] = {"role": "assistant", "content": text}
    if tool_calls:
        message["tool_calls"] = tool_calls
        finish_reason = "tool_calls"
    return FakeResponse(
        200,
        {
            "id": "chatcmpl-fake",
            "provider": provider,
            "choices": [{"index": 0, "message": message, "finish_reason": finish_reason}],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        },
    )


def tool_call(
    name: str,
    arguments: str | dict[str, Any],
    *,
    call_id: str = "call_1",
) -> dict[str, Any]:
    """One tool call. Pass `arguments` as a string to reproduce the real wire
    format -- including deliberately malformed JSON -- or as a dict to
    reproduce providers that pre-parse it."""
    return {
        "id": call_id,
        "type": "function",
        "function": {"name": name, "arguments": arguments},
    }


def error_response(status: int, message: str) -> FakeResponse:
    return FakeResponse(status, {"error": {"message": message, "code": status}})


class FakeOpenAISession:
    """Plays back queued responses in order, recording every request."""

    def __init__(self, responses: list[FakeResponse] | None = None) -> None:
        self.queue: list[FakeResponse] = list(responses or [])
        self.requests: list[dict[str, Any]] = []
        self.headers_seen: list[dict[str, str]] = []

    def queue_response(self, response: FakeResponse) -> None:
        self.queue.append(response)

    def post(
        self,
        url: str,
        *,
        json: dict,
        headers: dict[str, str],
        timeout: float = 120.0,
    ) -> FakeResponse:
        self.requests.append({"url": url, **json})
        self.headers_seen.append(dict(headers))
        if not self.queue:
            raise AssertionError(
                f"FakeOpenAISession ran out of queued responses at call "
                f"#{len(self.requests)} -- the test under-specified the conversation."
            )
        return self.queue.pop(0)
