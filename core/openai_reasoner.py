"""OpenAI reasoning layer for Denham's JARVIS V1.

Gemini Live remains the low-latency voice/session layer. This module gives
plugins a single, boring interface for deliberate OpenAI reasoning.

Secrets are NEVER stored here. Set OPENAI_API_KEY in the environment.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


DEFAULT_MODEL = os.getenv("JARVIS_OPENAI_MODEL", "gpt-5.6-sol")


@dataclass(frozen=True)
class ReasoningResult:
    text: str
    model: str


class OpenAIReasoner:
    def __init__(self, model: str | None = None):
        self.model = (model or DEFAULT_MODEL).strip()
        self._client = None

    def available(self) -> tuple[bool, str]:
        if OpenAI is None:
            return False, "The OpenAI Python package is not installed."
        if not os.getenv("OPENAI_API_KEY", "").strip():
            return False, "OPENAI_API_KEY is not set."
        return True, "ready"

    def _get_client(self):
        ok, why = self.available()
        if not ok:
            raise RuntimeError(why)
        if self._client is None:
            self._client = OpenAI()
        return self._client

    def reason(self, task: str, *, context: str = "", instructions: str = "") -> ReasoningResult:
        task = (task or "").strip()
        if not task:
            raise ValueError("A task is required.")

        system = (
            "You are the deliberate reasoning layer inside JARVIS, a personal AI "
            "assistant. Be precise, practical, security-conscious, and concise. "
            "Do not claim an external action happened unless the surrounding tool "
            "actually performed it. For code work, identify assumptions and give "
            "testable next steps."
        )
        if instructions.strip():
            system += "\n\nAdditional instructions:\n" + instructions.strip()

        user_input = task
        if context.strip():
            user_input = "CONTEXT:\n" + context.strip() + "\n\nTASK:\n" + task

        response = self._get_client().responses.create(
            model=self.model,
            instructions=system,
            input=user_input,
        )
        text = (getattr(response, "output_text", "") or "").strip()
        if not text:
            raise RuntimeError("OpenAI returned no text output.")
        return ReasoningResult(text=text, model=self.model)


def reason(task: str, *, context: str = "", instructions: str = "", model: str | None = None) -> str:
    return OpenAIReasoner(model=model).reason(
        task, context=context, instructions=instructions
    ).text
