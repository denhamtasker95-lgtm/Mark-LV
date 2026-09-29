"""Deliberate OpenAI reasoning tool for JARVIS."""
from core.openai_reasoner import OpenAIReasoner

PLUGIN = {
    "name": "openai_brain",
    "description": (
        "Use the OpenAI reasoning brain for difficult planning, coding analysis, "
        "architecture, debugging strategy, comparisons, or tasks that benefit from "
        "deeper deliberate reasoning. Do not use for simple conversation or actions "
        "that an existing JARVIS tool can perform directly."
    ),
    "behavior": "NON_BLOCKING",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "task": {"type": "STRING", "description": "The exact problem to reason about."},
            "context": {"type": "STRING", "description": "Useful facts, code snippets, errors, or constraints."},
            "mode": {
                "type": "STRING",
                "description": "Optional focus: general, coding, carflip, d_ai_lab, or research."
            },
        },
        "required": ["task"],
    },
}

_MODE_INSTRUCTIONS = {
    "coding": "Focus on root cause, minimal safe changes, tests, rollback, and observability.",
    "carflip": "Focus on CarFlip product engineering, reliability, security, UX, deployment, and measurable business value.",
    "d_ai_lab": "Focus on building practical digital solutions that can be delivered reliably to clients.",
    "research": "Separate verified facts, assumptions, unknowns, and recommended verification steps.",
    "general": "",
}


def run(parameters: dict, player=None, session_memory=None) -> str:
    task = str(parameters.get("task", "")).strip()
    context = str(parameters.get("context", "")).strip()
    mode = str(parameters.get("mode", "general")).strip().lower()
    if not task:
        return "I need a task for the OpenAI reasoning brain."

    brain = OpenAIReasoner()
    ok, why = brain.available()
    if not ok:
        return (
            "OpenAI reasoning is installed but not configured yet. "
            + why
            + " Set the key as an environment variable, not in the repository."
        )
    try:
        result = brain.reason(
            task,
            context=context,
            instructions=_MODE_INSTRUCTIONS.get(mode, _MODE_INSTRUCTIONS["general"]),
        )
        if player:
            try:
                player.write_log(f"OPENAI BRAIN [{result.model}]: completed {mode} reasoning")
            except Exception:
                pass
        return result.text
    except Exception as exc:
        return f"OpenAI reasoning failed: {exc}"
