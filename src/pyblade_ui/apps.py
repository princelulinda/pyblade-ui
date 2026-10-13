"""Django app, so that listing "pyblade_ui" in INSTALLED_APPS registers the filters."""

from django.apps import AppConfig


class PyBladeUIConfig(AppConfig):
    name = "pyblade_ui"
    verbose_name = "PyBlade UI"

    def ready(self):
        from . import utils  # noqa: F401 -- registers the `cn` filter
