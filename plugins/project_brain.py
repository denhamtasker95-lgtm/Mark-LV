"""Project-aware reasoning for CarFlip and D AI Lab."""
from core.openai_reasoner import OpenAIReasoner

PLUGIN = {
    "name": "project_brain",
    "description": (
        "Use for strategic or technical work specifically about CarFlip or D AI Lab. "
        "Adds stable project guardrails before delegating the reasoning to OpenAI."
    ),
    "behavior": "NON_BLOCKING",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "project": {
                "type": "STRING",
                "description": "Project name: carflip or d_ai_lab."
            },
            "task": {"type": "STRING", "description": "What needs to be solved."},
            "context": {"type": "STRING", "description": "Current code, error, goal, or other relevant context."},
        },
        "required": ["project", "task"],
    },
}

_PROJECTS = {
    "carflip": (
        "CarFlip is an automotive platform. Prioritize production reliability, "
        "security, mobile UX, vehicle/garage workflows, data-integrity, deployment "
        "safety, and measurable user/dealer value. Never invent production status "
        "or claim a deployment occurred without evidence."
    ),
    "d_ai_lab": (
        "D AI Lab builds practical digital solutions. Prefer reusable, maintainable "
        "systems over flashy demos. Keep customer data isolated and require explicit "
        "approval before destructive or externally visible actions."
    ),
}


def run(parameters: dict, player=None, session_memory=None) -> str:
    project = str(parameters.get("project", "")).strip().lower().replace(" ", "_")
    task = str(parameters.get("task", "")).strip()
    context = str(parameters.get("context", "")).strip()
    if project not in _PROJECTS:
        return "Choose project 'carflip' or 'd_ai_lab'."
    if not task:
        return "Tell me what you want solved."

    brain = OpenAIReasoner()
    ok, why = brain.available()
    if not ok:
        return "Project brain is ready, but " + why

    try:
        result = brain.reason(task, context=context, instructions=_PROJECTS[project])
        return result.text
    except Exception as exc:
        return f"{project} reasoning failed: {exc}"
