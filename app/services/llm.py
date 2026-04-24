"""Lightweight Groq LLM wrapper used by the Streamlit frontend."""

from __future__ import annotations

import os
from pathlib import Path

import dotenv
from groq import Groq

dotenv.load_dotenv()

DEFAULT_MODEL = "llama-3.3-70b-versatile"
SYSTEM_PROMPT_PATH = Path(__file__).resolve().parents[2] / "system.md"


def _load_system_prompt() -> str:
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8").strip()
    return (
        "You are an empathetic mental-health support companion. "
        "Always remind the user you are not a substitute for professional care."
    )


SYSTEM_PROMPT = _load_system_prompt()


class GroqUnavailableError(RuntimeError):
    """Raised when the Groq client cannot be constructed (missing key)."""


def _get_client(api_key: str | None = None) -> Groq:
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        raise GroqUnavailableError(
            "GROQ_API_KEY is not set. Add it to your .env file or Replit Secrets."
        )
    return Groq(api_key=key)


def generate_reply(
    history: list[dict[str, str]],
    *,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.6,
    max_tokens: int = 768,
) -> str:
    """Send the chat ``history`` to Groq and return the assistant message text.

    ``history`` is a list of ``{"role": "user"|"assistant", "content": str}``
    dicts. The therapy system prompt is prepended automatically.
    """

    client = _get_client(api_key)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return completion.choices[0].message.content or ""
