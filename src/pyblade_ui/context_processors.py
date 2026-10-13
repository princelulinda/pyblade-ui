"""Django context processors.

    TEMPLATES = [{"BACKEND": "pyblade.django.PyBladeEngine", ..., "OPTIONS": {"context_processors": [
        ...,
        "pyblade_ui.context_processors.sidebar",
    ]}}]
"""

from .sidebar import sidebar_open


def sidebar(request):
    """Adds `sidebar_open`, read from the cookie the sidebar saves."""
    return {"sidebar_open": sidebar_open(request)}
