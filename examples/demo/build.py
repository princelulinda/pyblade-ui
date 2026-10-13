"""Render the demo page to dist/index.html, then build its CSS with Tailwind.

    python build.py && npx @tailwindcss/cli -i static/css/tailwind.css -o dist/static/css/app.css
"""

from pathlib import Path

import pyblade_ui  # noqa: F401 -- registers the `cn` filter
from pyblade import PyBlade

ROOT = Path(__file__).parent

CONTEXT = {
    "dialog_open": False,
    "colors": ["neutral", "blue", "green", "violet", "rose", "orange"],
    "members": [
        {"name": "Ada Lovelace", "role": "Owner", "status": "success"},
        {"name": "Grace Hopper", "role": "Admin", "status": "warning"},
        {"name": "Alan Turing", "role": "Editor", "status": "destructive"},
    ],
}

if __name__ == "__main__":
    html = PyBlade(dirs=[str(ROOT / "templates")]).render_file("index", CONTEXT)
    out = ROOT / "dist" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")
