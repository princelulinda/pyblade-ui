"""The `pyblade-ui` command: init, add, list, diff and theme."""

from __future__ import annotations

import argparse
import difflib
import os
import sys
from pathlib import Path

from .. import __version__
from ..config import Project, ProjectNotFound
from ..registry import Registry, RegistryError
from ..themes import BASES, COLORS, RADII, custom_part, render_theme

COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _paint(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if COLOR else text


def info(text):
    print(text)


def success(text):
    print(_paint("32", "✔ ") + text)


def warning(text):
    print(_paint("33", "! ") + text)


def error(text):
    print(_paint("31", "✘ ") + text, file=sys.stderr)


def dim(text):
    return _paint("2", text)


def _confirm(question: str, assume_yes: bool) -> bool:
    if assume_yes or not sys.stdin.isatty():
        return assume_yes
    return input(f"{question} [y/N] ").strip().lower() in {"y", "yes", "o", "oui"}


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------

TAILWIND_STUB = """@import "tailwindcss";
@import "{theme}";

/* Where Tailwind looks for the classes you use. */
@source "{up}/templates";
@source "{up}/components";
"""


def write_theme(project: Project) -> Path:
    existing = project.theme_css.read_text(encoding="utf-8") if project.theme_css.is_file() else ""
    css = render_theme(project.theme.base, project.theme.color, project.theme.radius, custom_part(existing))
    project.theme_css.parent.mkdir(parents=True, exist_ok=True)
    project.theme_css.write_text(css, encoding="utf-8")
    return project.theme_css


def link_theme(project: Project) -> str:
    """Make the project's Tailwind stylesheet import the theme. Returns what was done."""
    theme = os.path.relpath(project.theme_css, project.css.parent).replace(os.sep, "/")
    theme = theme if theme.startswith(".") else f"./{theme}"
    line = f'@import "{theme}";'

    if not project.css.is_file():
        up = os.path.relpath(project.root, project.css.parent).replace(os.sep, "/")
        project.css.parent.mkdir(parents=True, exist_ok=True)
        project.css.write_text(TAILWIND_STUB.format(theme=theme, up=up), encoding="utf-8")
        return "created"

    css = project.css.read_text(encoding="utf-8")
    if line in css:
        return "unchanged"

    lines = css.splitlines()
    position = next((i + 1 for i, text in enumerate(lines) if text.strip().startswith('@import "tailwindcss"')), 0)
    lines.insert(position, line)
    project.css.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "updated"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_init(args, project: Project) -> int:
    if project.configured and not args.force:
        warning(f"{project.relative(project.root / 'pyblade-ui.toml')} already exists (use --force to rewrite it).")
    else:
        project.theme.base = args.base
        project.theme.color = args.color
        project.theme.radius = args.radius
        if args.css:
            project.css = project.root / args.css
        if args.registry:
            project.registry = args.registry
        success(f"Wrote {project.relative(project.save())}")

    success(f"Wrote {project.relative(write_theme(project))}")
    state = link_theme(project)
    if state != "unchanged":
        success(f"{state.capitalize()} {project.relative(project.css)} (imports the theme)")

    if not args.no_install:
        return _install(project, ["theme-script", "mode-toggle"], overwrite=False, dry_run=False, quiet=True)

    _next_steps(project)
    return 0


def _next_steps(project: Project):
    info("\nNext steps:")
    if project.framework == "django":
        info('  1. Add "pyblade_ui" to INSTALLED_APPS (registers the `cn` filter components use).')
    else:
        info("  1. `import pyblade_ui` once at startup (registers the `cn` filter components use).")
    info("  2. In the <head> of your layout:")
    info(dim("       <pb-ui.theme-script />"))
    info(dim('       <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.9/dist/cdn.min.js"></script>'))
    info("  3. Build the CSS: `pyblade dev` (or `pyblade tailwind:config` if Tailwind is not set up).")
    info("  4. Add components: `pyblade-ui add button card dialog`")


def _install(project: Project, names: list[str], overwrite: bool, dry_run: bool, quiet: bool = False) -> int:
    registry = Registry(project.registry)
    items = registry.resolve(names)

    created = skipped = conflicts = 0
    js: list[str] = []
    python: list[str] = []

    for item in items:
        for path in item.files:
            target = project.components / path
            content = registry.read_file(path)

            if target.is_file():
                if target.read_text(encoding="utf-8") == content:
                    skipped += 1
                    continue
                if not overwrite:
                    conflicts += 1
                    warning(f"{project.relative(target)} differs from the registry, kept (use --overwrite).")
                    continue

            if dry_run:
                info(f"  would write {project.relative(target)}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                success(f"{project.relative(target)}")
            created += 1

        js += [d for d in item.js if d not in js]
        python += [d for d in item.python if d not in python]

    if not quiet or created:
        info(dim(f"\n{created} written, {skipped} already up to date, {conflicts} kept."))
    if js:
        info("\nThese components need: " + ", ".join(js))
        if "alpinejs" in js:
            info(dim('  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.9/dist/cdn.min.js"></script>'))
    if python:
        info("\nPython packages to install: pip install " + " ".join(python))
    if quiet:
        _next_steps(project)
    return 0


def cmd_add(args, project: Project) -> int:
    registry = Registry(project.registry)
    names = list(registry.items) if args.all else args.components
    if not names:
        error("Name at least one component, or pass --all. See `pyblade-ui list`.")
        return 1
    return _install(project, names, overwrite=args.overwrite, dry_run=args.dry_run)


def cmd_list(args, project: Project | None) -> int:
    registry = Registry(args.registry or (project.registry if project else ""))
    width = max(len(name) for name in registry.items)
    for kind, label in (("registry:ui", "Components"), ("registry:block", "Blocks"), ("registry:lib", "Library")):
        items = [item for item in registry.items.values() if item.type == kind]
        if not items:
            continue
        info(_paint("1", f"\n{label}"))
        for item in items:
            installed = ""
            if project and all((project.components / path).is_file() for path in item.files):
                installed = _paint("32", " (installed)")
            info(f"  {item.name.ljust(width)}  {dim(item.description)}{installed}")
    return 0


def cmd_diff(args, project: Project) -> int:
    registry = Registry(project.registry)
    names = args.components or [
        item.name for item in registry.items.values() if any((project.components / p).is_file() for p in item.files)
    ]
    changed = 0
    for name in names:
        for path in registry.get(name).files:
            target = project.components / path
            if not target.is_file():
                continue
            ours = target.read_text(encoding="utf-8").splitlines(keepends=True)
            theirs = registry.read_file(path).splitlines(keepends=True)
            diff = list(difflib.unified_diff(theirs, ours, f"registry/{path}", project.relative(target)))
            if diff:
                changed += 1
                sys.stdout.writelines(diff)
                print()
    if not changed:
        success("Installed components match the registry.")
    return 0


def cmd_theme(args, project: Project) -> int:
    if args.action == "list":
        info(_paint("1", "Bases:  ") + ", ".join(BASES))
        info(_paint("1", "Colors: ") + ", ".join(COLORS))
        info(_paint("1", "Radii:  ") + ", ".join(RADII))
        info(dim(f"\nCurrent: base={project.theme.base} color={project.theme.color} radius={project.theme.radius}"))
        return 0

    if args.action == "show":
        print(render_theme(project.theme.base, project.theme.color, project.theme.radius))
        return 0

    # set
    project.theme.base = args.base or project.theme.base
    project.theme.color = args.color or project.theme.color
    project.theme.radius = args.radius or project.theme.radius
    if project.theme.base not in BASES or project.theme.color not in COLORS:
        error("Unknown base or color. See `pyblade-ui theme list`.")
        return 1
    project.save()
    success(f"Wrote {project.relative(write_theme(project))}")
    link_theme(project)
    info(dim(f"base={project.theme.base} color={project.theme.color} radius={project.theme.radius}"))
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pyblade-ui", description="Copy-paste components and themes for PyBlade.")
    parser.add_argument("--version", action="version", version=f"pyblade-ui {__version__}")
    parser.add_argument("--cwd", type=Path, help="Run as if started in this directory.")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="Set up the theme and configuration in a PyBlade project.")
    init.add_argument("--base", choices=list(BASES), default="neutral")
    init.add_argument("--color", choices=list(COLORS), default="neutral")
    init.add_argument("--radius", default="0.625rem")
    init.add_argument("--css", help="The project's Tailwind stylesheet (default static/css/tailwind.css).")
    init.add_argument("--registry", help="Registry URL or folder to install from.")
    init.add_argument("--no-install", action="store_true", help="Do not install theme-script and mode-toggle.")
    init.add_argument("-f", "--force", action="store_true", help="Rewrite pyblade-ui.toml.")

    add = commands.add_parser("add", help="Copy components into the project.")
    add.add_argument("components", nargs="*")
    add.add_argument("-a", "--all", action="store_true", help="Add every component.")
    add.add_argument("-o", "--overwrite", action="store_true", help="Replace files that differ from the registry.")
    add.add_argument("--dry-run", action="store_true")

    listing = commands.add_parser("list", help="List the components of the registry.")
    listing.add_argument("--registry")

    diff = commands.add_parser("diff", help="Show how installed components differ from the registry.")
    diff.add_argument("components", nargs="*")

    theme = commands.add_parser("theme", help="List, show or change the theme.")
    theme.add_argument("action", choices=["list", "show", "set"])
    theme.add_argument("--base", choices=list(BASES))
    theme.add_argument("--color", choices=list(COLORS))
    theme.add_argument("--radius")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        try:
            project = Project.load(args.cwd)
        except ProjectNotFound:
            if args.command != "list":
                raise
            project = None

        handler = {
            "init": cmd_init,
            "add": cmd_add,
            "list": cmd_list,
            "diff": cmd_diff,
            "theme": cmd_theme,
        }[args.command]
        return handler(args, project)
    except (ProjectNotFound, RegistryError, ValueError) as exc:
        error(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
