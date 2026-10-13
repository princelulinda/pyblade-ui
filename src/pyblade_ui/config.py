"""Where things live in the project PyBlade UI is installing into.

PyBlade's own `pyblade.toml` (or `[tool.pyblade]` in pyproject.toml) says
where components go; `pyblade-ui.toml`, next to it, holds what is ours: the
stylesheets to write the theme into, the registry to install from and the
current theme.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_FILE = "pyblade-ui.toml"
DEFAULT_CSS = "static/css/tailwind.css"
DEFAULT_THEME_CSS = "static/css/theme.css"


class ProjectNotFound(Exception):
    pass


def _read_toml(path: Path) -> dict:
    with path.open("rb") as file:
        return tomllib.load(file)


def find_root(start: Path | None = None) -> Path:
    """The closest directory holding a PyBlade configuration, from `start` upwards."""
    start = (start or Path.cwd()).resolve()

    for directory in [start, *start.parents]:
        if (directory / "pyblade.toml").is_file() or (directory / CONFIG_FILE).is_file():
            return directory
        pyproject = directory / "pyproject.toml"
        if pyproject.is_file() and "pyblade" in _read_toml(pyproject).get("tool", {}):
            return directory

    raise ProjectNotFound(
        "No PyBlade project found (no pyblade.toml in this directory or its parents). "
        "Run `pyblade init` first, or pass --cwd."
    )


def _pyblade_settings(root: Path) -> dict:
    """PyBlade's own settings, from pyblade.toml or [tool.pyblade], lower-cased keys."""
    if (root / "pyblade.toml").is_file():
        data = _read_toml(root / "pyblade.toml")
    elif (root / "pyproject.toml").is_file():
        data = _read_toml(root / "pyproject.toml").get("tool", {}).get("pyblade", {})
    else:
        data = {}

    def lower(value):
        return {k.lower(): lower(v) for k, v in value.items()} if isinstance(value, dict) else value

    return lower(data)


@dataclass
class ThemeSettings:
    base: str = "neutral"
    color: str = "neutral"
    radius: str = "0.625rem"


@dataclass
class Project:
    root: Path
    components: Path
    css: Path
    theme_css: Path
    registry: str = ""
    framework: str | None = None
    theme: ThemeSettings = field(default_factory=ThemeSettings)
    configured: bool = False

    @classmethod
    def load(cls, start: Path | None = None) -> "Project":
        root = find_root(start)
        pyblade = _pyblade_settings(root)

        ours = _read_toml(root / CONFIG_FILE) if (root / CONFIG_FILE).is_file() else {}
        ui = ours.get("ui", {})
        theme = ours.get("theme", {})

        return cls(
            root=root,
            components=root / pyblade.get("paths", {}).get("components", "components"),
            css=root / ui.get("css", DEFAULT_CSS),
            theme_css=root / ui.get("theme_css", DEFAULT_THEME_CSS),
            registry=ui.get("registry", ""),
            framework=pyblade.get("stack", {}).get("framework"),
            theme=ThemeSettings(**{k: str(v) for k, v in theme.items() if k in ("base", "color", "radius")}),
            configured=bool(ours),
        )

    def relative(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    def save(self) -> Path:
        """Write pyblade-ui.toml."""
        text = f"""# PyBlade UI configuration, read by the `pyblade-ui` command.
[ui]
# Where to install from: empty for the registry bundled with pyblade-ui,
# otherwise a URL or a folder holding a registry.json.
registry = "{self.registry}"
# The Tailwind stylesheet of the project, and the theme it imports.
css = "{self.relative(self.css)}"
theme_css = "{self.relative(self.theme_css)}"

[theme]
base = "{self.theme.base}"
color = "{self.theme.color}"
radius = "{self.theme.radius}"
"""
        path = self.root / CONFIG_FILE
        path.write_text(text, encoding="utf-8")
        self.configured = True
        return path
