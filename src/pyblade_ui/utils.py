"""Class merging for components, the `cn` of shadcn/ui.

PyBlade 0.3 spreads `{{ attributes }}` over a component's root element, but a
`class` written by the caller ends up as a second `class` attribute, which the
browser ignores. Components therefore render their root attributes with:

    <button {{ attributes.cn('inline-flex h-9 px-4', variants[variant]) }}>

which writes one `class` attribute (the component's classes first, the caller's
last, Tailwind conflicts resolved in favour of the caller) followed by every
other attribute the caller passed.
"""

from __future__ import annotations

import re
from html import escape

from pyblade.engine.contexts import AttributesContext, SafeContent
from pyblade.engine.filters import filters


class Markup(SafeContent):
    """Markup that PyBlade prints as is."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value


# ---------------------------------------------------------------------------
# A small subset of tailwind-merge: enough for the overrides people actually
# write on components (spacing, sizing, colors, radius, display...).
# ---------------------------------------------------------------------------

_SIZES = r"(xs|sm|base|md|lg|xl|[2-9]xl)"
_ALIGN = r"(left|center|right|justify|start|end)"
_FONT_WEIGHTS = r"(thin|extralight|light|normal|medium|semibold|bold|extrabold|black)"
_DISPLAY = {
    "block", "inline-block", "inline", "flex", "inline-flex", "grid", "inline-grid",
    "table", "contents", "hidden", "flow-root", "list-item",
}
_POSITION = {"static", "fixed", "absolute", "relative", "sticky"}

# Groups that are overridden by a more general one, e.g. `p-4` replaces `px-2`.
_CONFLICTS = {
    "p": ["px", "py", "pt", "pr", "pb", "pl", "ps", "pe"],
    "px": ["pl", "pr", "ps", "pe"],
    "py": ["pt", "pb"],
    "m": ["mx", "my", "mt", "mr", "mb", "ml", "ms", "me"],
    "mx": ["ml", "mr", "ms", "me"],
    "my": ["mt", "mb"],
    "size": ["w", "h"],
    "rounded": [
        "rounded-t", "rounded-r", "rounded-b", "rounded-l",
        "rounded-tl", "rounded-tr", "rounded-br", "rounded-bl",
    ],
    "gap": ["gap-x", "gap-y"],
    "inset": ["inset-x", "inset-y", "top", "right", "bottom", "left"],
}

_PREFIXED = re.compile(
    r"^(?P<group>p|px|py|pt|pr|pb|pl|ps|pe|m|mx|my|mt|mr|mb|ml|ms|me|w|h|size|min-w|min-h|max-w|max-h|"
    r"gap|gap-x|gap-y|space-x|space-y|inset|inset-x|inset-y|top|right|bottom|left|z|opacity|"
    r"leading|tracking|grid-cols|grid-rows|col-span|row-span|basis|grow|shrink|order|"
    r"justify|items|content|self|place-items|place-content|overflow|overflow-x|overflow-y|"
    r"cursor|duration|ease|line-clamp|aspect|object|whitespace|outline|ring-offset)-"
)


def _group(utility: str) -> str | None:
    """The conflict group of a class without its variants, or None if it never conflicts."""
    base = utility.lstrip("!")
    negative = base.startswith("-")
    base = base.lstrip("-")

    if base in _DISPLAY:
        return "display"
    if base in _POSITION:
        return "position"
    if base == "rounded" or base.startswith("rounded-"):
        side = re.match(r"^rounded-(t|r|b|l|tl|tr|br|bl|s|e|ss|se|es|ee)(-|$)", base)
        return f"rounded-{side.group(1)}" if side else "rounded"
    if re.match(rf"^text-{_SIZES}(/.*)?$", base):
        return "font-size"
    if re.match(rf"^text-{_ALIGN}$", base):
        return "text-align"
    if base.startswith("text-"):
        return "text-color"
    if re.match(rf"^font-{_FONT_WEIGHTS}$", base):
        return "font-weight"
    if base.startswith("font-"):
        return "font-family"
    if base == "shadow" or base.startswith("shadow-"):
        return "shadow"
    if base.startswith("bg-"):
        return "bg"
    if base == "border" or re.match(r"^border-(\d+|\[.*px\])$", base):
        return "border-width"
    if re.match(r"^border-(x|y|t|r|b|l|s|e)(-\d+)?$", base):
        return None
    if base.startswith("border-"):
        return "border-color"
    if base == "ring" or re.match(r"^ring-(\d+|\[.*px\])$", base):
        return "ring-width"
    if base.startswith("ring-") and not base.startswith("ring-offset-"):
        return "ring-color"
    if base.startswith("flex-"):
        return "flex-direction" if base in {"flex-row", "flex-col", "flex-row-reverse", "flex-col-reverse"} else "flex"

    match = _PREFIXED.match(base)
    if match:
        return ("-" if negative else "") + match.group("group")
    return None


def _split(token: str) -> tuple[str, str]:
    """`md:hover:px-4` -> ('md:hover:', 'px-4'), ignoring colons inside [brackets]."""
    depth, cut = 0, -1
    for index, char in enumerate(token):
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        elif char == ":" and depth == 0:
            cut = index
    return token[: cut + 1], token[cut + 1 :]


def tw_merge(*class_lists: str | None) -> str:
    """Join class lists, a later class replacing an earlier one of the same group."""
    tokens = [token for classes in class_lists if classes for token in str(classes).split()]

    kept: list[str] = []
    seen: set[str] = set()

    # Walk backwards: the last class of a group wins, and evicts what it overrides.
    for token in reversed(tokens):
        variants, utility = _split(token)
        group = _group(utility)

        if group is None:
            key = f"{variants}{utility}"
            if key in seen:
                continue
            seen.add(key)
            kept.append(token)
            continue

        key = f"{variants}{group}"
        if key in seen:
            continue

        seen.add(key)
        for overridden in _CONFLICTS.get(group, []):
            seen.add(f"{variants}{overridden}")
        kept.append(token)

    return " ".join(reversed(kept))


def cn(*class_lists: str | None) -> str:
    """Python twin of the template filter, for classes built in views or live components."""
    return tw_merge(*class_lists)


@filters.register("cn")
def cn_filter(owner, *classes):
    """`attributes.cn(...)` renders the root attributes; `'a b'.cn(...)` merges strings."""
    if isinstance(owner, AttributesContext):
        merged = tw_merge(*classes, owner.get("class") or None)
        rest = str(owner.exclude("class"))
        return Markup((f' class="{escape(merged)}"' if merged else "") + rest)

    return tw_merge(owner, *classes)


@filters.register("tojson")
def tojson_filter(value, indent=None):
    """`{{ rows.tojson() }}`: Python data as JSON, for Alpine (`x-data="{ rows: {{ rows.tojson() }} }"`).

    PyBlade escapes the output, so it is safe inside an attribute: the browser decodes the entities
    before Alpine reads the expression. Dates and other values JSON doesn't know become strings.
    """
    import json

    return json.dumps(value, indent=indent, default=str, ensure_ascii=False)
