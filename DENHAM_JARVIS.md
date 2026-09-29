# Denham JARVIS V1

This branch keeps Mark LV's proven Gemini Live voice/HUD stack and adds a separate
OpenAI reasoning layer. The goal is a reliable hybrid assistant, not a cosmetic fork.

## What is added

- `core/openai_reasoner.py`: one OpenAI Responses API gateway.
- `plugins/openai_brain.py`: deliberate reasoning for planning, coding and research.
- `plugins/project_brain.py`: project-aware reasoning for CarFlip and D AI Lab.
- Existing Mark LV computer, browser, vision, memory, dev, file, system-monitor,
  confirmation and undo capabilities remain intact.

## Security

Do not put API keys in GitHub or source files.

On Windows PowerShell for the current session:

    $env:OPENAI_API_KEY="YOUR_KEY"

Optional model override:

    $env:JARVIS_OPENAI_MODEL="gpt-5.6-sol"

For a persistent setup, use Windows' environment-variable UI or a proper secret
manager. The next hardening milestone is migrating legacy plugin secrets away from
plaintext `config/api_keys.json`.

## Architecture

Voice/HUD -> Gemini Live -> existing JARVIS tools
                         -> openai_brain -> OpenAI Responses API
                         -> project_brain -> CarFlip / D AI Lab reasoning

The OpenAI layer is deliberately advisory in V1. It does not bypass Mark LV's
confirmation gates and does not claim that actions occurred unless an action tool
actually performed them.

## Next milestones

1. Smoke-test Windows setup and voice.
2. Add secure secret storage.
3. Add a model router with cost/latency policies.
4. Add GitHub and deployment adapters behind explicit permissions.
5. Add local-model adapter for the future workstation.
6. Replace inherited UI/branding progressively with an original JARVIS interface.

Mark LV's upstream licence still applies to inherited code. Treat this branch as a
personal/non-commercial build unless appropriate commercial rights are obtained.
