"""Model backends, so the same corpus can be run across labs.

Everything measured so far (`docs/eval-findings.md`) used three Claude models.
That is a real confound in the project's sharpest claim: "every model resists
diversion and fails 100% of denial attacks" currently means *every Anthropic
model*, and a reviewer is entitled to ask whether the denial gap is a property
of agents or a property of one lab's post-training.

This module exists to answer that. It puts one normalized interface in front
of two wire formats:

- `AnthropicBackend` -- the existing path, unchanged in behaviour. The
  Anthropic runs already in `eval/runs/` must stay comparable to anything new,
  so this backend is a lift of the previous inline code, not a rewrite of it.
- `OpenAICompatBackend` -- OpenAI-shaped `/chat/completions`, which covers
  **both** OpenRouter and Google AI Studio (Google publishes an OpenAI-
  compatible endpoint), so one adapter reaches every non-Anthropic model this
  project can afford.

## The backend owns its own message list

Deliberate. Each wire format has a different notion of what an assistant turn
and a tool result look like, and normalizing *those* would mean inventing a
third format and translating twice. Instead the agent loop drives the
conversation with format-free verbs -- `add_user_text`, `add_tool_results`,
`complete` -- and each backend keeps history in its own native shape.

## Malformed tool arguments are their own outcome

Anthropic returns tool inputs as parsed objects. OpenAI-format returns
`function.arguments` as a **string**, and weaker models emit strings that are
not valid JSON. That is neither "the agent was compromised" nor "the agent
resisted" -- scoring it as either would corrupt the headline number. It
surfaces as `ToolCall.malformed` so the harness can count it separately.

## Provider pinning

OpenRouter routes to whichever backend provider is available, and providers
differ in quantization. For a project whose entire argument is measurement
rigour, "the model failed" and "someone's 4-bit re-host failed" must not be
the same data point. `provider_order` pins routing and `ModelTurn.provider`
records who actually served each call, so the run file can be audited after
the fact.
"""

from __future__ import annotations

import json
import random
import time
import os
from dataclasses import dataclass, field
from typing import Any, Protocol

OPENROUTER_BASE = "https://openrouter.ai/api/v1"
GOOGLE_OPENAI_BASE = "https://generativelanguage.googleapis.com/v1beta/openai"


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]
    malformed: bool = False
    raw_arguments: str | None = None


@dataclass
class ModelTurn:
    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    provider: str | None = None
    finish_reason: str | None = None


class ModelBackend(Protocol):
    model: str

    def reset(self) -> None: ...
    def add_user_text(self, text: str) -> None: ...
    def add_tool_results(self, results: list[tuple[str, str]]) -> None: ...
    def complete(self) -> ModelTurn: ...


class AnthropicBackend:
    """The original path. Behaviour-preserving: same call shape, same
    max_tokens, same message construction as the pre-refactor loop."""

    def __init__(
        self,
        model: str,
        system: str,
        tools: list[dict[str, Any]],
        *,
        client: Any | None = None,
        max_tokens: int = 4096,
    ) -> None:
        if client is None:
            import anthropic

            client = anthropic.Anthropic()
        self.model = model
        self._client = client
        self._system = system
        self._tools = tools
        self._max_tokens = max_tokens
        self._messages: list[dict[str, Any]] = []

    def reset(self) -> None:
        self._messages = []

    def add_user_text(self, text: str) -> None:
        self._messages.append({"role": "user", "content": text})

    def add_tool_results(self, results: list[tuple[str, str]]) -> None:
        self._messages.append(
            {
                "role": "user",
                "content": [
                    {"type": "tool_result", "tool_use_id": call_id, "content": content}
                    for call_id, content in results
                ],
            }
        )

    def complete(self) -> ModelTurn:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=self._max_tokens,
            system=self._system,
            tools=self._tools,
            messages=self._messages,
        )
        self._messages.append({"role": "assistant", "content": response.content})

        return ModelTurn(
            text="".join(b.text for b in response.content if b.type == "text"),
            tool_calls=[
                # Already-parsed objects on this wire format, so `malformed`
                # is structurally impossible here.
                ToolCall(id=b.id, name=b.name, arguments=dict(b.input))
                for b in response.content
                if b.type == "tool_use"
            ],
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            provider="anthropic",
            finish_reason=getattr(response, "stop_reason", None),
        )


def to_openai_tools(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Anthropic tool schema -> OpenAI function schema.

    The only real difference is `input_schema` becoming `parameters` and the
    whole thing nesting under a `function` key. Kept as a free function so a
    reader can check the translation without instantiating anything.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t["input_schema"],
            },
        }
        for t in tools
    ]


class OpenAICompatBackend:
    """OpenAI-shaped `/chat/completions`: OpenRouter, Google AI Studio, and
    anything else speaking that dialect."""

    def __init__(
        self,
        model: str,
        system: str,
        tools: list[dict[str, Any]],
        *,
        api_key: str,
        base_url: str = OPENROUTER_BASE,
        session: Any | None = None,
        max_tokens: int = 4096,
        timeout: float = 120.0,
        provider_order: list[str] | None = None,
        extra_headers: dict[str, str] | None = None,
        max_retries: int = 6,
        backoff_base: float = 2.0,
        sleep: Any = None,
    ) -> None:
        if not api_key:
            raise ValueError(f"an API key is required for {model!r}")
        if session is None:
            import requests

            session = requests.Session()
        self.model = model
        self._session = session
        self._key = api_key
        self._base = base_url.rstrip("/")
        self._system = system
        self._tools = to_openai_tools(tools)
        self._max_tokens = max_tokens
        self._timeout = timeout
        self._provider_order = provider_order
        self._extra_headers = extra_headers or {}
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._sleep = sleep or time.sleep
        self.retries_used = 0
        self._messages: list[dict[str, Any]] = []

    def reset(self) -> None:
        self._messages = []

    def add_user_text(self, text: str) -> None:
        self._messages.append({"role": "user", "content": text})

    def add_tool_results(self, results: list[tuple[str, str]]) -> None:
        # One message per result on this format, versus one message carrying
        # every result on Anthropic's.
        for call_id, content in results:
            self._messages.append(
                {"role": "tool", "tool_call_id": call_id, "content": content}
            )

    def _body(self) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self._max_tokens,
            "messages": [{"role": "system", "content": self._system}, *self._messages],
            "tools": self._tools,
        }
        if self._provider_order is not None:
            # allow_fallbacks off: better a hard failure than a silent reroute
            # to a differently-quantized host mid-run.
            body["provider"] = {
                "order": self._provider_order,
                "allow_fallbacks": False,
            }
        return body

    RETRYABLE = frozenset({429, 500, 502, 503, 504})

    def _post_with_retry(self) -> Any:
        """Retry transient provider failures with exponential backoff + jitter.

        Free tiers return 429 (quota) and 503 (high demand) routinely, and a
        run that drops those cases is a biased sample, not a smaller one. So
        they are retried rather than absorbed -- and when retries are
        exhausted the error is still raised, never swallowed, so the harness
        records a real failure and the report's error count stays honest.

        `Retry-After` is honoured when the provider sends it; providers know
        their own quota windows better than a backoff curve does.
        """
        headers = {
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
            **self._extra_headers,
        }
        last = None
        for attempt in range(self._max_retries + 1):
            last = self._session.post(
                f"{self._base}/chat/completions",
                json=self._body(),
                headers=headers,
                timeout=self._timeout,
            )
            if last.status_code not in self.RETRYABLE or attempt == self._max_retries:
                return last

            retry_after = getattr(last, "headers", {}) or {}
            try:
                delay = float(retry_after.get("Retry-After", ""))
            except (TypeError, ValueError):
                delay = self._backoff_base**attempt + random.uniform(0, 0.75)
            self.retries_used += 1
            self._sleep(min(delay, 60.0))
        return last

    def complete(self) -> ModelTurn:
        response = self._post_with_retry()
        try:
            payload = response.json()
        except Exception:  # noqa: BLE001
            payload = {"error": {"message": "unparseable body"}}

        # Google AI Studio returns errors as a JSON *array* -- [{"error": {...}}]
        # -- rather than the object the OpenAI shape specifies. Without this,
        # a Gemini 429 raises AttributeError from the error path instead of a
        # classified ModelBackendError, which is precisely the failure this
        # class exists to prevent: a rate-limited run has to be loudly
        # distinguishable from a completed one.
        if isinstance(payload, list):
            payload = payload[0] if payload and isinstance(payload[0], dict) else {}

        if response.status_code >= 400:
            err = payload.get("error", {})
            message = err.get("message", str(payload)[:200]) if isinstance(err, dict) else str(err)
            raise ModelBackendError(response.status_code, self.model, message)

        choice = (payload.get("choices") or [{}])[0]
        message = choice.get("message") or {}

        # Echo the assistant turn back verbatim. Providers vary in what extra
        # keys they attach, and re-synthesizing the message from parsed parts
        # is how tool_call ids get dropped.
        self._messages.append(
            {
                "role": "assistant",
                "content": message.get("content") or "",
                **({"tool_calls": message["tool_calls"]} if message.get("tool_calls") else {}),
            }
        )

        calls: list[ToolCall] = []
        for raw in message.get("tool_calls") or []:
            fn = raw.get("function") or {}
            raw_args = fn.get("arguments")
            parsed: dict[str, Any] = {}
            malformed = False
            if isinstance(raw_args, dict):
                # Some providers pre-parse despite the spec. Accept it.
                parsed = raw_args
            else:
                try:
                    loaded = json.loads(raw_args or "{}")
                    if isinstance(loaded, dict):
                        parsed = loaded
                    else:
                        malformed = True
                except (json.JSONDecodeError, TypeError):
                    malformed = True
            calls.append(
                ToolCall(
                    id=raw.get("id") or f"call_{len(calls)}",
                    name=fn.get("name", ""),
                    arguments=parsed,
                    malformed=malformed,
                    raw_arguments=raw_args if isinstance(raw_args, str) else None,
                )
            )

        usage = payload.get("usage") or {}
        return ModelTurn(
            text=message.get("content") or "",
            tool_calls=calls,
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
            provider=payload.get("provider"),
            finish_reason=choice.get("finish_reason"),
        )


class ModelBackendError(RuntimeError):
    """A non-2xx from a model provider.

    Carries the status so the harness can tell a 429 (rate limited -- the run
    is incomplete, and the cases that did finish are a biased sample) from a
    400 (the request was wrong). Conflating those is how a half-finished free
    tier run turns into a headline number.
    """

    def __init__(self, status_code: int, model: str, message: str) -> None:
        self.status_code = status_code
        self.model = model
        super().__init__(f"[{status_code}] {model}: {message}")

    @property
    def is_rate_limit(self) -> bool:
        return self.status_code == 429

    @property
    def is_out_of_credit(self) -> bool:
        return self.status_code == 402


def backend_for(
    model: str,
    system: str,
    tools: list[dict[str, Any]],
    *,
    session: Any | None = None,
    client: Any | None = None,
    **kwargs: Any,
) -> ModelBackend:
    """Pick a backend from the model id.

    - `claude-*`            -> Anthropic, the existing measured path
    - `gemini-*`            -> Google AI Studio's OpenAI-compatible endpoint
    - anything with a `/`   -> OpenRouter (`openai/gpt-5.1`, `nvidia/...`)
    """
    if model.startswith("claude-"):
        return AnthropicBackend(model, system, tools, client=client)

    if model.startswith("gemini"):
        key = os.environ.get("GOOGLE_API_KEY", "")
        if not key:
            raise RuntimeError(
                "GOOGLE_API_KEY is not set. Get a free key at "
                "https://aistudio.google.com/apikey"
            )
        return OpenAICompatBackend(
            model, system, tools,
            api_key=key, base_url=GOOGLE_OPENAI_BASE, session=session, **kwargs,
        )

    if "/" in model:
        key = os.environ.get("OPENROUTER_API_KEY", "")
        if not key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. Get one at https://openrouter.ai/keys"
            )
        return OpenAICompatBackend(
            model, system, tools,
            api_key=key, base_url=OPENROUTER_BASE, session=session,
            extra_headers={
                "HTTP-Referer": "https://github.com/csdeepak/razorpay_buildathon",
                "X-Title": "Warden adversarial eval",
            },
            **kwargs,
        )

    raise ValueError(
        f"unrecognised model {model!r} -- expected 'claude-*', 'gemini-*', "
        "or an OpenRouter 'vendor/model' id"
    )
