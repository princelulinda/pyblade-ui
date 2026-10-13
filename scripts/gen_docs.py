"""Write docs/components.md from the registry, so the docs never drift from it.

    python scripts/gen_docs.py
"""

from pathlib import Path

from pyblade_ui.registry import Registry

ROOT = Path(__file__).resolve().parent.parent


def main():
    registry = Registry()
    lines = [
        "# Composants",
        "",
        "Page générée par `scripts/gen_docs.py` depuis `registry.json` : ne pas éditer à la main.",
        "",
    ]
    for item in registry.items.values():
        lines += [f"## {item.title}", "", item.description, "", "```bash", f"pyblade-ui add {item.name}", "```", ""]
        if item.registry_dependencies:
            lines += ["Installe aussi : " + ", ".join(f"`{d}`" for d in item.registry_dependencies) + ".", ""]
        if item.js:
            lines += ["Nécessite : " + ", ".join(item.js) + ".", ""]
        lines += ["Fichiers : " + ", ".join(f"`components/{f}`" for f in item.files), ""]
        if item.usage:
            lines += ["```html", item.usage, "```", ""]
    out = ROOT / "docs" / "components.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
