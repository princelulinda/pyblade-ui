"""Server side of the sidebar: read the state it saved in a cookie, so the page is rendered collapsed or
expanded from the first byte, with no flash.

The sidebar writes `sidebar_state=true|false` whenever it is toggled. Read it back and pass it to
`<pb-ui.sidebar-provider :open="sidebar_open">`:

    # Django: add "pyblade_ui.context_processors.sidebar" to the PyBlade backend's context_processors
    # Flask:  render("dashboard", sidebar_open=sidebar_open(request))
    # FastAPI, Starlette, Litestar, Quart, Sanic: the same, with their request object
"""

from __future__ import annotations

from typing import Any

COOKIE = "sidebar_state"


def sidebar_open(request: Any, default: bool = True) -> bool:
    """Whether the sidebar should render expanded for this request.

    Works with any request that exposes its cookies as a mapping: `request.COOKIES` (Django) or
    `request.cookies` (Flask, Starlette, FastAPI, Litestar, Quart, Sanic). Without the cookie, `default`.
    """
    cookies = getattr(request, "COOKIES", None)
    if cookies is None:
        cookies = getattr(request, "cookies", None) or {}
    value = cookies.get(COOKIE)
    if value is None:
        return default
    return str(value).strip().lower() != "false"
