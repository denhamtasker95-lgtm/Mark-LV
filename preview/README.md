# JARVIS V1 visual preview

This is a zero-dependency visual checkpoint so the interface can be reviewed
before it is welded into the PyQt runtime.

## See it now

Open `preview/index.html` in any browser.

Or from the repository root:

    python preview_jarvis.py

The telemetry values in this preview are deliberately illustrative. They are not
presented as live system data. The production PyQt HUD will bind those widgets to
the existing `system_monitor`, voice/session state and plugin registry.

## Direction

- central JARVIS core and listening state
- intelligence stack: Gemini Live, OpenAI reasoning, future local AI
- project brains: CarFlip, D AI Lab, development/GitHub
- visible safety-gated computer/browser/vision/memory capabilities
- responsive layout for smaller displays

This preview is a design checkpoint, not a claim that every integration is live.
