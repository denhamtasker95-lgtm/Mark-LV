"""Open the zero-dependency JARVIS V1 visual preview in the default browser."""
from pathlib import Path
import webbrowser
p=Path(__file__).resolve().parent/"preview"/"index.html"
webbrowser.open(p.as_uri())
print("JARVIS V1 preview opened:",p)
